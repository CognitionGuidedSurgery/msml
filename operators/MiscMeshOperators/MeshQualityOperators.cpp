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
static vector<pair<string, int> > FillTetQualityMeasureVtkIdsForTypeName() {
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
static vector<pair<string, int> > TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME = FillTetQualityMeasureVtkIdsForTypeName();

static int tetQualityMeasureVtkIdForName(string name) {
    for (vector<pair<string, int> >::iterator it = TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.begin();
            it != TET_QUALITY_MEASURE_VTK_IDS_FOR_TYPE_NAME.end(); ++it) {
        if (it->first == name) {
            return it->second;
        }
    }
    return -1;
}

static vector<string> FillTetQualityMeasureTypeNames() {
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
    cout << "MeasureTetrahedricMeshQuality" << endl;

    vector<MeshQualityStats> results;

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

            cout << result.qualityMeasureName << " min=" << result.min << "; max=" << result.max << "; avg=" << result.avg << "; var="
                       << result.var << "; n=" << result.n << endl;

        }
        results.push_back(result);
    };

    return results;
}

}
}
