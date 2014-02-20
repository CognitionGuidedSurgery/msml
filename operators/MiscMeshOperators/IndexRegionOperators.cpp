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
#include "IndexRegionOperators.h"

#include <iostream>
#include <sstream>
#include <vtkUnstructuredGridReader.h>
#include <vtkPoints.h>
#include <vtkCellArray.h>
#include <vtkCellData.h>
#include <vtkPointData.h>
#include <vtkUnsignedCharArray.h>


//#include <boost/graph/sequential_vertex_coloring.hpp>
//#include <boost/graph/adjacency_list.hpp>


//using namespace boost;



namespace MSML
{



// ****************************************************************************
// Constructor / Destructor
// ****************************************************************************


// ****************************************************************************
// Methods
// ****************************************************************************

vector<unsigned int>	IndexRegionOperators::computeIndicesFromBoxROI(string filename, vector<double> box, string type)
{
//	std::cout<<infile<<"\n";
//	std::cout<<box[0]<<"\n";

	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	 vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(filename.c_str());
	reader->Update();

	vtkUnstructuredGrid* theMesh = reader->GetOutput();

	//get points
	vtkPoints* thePoints = theMesh->GetPoints();
	vector<unsigned int> indices;
	double* currentPoint = new double[3];

//	std::cout<<"Computing indices for mesh"<<filename<<"in BOX ROI\n";

	if(type.compare("points") == 0)
	{
    int count = 0;
		for(unsigned int i=0;i<thePoints->GetNumberOfPoints();i++)
		{
			thePoints->GetPoint(i, currentPoint);
			if( (currentPoint[0]>box[0]) && (currentPoint[1]>box[1]) && (currentPoint[2]>box[2]) 
        && (currentPoint[0]<box[3]) && (currentPoint[1]<box[4]) && (currentPoint[2]<box[5]))
					indices.push_back(i);
      count++;
		}
    cerr << count << " points found in box";
	}
  else if(type.compare("elements") == 0)
    {
      vtkCell* currentCell;
      vtkUnsignedCharArray* cellsTypes = reader->GetOutput()->GetCellTypesArray();
      vtkIdType numberOfPoints;
      double currentBounds[6];
		  int count = 0;
      for(unsigned int i=0;i<reader->GetOutput()->GetNumberOfCells();i++)
		  {
        if (*cellsTypes->GetTuple(i) == VTK_TETRA || *cellsTypes->GetTuple(i) == VTK_HEXAHEDRON ||
          *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TETRA || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_HEXAHEDRON)
        {
          reader->GetOutput()->GetCellBounds(i, currentBounds);
          if( (currentBounds[0]>=box[0]) && (currentBounds[2]>=box[1]) && (currentBounds[4]>=box[2]) 
            && (currentBounds[1]<=box[3]) && (currentBounds[3]<=box[4]) && (currentBounds[5]<=box[5]))
          {
            indices.push_back(i);
            count++;
          }
        } 
		  }
    }
  else
	{
		cerr<<"Error, this type is not supported\n";
	}


	delete [] currentPoint;

//	std::cout<<indices.size()<< "indices found \n";
	return indices;
}

vector<unsigned int> IndexRegionOperators::computeIndicesFromMaterialId(string filename, int id, string type)
{
    vector<unsigned int> indices;
  	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	  vtkSmartPointer<vtkUnstructuredGridReader>::New();
	  reader->SetFileName(filename.c_str());
	  reader->Update();
  	if(type.compare("points") == 0)
    {
  		vtkDataArray* pointData = reader->GetOutput()->GetPointData()->GetScalars();
  		for(unsigned int i=0;i< reader->GetOutput()->GetNumberOfPoints();i++)
	    {
  			if(*pointData->GetTuple(i) == id)
  				indices.push_back(i);
	    }
    }
    else if(type.compare("faces") == 0)
    {
      vtkCell* currentCell;
      vtkDataArray* cellsData = reader->GetOutput()->GetCellData()->GetScalars();
      vtkUnsignedCharArray* cellsTypes = reader->GetOutput()->GetCellTypesArray();
      vtkIdType numberOfPoints;
		  for(unsigned int i=0;i< reader->GetOutput()->GetNumberOfCells();i++)
		  {
        if ((*cellsTypes->GetTuple(i) == VTK_TRIANGLE || (*cellsTypes->GetTuple(i) ==VTK_QUAD)) ||
          *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TRIANGLE || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_QUAD)
          if((*cellsData->GetTuple(i)) == id)
            indices.push_back(i);
		  }
    }
    else if(type.compare("elements") == 0)
    {
      vtkCell* currentCell;
      vtkDataArray* cellsData = reader->GetOutput()->GetCellData()->GetScalars();
      vtkUnsignedCharArray* cellsTypes = reader->GetOutput()->GetCellTypesArray();
      vtkIdType numberOfPoints;
		  for(unsigned int i=0;i< reader->GetOutput()->GetNumberOfCells();i++)
		  {
        if (*cellsTypes->GetTuple(i) == VTK_TETRA || *cellsTypes->GetTuple(i) == VTK_HEXAHEDRON ||
          *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TETRA || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_HEXAHEDRON)
          if((*cellsData->GetTuple(i)) == id)
            indices.push_back(i);
		  }
    }
    else
	  {
		  cout<<"Error, this type is not supported\n";
	  }
    return indices;
}


//void PostProcessingOperators::computeIndicesFromBoxROI(vtkUnstructuredGrid* inputMesh, double box[6],std::vector<unsigned int> &indices)
//{
//
//}

}





