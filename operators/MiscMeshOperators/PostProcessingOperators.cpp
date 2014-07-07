/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, MiscMeshOperators
  Authors:   Markus Stoll, Stefan Suwelack

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
#include "PostProcessingOperators.h"
#include "IOHelper.h"
#include <iostream>
#include <fstream>
#include <sstream>


#include <string.h>
#include <stdio.h>

#include "vtkUnstructuredGrid.h"

#include <vtkXMLUnstructuredGridReader.h>
#include <vtkTetra.h>
#include <vtkCellArray.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkXMLImageDataWriter.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkSTLReader.h>
#include <vtkPolyDataWriter.h>

#include <vtkPointData.h>
#include <vtkIdList.h>
#include <vtkVertexGlyphFilter.h>
#include <vtkPoints.h>
#include <vtkUnstructuredGrid.h>

#include "vtkSTLWriter.h"
#include "vtkSTLReader.h"
#include "vtkPolyData.h"
#include "vtkImageData.h"
#include "vtkPoints.h"
#include "vtkCellArray.h"
#include "vtkCleanPolyData.h"

#include "vtkFloatArray.h"
#include "vtkDoubleArray.h"
#include "vtkCellData.h"


#include <vtkDataSetSurfaceFilter.h>
#include "vtkLongLongArray.h"

#include <vtkUnstructuredGridGeometryFilter.h>
#include <vtkUnstructuredGridWriter.h>

#include <vtkStructuredPoints.h>
#include <vtkStructuredPointsReader.h>
#include <vtkStructuredPointsWriter.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkCellLocator.h>

#include <vtkImageInterpolator.h>

#include "math.h"

#include <boost/graph/sequential_vertex_coloring.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/filesystem.hpp>
#include <boost/lexical_cast.hpp>

using namespace boost;

#include "../vtk6_compat.h"


namespace MSML
{



// ****************************************************************************
// Constructor / Destructor
// ****************************************************************************
PostProcessingOperators::PostProcessingOperators()
{

}

PostProcessingOperators::~PostProcessingOperators()
{
	//cleanup here
}

// ****************************************************************************
// Methods
// ****************************************************************************


void PostProcessingOperators::CompareMeshes(std::vector<double> & errorVec, const char* referenceFilename, const char* testFilename, bool surfaceOnly)
{
	//load the meshes
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(referenceFilename);
	reader->Update();
	vtkUnstructuredGrid* referenceGrid = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 =
	vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader2->SetFileName(testFilename);
	reader2->Update();
	vtkUnstructuredGrid* testGrid = reader2->GetOutput();

	CompareMeshes(errorVec, referenceGrid, testGrid, surfaceOnly);
}

void PostProcessingOperators::CompareMeshes(std::vector<double> & errorVec, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly)
{

	vtkPoints* refPoints = referenceMesh->GetPoints();
	vtkPoints* testPoints = testMesh->GetPoints();

	if(surfaceOnly)
	{
			vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
					vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
			__SetInput(geom, referenceMesh);
			geom->Update();

			vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom2 =
					vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
			__SetInput(geom2,testMesh);
			geom2->Update();

			refPoints->DeepCopy(geom->GetOutput()->GetPoints());
			testPoints->DeepCopy(geom2->GetOutput()->GetPoints());


	}


	//get the points
//	vtkPoints* refPoints = referenceMesh->GetPoints();
//	vtkPoints* testPoints = testMesh->GetPoints();

	unsigned int numberOfRefPoints = refPoints->GetNumberOfPoints();

	unsigned int numberOfTestPoints = testPoints->GetNumberOfPoints();

	if(numberOfRefPoints != numberOfTestPoints)
	{
		std::cout<<"Error, meshes have to be the same size!!";
				return;
	}

	//initialize errorVec
	errorVec.resize(numberOfRefPoints);




		double* currentTestPoint = new double[3];
		double* currentRefPoint = new double[3];
		double currentError;


		for(unsigned int i=0; i<numberOfRefPoints;i++)
		{
			refPoints->GetPoint(i, currentRefPoint);
			testPoints->GetPoint(i, currentTestPoint);

//			std::cout<<"Point No "<<i<<": ("<<currentRefPoint[0]<<","<<currentRefPoint[1]<<","<<currentRefPoint[2]<<"),("<<currentTestPoint[0]<<","<<currentTestPoint[1]<<","<<currentTestPoint[2]<<")\n";

			currentError =  sqrt(pow((currentRefPoint[0]-currentTestPoint[0]), 2) + pow((currentRefPoint[1]-currentTestPoint[1]), 2) + pow((currentRefPoint[2]-currentTestPoint[2]), 2));// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );
	//		currentError =  sqrt((currentRefPoint[0]-currentTestPoint[0])*(currentRefPoint[0]-currentTestPoint[0]) + (currentRefPoint[1]-currentTestPoint[1])*(currentRefPoint[1]-currentTestPoint[1]) + (currentRefPoint[2]-currentTestPoint[2])*(currentRefPoint[2]-currentTestPoint[2]) );// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );

	//		std::cout<<"CurrentError "<<currentError<<"\n";

			errorVec[i]= currentError;

		}





}

void PostProcessingOperators::CompareMeshes(double & errorRMS, double & errorMax, const char* referenceFilename, const char* testFilename, bool surfaceOnly)
{
	//load the meshes
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(referenceFilename);
	reader->Update();
	vtkUnstructuredGrid* referenceGrid = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 =
	vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader2->SetFileName(testFilename);
	reader2->Update();
	vtkUnstructuredGrid* testGrid = reader2->GetOutput();

	CompareMeshes(errorRMS, errorMax, referenceGrid, testGrid, surfaceOnly);

}

void PostProcessingOperators::CompareMeshes(double & errorRMS, double & errorMax, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly)
{

	errorRMS = 0;
	errorMax = 0;

	vtkPoints* refPoints = referenceMesh->GetPoints();
	vtkPoints* testPoints = testMesh->GetPoints();

	if(surfaceOnly)
	{
			vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
					vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
			__SetInput(geom, referenceMesh);
			geom->Update();

			vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom2 =
					vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
			__SetInput(geom2, testMesh);
			geom2->Update();

			refPoints->DeepCopy(geom->GetOutput()->GetPoints());
			testPoints->DeepCopy(geom2->GetOutput()->GetPoints());


	}


	//get the points
//	vtkPoints* refPoints = referenceMesh->GetPoints();
//	vtkPoints* testPoints = testMesh->GetPoints();

	unsigned int numberOfRefPoints = refPoints->GetNumberOfPoints();

	unsigned int numberOfTestPoints = testPoints->GetNumberOfPoints();

	if(numberOfRefPoints != numberOfTestPoints)
	{
		std::cout<<"Error, meshes have to be the same size!!";
				return;
	}




		double* currentTestPoint = new double[3];
		double* currentRefPoint = new double[3];
		double currentError;


		for(unsigned int i=0; i<numberOfRefPoints;i++)
		{
			refPoints->GetPoint(i, currentRefPoint);
			testPoints->GetPoint(i, currentTestPoint);

			currentError =  sqrt(pow((currentRefPoint[0]-currentTestPoint[0]), 2) + pow((currentRefPoint[1]-currentTestPoint[1]), 2) + pow((currentRefPoint[2]-currentTestPoint[2]), 2));// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );
	//		currentError =  sqrt((currentRefPoint[0]-currentTestPoint[0])*(currentRefPoint[0]-currentTestPoint[0]) + (currentRefPoint[1]-currentTestPoint[1])*(currentRefPoint[1]-currentTestPoint[1]) + (currentRefPoint[2]-currentTestPoint[2])*(currentRefPoint[2]-currentTestPoint[2]) );// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );

	//		std::cout<<"CurrentError "<<currentError<<"\n";

			errorRMS += currentError;
			if(currentError > errorMax)
				errorMax = currentError;

		}


		errorRMS = errorRMS / numberOfRefPoints;
		errorRMS = sqrt(errorRMS);






}

void PostProcessingOperators::ColorMeshFromComparison(const char* modelFilename, const char* referenceFilename, const char* coloredModelFilename)
{
	//load the meshes
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(referenceFilename);
	reader->Update();
	vtkUnstructuredGrid* referenceGrid = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 =
	vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader2->SetFileName(modelFilename);
	reader2->Update();
	vtkUnstructuredGrid* modelGrid = reader2->GetOutput();

	vtkSmartPointer<vtkUnstructuredGrid> coloredGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();

	ColorMeshFromComparison(modelGrid, referenceGrid, coloredGrid);

	//write output
	vtkSmartPointer<vtkUnstructuredGridWriter> writer =
	vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	writer->SetFileName(coloredModelFilename);
	__SetInput(writer, coloredGrid);
	writer->Write();
}

void PostProcessingOperators::FeBioToVTKConversion(const std::string modelFilename, const std::string lastStep, std::string inputMesh)
{
	vtkSmartPointer<vtkPoints> thePointsOutput =
		 vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkUnstructuredGrid> vtkGrid = 
		vtkSmartPointer<vtkUnstructuredGrid>::New();
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(inputMesh.c_str());
	reader->Update();
	vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = reader->GetOutput();
	vtkCellArray* theCells = referenceGrid->GetCells();
	vtkDataArray* scalars = referenceGrid->GetCellData()->GetScalars();
	int cellType = referenceGrid->GetCellType(1);
	fstream f;
	char cstring[256];
	f.open(modelFilename, ios::in);
	std::string prefix = "*";
	bool start = false;
	bool started = false;

    while (!f.eof())
    {
		double arr [4];
        f.getline(cstring, sizeof(cstring));
        int i = 0;
		stringstream ssin(cstring);
		std::string temp;
		if(cstring[0] == '*'){
			if(started == true){
				break;
			}
			while (ssin >> temp) {
				if(temp == lastStep) {
					start = true;
				}
			}
		} else {
			if(start){
				started = true;
				bool end = false;
				while (ssin.good() && i < 4){	
					if(!ssin.str().empty()){
						ssin>>arr[i];
						++i;
					} else {
						end = true;
						break;
					}
				}
				if(!end){
					thePointsOutput->InsertNextPoint(arr[1], arr[2], arr[3]);
				}
			}
		}
		
    }
    f.close();
	string::size_type idx = modelFilename.find('.');
	std::string vtkFile = modelFilename.substr(0, idx) + ".vtk";
	vtkGrid->SetPoints(thePointsOutput);
	vtkSmartPointer<vtkUnstructuredGridWriter> writer =
	vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	writer->SetFileName(vtkFile.c_str());
	vtkGrid->SetCells(cellType, theCells);
	vtkGrid->GetCellData()->SetScalars(scalars);
	__SetInput(writer, vtkGrid);
	writer->Write();
}

void PostProcessingOperators::ColorMeshFromComparison(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* referenceMesh,vtkUnstructuredGrid* coloredMesh)
{
	vtkSmartPointer<vtkUnstructuredGrid> theMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
	theMesh->DeepCopy(referenceMesh);

	std::vector<double> errorVec;
	CompareMeshes(errorVec, referenceMesh, inputMesh, false);

	if(errorVec.size() != inputMesh->GetNumberOfPoints())
	{
		std::cout<<"Size mismatch between errorVec and inputMesh size\n";
		return;
	}

	vtkSmartPointer<vtkDoubleArray> dataArray = vtkSmartPointer<vtkDoubleArray> ::New();
	dataArray->SetNumberOfComponents(1);
	dataArray->SetNumberOfTuples(errorVec.size());

	for(unsigned int i=0; i<errorVec.size(); i++)
	{
		dataArray->SetTuple1(i, errorVec[i]);
	}

	theMesh->GetPointData()->AddArray(dataArray);
	dataArray->SetName("Errors");

	coloredMesh->DeepCopy(theMesh);
}

std::string PostProcessingOperators::ColorMeshFromComparisonPython(std::string modelFilename, std::string referenceFilename, std::string coloredModelFilename)
{
	std::cout<<"Coloring mesh with errors...";
	ColorMeshFromComparison(modelFilename.c_str(), referenceFilename.c_str(),coloredModelFilename.c_str());
	return coloredModelFilename;
}

std::string PostProcessingOperators::ColorMeshPython(std::string modelFilename, std::string coloredModelFilename)
{
	std::cout<<"Coloring mesh...";
	ColorMesh(modelFilename.c_str(), coloredModelFilename.c_str());
	return coloredModelFilename;
}


void PostProcessingOperators::ColorMesh(const char* modelFilename, const char* coloredModelFilename)
{
		//load the vtk quadratic mesh
		vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
		reader->SetFileName(modelFilename);
		reader->Update();

		vtkUnstructuredGrid* currentGrid = reader->GetOutput();

		vtkSmartPointer<vtkPolyData> surface =
		 vtkSmartPointer<vtkPolyData>::New();

		ColorMesh(currentGrid, surface);

		//write output
		vtkSmartPointer<vtkPolyDataWriter> polywriter =
				vtkSmartPointer<vtkPolyDataWriter>::New();
		polywriter->SetFileName(coloredModelFilename);
		__SetInput(polywriter, surface);
		polywriter->Write();

}

void PostProcessingOperators::ComputeDiceCoefficient(const char* filename, const char* filename2)
{
		vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
		vtkSmartPointer<vtkUnstructuredGridReader> reader2 =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
		reader->SetFileName(filename);
		reader->Update();
		vtkUnstructuredGrid* currentGrid = reader->GetOutput();
		reader2->SetFileName(filename2);
		reader2->Update();
		vtkUnstructuredGrid* referenceGrid = reader2->GetOutput();
		double* currentPoint;
		double* referencePoint;
		int countOfEqualPoints = 0;
		int currentGridNumberOfPoints = currentGrid->GetNumberOfPoints();
		int referenceGridNumberOfPoints = referenceGrid->GetNumberOfPoints();
		for(int i=0; i < currentGridNumberOfPoints; i++){
			bool coordinateIsEqual[3];
			currentPoint = currentGrid->GetPoint(i);
			referencePoint = referenceGrid->GetPoint(i);
			for(int m = 0; m < 3; m++){
				currentPoint[m] == referencePoint[m] ? coordinateIsEqual[m] = true : coordinateIsEqual[m] = false;
			} 
			if(coordinateIsEqual[0] && coordinateIsEqual[1] && coordinateIsEqual[2]){
				countOfEqualPoints++;
			}
		}

		double diceCoefficient = (double)(2*countOfEqualPoints)/(currentGridNumberOfPoints +  referenceGridNumberOfPoints);
		std::cout << "Count equal points: " << countOfEqualPoints << std::endl << "Number of points input1: " << currentGridNumberOfPoints <<  std::endl << "Number of points input2: " << referenceGridNumberOfPoints
			<<  std::endl << "DICE Coefficient: " << diceCoefficient <<  std::endl;

}

void PostProcessingOperators::ComputeOrganVolume(const char* volumeFilename){
		vtkSmartPointer<vtkUnstructuredGridReader> reader =
		vtkSmartPointer<vtkUnstructuredGridReader>::New();
		reader->SetFileName(volumeFilename);
		reader->Update();
		vtkUnstructuredGrid* inputMesh = reader->GetOutput();
		vtkIdType* currentCellPoints;
		vtkIdType numberOfNodesPerElement;
		double volume = 0;
	 for(int i=0; i<inputMesh->GetNumberOfCells(); i++)
	 {
		 inputMesh->GetCellPoints(i, numberOfNodesPerElement, currentCellPoints);
		 if(numberOfNodesPerElement == 4) {
			 double tetraPoints[4][3]; 
			 double *currentPoint;
			
			 for(int j=0; j<numberOfNodesPerElement; j++)
			 {
				currentPoint = inputMesh->GetPoint(currentCellPoints[j]);

				for(int m=0; m < 3; m++){
					tetraPoints[j][m] = currentPoint[m];
				}
			 }
			 vtkTetra* vtkTetra = vtkTetra::New();
			 volume += vtkTetra->ComputeVolume(tetraPoints[0], tetraPoints[1], tetraPoints[2], tetraPoints[3]);
	    }
		
	 }

	 std::cout << "Count Tetrahedron: " << inputMesh->GetNumberOfCells() << endl << "Volume: " << volume << " mm^3" << endl;

}

void PostProcessingOperators::ColorMesh(vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)
{
	//extract the surface as unstructured grid
	vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
	  	    vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
	__SetInput(geom, inputMesh);
	geom->Update();


	//color the polydata elements

	vtkUnstructuredGrid* currentGrid = geom->GetOutput();

	vtkPoints* thePoints = currentGrid->GetPoints();
	vtkCellArray* theCells = currentGrid->GetCells();
	vtkIdType numberOfPoints = thePoints->GetNumberOfPoints();
	vtkIdType numberOfCells = theCells->GetNumberOfCells();


	int cellType = currentGrid->GetCellType(1);
	bool isQuadratic = false;

	std::cout<<"CellType is "<<cellType<<"\n";

	if(cellType == 22)
		isQuadratic = true;

	if(isQuadratic)
		std::cout<<"QuadraticMeshDetected\n";

	typedef adjacency_list<listS, vecS, undirectedS> Graph;
	typedef graph_traits<Graph>::vertex_descriptor vertex_descriptor;
	typedef graph_traits<Graph>::vertices_size_type vertices_size_type;
	typedef property_map<Graph, vertex_index_t>::const_type vertex_index_map;

	typedef std::pair<int, int> Edge;

	std::vector<Edge> edge_array;



	for(unsigned int i=0; i<numberOfCells;i++) // iterate over all triangles
	{
		// Returns the set of element indices connected to an input one (i.e. which can be reached by topological links)
		//vector<unsigned int> connectedElements = main->m_Topology->getConnectedElement(i); // seems not implemented in the topology!!

		std::set<int> connectedElements; // Set of all tetrahedra which are connected with the tetrahedra nr. "i"

		vtkSmartPointer<vtkIdList> cellPointIds =
		    vtkSmartPointer<vtkIdList>::New();

		currentGrid->GetCellPoints(i, cellPointIds);

		for(int edgeIter=0; edgeIter<3; edgeIter++)// over 3 faces
		{
			vtkSmartPointer<vtkIdList> idList =
			      vtkSmartPointer<vtkIdList>::New();
			idList->InsertNextId(cellPointIds->GetId((edgeIter+2)%3));
			idList->InsertNextId(cellPointIds->GetId((edgeIter)%3));

		    vtkSmartPointer<vtkIdList> neighborCellIds =
		      vtkSmartPointer<vtkIdList>::New();

		    currentGrid->GetCellNeighbors(i, idList, neighborCellIds);

		    for(vtkIdType j = 0; j < neighborCellIds->GetNumberOfIds(); j++)
		    {
		    	connectedElements.insert(neighborCellIds->GetId(j));
		    }

		}

//		if(i==163)
//			std::cout<<" Neighbors of triangle 163:";


		std::set<int>::iterator iter;
		for(iter=connectedElements.begin(); iter!=connectedElements.end(); ++iter)
		{
			Edge edge = Edge(i, *iter);
			edge_array.push_back(edge);

//			if(i==163)
//				std::cout<<", "<<(*iter);

		}

//		if(i==163)
//			std::cout<<" \n";

	}
	// eliminating duplicate edges - needed? seems not!

	// generating the Graph
	Graph g(edge_array.begin(), edge_array.end(), edge_array.size());

//	printf("InternalData.m_nNodes = %d \n", InternalData.m_nNodes);
//	printf("InternalData.m_nElements = %d \n", InternalData.m_nElements);
//	printf("num_vertices(g) = %d \n", num_vertices(g));
//	printf("edge_array.size() = %d \n", edge_array.size());

	// generating the colorvector in normal order
	std::vector<vertices_size_type> color_vec( num_vertices(g));
	iterator_property_map<vertices_size_type*, vertex_index_map> color(&color_vec.front(), get(vertex_index, g));
	vertices_size_type num_colors = sequential_vertex_coloring(g, color);

	//InternalData.m_nColors = num_colors;
	printf("num_colors = %d \n", num_colors);

	vtkSmartPointer<vtkFloatArray> colorData =
	      vtkSmartPointer<vtkFloatArray>::New();
	colorData->SetNumberOfComponents(1);
	colorData->SetName("colors");

    for(unsigned int i=0; i<numberOfCells;i++)
    {
    	colorData->InsertNextTuple1(color_vec.at(i));
    }

    currentGrid->GetCellData()->SetScalars(colorData);

	//subdivide the elements into smaller triangles and edges

    vtkSmartPointer<vtkDataSetSurfaceFilter> surfaceTessellator =
    			vtkSmartPointer<vtkDataSetSurfaceFilter>::New();

    __SetInput(surfaceTessellator, currentGrid);
    if(isQuadratic)
    {
    	surfaceTessellator->SetNonlinearSubdivisionLevel(3);
    	surfaceTessellator->Update();
    	//outputMesh->DeepCopy(surfaceTessellator->GetOutput());
    }
    else
    	//outputMesh->DeepCopy(currentGrid);

    surfaceTessellator->Update();
    outputMesh->DeepCopy(surfaceTessellator->GetOutput());

}



  void PostProcessingOperators::MergeMeshes(vtkUnstructuredGrid* pointsMesh, vtkUnstructuredGrid* cellsMesh, vtkUnstructuredGrid* outputMesh)
  {
    outputMesh->DeepCopy(cellsMesh);
    vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
    points->DeepCopy(pointsMesh->GetPoints());
    outputMesh->SetPoints(points);
#if VTK_MAJOR_VERSION <= 5    
    outputMesh->Update();
    //TODO is there really no method in vtk 6 for Update?
    //     In documentation is nothing listed
#endif
  }

void PostProcessingOperators::MergeMeshes(const char* pointsMeshFilename, const char* cellsMeshFilename, const char* outputMeshFilename)
  {
		vtkUnstructuredGrid* pointsMesh = IOHelper::VTKReadUnstructuredGrid(pointsMeshFilename);
		vtkUnstructuredGrid* cellsMesh = IOHelper::VTKReadUnstructuredGrid(cellsMeshFilename);
		vtkSmartPointer<vtkUnstructuredGrid> mergedGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();

		MergeMeshes(pointsMesh, cellsMesh, mergedGrid);

		//write output
		vtkSmartPointer<vtkUnstructuredGridWriter> writer =
		vtkSmartPointer<vtkUnstructuredGridWriter>::New();
		writer->SetFileName(outputMeshFilename);
		__SetInput(writer, mergedGrid);
		writer->Write();
  }
//TODO: Refactor+cleanup
  vector<pair<int, string> >* getAllFilesOfSeries(const char* filename)
  {
    vector<pair<int, string> >* aReturn = new vector<pair<int, string> >();
    boost::filesystem::path aPath(filename);
    boost::filesystem::path extension = aPath.extension();
    boost::filesystem::path file = aPath.filename().stem();
    std::string aFilename = file.string();
    
    int i=aFilename.length()-1;
    int numberOfDigits=0;
    while(i>0 && aFilename[i] >='0' && aFilename[i] <='9')
    {
        numberOfDigits++;
        i--;
    }
    aFilename = aFilename.substr(0,aFilename.length()-numberOfDigits);
    for (int i=0; i<pow(10.0,(double)numberOfDigits);i++)
    {
      boost::filesystem::path curentPath = aPath.parent_path() / (aFilename + lexical_cast<string>(i) + extension.string());
      if(boost::filesystem::exists(curentPath))
        aReturn->push_back(std::make_pair(i, curentPath.string()));
    }
    return aReturn;
  }


  std::string PostProcessingOperators::ApplyDVFPython(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool multipleDVF, bool reverseDirection)
  {
    if (multipleDVF)
    {
      return ApplyMultipleDVF(referenceImage, outputDeformedImage, DVF, reverseDirection);
    }
    else
    {
      ApplyDVF(referenceImage, outputDeformedImage, DVF, reverseDirection);
      return (std::string) outputDeformedImage;
    }

  }

    std::string PostProcessingOperators::ApplyMultipleDVF(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool reverseDirection)
  {
    vector<pair<int, string> >* allRefs = getAllFilesOfSeries(DVF);
    string currenOutputFile;
    boost::filesystem::path aPath(outputDeformedImage);
    for (int i=0; i<allRefs->size();i++)
    {
      cout << "Generating Deformed image " << currenOutputFile << std::endl;
      boost::filesystem::path curentPath = aPath.parent_path() / (aPath.filename().stem().string() + lexical_cast<string>(allRefs->at(i).first) + aPath.extension().string());
      currenOutputFile = curentPath.string();
      ApplyDVF(referenceImage, currenOutputFile.c_str(), allRefs->at(i).second.c_str(), reverseDirection);
    }
    return currenOutputFile;
  }

  void PostProcessingOperators::ApplyDVF(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool reverseDirection)
  {
    vtkSmartPointer<vtkImageData> refImage =  IOHelper::VTKReadImage(referenceImage);
    vtkSmartPointer<vtkImageData> dvfVecImage = IOHelper::VTKReadImage(DVF);
    vtkSmartPointer<vtkImageData> outputDefImage = vtkSmartPointer<vtkImageData>::New();


    ApplyDVF(refImage, outputDefImage, dvfVecImage, reverseDirection);
    cout << "Writing Deformed image.. "  << std::endl;
    //write output
		vtkSmartPointer<vtkXMLImageDataWriter> writer =
		vtkSmartPointer<vtkXMLImageDataWriter>::New();
		writer->SetFileName(outputDeformedImage);
		__SetInput(writer, outputDefImage);
    writer->SetCompressorTypeToZLib();
		writer->Write();
  }

  /*
   Deform input image by dvf: For each voxel of outputDefImage: Follow dvf to voxel in input voxel grid. 
   The dvf displacements will be inverted inside this method.
   pOut = pIn - d

   If GenerateDVF is used to create the DVF:
    - In GenerateDVF: Make sure the DVF is sampled on the output grid (output grid = Ref grid).
    - In ApplyDVF: Set reverseDirection=true

    -TODO: Areas outside definition zone of DVF are set to -99999 destroying up to an area of 1/2voxel size.
    How about nearest (3) neighbor interplotation during DVF creation - if voxel center is outside the defromed grid?
  */

  void PostProcessingOperators::ApplyDVF(vtkImageData* inputImage, vtkImageData* outputDefImage, vtkImageData* dvf, bool reverseDirection)
  {
    int* dims = inputImage->GetDimensions();
    double* origin = inputImage->GetOrigin();
    double* spacing = inputImage->GetSpacing();
    outputDefImage->SetDimensions(dims);
    outputDefImage->SetOrigin(origin);
    outputDefImage->SetSpacing(spacing);

    vtkSmartPointer<vtkImageInterpolator> dvfInterpolator = vtkSmartPointer<vtkImageInterpolator>::New();
    dvfInterpolator->SetOutValue(-1);
    dvfInterpolator->BreakOnError();
    dvfInterpolator->SetInterpolationModeToLinear();
    dvfInterpolator->Initialize(dvf);

    int M = dvf->GetNumberOfScalarComponents();
    int N  = dvfInterpolator->GetNumberOfComponents();

    vtkSmartPointer<vtkImageInterpolator> refImageInterpolator = vtkSmartPointer<vtkImageInterpolator>::New();
    refImageInterpolator->SetInterpolationModeToLinear();
    refImageInterpolator->Initialize(inputImage);


    //for each voxel of result image.
    for (int k=0; k<dims[2]; k++)
    {
      for (int j=0; j<dims[1]; j++)
      {
        for (int i=0; i<dims[0]; i++)
        {
          //default value for outsiders:
          double pixelValue = -1024; //CT air

          //current position in world coordinate system
          double pos[3] = {origin[0] + spacing[0] * i, origin[1] + spacing[1] * j, origin[2] + spacing[2] * k};
          double displacmentVec[3] = {-10,-10,-10};
          
          //get displacment vector (interpolated)
          bool inBoundsDVF = dvfInterpolator->Interpolate(pos, displacmentVec);
          displacmentVec[0] = dvfInterpolator->Interpolate(pos[0], pos[1], pos[2], 0);
          displacmentVec[1] = dvfInterpolator->Interpolate(pos[0], pos[1], pos[2], 1);
          displacmentVec[2] = dvfInterpolator->Interpolate(pos[0], pos[1], pos[2], 2);

          if (inBoundsDVF)
          {
            double posInRef[3];
            if (!reverseDirection)
            {
              posInRef[0] = pos[0] - displacmentVec[0];
              posInRef[1] = pos[1] - displacmentVec[1];
              posInRef[2] = pos[2] - displacmentVec[2];
            }
            else
            {
              posInRef[0] = pos[0] + displacmentVec[0];
              posInRef[1] = pos[1] + displacmentVec[1];
              posInRef[2] = pos[2] + displacmentVec[2];
            }

            double newPixelValue[1] = {0};
            //Follow displacment vector in refImage.
            bool inBoundsRef = refImageInterpolator->Interpolate(posInRef, newPixelValue);
            if (inBoundsRef)
              pixelValue = *newPixelValue;
          }
          //write pixel value refImage=>defImage
          double* pixel = static_cast<double*>(outputDefImage->GetScalarPointer(i,j,k));
          pixel[0] = pixelValue;
        }
      }
    }
  }

  std::string PostProcessingOperators::GenerateDVFPython(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename, bool multipleReferenceGrids)
  {
    if (multipleReferenceGrids)
    {
      return GenerateDVFMultipleRefGrids(referenceGridFilename, outputDVFFilename, deformedGridFilename);
    }
    else
    {
      GenerateDVF(referenceGridFilename, outputDVFFilename, deformedGridFilename);
      return (std::string) outputDVFFilename;
    }
  }

  string PostProcessingOperators::GenerateDVFMultipleRefGrids(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename)
  {
    vector<pair<int, string> >* allRefs = getAllFilesOfSeries(referenceGridFilename);
    string currenOutputFile;
    boost::filesystem::path aPath(outputDVFFilename);
    for (int i=0; i<allRefs->size();i++)
    {
      cout << "Generating DVF " << currenOutputFile << std::endl;
      boost::filesystem::path curentPath = aPath.parent_path() / (aPath.filename().stem().string() + lexical_cast<string>(allRefs->at(i).first) + aPath.extension().string());
      currenOutputFile = curentPath.string();
      GenerateDVF(allRefs->at(i).second.c_str(), currenOutputFile.c_str(), deformedGridFilename);
    }
    return currenOutputFile;
  }



  void PostProcessingOperators::GenerateDVF(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename)
  {
    
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceGridFilename);
		vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid(deformedGridFilename);
		vtkSmartPointer<vtkImageData> outputDVF = vtkSmartPointer<vtkImageData>::New();

		GenerateDVF(referenceGrid, outputDVF, deformedGrid);

		//write output
		vtkSmartPointer<vtkStructuredPointsWriter> writer = vtkSmartPointer<vtkStructuredPointsWriter>::New();
		writer->SetFileName(outputDVFFilename);
		__SetInput(writer, outputDVF);
		writer->Write();

    //write raw data
    /*
    FILE * pFile;
    pFile = fopen(((string)outputDVFFilename + ".dvf").c_str(),"wb");
    int size = 3 * outputDVF->GetDimensions()[0] * outputDVF->GetDimensions()[1] * outputDVF->GetDimensions()[2];
    void* data = malloc(sizeof(float) * size);
    outputDVF->GetPointData()->GetScalars()->ExportToVoidPointer(data);
    int error = fwrite(data,sizeof(float),size,pFile);*/
  }

  //Generate the displacment vector field (DVF) from reference to deformed mesh - sampled in reference. 
  //The results can be used to transfom points and meshes from Reference mesh to deformed mesh.
  //To transform voxel data, it is useful to generate the DFV using the deformed mesh as reference.
  // pDef - pRef = d     =>     pRef + d = pDef
  void PostProcessingOperators::GenerateDVF(vtkUnstructuredGrid* referenceGrid, vtkImageData* outputDVF, vtkUnstructuredGrid* deformedGrid)
  {
    float spacing = 5; //TODO use parameter

    //TODO: refactor this block wirh mishmeshoperators::
    //generate empty vector field 
    double bounds[6];
    referenceGrid->GetBounds(bounds);
    double spacingArray[3]; 
	  spacingArray[0] = spacing;
	  spacingArray[1] = spacing;
	  spacingArray[2] = spacing;
	  outputDVF->SetSpacing(spacingArray);
    // compute dimensions
	  int dim[3];
	  for (int i = 0; i < 3; i++)
	  {
	    dim[i] = static_cast<int>(ceil((bounds[i * 2 + 1] - bounds[i * 2]) / spacingArray[i]));
	  }
	  outputDVF->SetDimensions(dim);
	  outputDVF->SetExtent(0, dim[0] - 1, 0, dim[1] - 1, 0, dim[2] - 1);
    double origin[3];
	  origin[0] = bounds[0] + spacingArray[0] / 2;
	  origin[1] = bounds[2] + spacingArray[1] / 2;
	  origin[2] = bounds[4] + spacingArray[2] / 2;
	  outputDVF->SetOrigin(origin);
#if VTK_MAJOR_VERSION <= 5
    outputDVF->SetScalarTypeToFloat();
    outputDVF->SetNumberOfScalarComponents(3);
    outputDVF->AllocateScalars();
#else
    outputDVF->AllocateScalars(VTK_FLOAT, 3);
#endif

    
    //octree
    vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
    cellLocatorRef->SetDataSet(referenceGrid);
    cellLocatorRef->BuildLocator();

    // Zero the image
    double p_mm[3];
    for (int z = 0; z < dim[2]; z++)
    {
      for (int y = 0; y < dim[1]; y++)
      {
        for (int x = 0; x < dim[0]; x++)
        {
          //locate containing cell in ref cube
          p_mm[0] = origin[0]+x*spacingArray[0];
          p_mm[1] = origin[1]+y*spacingArray[1];
          p_mm[2] = origin[2]+z*spacingArray[2];
          vtkIdType containingCellRefId = cellLocatorRef->FindCell(p_mm);

          if (containingCellRefId>=0)
          {
            //calculate bcords: The barycentric coordinate uses 4 coeff [0..1] to linear combine the vertices of the cell to represent a point inside the cell. 
            vtkTetra*  containingCellRef = (vtkTetra*) referenceGrid->GetCell(containingCellRefId);
            double bcords[4];
            double x0[3]; double x1[3]; double x2[3]; double x3[3];
            vtkPoints* cellPoints = containingCellRef->GetPoints();
            cellPoints->GetPoint(0, x0);
            cellPoints->GetPoint(1, x1);
            cellPoints->GetPoint(2, x2);
            cellPoints->GetPoint(3, x3);
            containingCellRef->BarycentricCoords(p_mm, x0, x1, x2, x3, bcords);

            //apply bcords with deformed nodes to calculate the
            //cell id in reference and deformed mesh must be equal
            vtkTetra*  containingCellDef = (vtkTetra*) deformedGrid->GetCell(containingCellRefId); 
            cellPoints = containingCellDef->GetPoints();
            cellPoints->GetPoint(0, x0);
            cellPoints->GetPoint(1, x1);
            cellPoints->GetPoint(2, x2);
            cellPoints->GetPoint(3, x3);

            float* pixel = static_cast<float*>(outputDVF->GetScalarPointer(x,y,z));
            pixel[0] = (x0[0]*bcords[0] + x1[0]*bcords[1] + x2[0]*bcords[2] + x3[0]*bcords[3]) - p_mm[0];
            pixel[1] = (x0[1]*bcords[0] + x1[1]*bcords[1] + x2[1]*bcords[2] + x3[1]*bcords[3]) - p_mm[1];
            pixel[2] = (x0[2]*bcords[0] + x1[2]*bcords[1] + x2[2]*bcords[2] + x3[2]*bcords[3]) - p_mm[2];
          }
          else
          {
            float* pixel = static_cast<float*>(outputDVF->GetScalarPointer(x,y,z));
            pixel[0] = -99999;
            pixel[1] = -99999;
            pixel[2] = -99999;
          }
        } //x
      } //y
    } //z
 
  }

  }
