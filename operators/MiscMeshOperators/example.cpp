
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
#include <Sources.h>

using namespace MSML;

int main( int argc, char * argv[])
{
  double cordsArray[] = { 0, 0, 9, 1, 2,3};
  std::vector<double> coordinates(begin(cordsArray), end(cordsArray));
  Sources::GenerateSpheres(coordinates, 10.0, 10, 10, "C:/dev/msml/share/testdata/tmp/sphere_polydata.vtk");

	return EXIT_SUCCESS;
}













