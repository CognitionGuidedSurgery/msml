/*
 * MeshInfoOperators.cpp
 *
 *  Created on: 01.08.2014
 *      Author: simon
 */

#include "MeshInfoOperators.h"
#include <iostream>
#include <vtkPolyData.h>
#include <vtkSmartPointer.h>
#include <vtkPolyDataReader.h>
#include <vtkVersion.h>
#include <vtkMassProperties.h>

using namespace std;

namespace MSML {
namespace MeshInfo {

LIBRARY_API long long SurfaceMeshNumberOfPoints(std::string infile) {
    vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkPolyData *mesh = reader->GetOutput();

    return mesh->GetNumberOfPoints();
}

long long SurfaceMeshNumberOfElements(std::string infile) {
    vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkPolyData *mesh = reader->GetOutput();

    return mesh->GetNumberOfCells();
}

double SurfaceMeshVolume(std::string infile) {
    vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkPolyData *mesh = reader->GetOutput();

    vtkSmartPointer<vtkMassProperties> massProps = vtkSmartPointer<vtkMassProperties>::New();
#if VTK_MAJOR_VERSION <= 5
    massProps->SetInputConnection(mesh->GetProducerPort());
#else
    massProps->SetInputData(mesh);
#endif

    massProps->Update();

    return massProps->GetVolume();
}

double SurfaceMeshSurfaceArea(std::string infile) {
    vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    vtkPolyData *mesh = reader->GetOutput();

    vtkSmartPointer<vtkMassProperties> massProps = vtkSmartPointer<vtkMassProperties>::New();
#if VTK_MAJOR_VERSION <= 5
    massProps->SetInputConnection(mesh->GetProducerPort());
#else
    massProps->SetInputData(mesh);
#endif

    massProps->Update();

    return massProps->GetSurfaceArea();
}

}
}
