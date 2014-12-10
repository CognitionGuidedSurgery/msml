
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
#include <stdio.h>

#include "test/common.h"


using namespace MSML;

int main( int argc, char * argv[])
{

  MiscMeshOperators::GenerateDistanceMap(INPUT("bunny_polydata.vtk"), OUTPUT("bunny_pdist.vti"), 100, 2.0, "", 5.0);
   
	return EXIT_SUCCESS;
}













