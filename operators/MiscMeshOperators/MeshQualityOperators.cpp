/*
 * MeshQualityOperators.cpp
 *
 *  Created on: Jun 23, 2014
 *      Author: bungartz
 */

#include "MeshQualityOperators.h"
#include <iostream>
#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkCellData.h>
#include <vtkImageData.h>
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkSmartPointer.h>
#include <vtkXMLImageDataReader.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkPolyDataReader.h>
#include <vtkMeshQuality.h>
#include <vtkVersion.h>
#include <vtkCell.h>
#include <vtkCellLocator.h>
#include <vtkCellCenters.h>
#include <vtkKdTreePointLocator.h>

#include "../common/log.h"

using namespace std;

namespace MSML {
namespace MeshQuality {

MeshQualityStats::MeshQualityStats():
        min(0), max(0), avg(0), var(0), n(0),
        qualityMeasureName("UNKNOWN"),
        errorQualityMeasureNotFound(false) {
}

// NOT using an std::set since querying a non-existent name will insert it with value 0!
vector<pair<string, int> > FillTetQualityMeasureVtkIdsForTypeName() {
    vector<pair<string, int> > m;
    m.push_back(pair<string, int>("AspectRatio", VTK_QUALITY_ASPECT_RATIO));
    m.push_back(pair<string, int>("AspectFrobenius", VTK_QUALITY_ASPECT_FROBENIUS));
    m.push_back(pair<string, int>("EdgeRatio", VTK_QUALITY_EDGE_RATIO));
    m.push_back(pair<string, int>("CollapseRatio", VTK_QUALITY_COLLAPSE_RATIO));
    m.push_back(pair<string, int>("AspectBeta", VTK_QUALITY_ASPECT_BETA));
    m.push_back(pair<string, int>("AspectGamma", VTK_QUALITY_ASPECT_GAMMA));
    m.push_back(pair<string, int>("Volume", VTK_QUALITY_VOLUME));
    m.push_back(pair<string, int>("Condition", VTK_QUALITY_CONDITION));
    m.push_back(pair<string, int>("Jacobian", VTK_QUALITY_JACOBIAN));
    m.push_back(pair<string, int>("ScaledJacobian", VTK_QUALITY_SCALED_JACOBIAN));
    m.push_back(pair<string, int>("Shape", VTK_QUALITY_SHAPE));
    m.push_back(pair<string, int>("RelativeSizeSquared", VTK_QUALITY_RELATIVE_SIZE_SQUARED));
    m.push_back(pair<string, int>("ShapeAndSize", VTK_QUALITY_SHAPE_AND_SIZE));
    m.push_back(pair<string, int>("Distortion", VTK_QUALITY_DISTORTION));

    m.push_back(pair<string, int>("MinAngle", VTK_QUALITY_MIN_ANGLE));
    //m.push_back(pair<string, int>("AspectDelta", VTK_QUALITY_ASPECT_DELTA)); // Supported by verdict but not VTK
    m.push_back(pair<string, int>("RadiusRatio", VTK_QUALITY_RADIUS_RATIO));

    return m;
}
vector<pair<string, int> > TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME = FillTetQualityMeasureVtkIdsForTypeName();

int tetQualityMeasureVtkIdForName(string name) {
    for (vector<pair<string, int> >::iterator it = TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.begin();
            it != TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.end(); ++it) {
        if (it->first == name) {
            return it->second;
        }
    }
    return -1;
}

vector<string> FillTetQualityMeasureTypeNames() {
    vector<string> names;
    for (vector<pair<string, int> >::iterator it = TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.begin();
            it != TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.end(); ++it) {
        names.push_back(it->first);
    }
    return names;
}
const vector<string> TET_QUALITY_MEASURE_TYPE_NAMES = FillTetQualityMeasureTypeNames();

MeshQualityStats MeasureTetrahedricMeshQuality(string infile, string qualityMeasureName) {
    vector<string> names;
    names.push_back(qualityMeasureName);
    return MeasureTetrahedricMeshQuality(infile, names).front();
}

vector<MeshQualityStats> MeasureTetrahedricMeshQuality(string infile, vector<string> qualityMeasureNames) {
    log_debug() << "MeasureTetrahedricMeshQuality" << endl;

    vector<MeshQualityStats> results;

    vtkSmartPointer<vtkUnstructuredGridReader> reader = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkUnstructuredGrid* mesh = reader->GetOutput();
    log_debug() << "There are " << mesh->GetNumberOfCells() << " cells." << endl;

    vtkSmartPointer<vtkMeshQuality> quality = vtkSmartPointer<vtkMeshQuality>::New();
#if VTK_MAJOR_VERSION <= 5
    quality->SetInputConnection(mesh->GetProducerPort());
#else
    quality->SetInputData(mesh);
#endif

    quality->SaveCellQualityOff(); // Do not save the values for each cell, since we only return the aggregated values anyways.

    for (vector<string>::iterator it = qualityMeasureNames.begin(); it != qualityMeasureNames.end(); ++it) {
        MeshQualityStats result;
        result.qualityMeasureName = *it;
        int qualityMeasureId = tetQualityMeasureVtkIdForName(*it);
        if (qualityMeasureId < 0) {
            result.errorQualityMeasureNotFound = true;
        } else {
            quality->SetTetQualityMeasure(qualityMeasureId);
            quality->Update();

            vtkFieldData* fieldData = quality->GetOutput()->GetFieldData();
            vtkDataArray* aggregate = fieldData->GetArray("Mesh Tetrahedron Quality");
            double* tuple = aggregate->GetTuple(0);
            result.min = tuple[0];
            result.avg = tuple[1];
            result.max = tuple[2];
            result.var = tuple[3];
            result.n = tuple[4];

            log_debug() << result.qualityMeasureName << " min=" << result.min << "; max=" << result.max << "; avg=" << result.avg << "; var="
                       << result.var << "; n=" << result.n << endl;
        }
        results.push_back(result);
    };

    return results;
}

//Measures mesh quality depending on the matching count of material ids between original image(vti)
//and generated mesh.  
double measureMeshQuality(std::string infile, std::string source){
	
	vtkSmartPointer<vtkXMLImageDataReader> reader =
    vtkSmartPointer<vtkXMLImageDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkSmartPointer<vtkImageData> imageData = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader2->SetFileName( source.c_str());
    reader2->Update();

    vtkUnstructuredGrid* compareMesh = reader2->GetOutput();

	vtkSmartPointer<vtkCellLocator> cellLocatorCompareMesh = 
	vtkSmartPointer<vtkCellLocator>::New();
	cellLocatorCompareMesh->SetDataSet(compareMesh);
	cellLocatorCompareMesh->BuildLocator();

  //counters
  int diffVoxelCounter = 0;
  int totalVoxelCounter = 0;

  //vars for cellLocatorCompareMesh->FindClosestPoint(..)
	double closestPoint[3];
	double closestPointDist;  
  int subId; 
  vtkIdType closestCellIdMesh; 

  vtkIntArray* cellMaterialArray0 = (vtkIntArray*) compareMesh->GetCellData()->GetArray("Materials");

  int* dims = imageData->GetDimensions();
  double* origin = imageData->GetOrigin();
  double* spacing = imageData->GetSpacing();
  double quality =0.0;

  //for each voxel in the segmentation image
  for (int z = 0; z < dims[2]; z++)
  {
      for (int y = 0; y < dims[1]; y++)
      {
          for (int x = 0; x < dims[0]; x++)
          {
            totalVoxelCounter++;

            //grid indices to mm coordinates
            double pInMM[3];
            pInMM[0] = origin[0]+x*spacing[0];
            pInMM[1] = origin[1]+y*spacing[1];
            pInMM[2] = origin[2]+z*spacing[2];

            //get image value at position pInMM (material id)
            float material_id_in_image = imageData->GetScalarComponentAsFloat(x,y,z, 0); 
            
            //find nearset tetrahedron, and get the correspondig material id
            cellLocatorCompareMesh->FindClosestPoint(pInMM,closestPoint,closestCellIdMesh,subId,closestPointDist); 
            double material_id_in_mesh = *cellMaterialArray0->GetTuple(closestCellIdMesh); 

            //count voxel having a different material id, dont care for air-voxels (material=0)
            if(material_id_in_image>0 && material_id_in_mesh != material_id_in_image)
            {
			        diffVoxelCounter++;
		    }
          } //x
          quality = 1-(double(diffVoxelCounter)/double(totalVoxelCounter));
      } //y
      
  } //z
	log_debug() <<  quality <<  std::endl;
	return quality;
}


double calculateHausdorffDistance(string fileMesh1, string fileMesh2, bool points) {

	log_debug() << "calculateHausdorffDistance" << endl;
	
	double relativeDistance0 =0.0;
	double relativeDistance1 =0.0;
	double hausdorffDistance =0.0;
	
	vtkSmartPointer<vtkUnstructuredGridReader> reader = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(fileMesh1.c_str());
    reader->Update();

    vtkUnstructuredGrid* mesh1 = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader2->SetFileName(fileMesh2.c_str());
    reader2->Update();

    vtkUnstructuredGrid* mesh2 = reader2->GetOutput();

	vtkSmartPointer<vtkCellLocator> cellLocatorMesh1 = 
	vtkSmartPointer<vtkCellLocator>::New();
	cellLocatorMesh1->SetDataSet(mesh1);
	cellLocatorMesh1->BuildLocator();

	vtkSmartPointer<vtkCellLocator> cellLocatorMesh2 = 
	vtkSmartPointer<vtkCellLocator>::New();
	cellLocatorMesh2->SetDataSet(mesh2);
	cellLocatorMesh2->BuildLocator();

	vtkSmartPointer<vtkKdTreePointLocator> pointLocatorMesh1 = vtkSmartPointer<vtkKdTreePointLocator>::New();
	vtkSmartPointer<vtkKdTreePointLocator> pointLocatorMesh2 = vtkSmartPointer<vtkKdTreePointLocator>::New();
	
	pointLocatorMesh1->SetDataSet(mesh1);
	pointLocatorMesh1->BuildLocator();
	pointLocatorMesh2->SetDataSet(mesh2);
	pointLocatorMesh2->BuildLocator();

	  double p[3];
	  double closestPoint[3];
	  double closestPointDist; 
	  double currentPoint[3];
	  vtkIdType cellId; 
	  int subId; 

	  // Access the cell centers
	  for(vtkIdType i = 0; i < mesh1->GetNumberOfPoints(); i++) {
		//cellCentersFilterOriginalMesh->GetOutput()->GetPoint(i, p);
		
		mesh1->GetPoint(i, currentPoint);
		if(points){
			vtkIdType closestPointId = pointLocatorMesh2->FindClosestPoint(currentPoint);
			mesh2->GetPoint(closestPointId,closestPoint);
			closestPointDist = sqrt(pow(currentPoint[0]-closestPoint[0],2)+pow(currentPoint[1]-closestPoint[1],2)+pow(currentPoint[2]-closestPoint[2],2));
		} else {
			cellLocatorMesh2->FindClosestPoint(currentPoint,closestPoint,cellId,subId,closestPointDist);
		}
		
		if( closestPointDist > relativeDistance0) {
			relativeDistance0 = closestPointDist;
		}
	   }

	   for(vtkIdType i = 0; i < mesh2->GetNumberOfPoints(); i++) {
		//cellCentersFilterCompareMesh->GetOutput()->GetPoint(i, p); 
		//cellLocatorOriginalMesh->FindClosestPoint(p, closestPoint, cellId, subId, closestPointDist);
		mesh2->GetPoint(i, currentPoint);
		if(points){
			vtkIdType closestPointId = pointLocatorMesh1->FindClosestPoint(currentPoint);
			mesh1->GetPoint(closestPointId,closestPoint);
			closestPointDist = sqrt(pow(currentPoint[0]-closestPoint[0],2)+pow(currentPoint[1]-closestPoint[1],2)+pow(currentPoint[2]-closestPoint[2],2));
		} else {
			cellLocatorMesh1->FindClosestPoint(currentPoint,closestPoint,cellId,subId,closestPointDist);
		}
		if( closestPointDist > relativeDistance1) {
			relativeDistance1 = closestPointDist;
		}
	   }

	   if(relativeDistance0 >= relativeDistance1){
		 hausdorffDistance = relativeDistance0;
	   } else {
		 hausdorffDistance = relativeDistance1;
	   }
		log_debug() << hausdorffDistance << endl;
	  
	  return hausdorffDistance;
	}
  }
}
