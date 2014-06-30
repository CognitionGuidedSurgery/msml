/*
 * FeatureExtractionOperators.cpp
 *
 *  Created on: Jun 25, 2014
 *      Author: bungartz
 */

#include "FeatureExtractionOperators.h"
#include <iostream>

#include <vtkSmartPointer.h>
#include <vtkPolyData.h>
#include <vtkPolyDataReader.h>
#include <vtkTriangleFilter.h>
#include <vtkMassProperties.h>

using namespace std;

namespace MSML {
namespace FeatureExtractionOperators {

Features ExtractFeatures(std::string infile) {
    cout << "Extracting features from " << infile << endl;

    vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile.c_str());
    reader->Update();

    // vtkMassProperties only processes triangles, so we use vtkTriangleFilter to convert all Polygons to triangles:
    vtkSmartPointer<vtkTriangleFilter> triangleFilter = vtkSmartPointer<vtkTriangleFilter>::New();
    triangleFilter->SetInputConnection(reader->GetOutput()->GetProducerPort());
    triangleFilter->Update();

    vtkPolyData* mesh = triangleFilter->GetOutput();

    vtkSmartPointer<vtkMassProperties> massProps = vtkSmartPointer<vtkMassProperties>::New();
    massProps->SetInputConnection(mesh->GetProducerPort());
    massProps->Update();

    Features features;
    features.surfaceArea = massProps->GetSurfaceArea();
    features.volume = massProps->GetVolume();
    return features;
}

}
}

