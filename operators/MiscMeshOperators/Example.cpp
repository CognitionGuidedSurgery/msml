
#include "PostProcessingOperators.h"
#include "MiscMeshOperators.h"
#include <vector>
#include <iostream>
#include <string>
#include <sstream> 
#include <VTKMeshgen.h>
#include <IOHelper.h>

using namespace MSML;


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

void TestComputeVolume()
{
	
  std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume1.vtk");
  std::string inputMesh1("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume2.vtk");
  std::string inputMesh2("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume3.vtk");
  std::string inputMesh3("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume4.vtk");
  std::string inputMesh4("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume100.vtk");
  cout << "Bladder" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh.c_str());
  cout << "Rectum" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh1.c_str());
  cout << "Bowel" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh2.c_str());
  cout << "Bone" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh3.c_str());
  cout << "Prostate" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh4.c_str());
}

void TestComputeCrossSectionArea()
{
	
  std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume1.vtk");
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMesh.c_str());
}

void TestComputeDICECoeff()
{
	
  std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume1.vtk");
  std::string inputMesh2("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume1.vtk");
  PostProcessingOperators::ComputeDiceCoefficient(inputMesh.c_str(), inputMesh2.c_str());
}

void TestTransformMeshBarycentric()
{
  vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\combo.vtk");
	vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\disp10.vtu");
  vtkSmartPointer<vtkUnstructuredGrid> refSurface = IOHelper::VTKReadUnstructuredGrid("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\combo.vtk");
	vtkSmartPointer<vtkUnstructuredGrid> out_surface = vtkSmartPointer<vtkUnstructuredGrid>::New();
  PostProcessingOperators::TransformMeshBarycentric(referenceGrid,out_surface, refSurface, deformedGrid);

}

void TestComparisonFeBioAndSofa()
{
  std::string referenceGrid("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\disp0.vtu");
  std::string deformedGrid("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\disp100.vtu");
  std::string refSurface("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\combo.vtk");
  std::string out_surface("C:\\MSML\\msml\\examples\\CGALPelvis_DKFZ_internal\\disp100_pressure8_10s.vtk");
  std::string outputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk");
  PostProcessingOperators::TransformMeshBarycentric(referenceGrid.c_str(),out_surface.c_str(), refSurface.c_str(), deformedGrid.c_str());
  MiscMeshOperators::ExtractAllSurfacesByMaterial(out_surface.c_str(), outputMesh.c_str(), false);
  
  std::string inputMesh0("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume0.vtk");
  std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume1.vtk");
  std::string inputMesh1("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume2.vtk");
  std::string inputMesh2("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume3.vtk");
  std::string inputMesh3("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume4.vtk");
  std::string inputMesh4("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk-volume100.vtk");

  cerr << "initial Bladder" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh.c_str());
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMesh.c_str());
  cerr << "initial Rectum" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh1.c_str());
  cerr << "initial Bowel" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh2.c_str());
  cerr << "initial Bone" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh3.c_str());
  cerr << "initial Prostate" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMesh4.c_str());
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMesh4.c_str());
  cerr << endl;

  std::string inputMeshFeb0("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume0.vtk");
  std::string inputMeshFeb("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume1.vtk");
  std::string inputMeshFeb1("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume2.vtk");
  std::string inputMeshFeb2("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume3.vtk");
  std::string inputMeshFeb3("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume4.vtk");
  std::string inputMeshFeb4("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/feb_surface.vtk-volume100.vtk");

  cerr << "feb Bladder Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshFeb.c_str());
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMeshFeb.c_str());
  cerr << "feb Rectum Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshFeb1.c_str());
  cerr << "feb Bowel Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshFeb2.c_str());
  cerr << "feb Bone Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshFeb3.c_str());
  cerr << "feb Prostate Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshFeb4.c_str());
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMeshFeb4.c_str());
  cerr << endl;

  std::string inputMeshSofa0("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk-volume0.vtk");
  std::string inputMeshSofa("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk-volume1.vtk");
  std::string inputMeshSofa1("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk-volume2.vtk");
  std::string inputMeshSofa2("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk-volume3.vtk");
  std::string inputMeshSofa3("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk-volume4.vtk");
  std::string inputMeshSofa4("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk-volume100.vtk");

  cerr << "Sofa Bladder Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshSofa.c_str());
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMeshSofa.c_str());
  cerr << "Sofa Rectum Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshSofa1.c_str());
  cerr << "Sofa Bowel Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshSofa2.c_str());
  cerr << "Sofa Bone Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshSofa3.c_str());
  cerr << "Sofa Prostate Pressure 8" << endl;
  PostProcessingOperators::ComputeOrganVolume(inputMeshSofa4.c_str());
  PostProcessingOperators::ComputeOrganCrossSectionArea(inputMeshSofa4.c_str());
  cout << endl;

  cerr << "DICE Coeff Sofa Initial Pelvis" << endl;
  PostProcessingOperators::ComputeDiceCoefficient(inputMesh3.c_str(), inputMeshSofa3.c_str());
  cout << endl;
  cerr << "DICE Coeff Feb Initial Pelvis" << endl;
  PostProcessingOperators::ComputeDiceCoefficient(inputMesh3.c_str(), inputMeshFeb3.c_str());
  cout << endl;
  cerr << "DICE Coeff Feb Initial Bladder" << endl;
  PostProcessingOperators::ComputeDiceCoefficient(inputMesh.c_str(), inputMeshFeb.c_str());
  cout << endl;
  cerr << "DICE Coeff Sofa Initial Bladder" << endl;
  PostProcessingOperators::ComputeDiceCoefficient(inputMesh.c_str(), inputMeshSofa.c_str());
  cout << endl;
  cerr << "DICE Coeff Feb Sofa Bladder" << endl;
  PostProcessingOperators::ComputeDiceCoefficient(inputMeshSofa.c_str(), inputMeshFeb.c_str());
  cout << endl;
  cerr << "DICE Coeff Feb Sofa Prostate" << endl;
  PostProcessingOperators::ComputeDiceCoefficient(inputMeshSofa4.c_str(), inputMeshFeb4.c_str());
}

void TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator()
{
	//std::string inputMesh("E:/GIT/msml/Testdata/CGALi2vExampleResults/liver_kidney_gallbladder.vtk");
	//std::string outputMesh("E:/GIT/msml/Testdata/CGALi2vExampleResults/liver_kidney_gallbladder_surface.vtk");
   //std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/pelvisCase2.vtk");
  //std::string outputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/pelvisCase2_surface.vtk");
	std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/disp50.vtu");
	std::string outputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/sofa_surface.vtk");

	string errorMessage;
	std::string asd("asd");
	MiscMeshOperators::ExtractAllSurfacesByMaterial(inputMesh.c_str(), outputMesh.c_str(), false);

}

void TestConvertFebToVTK(){
  std::string inputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/combo.vtk");
  std::string outputMesh("C:/MSML/msml/examples/CGALPelvis_DKFZ_internal/pelvisCase2.txt");

 PostProcessingOperators::ConvertFEBToVTK(outputMesh, "100", inputMesh);


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


  std::string ref("E:/GIT/msml/examples/CGALi2vExample/CGALExample_lowResults/3Dircadb0101Labeled.vtk");
  std::string def("E:/GIT/msml/examples/CGALi2vExample/CGALExample_lowResults/dispOutput7.vtu");
  std::string dvf("E:/GIT/msml/examples/CGALi2vExample/CGALExample_lowResults/dispOutput7DVF.vtk");

//  PostProcessingOperators::GenerateDVF(ref.c_str(), dvf.c_str(), def.c_str());
}
void TestReadCTX()
{
  IOHelper::CTXReadImage("E:\\02_Data\\skelettonPatModel\\04_HNCfinalIGRTdose\\segmentation.ctx");
}



void TestApplyDVF()
{
  /*std::string ref("E:/02_Data/m_mechanic/simpleResults/refImage.vtk");
  std::string def("E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/deformedImage9.vtk");
  std::string dvf("E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/dvf9.vtk");

  PostProcessingOperators::ApplyDVF(ref.c_str(), def.c_str(), dvf.c_str());

  ref = "E:/02_Data/m_mechanic/simpleResults/refImage.vtk";
  def = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/deformedImage10.vtk";
  dvf = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/dvf10.vtk";

  PostProcessingOperators::ApplyDVF(ref.c_str(), def.c_str(), dvf.c_str());

  ref = "E:/02_Data/m_mechanic/simpleResults/refImage.vtk";
  def = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/deformedImage11.vtk";
  dvf = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/dvf11.vtk";

  PostProcessingOperators::ApplyDVF(ref.c_str(), def.c_str(), dvf.c_str());*/

  std::string ref = "E:/02_Data/m_mechanic/simpleResults/refImage.vtk";
  std::string def = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFApplyResults/deformedImagedvf12_dispToRef_on_disp.vtk";
  std::string dvf = "E:\\02_Data\\m_mechanic\\simpleResults\\generateTheDVFApplyResults\\dvf12_dispToRef_on_disp.vtk";
  
//  PostProcessingOperators::ApplyDVF(ref.c_str(), def.c_str(), dvf.c_str());

  /*ref = "E:/02_Data/m_mechanic/simpleResults/refImage.vtk";
  def = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/deformedImage13.vtk";
  dvf = "E:/02_Data/m_mechanic/simpleResults/generateTheDVFResults/dvf13.vtk";

  PostProcessingOperators::ApplyDVF(ref.c_str(), def.c_str(), dvf.c_str());*/

}


int main( int argc, char * argv[])
{

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
	//TestConvertFebToVTK();
	//TestComputeVolume();
	//TestComputeCrossSectionArea();
	//TestComputeDICECoeff();
	//TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator();
	//return EXIT_SUCCESS;
	//TestExtractSurfaceMeshFromVolumeMeshByCelldataOperator();

	
	TestComparisonFeBioAndSofa();
	
}













