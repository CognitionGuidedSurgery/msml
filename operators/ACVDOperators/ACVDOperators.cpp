/*  =========================================================================

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

#include "ACVDOperators.h"
#include "IOHelper.h"


#include "../vtk6_compat.h"

#include "../common/log.h"
#include "vtkManifoldSimplification.h"
#include "vtkIsotropicDiscreteRemeshing.h"


using namespace std;

namespace MSML {
namespace ACVDOperators {

std::string ReduceSurfaceMeshPython(std::string infile, std::string outfile, int verticesCount)
{
	vtkSmartPointer<vtkPolyData> inputPoly = IOHelper::VTKReadPolyData(infile.c_str());
	vtkSmartPointer<vtkPolyData> outputPoly = vtkSmartPointer<vtkPolyData>::New();
	ReduceSurfaceMesh( inputPoly, outputPoly, verticesCount);
	bool success = IOHelper::VTKWritePolyData(outfile.c_str(), outputPoly);
	if(!success)
		std::cout<<"Error: Polydata could not be written\n";
    return outfile;
}

bool ReduceSurfaceMesh(vtkPolyData* in, vtkPolyData* out, int verticesCount)
{
	std::cout<<"Mesh reduce called....";

//	vtkSmartPointer<vtkSurface> Mesh=vtkSmartPointer<vtkSurface>::New();
//	Mesh->CreateFromPolyData(in);
//
//	vtkSmartPointer<vtkManifoldSimplification> Simplification=vtkManifoldSimplification::New();
//	Simplification->SetInput(Mesh);
//	Simplification->SetNumberOfOutputVertices(verticesCount);
//	Simplification->Simplify();
//	vtkSurface *CleanOutput=Mesh->CleanMemory();
	
	
	//////////////

	vtkSmartPointer<vtkSurface> Mesh=vtkSmartPointer<vtkSurface>::New();
	vtkSmartPointer<vtkIsotropicDiscreteRemeshing> Remesh=vtkSmartPointer<vtkIsotropicDiscreteRemeshing>::New();

	int SubsamplingThreshold=10;
	double Gradation=0;

	Mesh->CreateFromPolyData(in);
	Mesh->GetCellData()->Initialize();
	Mesh->GetPointData()->Initialize();

	Remesh->SetForceManifold(1);
	Remesh->SetInput(Mesh);
	Remesh->SetFileLoadSaveOption(0);
	Remesh->SetNumberOfClusters(verticesCount);
	Remesh->SetConsoleOutput(2);
	Remesh->SetSubsamplingThreshold(SubsamplingThreshold);
	Remesh->GetMetric()->SetGradation(Gradation);

	Remesh->Remesh();

//	if (QuadricsOptimizationLevel!= 0)
//	{
//		// Note : this is an adaptation of Siggraph 2000 Paper : Out-of-core simplification of large polygonal models
//		vtkIntArray *Clustering=Remesh->GetClustering();
//
//		char REALFILE[5000];
//		char FileBeforeProcessing[500];
//		strcpy (FileBeforeProcessing,"smooth_");
//		strcat (FileBeforeProcessing, outputfile);
//		if (OutputDirectory)
//		{
//			strcpy (REALFILE,OutputDirectory);
//			strcat (REALFILE,FileBeforeProcessing);
//		}
//		else
//			strcpy (REALFILE,FileBeforeProcessing);
//
//		Remesh->GetOutput()->WriteToFile(REALFILE);
//
//		int Cluster,NumberOfMisclassedItems=0;
//
//		double **ClustersQuadrics =new double*[NumberOfSamples];
//		for (int i = 0; i < NumberOfSamples; i++)
//		{
//			ClustersQuadrics[i]=new double[9];
//			for (int j=0;j<9;j++)
//				ClustersQuadrics[i][j]=0;
//		}
//
//		vtkIdList *FList=vtkIdList::New();
//
//		for (int i = 0; i < Remesh->GetNumberOfItems (); i++)
//		{
//			Cluster = Clustering->GetValue (i);
//			if ((Cluster >= 0)&& (Cluster < NumberOfSamples))
//			{
//				if (Remesh->GetClusteringType() == 0)
//				{
//					vtkQuadricTools::AddTriangleQuadric(ClustersQuadrics[Cluster],Remesh->GetInput(),i,false);
//				}
//				else
//				{
//					Remesh->GetInput()->GetVertexNeighbourFaces(i,FList);
//					for (int j=0;j<FList->GetNumberOfIds();j++)
//						vtkQuadricTools::AddTriangleQuadric(ClustersQuadrics[Cluster]
//								,Remesh->GetInput(),FList->GetId(j),false);
//				}
//			}
//			else
//				NumberOfMisclassedItems++;
//		}
//		FList->Delete();
//
//		if (NumberOfMisclassedItems)
//			cout<<NumberOfMisclassedItems<<" Items with wrong cluster association"<<endl;
//
//		double P[3];
//		for (int i = 0; i < NumberOfSamples; i++)
//		{
//			Remesh->GetOutput()->GetPoint (i, P);
//			vtkQuadricTools::ComputeRepresentativePoint(ClustersQuadrics[i], P,QuadricsOptimizationLevel);
//			Remesh->GetOutput()->SetPointCoordinates (i, P);
//			delete[] ClustersQuadrics[i];
//		}
//		delete [] ClustersQuadrics;
//
//		Mesh->GetPoints()->Modified ();
//
//
//		cout<<"After Quadrics Post-processing : "<<endl;
//		Remesh->GetOutput()->DisplayMeshProperties();
//
//		if (Display > 0)
//		{
//			RenderWindow *OptimizedMeshWindow=RenderWindow::New();
//			OptimizedMeshWindow->AttachToRenderWindow(Remesh->GetDisplayWindow());
//			OptimizedMeshWindow->SetInput(Remesh->GetOutput());
//			OptimizedMeshWindow->SetWindowName("Coarsened model (quadric based placement)");
//			OptimizedMeshWindow->Render ();
//			OptimizedMeshWindow->Interact ();
//		}
//	}


	out->DeepCopy(Remesh->GetOutput());

	return true;
}



}//end namepace MiscExtOperators
}//end namepace MSML
