#include "common.h"

#define BOOST_TEST_MODULE MiscMeshOperatorsTest
#include <boost/test/unit_test.hpp>

#define INPUT(x) (TESTDATA_PATH "/input/" x)
#define OUTPUT(x) (TESTDATA_PATH "/tmp/" x)
#define REFERENCE(x) (TESTDATA_PATH "/reference/" x)


BOOST_AUTO_TEST_CASE( TestAssignRegionOperator )
{
    const char* inputMesh = INPUT("liverMVolume.vtk");
    const char* outputMesh = OUTPUT("liverMVolumeRegions.vtk");

    REQUIRE_FILE_EXISTS(inputMesh);

    std::vector<std::string> regionMeshes;
    regionMeshes.push_back(INPUT("liverSurfaceXLIniFixedBC.vtk"));

    string errorMessage;
    MiscMeshOperators::AssignSurfaceRegion(inputMesh, outputMesh, regionMeshes);
}

BOOST_AUTO_TEST_CASE( TestTransformMeshBarycentric)
{
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid =
        IOHelper::VTKReadUnstructuredGrid(REFERENCE("dispOutput0.vtu"));
    vtkSmartPointer<vtkUnstructuredGrid> deformedGrid =
        IOHelper::VTKReadUnstructuredGrid("dispOutput125.vtu");
    vtkSmartPointer<vtkUnstructuredGrid> refSurface =
        IOHelper::VTKReadUnstructuredGrid("boneMesh16.vtk");
    vtkSmartPointer<vtkUnstructuredGrid> out_surface =
        vtkSmartPointer<vtkUnstructuredGrid>::New();

    PostProcessingOperators::TransformMeshBarycentric(referenceGrid,out_surface,
                                                      refSurface, deformedGrid, 10);
}

BOOST_AUTO_TEST_CASE( TestPositionFromIndices)
{
    std::vector<unsigned int> ids;
    ids.push_back(1);
    vector<double> pos = IndexRegionOperators::positionFromIndices(
              INPUT("liver0.vtu"), ids, "points");
}

BOOST_AUTO_TEST_CASE(TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator)
{
    const char* inputMesh = INPUT("3Direcadb11Labeled.vtk.tmp");
    const char* outputMesh = OUTPUT("3Direcadb11Labeled_surface.vtk");
    std::string output = MiscMeshOperators::ExtractAllSurfacesByMaterial(
                             inputMesh, outputMesh, true);

    BOOST_CHECK(outputMesh==output);
}

BOOST_AUTO_TEST_CASE( TestMergeMeshes)
{
    const char* inputCells = INPUT("cycytube_labled_combo.vtk-volume1.vtk");
    const char* inputPoints = INPUT("dispOutputOne");
    const char* outputMesh  = OUTPUT("case1_T00_labledOutputOne");

    for (int i=0; i<=55; i++)
    {
        std::ostringstream s1;
        s1 << inputPoints << i << ".vtu";
        string p = s1.str();

        std::ostringstream s2;
        s2 << outputMesh << i << ".vtk";
        string m = s2.str();

        PostProcessingOperators::MergeMeshes(p.c_str(), inputCells, m.c_str());
    }
}

BOOST_AUTO_TEST_CASE( TestGenerateDVF)
{
    const char* ref = REFERENCE("tetmesh.vtk");
    const char* def = "output_pelvisCase_new_12.09.2014\\disp20.vtu";
    const char* dvf = OUTPUT("tmpTes.vtk");

    PostProcessingOperators::GenerateDVF(ref,  def, dvf, 5, "", 10);
}

BOOST_AUTO_TEST_CASE( TestReadCTX)
{
    IOHelper::VTKReadImage(INPUT("pelvisCase.ctx.gz")); //internal data type
}

BOOST_AUTO_TEST_CASE( TestMarchingCube )
{
    VTKMeshgen::MarchingCube("RTSS_BLASE.ctx.gz", "RTSS_BLASE.vtk", 0.5);
}

BOOST_AUTO_TEST_CASE( TestApplyDVF)
{
    const char* ref = REFERENCE("pelvisCaseCTImage.vti");
    const char* def = INPUT("defed10.vtk");
    const char* dvf = OUTPUT("dvf10.vtk");

    PostProcessingOperators::ApplyDVFPython(ref, dvf, def, false,  2);
}

BOOST_AUTO_TEST_CASE( TestConvertLinearToQuadraticTetrahedralMesh)
{
    MiscMeshOperators::ConvertLinearToQuadraticTetrahedralMesh(
        INPUT("/bunny_tets.vtk"),
        OUTPUT("TestConvertLinearToQuadraticTetrahedralMesh.vtk"));
}

BOOST_AUTO_TEST_CASE( TestConvertSTLToVTK)
{
    MiscMeshOperators::ConvertSTLToVTKPython((string(TESTDATA_PATH)+"/bunny_xl.stl").c_str(), (string(TESTDATA_PATH)+ "/TestConvertSTLToVTKPython.vtk").c_str());
}

BOOST_AUTO_TEST_CASE( TestConvertVTKMeshToAbaqusMeshStringPython)
{
    std::ofstream aFile;
    aFile.open((string(TESTDATA_PATH)+ "/TestConvertVTKMeshToAbaqusMeshStringPython.abq").c_str());
    string aReturn = MiscMeshOperators::ConvertVTKMeshToAbaqusMeshStringPython((string(TESTDATA_PATH)+"/bunny_tets.vtk").c_str(), "aPart", "aMaterial");
    aFile << aReturn << "\n";
    aFile.close();
}

BOOST_AUTO_TEST_CASE( TestConvertVTKPolydataToUnstructuredGridPython)
{
    MiscMeshOperators::ConvertVTKPolydataToUnstructuredGridPython((string(TESTDATA_PATH)+"/bunny_polydata.vtk").c_str(),(string(TESTDATA_PATH)+ "/TestConvertVTKPolydataToUnstructuredGridPython.vtu").c_str());
}

BOOST_AUTO_TEST_CASE( TestConvertVTKToOFF)
{
    MiscMeshOperators::ConvertVTKToOFF(
        IOHelper::VTKReadPolyData(
            INPUT("bunny_polydata.vtk")),
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

double abs(double d)
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

    BOOST_CHECK( abs(aReturn[1] - 0.0660446) > 0.000001 );
}

BOOST_AUTO_TEST_CASE( TestExtractVectorField )
{
    std::vector<unsigned int> indices;
    indices.push_back(0);
    indices.push_back(1);
    indices.push_back(2);
    MiscMeshOperators::ExtractVectorField(
        INPUT("/bunny_tets.vtk"),
        "nonExistinFieldTestdataNeeded", indices);
}
BOOST_AUTO_TEST_CASE( TestExtractSurfaceMeshPython)
{
    MiscMeshOperators::ExtractSurfaceMeshPython(
        INPUT("/bunny_tets.vtk"),
        INPUT("/TestExtractSurfaceMeshPython_AKA_ugrid_to_polydata.vtk"));
}

BOOST_AUTO_TEST_CASE( TestProjectSurfaceMeshPython )
{
    MiscMeshOperators::ProjectSurfaceMeshPython(INPUT("bunny_polydata_highres.vtk"),
                                                OUTPUT("TestProjectSurfaceMeshPython.vtk"),
                                                INPUT("bunny_polydata.vtk"));
}

BOOST_AUTO_TEST_CASE( TestVoxelizeSurfaceMeshPython )
{
    MiscMeshOperators::VoxelizeSurfaceMeshPython(
        INPUT("/bunny_polydata.vtk"),
        OUTPUT("/TestVoxelizeSurfaceMeshPython.vtk"),
        100, "");
}

BOOST_AUTO_TEST_CASE( TestPostProcessingOperators)
{
    PostProcessingOperators::ApplyDVFPython(
        INPUT("/ircad_ct_image.vti"),
        INPUT("ircad_dvf.vti"),
        OUTPUT("/TestApplyDVF.vtk"), true, 2.0);

    PostProcessingOperators::ColorMeshFromComparisonPython(
        INPUT("ircad_disp0.vtu"),
        INPUT("ircad_disp50.vtu"),
        OUTPUT("ColorMeshFromComparisonPython.vtk"));

    double error_max=-1;
    double error_rms=-1;
    PostProcessingOperators::CompareMeshes(error_rms, error_max, (string(TESTDATA_PATH)+"/ircad_disp0.vtu").c_str(),  (string(TESTDATA_PATH)+"/ircad_disp50.vtu").c_str(), true);

    BOOST_REQUIRE(error_max < 1);

    PostProcessingOperators::TransformMeshBarycentricPython(
        INPUT("ircad_tris_labled.vtk"),
        INPUT("ircad_disp0.vtu"),
        INPUT("ircad_disp50.vtu"),
        OUTPUT("TestTransformMeshBarycentricPython.vtu"), false);

    PostProcessingOperators::GenerateDVF(INPUT("ircad_disp50.vtu"),
                                         INPUT("ircad_disp0.vtu"),
                                         OUTPUT("TestGenerateDVF.vti"), 10, "", 10);
}
