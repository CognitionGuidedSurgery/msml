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
MeshQualityStats MeasureTetrahedricMeshQuality(std::string infile) {
    cout << "MeasureTetrahedricMeshQuality" << endl;
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
    quality->SetTetQualityMeasureToEdgeRatio();
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
    MeshQualityStats stats;
    stats.min = tuple[0];
    stats.avg = tuple[1];
    stats.max = tuple[2];
    stats.var = tuple[3];
    stats.n = tuple[4];

    cout << "min=" << stats.min << "; max=" << stats.max << "; avg=" << stats.avg << "; var=" << stats.var << "; n=" << stats.n << endl;

    return stats;
}

}
}
