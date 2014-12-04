
#include "PostProcessingOperators.h"
#include "MiscMeshOperators.h"
#include "IndexRegionOperators.h"
#include <vector>
#include <iostream>
#include <string>
#include <sstream> 
#include <VTKMeshgen.h>
#include <vtkPolyData.h>
#include <IOHelper.h>
#include <SurfaceToVoxelDataOperator.h>

using namespace MSML;

int main( int argc, char * argv[])
{
  vtkPolyData* aBunny = IOHelper::VTKReadPolyData("C:/dev/msml/share/testdata/references/bunny_polydata.vtk");
  SurfaceToVoxelDataOperator::SurfaceToVoxelDataOperator("C:/dev/msml/share/testdata/references/bunny_polydata.vtk", "C:/dev/msml/share/testdata/tmp/bunny_image.vti", 8.0);

	return EXIT_SUCCESS;
}













