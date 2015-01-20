#include "../common/test_common.h"

#define BOOST_TEST_MODULE MiscMeshOperatorsTest
#include <boost/test/unit_test.hpp>
#include "FeatureExtractionOperators.h"

//BOOST_AUTO_TEST_CASE( TestAssignRegionOperator )
//{
//    const char* inputMesh = INPUT("liverMVolume.vtk");
//    const char* outputMesh = OUTPUT("liverMVolumeRegions.vtk");
//
//    REQUIRE_FILE_EXISTS(inputMesh);
//
//    std::vector<std::string> regionMeshes;
//    regionMeshes.push_back(INPUT("liverSurfaceXLIniFixedBC.vtk"));
//
//    string errorMessage;
//    MiscMeshOperators::AssignSurfaceRegion(inputMesh, outputMesh, regionMeshes);
//}

BOOST_AUTO_TEST_CASE( TestGenerateDistanceMap)
{
  vtkSmartPointer<vtkImageData> aDistMap = MiscMeshOperators::
    GenerateDistanceMap(IOHelper::VTKReadUnstructuredGrid(INPUT("bunny_tets.vtk.vtk")), 10, 0, "", 0);
}


BOOST_AUTO_TEST_CASE( TestTransformMeshBarycentric)
{
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid =
        IOHelper::VTKReadUnstructuredGrid(REFERENCE("ircad_disp0.vtu"));
    vtkSmartPointer<vtkUnstructuredGrid> deformedGrid =
        IOHelper::VTKReadUnstructuredGrid(REFERENCE("ircad_disp50.vtu"));
    vtkSmartPointer<vtkUnstructuredGrid> refSurface =
        IOHelper::VTKReadUnstructuredGrid(REFERENCE("ircad_tris_kidney.vtu"));
    vtkSmartPointer<vtkUnstructuredGrid> out_surface =
        vtkSmartPointer<vtkUnstructuredGrid>::New();

    PostProcessingOperators::TransformMeshBarycentric(refSurface, referenceGrid, deformedGrid, out_surface, 10);
}

BOOST_AUTO_TEST_CASE( TestPositionFromIndices)
{
    std::vector<unsigned int> ids;
    ids.push_back(1);
    vector<double> pos = IndexRegionOperators::PositionFromIndices(
              INPUT("ircad_disp0.vtu"), ids, "points");
}

BOOST_AUTO_TEST_CASE(TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator)
{
    const char* inputMesh = INPUT("ircad_tets_labled.vtk");
    const char* outputMesh = OUTPUT("TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator.vtk");
    std::string output = MiscMeshOperators::ExtractAllSurfacesByMaterial(
                             inputMesh, outputMesh, false);

    BOOST_CHECK(outputMesh==output);
}

BOOST_AUTO_TEST_CASE( TestMergeMeshes)
{
    const char* inputCells = INPUT("ircad_tets_labled.vtk");
    const char* inputPoints = INPUT("ircad_disp50.vtu");
    const char* outputMesh  = OUTPUT("TestMergeMeshes");
    PostProcessingOperators::MergeMeshes(inputCells, inputCells, outputMesh);

}

BOOST_AUTO_TEST_CASE( TestGenerateDVF)
{
PostProcessingOperators::GenerateDVF(
    INPUT("ircad_disp50.vtu"),
    INPUT("ircad_disp0.vtu"),
    OUTPUT("TestGenerateDVF.vti"), 10, "", 10);
}

BOOST_AUTO_TEST_CASE( TestMarchingCube )
{
    VTKMeshgen::vtkMarchingCube(
      INPUT("ircad_segmentation.vti"),  
      OUTPUT("TestMarchingCube.vtp"), 50);
}

BOOST_AUTO_TEST_CASE( TestApplyDVF)
{
  PostProcessingOperators::ApplyDVF(
    INPUT("ircad_ct_image.vti"),
    INPUT("ircad_dvf.vti"),
    OUTPUT("TestApplyDVF.vti"), true, 2.0);

}

BOOST_AUTO_TEST_CASE( TestConvertLinearToQuadraticTetrahedralMesh)
{
    MiscMeshOperators::ConvertLinearToQuadraticTetrahedralMesh(
        INPUT("bunny_tets.vtk"),
        OUTPUT("TestConvertLinearToQuadraticTetrahedralMesh.vtk"));
}

BOOST_AUTO_TEST_CASE( TestConvertSTLToVTK)
{
    MiscMeshOperators::ConvertSTLToVTK(
      INPUT("bunny_xl.stl"), 
      OUTPUT("TestConvertSTLToVTK.vtk"));
}

BOOST_AUTO_TEST_CASE( TestConvertVTKMeshToAbaqusMeshString)
{
  MiscMeshOperators::ConvertVTKMeshToAbaqusMeshString(
    INPUT("bunny_tets.vtk"), "aPart", "aMaterial");
}

BOOST_AUTO_TEST_CASE( TestConvertVTKPolydataToUnstructuredGrid)
{
    MiscMeshOperators::ConvertVTKPolydataToUnstructuredGrid(
      INPUT("bunny_polydata.vtk"), 
      OUTPUT("TestConvertVTKPolydataToUnstructuredGrid.vtu"));
}

BOOST_AUTO_TEST_CASE( TestConvertVTKToOFF)
{
    MiscMeshOperators::ConvertVTKToOFF(
        IOHelper::VTKReadPolyData(INPUT("bunny_polydata.vtk")),
        OUTPUT("TestConvertVTKToOFF.off"));
}

BOOST_AUTO_TEST_CASE( TestExtractAllSurfacesByMaterial)
{
    MiscMeshOperators::ExtractAllSurfacesByMaterial(
        INPUT("ircad_tets_labled.vtk"),
        OUTPUT("TestExtractAllSurfacesByMaterial.vtk"), false);
}

BOOST_AUTO_TEST_CASE( TestExtractNodeSet)
{
    MiscMeshOperators::ExtractNodeSet(
        INPUT("ircad_tets_labled.vtk"),
        "nonExtistingNodeset-TestdataNeeded");
}

double abs_msml(double d) //abs is already defined in msvc
{
    return d<0?-d:d;
}

BOOST_AUTO_TEST_CASE( TestExtractPointPositions )
{
    std::vector<int> indices;
    indices.push_back(0);
    indices.push_back(1);
    indices.push_back(2);
    std::vector<double> aReturn = MiscMeshOperators::ExtractPointPositions(
        indices, INPUT("bunny_tets.vtk"));
    BOOST_REQUIRE( abs_msml(aReturn[1] - 0.0660446) < 0.000001 );
}

BOOST_AUTO_TEST_CASE( TestExtractVectorField )
{
    std::vector<unsigned int> indices;
    indices.push_back(0);
    indices.push_back(1);
    indices.push_back(2);
    MiscMeshOperators::ExtractVectorField(
        INPUT("bunny_tets.vtk"),
        "nonExistinFieldTestdataNeeded", indices);
}
BOOST_AUTO_TEST_CASE( TestExtractSurfaceMesh)
{
    MiscMeshOperators::ExtractSurfaceMesh(
        INPUT("bunny_tets.vtk"),
        OUTPUT("TestExtractSurfaceMesh_AKA_ugrid_to_polydata.vtk"));
}

BOOST_AUTO_TEST_CASE( TestProjectSurfaceMesh )
{
    MiscMeshOperators::ProjectSurfaceMesh(INPUT("bunny_polydata_highres.vtk"),
                                                OUTPUT("TestProjectSurfaceMesh.vtk"),
                                                INPUT("bunny_polydata.vtk"));
}

BOOST_AUTO_TEST_CASE( TestVoxelizeSurfaceMesh )
{
    MiscMeshOperators::VoxelizeSurfaceMesh(
        INPUT("/bunny_polydata.vtk"),
        OUTPUT("/TestVoxelizeSurfaceMesh.vtk"),
        100, 0, "", false, 0);
}

BOOST_AUTO_TEST_CASE( TestCompareMeshes)
{
    double error_max=-1;
    double error_rms=-1;
    PostProcessingOperators::CompareMeshes(
      error_rms, error_max, INPUT("ircad_disp0.vtu"),  INPUT("ircad_disp50.vtu"), true
      );
    BOOST_REQUIRE(error_max > 5);
    BOOST_REQUIRE(error_max < 6);
}

BOOST_AUTO_TEST_CASE( TestCompareMeshesSame)
{
    double error_max=-1;
    double error_rms=-1;
    PostProcessingOperators::CompareMeshes(
      error_rms, error_max, INPUT("ircad_disp0.vtu"),  INPUT("ircad_disp0.vtu"), true
      );
    BOOST_REQUIRE(error_max < 0.001);
}

BOOST_AUTO_TEST_CASE( TestSelectVolumesByMaterialID)
{
	std::vector<int> group;
	//extract the cylinder mesh (which has a material id of 999)
	group.push_back(999);
    std::string resultMeshFile = MiscMeshOperators::SelectVolumesByMaterialID(INPUT("cylinder_piston.vtk"),
								 OUTPUT("cylinder.vtk"), group);	
	vtkSmartPointer<vtkUnstructuredGrid> resultMesh = IOHelper::VTKReadUnstructuredGrid(resultMeshFile.c_str());
	BOOST_CHECK(resultMesh&&(resultMesh->GetNumberOfCells()>0));
}

BOOST_AUTO_TEST_CASE( TestReplaceMaterialID)
{
	std::vector<int> toReplace;
	toReplace.push_back(1000);
	toReplace.push_back(1001);
	int replaceBy = 42;
	const char* inputImage  =INPUT("cylinder_piston.ctx.gz");
	const char* outputImage  = OUTPUT("cylinder_piston_repl.vti");
	//replace all occurences of 1000 and 1001 by 42
	std::string resultImageFile = MiscMeshOperators::ReplaceMaterialID(inputImage, 
																	   outputImage,toReplace,replaceBy);
	BOOST_CHECK(outputImage==resultImageFile);
 
}

BOOST_AUTO_TEST_CASE(TestExtractFeatures)
{	
	const char* inputMeshFile  = INPUT("bunny_polydata.vtk");
	MSML::FeatureExtractionOperators::Features features = FeatureExtractionOperators::ExtractFeatures(inputMeshFile);
	//bunny has a surface area and volume creater zero, this is known!
	BOOST_CHECK(features.surfaceArea>0);
	BOOST_CHECK(features.volume>0);
 
}

BOOST_AUTO_TEST_CASE(TestBoundsFromMaterialID)
{	
	const char* inputMeshFile  = INPUT("meshed_volume.vtk");
	//get bounds of image thresholded with material ID 42 (inner part)
	std::vector<double> innerBounds = MiscMeshOperators::BoundsFromMaterialID(inputMeshFile,42);
	//get bounds of image thresholded with material ID 1 (outer part)
	std::vector<double> outerBounds = MiscMeshOperators::BoundsFromMaterialID(inputMeshFile,1);
	//xmin_inner > xmin_outer and xmax_inner<xmax_outer
	BOOST_CHECK(innerBounds[0]>outerBounds[0]&&innerBounds[1]<outerBounds[1]);
	//ymin_inner > ymin_outer and ymax_inner<ymax_outer
	BOOST_CHECK(innerBounds[2]>outerBounds[2]&&innerBounds[3]<outerBounds[3]);
	//zmin_inner > zmin_outer and zmax_inner<zmax_outer
	BOOST_CHECK(innerBounds[4]>outerBounds[4]&&innerBounds[5]<outerBounds[5]); 
}


BOOST_AUTO_TEST_CASE(TestSurfaceFromVolumeAndNormalDirection)
{	
	const char* inputMeshFile  = INPUT("bowl.vtk");
	const char* outputMeshFile = OUTPUT("bowl_normals_selected.vtk");
	//select all surface elements with normals facing in z-direction (0,0,1), using an angle margin of 30 deg
	std::vector<double> desiredNormalDir;
	desiredNormalDir.push_back(0);
	desiredNormalDir.push_back(0);
	desiredNormalDir.push_back(1);
	std::string resultFile = MiscMeshOperators::SurfaceFromVolumeAndNormalDirection(inputMeshFile,outputMeshFile,desiredNormalDir,30);
	BOOST_CHECK(outputMeshFile==resultFile);
	//check if resulting surface mesh has less elements than input mesh, but more than zero elements (stupid test)
	vtkSmartPointer<vtkUnstructuredGrid> resultMesh = IOHelper::VTKReadUnstructuredGrid(outputMeshFile);
	vtkSmartPointer<vtkPolyData> inputMesh = IOHelper::VTKReadPolyData(inputMeshFile);
	
	BOOST_CHECK(resultMesh->GetNumberOfCells()>0&&
			   (resultMesh->GetNumberOfCells()<inputMesh->GetNumberOfCells()));		

}

BOOST_AUTO_TEST_CASE(TestComputeDiceCoefficientPolydata)
{	
	const char* inputMeshFileA  = INPUT("bunny_polydata.vtk");
	const char* inputMeshFileB = INPUT("bunny_polydata_transformed.vtk");

	//meshB is a slightly scaled and rotated version of meshA
	double dice = PostProcessingOperators::ComputeDiceCoefficientPolydata(inputMeshFileA,inputMeshFileB,"intersection.vtk");
	//dice coefficient should be over 0.5 
	BOOST_CHECK(dice>0.5&&dice<1);
}



