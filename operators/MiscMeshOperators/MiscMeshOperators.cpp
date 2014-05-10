/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, MiscMeshOperators
  Authors:   Markus Stoll, Stefan Suwelack, Nicolai Schoch

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

=========================================================================*/

// ****************************************************************************
// Includes
// ****************************************************************************
#include "MiscMeshOperators.h"
#include <iostream>
#include <sstream>

#include <string.h>

#include <stdio.h>

#include "vtkUnstructuredGrid.h"

#include <vtkXMLUnstructuredGridReader.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkTetra.h>
#include <vtkCellArray.h>
#include <vtkSmartPointer.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkPolyDataWriter.h>
#include <vtkGenericDataObjectReader.h>

#include <vtkPointData.h>
#include <vtkIdList.h>
#include <vtkVertexGlyphFilter.h>
#include <vtkPoints.h>

#include "vtkSTLWriter.h"
#include "vtkPolyDataWriter.h"
#include "vtkPolyDataReader.h"
#include "vtkPolyData.h"
#include "vtkPoints.h"
#include "vtkCellArray.h"
#include <vtkCellData.h>
#include "vtkCleanPolyData.h"
#include "vtkUnsignedIntArray.h"

#include "vtkFloatArray.h"
#include "vtkIntArray.h"
#include "vtkCellData.h"
#include "vtkSTLReader.h"
#include "vtkKdTreePointLocator.h"
#include "vtkVoxelModeller.h"
#include "vtkImageWriter.h"
#include "vtkPNGWriter.h"


#include <vtkDataSetSurfaceFilter.h>
#include "vtkLongLongArray.h"

#include <vtkUnstructuredGridGeometryFilter.h>
#include <vtkUnstructuredGridWriter.h>
#include "vtkDataSetSurfaceFilter.h"
#include "vtkUnstructuredGridGeometryFilter.h"

#include <vtkXMLImageDataReader.h>
#include <vtkXMLImageDataWriter.h>
#include <vtkImageData.h>
#include <vtkPolyDataToImageStencil.h>
#include <vtkImageStencil.h>
#include "vtkFeatureEdges.h"
#include "vtkFillHolesFilter.h"
#include "vtkCleanPolyData.h"
#include "vtkAppendFilter.h"


#include <vtkThreshold.h>
#include <vtkMergeCells.h>

#include "../vtk6_compat.h"
//#include <SOLID/SOLID.h>


using namespace std;

namespace MSML
{

// ****************************************************************************
// Constructor / Destructor
// ****************************************************************************
MiscMeshOperators::MiscMeshOperators()
{

}

MiscMeshOperators::~MiscMeshOperators()
{
	//cleanup here
}

// ****************************************************************************
// Methods
// ****************************************************************************
std::string MiscMeshOperators::ConvertSTLToVTKPython(std::string infile, std::string outfile)
{
	ConvertSTLToVTK( infile.c_str(), outfile.c_str());

	return outfile;
}

bool MiscMeshOperators::ConvertSTLToVTK(const char* infile, const char* outfile)
{
	vtkSmartPointer<vtkPolyData> mesh =
	 vtkSmartPointer<vtkPolyData>::New();

	ConvertSTLToVTK( infile, mesh);

	vtkSmartPointer<vtkPolyDataWriter> writer =
	 vtkSmartPointer<vtkPolyDataWriter>::New();
	writer->SetFileName(outfile);

	__SetInput(writer, mesh);
	writer->Write();

	return true;
}

bool MiscMeshOperators::ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh)
{
	vtkSmartPointer<vtkSTLReader> reader =
	 vtkSmartPointer<vtkSTLReader>::New();
	reader->SetFileName(infile);
	reader->Update();

	//deep copy
	outputMesh->DeepCopy(reader->GetOutput());

	return true;
}

std::string MiscMeshOperators::ConvertVTKToSTLPython(std::string infile, std::string outfile)
{
	ConvertVTKToVTU( infile.c_str(), outfile.c_str());

	return outfile;
}

bool MiscMeshOperators::ConvertVTKToSTL(const char* infile, const char* outfile)
{
	std::cout<<"Converting "<<infile <<" to STL\n";
	vtkSmartPointer<vtkPolyDataReader> reader =
	 vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(infile);
	reader->Update();
	vtkPolyData* currentPolydata = reader->GetOutput();


	vtkSmartPointer<vtkSTLWriter> writer =
	 vtkSmartPointer<vtkSTLWriter>::New();
	writer->SetFileTypeToBinary();
	writer->SetFileName(outfile);
	__SetInput(writer, reader->GetOutput());
	writer->Write();
	std::cout<<"STL file written\n";

	return true;
}

//---------------------------- start of new by Nico on 2014-05-10.
std::string MiscMeshOperators::ConvertVTKToVTUPython(std::string infile, std::string outfile)
{
	ConvertVTKToSTL( infile.c_str(), outfile.c_str());

	return outfile;
}

bool MiscMeshOperators::ConvertVTKToVTU(const char* infile, const char* outfile )
{
	std::cout<<"Converting "<<infile <<" to VTU\n";
	vtkSmartPointer<vtkXMLUnstructuredGridReader> reader = vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();
	reader->SetFileName(infile);
	reader->Update();
	//vtkPolyData* currentPolydata = reader->GetOutput();
	// OR: ?!
	//vtkSmartPointer<vtkUnstructuredGrid> mesh = vtkSmartPointer<vtkUnstructuredGrid>::New();

	//write output
	vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer = vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New(); // vtkUnstructuredGridXML-Writer
	// OR: ?!
	//vtkSmartPointer<vtkUnstructuredGridWriter> writer = vtkSmartPointer<vtkUnstructuredGridWriter>::New(); // vtkUnstructuredGridXML-Writer
	writer->SetFileTypeToBinary();
	writer->SetFileName(outfile);
	__SetInput(writer, reader->GetOutput());
	// OR: ?!
	//__SetInput(writer, mesh);
	writer->Write();
	std::cout<<"VTU file written\n";

	return true;
}

/*
bool ConvertVTKToVTU(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh) // is this needed at all?!
{
	  // Combine the two data sets
	  vtkSmartPointer<vtkAppendFilter> appendFilter = vtkSmartPointer<vtkAppendFilter>::New();

	  __AddInput(appendFilter, inputPolyData);

	  appendFilter->Update();

	  outputMesh->DeepCopy(appendFilter->GetOutput());

	 return true;
}
*/
//---------------------------- end of new by Nico on 2014-05-10.

bool MiscMeshOperators::ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile)
{
	vtkPoints* thePoints = inputMesh->GetPoints();
	vtkIdType noPoints = thePoints->GetNumberOfPoints();

	//open file and generate textstream
	 std::ofstream file(outfile);
	 if (!file.is_open())
		 return false;


	// std::cout<<" number of points3"<<inputMesh->GetNumberOfPoints();
	 //write Header
	 file << "OFF\n"
		<<	 noPoints << " " << inputMesh->GetNumberOfCells() <<" 0\n";

	 std::cout <<" write points \n";

	 double* currentPoint;
	 for(int i=0; i<noPoints; i++)
	 {
		 currentPoint = thePoints->GetPoint(i);
		 file<<currentPoint[0]<<" "<<currentPoint[1]<<" "<<currentPoint[2]<<"\n";
	 }

	 inputMesh->BuildCells(); //this call caused an access violation when this method was part of a SHARED (.dll) library and the ConvertVTKtoOff was called from outside the dll .


		vtkIdType* currentCellPoints;
		//currentCellPoints = new vtkIdType[3];
		vtkIdType numberOfNodes=3;

	 for(int i=0; i<inputMesh->GetNumberOfCells(); i++)
	 {
		 inputMesh->GetCellPoints(i,numberOfNodes,currentCellPoints);
		 file<<3<<" "<<currentCellPoints[0]<<" "<<currentCellPoints[1]<<" "<<currentCellPoints[2]<<"\n";
	 }
	// delete [] currentCellPoints;

	 file.close();

	 return true; //todo: add useful return value
}


bool MiscMeshOperators::ConvertInpToVTK(const char* infile, const char* outfile)
{
	return true;
}

bool MiscMeshOperators::ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh )
{
	return true;
}

std::string MiscMeshOperators::VTKToInpPython( std::string infile, std::string outfile)
{

	VTKToInp( infile.c_str(),  outfile.c_str());
	return outfile;
}

bool MiscMeshOperators::VTKToInp( const char* infile, const char* outfile)
{
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	 vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(infile);
	reader->Update();


	return MiscMeshOperators::VTKToInp(reader->GetOutput(),  outfile);

}

 bool MiscMeshOperators::VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile)
 {
		//open file and generate textstream
//		 QFile file(GetCompleteFilename(filename));
//		 if (!file.open(QFile::WriteOnly | QFile::Truncate))
//			 return false;
//
//		 QTextStream out(&file);

		 std::ofstream out(outfile);
		 if (!out.is_open())
			 return false;

		 out << ConvertVTKMeshToAbaqusMeshString( inputMesh,  std::string("Part1"), std::string("Neo-Hookean"));



		return true;
 }

 std::string MiscMeshOperators::ExtractAllSurfacesByMaterial( const char* infile, const char* outfile, bool theCutIntoPieces)
{
	//load the vtk volume mesh
	vtkSmartPointer<vtkGenericDataObjectReader> reader =
	vtkSmartPointer<vtkGenericDataObjectReader>::New();
	reader->SetFileName(infile);
	reader->Update();
  if (!reader->IsFileUnstructuredGrid())
  {
    cerr << infile << " is not a vtkUnstructuredGrid";
    exit (1);
  }

  vtkUnstructuredGrid* inputGrid = reader->GetUnstructuredGridOutput();
  
  //cut model in pieces
  if (theCutIntoPieces)
  {
    cerr << "Cutting" << std::endl;
    map<int, int> belongstTo;
    std::map<std::pair<int,int>, int> newPrivatePoints; // <oldKey, MaterialId> => newKey
    vtkIntArray* cellMaterialArray0 = (vtkIntArray*) inputGrid->GetCellData()->GetArray("Materials");


    for (int kk= 0;kk<10;kk++)
    {
      belongstTo.clear();

      for(vtkIdType i = 0; i < inputGrid->GetNumberOfCells(); i++)
      {
        ;//cerr << "Checking element " << i << std::endl;
        vtkCell* currentCell = inputGrid->GetCell(i);
        vtkIdList* currentPointIds = currentCell->GetPointIds();
        for(vtkIdType pointId = 0; pointId < currentPointIds->GetNumberOfIds(); pointId++)
        {
          vtkIdType currentPoint = currentPointIds->GetId(pointId);
          if (belongstTo[currentPoint] == 0)
          {
            belongstTo[currentPoint] = (int)*cellMaterialArray0->GetTuple(i);
            ;//cerr << "   empty <- " << (int)*cellMaterialArray0->GetTuple(i) << std::endl;
          }
          else if (belongstTo[currentPoint] == (int)*cellMaterialArray0->GetTuple(i))
            ;//cerr << "   same <-" << (int)*cellMaterialArray0->GetTuple(i) << std::endl;
          else
          {
            cerr << "   replace needed" << pointId << std::endl;
            double* cords = currentCell->GetPoints()->GetPoint(pointId);
            if ( newPrivatePoints[std::make_pair(currentPoint,(int)*cellMaterialArray0->GetTuple(i))] == 0 )
            {
              vtkIdType aNewPointId = inputGrid->GetPoints()->InsertNextPoint(cords[0], cords[1], cords[2] + 0.01 * (int)*cellMaterialArray0->GetTuple(i));
              *(currentPointIds->GetPointer(pointId)) = aNewPointId;
              inputGrid->ReplaceCell(i,currentPointIds->GetNumberOfIds(), currentPointIds->GetPointer(0));
              newPrivatePoints[std::make_pair(currentPoint,(int)*cellMaterialArray0->GetTuple(i))] = aNewPointId;
            }
            else
            {
              *(currentPointIds->GetPointer(pointId)) = newPrivatePoints[std::make_pair(currentPoint,(int)*cellMaterialArray0->GetTuple(i))] ;
              inputGrid->ReplaceCell(i,currentPointIds->GetNumberOfIds(), currentPointIds->GetPointer(0));
            }

          }
        }
      }
      std::cout << "There are " << inputGrid->GetNumberOfCells()  << std::endl;
    }
    vtkSmartPointer<vtkUnstructuredGridWriter> cutGridWriter = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    cutGridWriter->SetFileName((string(outfile) + "-cut.vtk").c_str());
    __SetInput(cutGridWriter,inputGrid);
    cutGridWriter->Write();
  }
  //done cutting



  std::cout << "There are " << reader->GetUnstructuredGridOutput()->GetNumberOfCells()  << " cells before thresholding." << std::endl;

  //get alle surfaces
  vtkIntArray* cellMaterialArray = (vtkIntArray*) reader->GetUnstructuredGridOutput()->GetCellData()->GetArray("Materials");
  map<int,int>* cellDataHist = createHist(cellMaterialArray);


  //create a surface for each material 
  std::vector<vtkSmartPointer<vtkPolyData> > surfaces;
  for (map<int,int>::iterator it=cellDataHist->begin(); it!=cellDataHist->end();it++) //filter for each material
  {
    cout << it->second << " cells of MaterialId=" << it->first << " found." << std::endl;
    vtkSmartPointer<vtkThreshold> threshold = vtkSmartPointer<vtkThreshold>::New();
    __SetInput(threshold, inputGrid);
    threshold->ThresholdBetween(it->first, it->first);
    threshold->SetInputArrayToProcess(0, 0, 0, vtkDataObject::FIELD_ASSOCIATION_CELLS, "Materials"); 
    threshold->Update();

    //debug out surface
    vtkSmartPointer<vtkUnstructuredGridWriter> aUGridWriter = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    stringstream itFirst;
    itFirst << it->first;
    aUGridWriter->SetFileName((string(outfile) + "-volume" + itFirst.str() + ".vtk").c_str());
    __SetInput(aUGridWriter, threshold->GetOutput());
    aUGridWriter->Write();
    //done debug out

    cout << "There are " << threshold->GetOutput()->GetNumberOfCells() << " cells after thresholding with " <<  it->first << std::endl;
    //extract surface
		vtkSmartPointer<vtkPolyData> mesh = vtkSmartPointer<vtkPolyData>::New();

    string error_message;
    bool result = MiscMeshOperators::ExtractSurfaceMesh(threshold->GetOutput(), mesh);
    
    //debug out surface
    vtkSmartPointer<vtkPolyDataWriter> aGridWriter = vtkSmartPointer<vtkPolyDataWriter>::New();
    aGridWriter->SetFileName((string(outfile) + "-surface" + itFirst.str() + ".vtk").c_str());
    __SetInput(aGridWriter, mesh);
    aGridWriter->Write();
    //done debug out

    surfaces.push_back(mesh);
  }

  //merge all surfaces back into a single unstuctured grid - togther with volume cells. Points are unified.
  int numberOfMehes = surfaces.size()+1;
  int numberOfPoints=inputGrid->GetNumberOfPoints();
  int numberOfCells=inputGrid->GetNumberOfCells();
  for (int i=0; i<surfaces.size();i++)
  {
    numberOfPoints+=surfaces[i]->GetNumberOfPoints();
    numberOfCells+=surfaces[i]->GetNumberOfCells();
  }
  vtkSmartPointer<vtkMergeCells> merger = vtkSmartPointer<vtkMergeCells>::New();
  vtkSmartPointer<vtkUnstructuredGrid> unionMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
  merger->SetUnstructuredGrid(unionMesh);
  merger->SetTotalNumberOfCells(numberOfCells);
  merger->SetTotalNumberOfPoints(numberOfPoints);
  merger->MergeDuplicatePointsOn();
  merger->SetPointMergeTolerance(0.00001);
  merger->SetTotalNumberOfDataSets(numberOfMehes);
  //merge it
  for (int i=0; i<surfaces.size();i++)
  {
    int error = merger->MergeDataSet(surfaces[i]);
    if (error) 
    {
      cerr << "vtkMergeCells error during MergeDataSet with surfaces " << i;
      exit(2);
    }
  }
  int error = merger->MergeDataSet(inputGrid);
  if (error) 
    {
      cerr << "vtkMergeCells error during MergeDataSet with volume.";
      exit(2);
    }
  merger->Finish();

	//save the merged data
  vtkSmartPointer<vtkUnstructuredGridWriter> unioGridWriter = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
  unioGridWriter->SetFileName(outfile);
  __SetInput(unioGridWriter, unionMesh);
  unioGridWriter->Write();
  return outfile;
}


    map<int,int>* MiscMeshOperators::createHist(vtkDataArray* theVtkDataArray)
  {
    map<int,int>* hist = new map<int,int>();
    int N = theVtkDataArray->GetNumberOfTuples();
    for (int i=0; i<N;i++)
    { 
      double* v = theVtkDataArray->GetTuple(i);
      //hist[(int)*v] =  hist[(int)*v] + 1 ;
      if (hist->find(*v)!=hist->end())
        hist->at(*v) = hist->at(*v) + 1;
      else
        hist->insert(pair<int,int>(*v,1));
    }
    return hist;
  }

std::string  MiscMeshOperators::ExtractSurfaceMeshPython( std::string infile, std::string outfile)
{
	ExtractSurfaceMesh(infile.c_str(), outfile.c_str());
	return outfile;
}

bool MiscMeshOperators::ExtractSurfaceMesh( const char* infile, const char* outfile)
{
	//load the vtk quadratic mesh
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
	  reader->SetFileName(infile);
	  reader->Update();

		vtkSmartPointer<vtkPolyData> mesh =
		 vtkSmartPointer<vtkPolyData>::New();

	  bool result = MiscMeshOperators::ExtractSurfaceMesh( reader->GetOutput(), mesh);



	  //save the subdivided polydata
	  vtkSmartPointer<vtkPolyDataWriter> polywriter =
	  vtkSmartPointer<vtkPolyDataWriter>::New();
	  polywriter->SetFileName(outfile);
	  __SetInput(polywriter, mesh);
	  polywriter->Write();

	  return result;


}

bool MiscMeshOperators::ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)
{

	//extract the surface as unstructured grid
	vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
		vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
	__SetInput(geom, inputMesh);
	geom->Update();


	//color the polydata elements

	vtkUnstructuredGrid* currentGrid = geom->GetOutput();

	int cellType = currentGrid->GetCellType(1);
	bool isQuadratic = false;

	std::cout<<"CellType is "<<cellType<<"\n";

	if(cellType == 22)
		isQuadratic = true;

	if(isQuadratic)
		std::cout<<"QuadraticMeshDetected\n";

	vtkSmartPointer<vtkDataSetSurfaceFilter> surfaceTessellator =
		vtkSmartPointer<vtkDataSetSurfaceFilter>::New();

	__SetInput(surfaceTessellator, currentGrid);
	if(isQuadratic)
		surfaceTessellator->SetNonlinearSubdivisionLevel(3);
	surfaceTessellator->Update();



	outputMesh->DeepCopy(surfaceTessellator->GetOutput());

	return true; //todo: add useful return value
}

bool MiscMeshOperators::AssignSurfaceRegion( const char* infile, const char* outfile,  std::vector<std::string> regionMeshes )
{
	//load the vtk  mesh
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(infile);
	reader->Update();

	vtkSmartPointer<vtkUnstructuredGrid> mesh =
		vtkSmartPointer<vtkUnstructuredGrid>::New();


	unsigned int meshCount = regionMeshes.size();

	std::vector<vtkSmartPointer<vtkPolyData> > regionMeshesVec;

	for(unsigned int i=0;i<meshCount;i++)
	{
		vtkSmartPointer<vtkPolyDataReader> tempReader =
			vtkSmartPointer<vtkPolyDataReader>::New();
		tempReader->SetFileName(regionMeshes[i].c_str());
		tempReader->Update();

		vtkSmartPointer<vtkPolyData> currentMesh =
			vtkSmartPointer<vtkPolyData>::New();

		currentMesh->DeepCopy(tempReader->GetOutput());
		regionMeshesVec.push_back(currentMesh);


	}


	bool result = MiscMeshOperators::AssignSurfaceRegion( reader->GetOutput() , mesh, regionMeshesVec);



	  //save the subdivided polydata
	  vtkSmartPointer<vtkUnstructuredGridWriter> polywriter =
	  vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	  polywriter->SetFileName(outfile);
	  __SetInput(polywriter, mesh);
	  polywriter->Write();

	  return result;
}

bool MiscMeshOperators::AssignSurfaceRegion( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, std::vector<vtkSmartPointer<vtkPolyData> > &regionMeshes)
{
	unsigned int numberOfVolumePoints = inputMesh->GetNumberOfPoints();

	//deep copy to output mesh
	outputMesh->DeepCopy(inputMesh);

	//create point data with indices
	vtkSmartPointer<vtkUnsignedIntArray> indexData =
		  vtkSmartPointer<vtkUnsignedIntArray>::New();
	indexData->SetNumberOfComponents(1);
	indexData->SetName("indices");

	//create point data and reset to 0
	//create point data with indices
	vtkSmartPointer<vtkUnsignedIntArray> regionData =
		  vtkSmartPointer<vtkUnsignedIntArray>::New();
	regionData->SetNumberOfComponents(1);
	regionData->SetName("indices");

	for(unsigned int i=0; i<numberOfVolumePoints;i++)
	{
		indexData->InsertNextTuple1(i);
		regionData->InsertNextTuple1(0);
	}

	inputMesh->GetPointData()->SetScalars(indexData);




	//extract surface as ug
	vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
			vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
	__SetInput(geom,inputMesh);
	geom->Update();

	vtkUnstructuredGrid* currentSurfaceMesh = geom->GetOutput();


	//for each region mesh
	unsigned int meshCount = regionMeshes.size();
	double* currentPoint = new double[3];

	  vtkSmartPointer<vtkKdTreePointLocator> kDTree =
	    vtkSmartPointer<vtkKdTreePointLocator>::New();
	  kDTree->SetDataSet(currentSurfaceMesh);
	  kDTree->BuildLocator();


	 for(unsigned int i=0;i<meshCount;i++)
	 {
			vtkPoints* currentPoints = regionMeshes[i]->GetPoints();


			//iterate over points
			for( unsigned int iterPoint = 0; iterPoint < currentPoints->GetNumberOfPoints(); iterPoint++)
			{
				//for each point:: assign region to point closest to that point
				currentPoints->GetPoint(iterPoint, currentPoint);

				 vtkIdType iD = kDTree->FindClosestPoint(currentPoint);

				 unsigned int realId = currentSurfaceMesh->GetPointData()->GetScalars()->GetTuple1(iD);

				 regionData->SetTuple1(realId, i+1);

			}

	 }


	 outputMesh->GetPointData()->SetScalars(regionData);


	 return true;

}

std::string MiscMeshOperators::ConvertVTKMeshToAbaqusMeshStringPython(std::string inputMesh,  std::string partName, std::string materialName)
{
	//load the vtk  mesh
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
	  reader->SetFileName(inputMesh.c_str());
	  reader->Update();
	  std::string output = ConvertVTKMeshToAbaqusMeshString( reader->GetOutput(),   partName,  materialName);
	  return output;

}

std::string MiscMeshOperators::ConvertVTKMeshToAbaqusMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName, std::string materialName)
{
	std::stringstream out;
	 //write Header
	 out << "*HEADING\n"
		<< "**  \n"
		<<	 "**  ABAQUS Input Deck Generated by MediAssist FEM Plugin \n"
		<<	 "** \n";

	 //part name
	 out << "*Part, name="<<partName<<"-Part\n";

	 //nodes
	 out << "*Node \n";
	 double* currentPoint;
	 for(int i=0; i<inputMesh->GetNumberOfPoints(); i++)
	 {
		 currentPoint = inputMesh->GetPoint(i);
		 out<<i+1<<", "<<currentPoint[0]<<" , "<<currentPoint[1]<<" , "<<currentPoint[2]<<"\n";
	 }

	 //elements
	 out << "*Element, type=";
	 vtkIdType* currentCellPoints;
	 vtkIdType numberOfNodesPerElement;
	 vtkIdType cellType = inputMesh->GetCellType(0);
	 if(cellType == 24)
	 {
		 out<<"C3D10\n";
		 numberOfNodesPerElement = 10;
		 //currentCellPoints = new double[10];
	 }
	 else
	 {
		 out<<"C3D4\n";
		 numberOfNodesPerElement = 4;
		// currentCellPoints = new double[4];
	 }

	 for(int i=0; i<inputMesh->GetNumberOfCells(); i++)
	 {
		 inputMesh->GetCellPoints(i, numberOfNodesPerElement,currentCellPoints);
		 out<<i+1;
		 for(int j=0;j<numberOfNodesPerElement;j++)
		 {
			out<<" ,"<<currentCellPoints[j]+1;
		 }
		 out<<"\n";
	 }

	 ////////////////////
	 out<<"*Elset, elset=SolidSectionSet, internal, generate\n";
	 out<<"  1,  "<<inputMesh->GetNumberOfCells()<<",     1\n";
	 out<<"** Section: "<<partName<<"-Section\n";
	 out<<"*Solid Section, elset=SolidSectionSet, material="<<materialName<<"\n";

	 ////////////////////////////

	 //end part
	 out<<"*End Part\n";

	return out.str();
}

std::string MiscMeshOperators::ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile)
{
	std::cout<< " Converting vtkPolydata "<<infile.c_str()<<" to vtkUnstructuredGrid "<<outfile.c_str()<<"\n";
	bool result = ConvertVTKPolydataToUnstructuredGrid(infile.c_str(), outfile.c_str());
	return outfile;
}

bool MiscMeshOperators::ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile )
{
	vtkSmartPointer<vtkPolyDataReader> reader =
	vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(infile);
	reader->Update();
	vtkPolyData* currentPolydata = reader->GetOutput();

	//load surface model to solid
	vtkSmartPointer<vtkUnstructuredGrid> mesh =
	 vtkSmartPointer<vtkUnstructuredGrid>::New();

//	vtkSmartPointer<vtkPolyData> mesh =
//	 vtkSmartPointer<vtkPolyData>::New();

	bool returnValue = ConvertVTKPolydataToUnstructuredGrid(currentPolydata ,  mesh);

	//write output
	vtkSmartPointer<vtkUnstructuredGridWriter> writer =
	vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	writer->SetFileName(outfile);
	writer->SetFileTypeToBinary();
	__SetInput(writer, mesh);
	writer->Write();

	return returnValue;
}

bool MiscMeshOperators::ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh)
{

	  // Combine the two data sets
	  vtkSmartPointer<vtkAppendFilter> appendFilter =
	    vtkSmartPointer<vtkAppendFilter>::New();

	  __AddInput(appendFilter, inputPolyData);

	  appendFilter->Update();

	  outputMesh->DeepCopy(appendFilter->GetOutput());

	 return true;

}

std::string MiscMeshOperators::ProjectSurfaceMeshPython(std::string infile, std::string outfile, std::string referenceMesh)
{
	std::cout<< " Projecting surface mesh "<<infile.c_str()<<" to "<<referenceMesh<<" and writing results to "<<outfile<<"\n";
	bool result = ProjectSurfaceMesh(infile.c_str(), outfile.c_str(), referenceMesh.c_str());
	return outfile;
}


bool MiscMeshOperators::ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh )
{
	vtkSmartPointer<vtkPolyDataReader> reader =
	vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(infile);
	reader->Update();
	vtkPolyData* currentGrid = reader->GetOutput();

	//load surface model to solid
	vtkPolyDataReader* readerSTL = vtkPolyDataReader::New();
	readerSTL->SetFileName(referenceMesh);
	readerSTL->Update();

	vtkPolyData*reference = readerSTL->GetOutput();

//	vtkSmartPointer<vtkPolyData> mesh =
//	 vtkSmartPointer<vtkPolyData>::New();

	ProjectSurfaceMesh(currentGrid,  reference);

	//write output
	vtkSmartPointer<vtkPolyDataWriter> writer =
	vtkSmartPointer<vtkPolyDataWriter>::New();
	writer->SetFileName(outfile);
	writer->SetFileTypeToBinary();
	__SetInput(writer,currentGrid);
	writer->Write();

	return true;
}

bool MiscMeshOperators::ProjectSurfaceMesh(vtkPolyData* inputMesh,  vtkPolyData* referenceMesh )
{
//	inputMesh->BuildCells();
//
////	//first add a point data id to each point
////	vtkPoints* thePoints = inputMesh->GetPoints();
////	vtkCellArray* theCells = inputMesh->GetCells();
////	vtkIdType numberOfPoints = thePoints->GetNumberOfPoints();
////	vtkIdType numberOfCells = theCells->GetNumberOfCells();
////
////	vtkSmartPointer<vtkLongLongArray> pointIds =
////	  vtkSmartPointer<vtkLongLongArray>::New();
////	pointIds->SetNumberOfComponents(1);
////	pointIds->SetName("pointIds");
////
////
////	for(unsigned int i=0; i<numberOfPoints;i++) // iterate over all triangles
////	{
////	pointIds->InsertNextTuple1(i);
////	}
////
////	inputMesh->GetPointData()->SetGlobalIds(pointIds);
////
////
////	//extract the surface
////	vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
////		vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
////	geom->SetInput(inputMesh);
////	geom->PassThroughPointIdsOn();
////	geom->SetOriginalPointIdsName("pointIds");
////	geom->Update();
//
//
//	//initialize collision detection
//
//
//
//	DT_ShapeHandle meshShapeHandle = DT_NewComplexShape(0);
//	vtkIdType* currentCellPoints;
//	vtkIdType numberOfNodes=3;
//	float currentVertex[3];
//	double currentVTKVertex[3];
//
//	referenceMesh->BuildCells();
//
//	std::cout<<"Add reference surface mesh to solid \n";
//
//	for(int i=0; i<referenceMesh->GetNumberOfCells(); i++)
//	{
//	 referenceMesh->GetCellPoints(i, numberOfNodes,currentCellPoints);
//	 if(numberOfNodes != 3)
//		 std::cerr<<"WTF:Number of nodes not 3 \n";
//
//	 DT_Begin();
//
//	 for(int j=0; j<numberOfNodes; j++)
//	 {
//		 referenceMesh->GetPoint(currentCellPoints[j], currentVTKVertex);
//		 currentVertex[0] = currentVTKVertex[0];
//		 currentVertex[1] = currentVTKVertex[1];
//		 currentVertex[2] = currentVTKVertex[2];
//		 DT_Vertex(currentVertex);
//	 }
//
//	 DT_End();
//
//	}
//
//	DT_EndComplexShape();
//
//	DT_ObjectHandle meshObjectHandle = DT_CreateObject(0,meshShapeHandle);
//
//
//
//	//iterate over all surface point
////	vtkUnstructuredGrid* surfaceGrid = geom->GetOutput();
////
//	vtkPoints* thePointsSurface = inputMesh->GetPoints();
////	vtkCellArray* theCellsSurface = surfaceGrid->GetCells();
//	vtkIdType numberOfPointsSurface = thePointsSurface->GetNumberOfPoints();
////	vtkIdType numberOfCellsSurface = theCellsSurface->GetNumberOfCells();
//
//
//
//	std::vector<DT_ShapeHandle> pointShapeHandles;
//	pointShapeHandles.resize(numberOfPointsSurface);
//	std::vector<DT_ObjectHandle> pointObjectHandles;
//	pointObjectHandles.resize(numberOfPointsSurface);
//	DT_ShapeHandle currentShapeHandle;
//	DT_ObjectHandle currentObjectHandle;
//
//
//	std::cout<<"Add quadratic surface points to solid \n";
//
//	for(int i=0; i<numberOfPointsSurface; i++)
//	{
//	thePointsSurface->GetPoint(i,currentVTKVertex);
//	currentVertex[0]=currentVTKVertex[0];
//	currentVertex[1]=currentVTKVertex[1];
//	currentVertex[2]=currentVTKVertex[2];
//
//	pointShapeHandles[i] = DT_NewPoint(currentVertex);
//	DT_EndComplexShape();
//	pointObjectHandles[i] = DT_CreateObject(0,pointShapeHandles[i]);
//
//	}
//
//	//for each surface point: project
//
//	float currentPointOnMesh[3];
//	float currentTempPoint[3];
//
//	//vtkLongLongArray* globalIdsSurface = (vtkLongLongArray*)surfaceGrid->GetPointData()->GetGlobalIds("pointIds");//->GetPointData()->get->GetScalars("pointIds");
//
//	std::cout<<"Numberof surface points: "<<numberOfPointsSurface<<"\n";
//
//	std::cout<<"Query nearest point on surface \n";
//
//	for(int i=0; i<numberOfPointsSurface; i++)
//	{
//	currentObjectHandle = pointObjectHandles[i];
//
//	//std::cout<<"CurrentSurfacePointId: "<<i<<" globalID: "<<globalIdsSurface->GetValue(i)<<"\n";
//
//	DT_GetClosestPair(meshObjectHandle,currentObjectHandle,currentPointOnMesh,currentTempPoint);
//
//
//	thePointsSurface->SetPoint(i,  currentPointOnMesh[0],currentPointOnMesh[1],currentPointOnMesh[2] );
//
//	}
//
//	std::cout<<"Save output\n";




	return true;
}

std::string MiscMeshOperators::VoxelizeSurfaceMeshPython(std::string infile, std::string outfile, int resolution)
{
	std::cout<<"Creating image from surface mesh (voxelization)...";
	std::cout<<"Resolution of the longest bound is "<<resolution<<"\n";
	VoxelizeSurfaceMesh(infile.c_str(), outfile.c_str(), resolution);
	return outfile;

}

bool MiscMeshOperators::VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution)
{
	vtkSmartPointer<vtkPolyDataReader> reader =
	 vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(infile);
	reader->Update();

	//deep copy
	vtkPolyData* inputMesh = reader->GetOutput();


	vtkSmartPointer<vtkImageData> outputImage =
	 vtkSmartPointer<vtkImageData>::New();



	bool result = VoxelizeSurfaceMesh(inputMesh, outputImage, resolution);


	vtkSmartPointer<vtkXMLImageDataWriter> writer =
	 vtkSmartPointer<vtkXMLImageDataWriter>::New();
	writer->SetFileName(outfile);
	__SetInput(writer, outputImage);
	writer->Write();

//	vtkSmartPointer<vtkPNGWriter> writer2 =
//	 vtkSmartPointer<vtkPNGWriter>::New();
//	writer2->SetFilePrefix(outfile);
//	writer2->SetInput(outputImage);
//	writer2->Write();



	return true;

}

bool MiscMeshOperators::VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int resolution)
{

//	vtkSmartPointer<vtkVoxelModeller> voxelizer =
//	 vtkSmartPointer<vtkVoxelModeller>::New();
//
//	voxelizer->SetInput(inputMesh);
//	voxelizer->SetScalarTypeToUnsignedChar ();
//	voxelizer->SetSampleDimensions (50,50,50);//

//	voxelizer->Update();

	//clean mesh and fill holes
	  double bounds[6];
	  inputMesh->GetBounds(bounds);

	  //find longest bound
	  double longestBoundValue = 0;
	  double spacing = -1;

	  for (int i = 0; i < 3; i++)
	    {
		  double currentValue = (bounds[i * 2 + 1] - bounds[i * 2]);
		  if(currentValue>longestBoundValue)
		  {
			  longestBoundValue = currentValue;
			  spacing = currentValue / (double)resolution;
		  }
	    }
	  std::cout<<"Longest bound is "<<longestBoundValue<<"\n";
	  std::cout<<"Spacing is "<<spacing<<"\n";

	//detect holes
	vtkSmartPointer<vtkFeatureEdges> featureEdges =
	    vtkSmartPointer<vtkFeatureEdges>::New();

	    featureEdges->FeatureEdgesOff();
	    featureEdges->BoundaryEdgesOn();
	    featureEdges->NonManifoldEdgesOn();
	    __SetInput(featureEdges, inputMesh);
	    featureEdges->Update();
	    int num_open_edges = featureEdges->GetOutput()->GetNumberOfCells();

	    if(num_open_edges)
	    {
	    	double holeSize = 1e20;//bounds[1]-bounds[0];
			std::cout<<"Number of holes is "<<num_open_edges<<", trying to close with hole filler and size of "<< holeSize<<"\n";

			//fill holes
			vtkSmartPointer<vtkFillHolesFilter> fillHolesFilter =
			vtkSmartPointer<vtkFillHolesFilter>::New();

			__SetInput(fillHolesFilter, inputMesh);

			fillHolesFilter->SetHoleSize(holeSize);;

			vtkSmartPointer<vtkCleanPolyData> cleanFilter =
			vtkSmartPointer<vtkCleanPolyData>::New();

			__SetInput(cleanFilter, fillHolesFilter->GetOutput());
			cleanFilter->Update();

			//test again
			__SetInput(featureEdges, fillHolesFilter->GetOutput());
			featureEdges->Update();
			num_open_edges = featureEdges->GetOutput()->GetNumberOfCells();
			std::cout<<"Number of holes ofter filling is "<<num_open_edges<<"\n";

			//replace inputMesh with cleaned data
			inputMesh->DeepCopy(cleanFilter->GetOutput());

	    }

	    std::cout<<"Performing voxelization (this might take while)...\n";

	vtkSmartPointer<vtkImageData> whiteImage =
	    vtkSmartPointer<vtkImageData>::New();

	  double spacingArray[3]; // desired volume spacing
	  spacingArray[0] = spacing;
	  spacingArray[1] = spacing;
	  spacingArray[2] = spacing;
	  whiteImage->SetSpacing(spacingArray);

	  // compute dimensions
	  int dim[3];
	  for (int i = 0; i < 3; i++)
	    {
	    dim[i] = static_cast<int>(ceil((bounds[i * 2 + 1] - bounds[i * 2]) / spacingArray[i]));
	    }

	  whiteImage->SetDimensions(dim);
	  whiteImage->SetExtent(0, dim[0] - 1, 0, dim[1] - 1, 0, dim[2] - 1);

	  double origin[3];
	  origin[0] = bounds[0] + spacingArray[0] / 2;
	  origin[1] = bounds[2] + spacingArray[1] / 2;
	  origin[2] = bounds[4] + spacingArray[2] / 2;
	  whiteImage->SetOrigin(origin);

#if VTK_MAJOR_VERSION <= 5	 
	  whiteImage->SetScalarTypeToUnsignedChar();
	  whiteImage->AllocateScalars();
#else
	  whiteImage->AllocateScalars(VTK_UNSIGNED_CHAR,3);
	  // 3 could be wrong, no   image->SetNumberOfScalarComponents(3); found /Weigl
#endif 


	  // fill the image with foreground voxels:
	  unsigned char inval = 255;
	  unsigned char outval = 0;
	  vtkIdType count = whiteImage->GetNumberOfPoints();
	  for (vtkIdType i = 0; i < count; ++i)
	    {
	    whiteImage->GetPointData()->GetScalars()->SetTuple1(i, inval);
	    }

	  // polygonal data --> image stencil:
	  vtkSmartPointer<vtkPolyDataToImageStencil> pol2stenc =
	    vtkSmartPointer<vtkPolyDataToImageStencil>::New();

	  __SetInput(pol2stenc, inputMesh);
		  


	  pol2stenc->SetOutputOrigin(origin);
	  pol2stenc->SetOutputSpacing(spacingArray);
	  pol2stenc->SetOutputWholeExtent(whiteImage->GetExtent());
	  pol2stenc->Update();

	  // cut the corresponding white image and set the background:
	  vtkSmartPointer<vtkImageStencil> imgstenc =
	    vtkSmartPointer<vtkImageStencil>::New();

	  __SetInput(imgstenc, whiteImage);
	  __SetStencil(imgstenc,pol2stenc->GetOutput());

	  imgstenc->ReverseStencilOff();
	  imgstenc->SetBackgroundValue(outval);
	  imgstenc->Update();

	outputImage->DeepCopy(imgstenc->GetOutput());

	return true;
}

//boost::python::list MiscMeshOperators::ExtractPointPositionsPython( boost::python::list indices, std::string infile)
//{
//	unsigned int indicesSize = boost::python::len(indices);
//	std::vector<int> c_indices;
//	for(int i=0; i<indicesSize; i++)
//	{
//		unsigned int currentIndex = boost::python::extract<int>(indices[i]);
//		c_indices.push_back(currentIndex);
//		std::cout<<"Current index "<<currentIndex;
//	}
//
//	std::vector<double> pointPositions = ExtractPointPositions( c_indices, infile.c_str());
//	boost::python::list positionsPython;
//
//	for(int i=0; i< pointPositions.size();i++)
//	{
//		positionsPython.append(pointPositions[i]);
//	}
//
//
//}

std::vector<double> MiscMeshOperators::ExtractPointPositions( std::vector<int> indices, const char* infile)
{
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	 vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(infile);
	reader->Update();


	return MiscMeshOperators::ExtractPointPositions(indices ,reader->GetOutput());
}

std::vector<double> MiscMeshOperators::ExtractPointPositions( std::vector<int> indices, vtkUnstructuredGrid* inputMesh)
{
	std::vector<double> outputPositions;

	vtkPoints* thePoints = inputMesh->GetPoints();
	double currentPoint[3];

	for(int i=0; i<indices.size(); i++)
	{
		thePoints->GetPoint(indices[i],currentPoint);
		outputPositions.push_back(currentPoint[0]);
		outputPositions.push_back(currentPoint[1]);
		outputPositions.push_back(currentPoint[2]);

	}

	return outputPositions;

}



}
