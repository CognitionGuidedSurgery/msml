
#include "PostProcessingOperators.h"
#include "MiscMeshOperators.h"
#include "IndexRegionOperators.h"
#include <vector>
#include <iostream>
#include <string>
#include <sstream> 
#include <VTKMeshgen.h>
#include <IOHelper.h>

using namespace MSML;

#define SMOKE_TEST_DIR_PREFIX smoke
void TestAssignRegionOperator()
{
//	std::string inputMesh("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Medical/Helios_Aktuell/Leber/LeberXSTet4.vtk");
//	std::string outputMesh("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Medical/Helios_Aktuell/Leber/LeberXSTet4Regions.vtk");
//
//
//	std::vector<std::string> regionMeshes;
//	regionMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Medical/Helios_Aktuell/Leber/LeberRegion1.vtk");


	std::string inputMesh("/home/suwelack/IPCAI/Volumes/liverMVolume.vtk");
	std::string outputMesh("/home/suwelack/IPCAI/Volumes/liverMVolumeRegions.vtk");


	std::vector<std::string> regionMeshes;
	regionMeshes.push_back("/home/suwelack/IPCAI/Surfaces/liverSurfaceXLIniFixedBC.vtk");



	string errorMessage;

	MiscMeshOperators::AssignSurfaceRegion(inputMesh.c_str(), outputMesh.c_str(), regionMeshes);

}

void TestTransformMeshBarycentric()
{
  vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid("E:\\02_Data\\j_mechanic\\scenarios_1stmode99\\dispOutput0.vtu");
	vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid("E:\\02_Data\\j_mechanic\\scenarios_1stmode99\\dispOutput125.vtu");
  vtkSmartPointer<vtkUnstructuredGrid> refSurface = IOHelper::VTKReadUnstructuredGrid("E:\\02_Data\\j_mechanic\\allIn100justCGALOptimizerAllOnResults\\boneMesh16.vtk");
	vtkSmartPointer<vtkUnstructuredGrid> out_surface = vtkSmartPointer<vtkUnstructuredGrid>::New();
  PostProcessingOperators::TransformMeshBarycentric(referenceGrid,out_surface, refSurface, deformedGrid, 10);
}

void TestPositionFromIndices()
{
  std::vector<unsigned int> ids;
  ids.push_back(1);
  vector<double> pos = IndexRegionOperators::positionFromIndices("C:\\Projekte\\msml_github\\examples\\BunnyExample\\bunnyout\\liver0.vtu", ids, "points");
}

void TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator()
{
	//std::string inputMesh("E:/GIT/msml/Testdata/CGALi2vExampleResults/liver_kidney_gallbladder.vtk");
	//std::string outputMesh("E:/GIT/msml/Testdata/CGALi2vExampleResults/liver_kidney_gallbladder_surface.vtk");
  std::string inputMesh("E:/GIT/msml/Testdata/3Direcadb11Labeled.vtk.tmp");
  std::string outputMesh("E:/GIT/msml/Testdata/3Direcadb11Labeled_surface.vtk");

	string errorMessage;
  std::string asd("asd");
	MiscMeshOperators::ExtractAllSurfacesByMaterial(inputMesh.c_str(), outputMesh.c_str(), true);

}

void TestMergeMeshes()
{
  /*
  std::string inputCells("E:/GIT/msml/MSML_Python/LungsHighResResults/case1_T00_labled_combo.vtk");
  std::string inputPoints("E:/GIT/msml/MSML_Python/LungsHighResResults/dispOutput");
  std::string outputMesh("E:/GIT/msml/MSML_Python/LungsHighResResults/case1_T00_labledOutput");*/
  
  std::string inputCells("E:/SOFA_trunk/build/applications/projects/runSofa/cycytube_labled_combo.vtk-volume1.vtk");
  std::string inputPoints("E:/SOFA_trunk/build/applications/projects/runSofa/dispOutputOne");
  std::string outputMesh("E:/SOFA_trunk/build/applications/projects/runSofa/case1_T00_labledOutputOne");

  for (int i=0; i<=55;i++)
  {
    std::ostringstream ss;
    ss << i;
    string str = ss.str();

    PostProcessingOperators::MergeMeshes((inputPoints + str + ".vtu").c_str(), inputCells.c_str(), (outputMesh + str + ".vtk").c_str());
  }
}

void TestGenerateDVF()
{
  /*
  std::string inputCells("E:/GIT/msml/MSML_Python/LungsHighResResults/case1_T00_labled_combo.vtk");
  std::string inputPoints("E:/GIT/msml/MSML_Python/LungsHighResResults/dispOutput");
  std::string outputMesh("E:/GIT/msml/MSML_Python/LungsHighResResults/case1_T00_labledOutput");*/


  std::string ref("C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\tetmesh.vtk");
  std::string def("C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\disp20.vtu");
  std::string dvf("C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\tmpTes.vtk");

  PostProcessingOperators::GenerateDVF(ref.c_str(),  def.c_str(), dvf.c_str(), 5, "", 10);
}
void TestReadCTX()
{
  IOHelper::VTKReadImage("C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\pelvisCase.ctx.gz"); //internal data type
}

void TestMarchingCube()
{
  VTKMeshgen::MarchingCube("C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\output_transformFullRTSSmarching_15.09.2014\\RTSS_BLASE.ctx.gz", 
    "C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\output_transformFullRTSSmarching_15.09.2014\\RTSS_BLASE.vtk", 0.5);
}


void TestApplyDVF()
{


  std::string ref = string(TESTDATA_PATH) + "\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\pelvisCaseCTImage.vti";
  std::string def = "C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\output_postprocessing_19.09.2014\\defed10.vtk";
  std::string dvf = "C:\\Projekte\\msml_github\\examples\\CGALPelvis_DKFZ_internal_fuer_MB\\output_pelvisCase_new_12.09.2014\\output_postprocessing_19.09.2014\\dvf10.vtk";
  
  PostProcessingOperators::ApplyDVFPython(ref.c_str(), dvf.c_str(), def.c_str(), false,  2);
}

namespace TestMiscMeshoperators
{
  void TestConvertLinearToQuadraticTetrahedralMesh()
  {
    MiscMeshOperators::ConvertLinearToQuadraticTetrahedralMesh((string(TESTDATA_PATH)+"/bunny_tets.vtk").c_str(), (string(TESTDATA_PATH)+ "/TestConvertLinearToQuadraticTetrahedralMesh.vtk").c_str());
  }

  void TestConvertSTLToVTK()
  {
    MiscMeshOperators::ConvertSTLToVTKPython((string(TESTDATA_PATH)+"/bunny_xl.stl").c_str(), (string(TESTDATA_PATH)+ "/TestConvertSTLToVTKPython.vtk").c_str());
  }

  void TestConvertVTKMeshToAbaqusMeshStringPython()
  {
    std::ofstream aFile;
    aFile.open((string(TESTDATA_PATH)+ "/TestConvertVTKMeshToAbaqusMeshStringPython.abq").c_str());
    string aReturn = MiscMeshOperators::ConvertVTKMeshToAbaqusMeshStringPython((string(TESTDATA_PATH)+"/bunny_tets.vtk").c_str(), "aPart", "aMaterial");
    aFile << aReturn << "\n";
    aFile.close();
  }

  void TestConvertVTKPolydataToUnstructuredGridPython()
  {
    MiscMeshOperators::ConvertVTKPolydataToUnstructuredGridPython((string(TESTDATA_PATH)+"/bunny_polydata.vtk").c_str(),(string(TESTDATA_PATH)+ "/TestConvertVTKPolydataToUnstructuredGridPython.vtu").c_str());
  }

  void TestConvertVTKToOFF()
  {
    MiscMeshOperators::ConvertVTKToOFF(IOHelper::VTKReadPolyData((string(TESTDATA_PATH)+"/bunny_polydata.vtk").c_str()),(string(TESTDATA_PATH)+ "/TestConvertVTKToOFF.off").c_str());
  }

  void TestExtractAllSurfacesByMaterial()
  {
    MiscMeshOperators::ExtractAllSurfacesByMaterial((string(TESTDATA_PATH)+"/ircad_tets_labled.vtk").c_str(), (string(TESTDATA_PATH)+ "/TestExtractAllSurfacesByMaterial.vtk").c_str(), false);
  }

  void TestExtractNodeSet()
  {
    MiscMeshOperators::ExtractNodeSet((string(TESTDATA_PATH)+"/ircad_tets_labled.vtk").c_str(), "nonExtistingNodeset-TestdataNeeded");
  } 

  void TestExtractPointPositions()
  {
    std::vector<int> indices;
    indices.push_back(0);indices.push_back(1);indices.push_back(2);
    std::vector<double> aReturn = MiscMeshOperators::ExtractPointPositions(indices, (string(TESTDATA_PATH)+"/bunny_tets.vtk").c_str());
    if (abs(aReturn[1] - 0.0660446) > 0.000001)
      throw;
  } 

  void TestExtractVectorField()
  {
    std::vector<unsigned int> indices;
    indices.push_back(0);indices.push_back(1);indices.push_back(2);
    MiscMeshOperators::ExtractVectorField((string(TESTDATA_PATH)+"/bunny_tets.vtk").c_str(), "nonExistinFieldTestdataNeeded", indices);
  }
  void TestExtractSurfaceMeshPython()
  {
    MiscMeshOperators::ExtractSurfaceMeshPython((string(TESTDATA_PATH)+"/bunny_tets.vtk").c_str(), (string(TESTDATA_PATH)+ "/TestExtractSurfaceMeshPython_AKA_ugrid_to_polydata.vtk").c_str());
  }

  void TestProjectSurfaceMeshPython()
  {
    MiscMeshOperators::ProjectSurfaceMeshPython((string(TESTDATA_PATH)+"/bunny_polydata_highres.vtk").c_str(), (string(TESTDATA_PATH)+ "/TestProjectSurfaceMeshPython.vtk").c_str(), (string(TESTDATA_PATH)+"/bunny_polydata.vtk").c_str());
  }

  void TestVoxelizeSurfaceMeshPython()
  {
    MiscMeshOperators::VoxelizeSurfaceMeshPython((string(TESTDATA_PATH) + "/bunny_polydata.vtk").c_str(), (string(TESTDATA_PATH) + "/TestVoxelizeSurfaceMeshPython.vtk").c_str(), 100, 0, string("").c_str(), false, 0);
  }
}

void TestPostProcessingOperators()
{
    PostProcessingOperators::ApplyDVFPython((string(TESTDATA_PATH)+"/ircad_ct_image.vti").c_str(), (string(TESTDATA_PATH)+"/ircad_dvf.vti").c_str(), (string(TESTDATA_PATH)+"/TestApplyDVF.vtk").c_str(), true, 2.0);

    PostProcessingOperators::ColorMeshFromComparisonPython((string(TESTDATA_PATH)+"/ircad_disp0.vtu").c_str(),(string(TESTDATA_PATH)+"/ircad_disp50.vtu").c_str(),(string(TESTDATA_PATH)+"/ColorMeshFromComparisonPython.vtk").c_str());
    
    double error_max=-1; double error_rms=-1;
    PostProcessingOperators::CompareMeshes(error_rms, error_max, (string(TESTDATA_PATH)+"/ircad_disp0.vtu").c_str(),  (string(TESTDATA_PATH)+"/ircad_disp50.vtu").c_str(), true);
    if (error_max<1)
      throw;

    PostProcessingOperators::TransformMeshBarycentricPython((string(TESTDATA_PATH)+"/ircad_tris_labled.vtk").c_str(), (string(TESTDATA_PATH)+"/ircad_disp0.vtu").c_str(),  (string(TESTDATA_PATH)+"/ircad_disp50.vtu").c_str(),(string(TESTDATA_PATH)+"/TestTransformMeshBarycentricPython.vtu").c_str(), false);
      
    PostProcessingOperators::GenerateDVF((string(TESTDATA_PATH)+"/ircad_disp50.vtu").c_str(),  (string(TESTDATA_PATH)+"/ircad_disp0.vtu").c_str(),
      (string(TESTDATA_PATH)+"/TestGenerateDVF.vti").c_str(), 10, "", 10);
}

std::vector<std::string> LoadFileNames(std::string theFileListTxt)
{
  std::vector<std::string> fileNames;
	std::ifstream fileStream;
	fileStream.open(theFileListTxt.c_str(), std::ifstream::in);
  if (fileStream)
  {
	  std::string line;  
	  while(getline(fileStream,line))
	  {
      fileNames.push_back(line);
	  }
	  fileStream.close();
  }
  return fileNames;
}
void TestImageSumPrivateData() //TODO: Add test with open accesss data.
{
  std::vector<std::string> files = LoadFileNames("C:\\Projekte\\msml_dkfz\\examples\\j_mechanic\\CTV_2B_mesh_mesh_deformed_sparse_grid_20141117_19_3_5_15_files.txt");
  //files.resize(5);

  /*std::string refCube = "C:\\Projekte\\msml_dkfz\\examples\\j_mechanic\\CTV_2B_refCube_enlarged.vti";
  vtkSmartPointer<vtkPolyData> refMesh = IOHelper::VTKReadPolyData(files[0].c_str());
  vtkSmartPointer<vtkImageData> firstImage = MiscMeshOperators::ImageCreateWithMesh(refMesh, 50);
  MiscMeshOperators::ImageEnlargeIsotropic(firstImage, 50);
  IOHelper::VTKWriteImage(refCube.c_str(), firstImage);*/
  std::string refCube = "C:\\Projekte\\msml_dkfz\\examples\\j_mechanic\\summing_mc_2014117\\CTV_2B_mesh_mesh_deformed_mc_20141117_19_3_5_15_summed_new.vti_voxels_1.vtk";

  PostProcessingOperators::ImageWeightedSum(files, refCube.c_str(), true, "C:\\Projekte\\msml_dkfz\\examples\\j_mechanic\\CTV_2B_mesh_mesh_deformed_sparse_grid_20141117_19_3_5_15__summed_new.vti");
}

int main( int argc, char * argv[])
{
  TestImageSumPrivateData();
  return 0;
  TestPostProcessingOperators();
  
  TestMiscMeshoperators::TestConvertLinearToQuadraticTetrahedralMesh();
  TestMiscMeshoperators::TestConvertSTLToVTK();
  TestMiscMeshoperators::TestConvertVTKMeshToAbaqusMeshStringPython();
  TestMiscMeshoperators::TestConvertVTKPolydataToUnstructuredGridPython();
  TestMiscMeshoperators::TestConvertVTKToOFF();
  TestMiscMeshoperators::TestExtractAllSurfacesByMaterial();
  TestMiscMeshoperators::TestExtractNodeSet();
  TestMiscMeshoperators::TestExtractPointPositions();
  TestMiscMeshoperators::TestExtractVectorField();
  TestMiscMeshoperators::TestExtractSurfaceMeshPython();
  TestMiscMeshoperators::TestProjectSurfaceMeshPython();
  TestMiscMeshoperators::TestVoxelizeSurfaceMeshPython();



	//example: mesh stl surface files with tetgen, export volume to vtk and inp (Abaqus) and export the corresponding surface to stl
  //	std::vector<std::string> inputSurfaceMeshes;
//	std::vector<std::string> outputVolumeMeshes;
//	std::vector<std::string> outputVolumeMeshesINP;
//	std::vector<std::string> outputSurfaceMeshes;
//	TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator();
//
//	inputSurfaceMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon3kTet10.inp");
//	outputVolumeMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon3kTet10.vtk");
//
//	inputSurfaceMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon1kTet10.inp");
//	outputVolumeMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon1kTet10.vtk");
//
//	inputSurfaceMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon220Tet10.inp");
//	outputVolumeMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon220Tet10.vtk");
//
//	inputSurfaceMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon3kTet10Projected.inp");
//	outputVolumeMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon3kTet10Projected.vtk");
//
//	inputSurfaceMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon1kTet10Projected.inp");
//	outputVolumeMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Graphical/AsianDragon/Volume/AsianDragon1kTet10Projected.vtk");
//
//	inputSurfaceMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Medical/Rectum/Rectum.vtk");
//	outputVolumeMeshes.push_back("/org/share/home/mediassi/MediAssistData/Modelle/MIC/Modellbibliothek/Medical/Rectum/RectumVolume.vtk");
//
//	int numberOfModels = inputSurfaceMeshes.size();
//
//	for (unsigned int i = 0; i< numberOfModels;i++)
//	{
//		string errormessage;
//		TetgenOperators::CreateVolumeMesh(inputSurfaceMeshes[i].c_str(), outputVolumeMeshes[i].c_str(), true, false, &errormessage);
////		MiscMeshOperators::VTKToInp( outputVolumeMeshes[i].c_str(), outputVolumeMeshesINP[i].c_str(),  &errormessage);
////		MiscMeshOperators::ExtractSurfaceMesh( outputVolumeMeshes[i].c_str(), outputSurfaceMeshes[i].c_str(),  &errormessage);
////		MiscMeshOperators::ConvertInpToVTK(inputSurfaceMeshes[i].c_str(), outputVolumeMeshes[i].c_str(),&errormessage );
//
//	}
	return EXIT_SUCCESS;
}













