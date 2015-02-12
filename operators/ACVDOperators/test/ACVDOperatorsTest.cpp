#include "ACVDOperators.h"
#include "../common/test_common.h"

#define BOOST_TEST_MODULE ACVDOperatorsTest
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE(TestReduceSurfaceMesh)
{  
	int desiredVerticeCount = 2000;
	vtkSmartPointer<vtkPolyData> reducedMesh = vtkSmartPointer<vtkPolyData>::New();
	bool result = ACVDOperators::ReduceSurfaceMesh(IOHelper::VTKReadPolyData(INPUT("TestACVD_cylinder_rough.vtk")), 
												   reducedMesh,desiredVerticeCount,true);	
	BOOST_CHECK(result);
	BOOST_CHECK(reducedMesh->GetPoints()->GetNumberOfPoints()==desiredVerticeCount);
}
