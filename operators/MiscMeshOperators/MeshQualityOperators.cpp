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

void measureMeshQuality(std::string infile, std::string source){
	vtkSmartPointer<vtkXMLImageDataReader> reader =
    vtkSmartPointer<vtkXMLImageDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkSmartPointer<vtkImageData> imageData = reader->GetOutput();

	/*vtkSmartPointer<vtkCellCenters> cellCentersFilterOriginalMesh = 
    vtkSmartPointer<vtkCellCenters>::New();
#if VTK_MAJOR_VERSION <= 5
  cellCentersFilterOriginalMesh->SetInputConnection(imageData->GetProducerPort());
#else
	cellCentersFilterOriginalMesh->SetInputData(imageData);
#endif
  cellCentersFilterOriginalMesh->VertexCellsOn();
  cellCentersFilterOriginalMesh->Update();

  vtkSmartPointer<vtkCellCenters> cellCentersFilterCompareMesh = 
    vtkSmartPointer<vtkCellCenters>::New();
#if VTK_MAJOR_VERSION <= 5
  cellCentersFilterCompareMesh->SetInputConnection(imageData->GetProducerPort());
#else
	cellCentersFilterCompareMesh->SetInputData(imageData);
#endif
  cellCentersFilterCompareMesh->VertexCellsOn();
  cellCentersFilterCompareMesh->Update();*/

	double center[3] = {0,0,0};
	for(vtkIdType cellId = 0; cellId < imageData->GetNumberOfCells(); ++cellId)
	{
	GetCellCenter(imageData, cellId, center);
 
	std::cout << "Cell " << cellId << " center: " << center[0] << " " 
				<< center[1] << " " << center[2] << std::endl;
	}



}

void GetCellCenter(vtkImageData* imageData, const unsigned int cellId, double center[3])
{
  double pcoords[3] = {0,0,0};
  double *weights = new double [imageData->GetMaxCellSize()];
  vtkCell* cell = imageData->GetCell(cellId);
  int subId = cell->GetParametricCenter(pcoords);
  cell->EvaluateLocation(subId, pcoords, center, weights);
}

void  calculateHausdorffDistance(string originalFile, string compareFile, bool points) {

	log_debug() << "calculateHausdorffDistance" << endl;
	
	double relativeDistance0 =0.0;
	double relativeDistance1 =0.0;
	double hausdorffDistance =0.0;
	
	vtkSmartPointer<vtkUnstructuredGridReader> reader = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(originalFile.c_str());
    reader->Update();

    vtkUnstructuredGrid* originalMesh = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader2->SetFileName(compareFile.c_str());
    reader2->Update();

    vtkUnstructuredGrid* compareMesh = reader2->GetOutput();

	vtkSmartPointer<vtkCellLocator> cellLocatorOriginalMesh = 
	vtkSmartPointer<vtkCellLocator>::New();
	cellLocatorOriginalMesh->SetDataSet(originalMesh);
	cellLocatorOriginalMesh->BuildLocator();

	vtkSmartPointer<vtkCellLocator> cellLocatorCompareMesh = 
	vtkSmartPointer<vtkCellLocator>::New();
	cellLocatorCompareMesh->SetDataSet(originalMesh);
	cellLocatorCompareMesh->BuildLocator();

	vtkSmartPointer<vtkKdTreePointLocator> pointLocatorOriginal = vtkSmartPointer<vtkKdTreePointLocator>::New();
	vtkSmartPointer<vtkKdTreePointLocator> pointLocatorCompare = vtkSmartPointer<vtkKdTreePointLocator>::New();
  
	vtkSmartPointer<vtkDoubleArray> distanceOriginalToCompare = vtkSmartPointer<vtkDoubleArray>::New();
	distanceOriginalToCompare->SetNumberOfComponents(1);
	distanceOriginalToCompare->SetNumberOfTuples(originalMesh->GetNumberOfPoints());
	distanceOriginalToCompare->SetName( "Distance" );
      
	vtkSmartPointer<vtkDoubleArray> distanceCompareToOriginal = vtkSmartPointer<vtkDoubleArray>::New();
	distanceCompareToOriginal->SetNumberOfComponents(1);
	distanceCompareToOriginal->SetNumberOfTuples(compareMesh->GetNumberOfPoints());
	distanceCompareToOriginal->SetName( "Distance" );
	
	pointLocatorOriginal->SetDataSet(originalMesh);
	pointLocatorOriginal->BuildLocator();
	pointLocatorCompare->SetDataSet(compareMesh);
	pointLocatorCompare->BuildLocator();

	  double p[3];
	  double closestPoint[3];
	  double closestPointDist; 
	  double currentPoint[3];
	  vtkIdType cellId; 
	  int subId; 

	  // Access the cell centers
	  for(vtkIdType i = 0; i < originalMesh->GetNumberOfPoints(); i++) {
		//cellCentersFilterOriginalMesh->GetOutput()->GetPoint(i, p);
		
		originalMesh->GetPoint(i, currentPoint);
		if(points){
			vtkIdType closestPointId = pointLocatorCompare->FindClosestPoint(currentPoint);
			compareMesh->GetPoint(closestPointId,closestPoint);
			closestPointDist = sqrt(pow(currentPoint[0]-closestPoint[0],2)+pow(currentPoint[1]-closestPoint[1],2)+pow(currentPoint[2]-closestPoint[2],2));
		} else {
			cellLocatorCompareMesh->FindClosestPoint(currentPoint,closestPoint,cellId,subId,closestPointDist);
		}
		
		distanceOriginalToCompare->SetValue(i, closestPointDist);
		if( closestPointDist > relativeDistance0) {
			relativeDistance0 = closestPointDist;
		}
	   }

	   for(vtkIdType i = 0; i < compareMesh->GetNumberOfPoints(); i++) {
		//cellCentersFilterCompareMesh->GetOutput()->GetPoint(i, p); 
		//cellLocatorOriginalMesh->FindClosestPoint(p, closestPoint, cellId, subId, closestPointDist);
		compareMesh->GetPoint(i, currentPoint);
		if(points){
			vtkIdType closestPointId = pointLocatorOriginal->FindClosestPoint(currentPoint);
			originalMesh->GetPoint(closestPointId,closestPoint);
			closestPointDist = sqrt(pow(currentPoint[0]-closestPoint[0],2)+pow(currentPoint[1]-closestPoint[1],2)+pow(currentPoint[2]-closestPoint[2],2));
		} else {
			cellLocatorOriginalMesh->FindClosestPoint(currentPoint,closestPoint,cellId,subId,closestPointDist);
		}
		distanceCompareToOriginal->SetValue(i, closestPointDist);
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
	}
  }
}
