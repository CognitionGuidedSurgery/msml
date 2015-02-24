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
#include <IOHelper.h>

#include "../vtk6_compat.h"
#include "../common/log.h"

using namespace std;

namespace MSML {
namespace FeatureExtractionOperators {

Features ExtractFeatures(std::string infile) {
    log_info() << "Extracting features from " << infile << endl;
	  
	vtkSmartPointer<vtkPolyData> polyData = IOHelper::VTKReadPolyData(infile.c_str());

    // vtkMassProperties only processes triangles, so we use vtkTriangleFilter to convert all Polygons to triangles:
    vtkSmartPointer<vtkTriangleFilter> triangleFilter = vtkSmartPointer<vtkTriangleFilter>::New();
	__SetInput(triangleFilter, polyData);
    triangleFilter->Update();

    vtkPolyData* mesh = triangleFilter->GetOutput();

    vtkSmartPointer<vtkMassProperties> massProps = vtkSmartPointer<vtkMassProperties>::New();
    __SetInput(massProps, mesh);
    massProps->Update();

    Features features;
    features.surfaceArea = massProps->GetSurfaceArea();
    features.volume = massProps->GetVolume();
    return features;
}

}
}

