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
#include <vtkDataArray.h>
#include <vtkDoubleArray.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkPolyDataReader.h>
#include <vtkMeshQuality.h>
#include <vtkVersion.h>

using namespace std;

namespace MSML {
namespace MeshQuality {

MeshQualityStats::MeshQualityStats():
        min(0), max(0), avg(0), var(0), n(0),
        qualityMeasureName("UNKNOWN"),
        errorQualityMeasureNotFound(false) {
}

// NOT using an std::set since querying a non-existent name will insert it with value 0!
static vector<pair<string, int>> FillTetQualityMeasureVtkIdsForTypeName() {
    vector<pair<string, int>> m;
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
    return m;
}
static vector<pair<string, int>> TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME = FillTetQualityMeasureVtkIdsForTypeName();

static int tetQualityMeasureVtkIdForName(string name) {
    for(vector<pair<string, int>>::iterator it = TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.begin(); it != TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.end(); ++it) {
        if(it->first == name) {
            return it->second;
        }
    }
    return -1;
}

static vector<string> FillTetQualityMeasureTypeNames() {
    vector<string> names;
    for(vector<pair<string, int>>::iterator it = TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.begin(); it != TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.end(); ++it) {
        names.push_back(it->first);
    }
    return names;
}
const vector<string> TET_QUALITY_MEASURE_TYPE_NAMES = FillTetQualityMeasureTypeNames();

const int DERP = 235;

MeshQualityStats MeasureTetrahedricMeshQuality(std::string infile, std::string qualityMeasureName) {
    cout << "MeasureTetrahedricMeshQuality" << endl;

    MeshQualityStats stats;
    stats.qualityMeasureName = qualityMeasureName;

    int qualityMeasure = tetQualityMeasureVtkIdForName(qualityMeasureName);
    if(qualityMeasure < 0) {
        stats.errorQualityMeasureNotFound = true;
        return stats;
    }

    //vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
    vtkSmartPointer<vtkUnstructuredGridReader> reader = vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkUnstructuredGrid* mesh = reader->GetOutput();
    cout << "There are " << mesh->GetNumberOfCells() << " cells." << endl;

    vtkSmartPointer<vtkMeshQuality> quality = vtkSmartPointer<vtkMeshQuality>::New();
#if VTK_MAJOR_VERSION <= 5
    quality->SetInputConnection(mesh->GetProducerPort());
#else
    quality->SetInputData(mesh);
#endif
    quality->SetTetQualityMeasure(qualityMeasure);
    quality->Update();

    vtkCellData* cellData = quality->GetOutput()->GetCellData();
    vtkFieldData* fieldData = quality->GetOutput()->GetFieldData();
    vtkSmartPointer<vtkDoubleArray> qualityArray = vtkDoubleArray::SafeDownCast(cellData->GetArray("Quality"));

    std::cout << "There are " << qualityArray->GetNumberOfTuples() << " values." << std::endl;

    for (vtkIdType i = 0; i < qualityArray->GetNumberOfTuples(); i++) {
        double val = qualityArray->GetValue(i);
        //std::cout << "value " << i << " : " << val << std::endl;
    }

    vtkDataArray* aggregate = fieldData->GetArray("Mesh Tetrahedron Quality");
    double* tuple = aggregate->GetTuple(0);
    stats.min = tuple[0];
    stats.avg = tuple[1];
    stats.max = tuple[2];
    stats.var = tuple[3];
    stats.n = tuple[4];

    cout << qualityMeasureName << " min=" << stats.min << "; max=" << stats.max << "; avg=" << stats.avg << "; var=" << stats.var << "; n=" << stats.n << endl;

    return stats;
}

}
}
