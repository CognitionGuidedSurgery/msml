/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, NetgenOperators
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
#include "NetgenOperators.h"
#include <iostream>
#include <string.h>
#include <stdio.h>

#include "vtkUnstructuredGrid.h"
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkTetra.h>
#include <vtkCellArray.h>
#include <vtkSmartPointer.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkPolyDataReader.h>
#include <vtkPolyDataWriter.h>

#include <vtkPointData.h>
#include <vtkIdList.h>
#include <vtkVertexGlyphFilter.h>
#include <vtkPoints.h>

#include "vtkSTLWriter.h"
#include "vtkSTLReader.h"
#include "vtkPolyData.h"
#include "vtkPoints.h"
#include "vtkCellArray.h"
#include "vtkCleanPolyData.h"

#include "vtkFloatArray.h"
#include "vtkCellData.h"


#include <vtkDataSetSurfaceFilter.h>
#include "vtkLongLongArray.h"

#include <vtkUnstructuredGridGeometryFilter.h>
#include <vtkUnstructuredGridWriter.h>

namespace nglib {

#include "nglib.h"

}


#include "../common/log.h"

using namespace std;
using namespace nglib;

namespace MSML {
    namespace Netgen {

std::string RemeshSurfacePython(std::string infile, std::string outfile)
{
	log_info() << "Creating volume mesh with Netgen..." << std::endl;
	RemeshSurface(infile.c_str(), outfile.c_str());
	return outfile;
}

bool RemeshSurface(const char* infile, const char* outfile )
{

	vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(infile);
	reader->Update();

	//deep copy
	vtkPolyData* inputMesh = reader->GetOutput();
	vtkSmartPointer<vtkPolyData> outputMesh = vtkSmartPointer<vtkPolyData>::New();
	RemeshSurface(inputMesh, outputMesh);


	vtkSmartPointer<vtkPolyDataWriter> writer = vtkSmartPointer<vtkPolyDataWriter>::New();
	writer->SetFileName(outfile);

#if VTK_MAJOR_VERSION <= 5
	writer->SetInput(outputMesh);
#else
	writer->SetInputData(outputMesh);
#endif

	writer->Write();



	return true;
}

bool RemeshSurface(vtkPolyData* inputMesh, vtkPolyData* outputMesh )
{
	cout << "Netgen (nglib) STL meshing "  << endl;


	// Initialise the Netgen Core library
	Ng_Init();

   // Define pointer to a new Netgen Mesh
   Ng_Mesh *mesh;

   // Define pointer to STL Geometry
   //create STL geometry
   Ng_STL_Geometry *stl_geom;// = Ng_STL_NewGeometry();;

   // Result of Netgen Operations
   Ng_Result ng_res;



   // Actually create the mesh structure
   mesh = Ng_NewMesh();

   int np, ne;


   cout << "Copy VTK datastructures...." << endl;
	int numberOfFaces = inputMesh->GetNumberOfCells();
	int numberOfPoints = inputMesh->GetNumberOfPoints();

	cout << "Number of faces  "<<numberOfFaces<<"\n";


	//vtkIdType* currentCellPoints = new vtkIdType[3];
	vtkIdType numberOfNodes=3;
	double point1[3];
	double point2[3];
	double point3[3];

	vtkIdList* pointIds = vtkIdList::New();

//inputMesh->GetCellPoints(2,pointIds);
	cout << "Number of points  "<<numberOfPoints<<"\n";

//	for(int i=0; i<numberOfFaces; i++)
//	{
//		//cout << "Adding face !  "<<i<<"\n";
//		inputMesh->GetCellPoints(i,pointIds);
//		if(pointIds->GetNumberOfIds() != 3)
//		{
//			cout<<"Error, only triangles are supported\n";
//		}
//		//cout << "Points are "<<pointIds->GetId(0)<<" "<<pointIds->GetId(1)<<" " <<pointIds->GetId(2)<<" "  <<"\n";
//		inputMesh->GetPoint(pointIds->GetId(0), &point1[0]);
//		inputMesh->GetPoint(pointIds->GetId(1), &point2[0]);
//		inputMesh->GetPoint(pointIds->GetId(2), &point3[0]);
//		//cout << "Points  "<<pointIds->GetId(0) <<" " <<pointIds->GetId(1) <<" " <<pointIds->GetId(2) <<" " <<"\n";
//		//cout << "Point1  "<<point1[0] <<" " <<point1[1] <<" " <<point1[2] <<" " <<"\n";
//		//cout << "Point2  "<<point2[0] <<" " <<point2[1] <<" " <<point2[2] <<" " <<"\n";
//		//cout << "Point3  "<<point3[0] <<" " <<point3[1] <<" " <<point3[2] <<" " <<"\n";
//
//
//		Ng_STL_AddTriangle( stl_geom,	point1, point2, point3);
//		//cout << "Added face  "<<i<<"\n";
//	}


	vtkSmartPointer<vtkSTLWriter> writer = vtkSmartPointer<vtkSTLWriter>::New();
	writer->SetFileName("/tmp/theTempSTL.stl");
	writer->SetFileTypeToASCII();

#if VTK_MAJOR_VERSION <= 5
	writer->SetInput(inputMesh);
#else
	writer->SetInputData(inputMesh);
#endif
	writer->Write();

	stl_geom = Ng_STL_LoadGeometry("/tmp/theTempSTL.stl");
	   if(!stl_geom)
	   {
	      cout << "Error reading in STL File: " <<  endl;
		  return 1;
	   }
	   cout << "Successfully loaded STL File: " <<  endl;



   // Set the Meshing Parameters to be used
   Ng_Meshing_Parameters mp;
   mp.closeedgeenable = 1;
//   mp.maxh = 1.0e+6;
//   mp.fineness = 0.4;
//   mp.grading = 0.2;
//   mp.second_order = 0;

   cout << "Initialise the STL Geometry structure...." << endl;
   ng_res = Ng_STL_InitSTLGeometry(stl_geom);
   if(ng_res != NG_OK)
   {
	  cout << "Error Initialising the STL Geometry....Aborting!!" << endl;
	   return 1;
   }

   cout << "Start Edge Meshing...." << endl;
   ng_res = Ng_STL_MakeEdges(stl_geom, mesh, &mp);
   if(ng_res != NG_OK)
   {
	  cout << "Error in Edge Meshing....Aborting!!" << endl;
	   return 1;
   }

   cout << "Start Surface Meshing...." << endl;
   ng_res = Ng_STL_GenerateSurfaceMesh(stl_geom, mesh, &mp);
   if(ng_res != NG_OK)
   {
	  cout << "Error in Surface Meshing....Aborting!!" << endl;
	   return 1;
   }

   cout << "Start Volume Meshing...." << endl;
  // ng_res = Ng_GenerateVolumeMesh (mesh, &mp);
   //if(ng_res != NG_OK)
   //{
//	  cout << "Error in Volume Meshing....Aborting!!" << endl;
//	  return 1;
 //  }

   cout << "Meshing successfully completed....!!" << endl;

   // volume mesh output
   np = Ng_GetNP(mesh);
   cout << "Points: " << np << endl;

   ne = Ng_GetNSE(mesh);
   cout << "Elements: " << ne << endl;

  // cout << "Saving Mesh in VOL Format...." << endl;
//   Ng_SaveMesh(mesh,"test.vol");


   // refinement without geomety adaption:
   // Ng_Uniform_Refinement (mesh);

   // refinement with geomety adaption:
//   Ng_STL_Uniform_Refinement (stl_geom, mesh);

   cout << "elements after refinement: " << Ng_GetNSE(mesh) << endl;
   cout << "points   after refinement: " << Ng_GetNP(mesh) << endl;
   np = Ng_GetNP(mesh);
   ne = Ng_GetNSE(mesh);

  // Ng_SaveMesh(mesh,"/tmp/test_ref.vol");

	vtkSmartPointer<vtkPoints> thePointsOutput = vtkSmartPointer<vtkPoints>::New();

	vtkSmartPointer<vtkCellArray> theCellsOutput = vtkSmartPointer<vtkCellArray>::New();

	double currentPoint[3];
   for(unsigned int iter=0; iter<np; iter++)
   {
	   Ng_GetPoint (mesh, iter+1, &currentPoint[0]);
	   thePointsOutput->InsertNextPoint(currentPoint[0], currentPoint[1], currentPoint[2]);
   }

   outputMesh->SetPoints(thePointsOutput);
   int* currentElementPoints = new int[numberOfNodes];
   vtkIdType* currentVTKElementPoints = new vtkIdType[numberOfNodes];

   std::cout<<"ne is "<<ne<<endl;
	for(int iter=0; iter<ne; iter++)
	{
//		std::cout<<"Getting cell no "<<iter<<endl;
		Ng_GetSurfaceElement(mesh, iter+1, currentElementPoints);

		for(int nodeIter=0; nodeIter<numberOfNodes; nodeIter++)
		 {

			currentVTKElementPoints[nodeIter] = currentElementPoints[nodeIter]-1;
		 }
//		std::cout<<"Inserting cell no "<<iter<<endl;
		 theCellsOutput->InsertNextCell(numberOfNodes,currentVTKElementPoints);
	}

	outputMesh->SetPolys(theCellsOutput);


	  cout << "elements saved to vtk " << outputMesh->GetNumberOfPolys() << endl;
	  cout << "points saved to vtk " << outputMesh->GetNumberOfPoints() << endl;

//	  Ng_SaveMesh(mesh,"/home/suwelack/Beam97Surface-remeshed.vol");

	delete [] currentElementPoints;
	delete stl_geom;
	pointIds->Delete();

	Ng_Exit ();




	return true;
}
}
}
