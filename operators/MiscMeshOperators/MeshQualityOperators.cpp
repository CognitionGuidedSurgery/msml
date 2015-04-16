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

void MeasureGeometricalAccuracy(string infile, string source){

	log_debug() << "MeasureTetrahedricMeshQuality" << endl;
	
	vtkSmartPointer<vtkUnstructuredGridReader> reader = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(source.c_str());
    reader->Update();

    vtkUnstructuredGrid* mesh = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader2->SetFileName(infile.c_str());
    reader2->Update();

    vtkUnstructuredGrid* imageData = reader->GetOutput();

	
	/*vtkSmartPointer<vtkXMLImageDataReader> reader2 =
    vtkSmartPointer<vtkXMLImageDataReader>::New();
    reader2->SetFileName(infile.c_str());
    reader2->Update();

    vtkSmartPointer<vtkImageData> imageData = reader2->GetOutput();*/

	log_debug() << "There are " << imageData->GetNumberOfCells() << " cells." << endl;
	log_debug() << "There are " << mesh->GetNumberOfCells() << " cells." << endl;

	/*vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New(); 
  
	int subId, cellNum; 
	double *paraCoords = new double[3]; 
	double *xyzCoords  = new double[3]; 
	double *vtkcellweights = new double[4]; 

	int NumberOfImageDataVoxels= imageData->GetNumberOfPoints(); 

	for (cellNum = 0; cellNum < NumberOfImageDataVoxels; cellNum++ ) { 
		
		subId = imageData->GetCell( cellNum )->GetParametricCenter(paraCoords); 
		int &subIDadd = subId; 
		imageData->GetCell(cellNum)->EvaluateLocation(subIDadd, paraCoords, 
		xyzCoords, vtkcellweights); 
		points->InsertNextPoint(xyzCoords);
	}*/

	vtkSmartPointer<vtkCellLocator> cellLocator = 
	vtkSmartPointer<vtkCellLocator>::New();
	cellLocator->SetDataSet(imageData);
	cellLocator->BuildLocator();


	vtkSmartPointer<vtkCellCenters> cellCentersFilter = 
    vtkSmartPointer<vtkCellCenters>::New();
#if VTK_MAJOR_VERSION <= 5
  cellCentersFilter->SetInputConnection(imageData->GetProducerPort());
#else
  cellCentersFilter->SetInputData(mesh);
#endif
  cellCentersFilter->VertexCellsOn();
  cellCentersFilter->Update();
	


  // Access the cell centers
  for(vtkIdType i = 0; i < cellCentersFilter->GetOutput()->GetNumberOfPoints(); i++)
    {
    double p[3];
    cellCentersFilter->GetOutput()->GetPoint(i, p);
    double closestPoint[3];//the coordinates of the closest point will be returned here
	double closestPointDist2; //the squared distance to the closest point will be returned here
	vtkIdType cellId; //the cell id of the cell containing the closest point will be returned here
	int subId; //this is rarely used (in triangle strips only, I believe)
	cellLocator->FindClosestPoint(p, closestPoint, cellId, subId, closestPointDist2);
	std::cout << "Coordinates of closest point: " << closestPoint[0] << " " << closestPoint[1] << " " << closestPoint[2] << std::endl;
	std::cout << "Squared distance to closest point: " << closestPointDist2 << std::endl;
	std::cout << "CellId: " << cellId << std::endl;
	//cout << "Point " << i << " : " << p[0] << " , " << p[1] << " , " << p[2] << endl;
    }
}

}
}
