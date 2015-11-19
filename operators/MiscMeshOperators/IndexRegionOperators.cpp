/*  =========================================================================

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

#include "IndexRegionOperators.h"

#include <set>
#include <iostream>
#include <sstream>
#include <vtkUnstructuredGridReader.h>
#include <vtkPoints.h>
#include <vtkCellArray.h>
#include <vtkCellData.h>
#include <vtkPointData.h>
#include <vtkUnsignedCharArray.h>

#include "IOHelper.h"

#include "../common/log.h"

#define EPSILON 1e-10

//#include <boost/graph/sequential_vertex_coloring.hpp>
//#include <boost/graph/adjacency_list.hpp>
//using namespace boost;
namespace MSML {
    namespace IndexRegionOperators {	

        vector<unsigned int>  ComputeIndicesFromBoxROI(string filename, vector<double> box, string type)
        {			
			vtkSmartPointer<vtkUnstructuredGrid> theMesh = IOHelper::VTKReadUnstructuredGrid(filename.c_str());
			
            //get points
            vtkPoints* thePoints = theMesh->GetPoints();
            vector<unsigned int> indices;
            
            double* currentPoint = new double[3];


            if(type.compare("points") == 0)
            {
                int count = 0;
				int numPoints = thePoints->GetNumberOfPoints();
				for(unsigned int i=0; i<numPoints; i++)
                {
                    thePoints->GetPoint(i, currentPoint);

                    if( (currentPoint[0]>=box[0]) && (currentPoint[1]>=box[1]) && (currentPoint[2]>=box[2])
                            && (currentPoint[0]<=box[3]) && (currentPoint[1]<=box[4]) && (currentPoint[2]<=box[5]))
                    {
                        indices.push_back(i);
                        count++;
                    }
                }

                log_error() << count << " points found in box" << endl;
            }

            else if(type.compare("elements") == 0)
            {
                vtkCell* currentCell;
                vtkUnsignedCharArray* cellsTypes = theMesh->GetCellTypesArray();
                vtkIdType numberOfPoints;
                double currentBounds[6];
                int count = 0;
				int numCells = theMesh->GetNumberOfCells();
				for(unsigned int i=0; i<numCells; i++)
                {
                    if (*cellsTypes->GetTuple(i) == VTK_TETRA || *cellsTypes->GetTuple(i) == VTK_HEXAHEDRON ||
                            *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TETRA || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_HEXAHEDRON)
                    {
                        theMesh->GetCellBounds(i, currentBounds);

                        if( (currentBounds[0]>=box[0]) && (currentBounds[2]>=box[1]) && (currentBounds[4]>=box[2])
                                && (currentBounds[1]<=box[3]) && (currentBounds[3]<=box[4]) && (currentBounds[5]<=box[5]))
                        {
                            indices.push_back(i);
                            count++;
                        }
                    }
                }
                log_error() << count << " elements found in box" << endl;
            }	

            else if(type.compare("surfaceElements") == 0)
			{
				vtkCell* currentCell;
				vtkUnsignedCharArray* cellsTypes = theMesh->GetCellTypesArray();
				vtkIdType numberOfPoints;
				double currentBounds[6];
				int count = 0;
				int numCells = theMesh->GetNumberOfCells();
				for(unsigned int i=0; i<numCells; i++)
				{
					if (*cellsTypes->GetTuple(i) == VTK_TRIANGLE ||	*cellsTypes->GetTuple(i) == VTK_QUADRATIC_TRIANGLE)
					{

						theMesh->GetCellBounds(i, currentBounds);

						if( (currentBounds[0]>=box[0]) && (currentBounds[2]>=box[1]) && (currentBounds[4]>=box[2])
								&& (currentBounds[1]<=box[3]) && (currentBounds[3]<=box[4]) && (currentBounds[5]<=box[5]))
						{
							log_info() << "Triangle found with id "<<i<< endl;
							log_info() << "Bounds are "<<box[0]<<","<<box[1]<<","<<box[2]<<","<<box[3]<<","<<box[4]<<","<<box[5]<<endl;
							log_info() << "CurrentTri bounds are "<<currentBounds[0]<<","<<currentBounds[2]<<","<<currentBounds[4]<<","<<currentBounds[1]<<","<<currentBounds[3]<<","<<currentBounds[5]<<endl;

							indices.push_back(i);
							count++;
						}
					}
				}
			}

            else
            {
                log_error() <<"Error, this type is not supported" << endl;
            }


            delete [] currentPoint;
            return indices;
        }

        vector<unsigned int> ComputeIndicesFromMaterialId(string filename, int id, string type)
        {
            std::set<unsigned int> indicesSet;
            std::vector<unsigned int> indices;
			      vtkSmartPointer<vtkUnstructuredGrid> theMesh = IOHelper::VTKReadUnstructuredGrid(filename.c_str());

            if(type.compare("points_experimental") == 0)
            {
                vtkCell* currentCell;
                vtkDataArray* cellsData = theMesh->GetCellData()->GetScalars();
                vtkUnsignedCharArray* cellsTypes = theMesh->GetCellTypesArray();
                vtkIdType numberOfPoints;
                vtkIdList* pointIds; 
				        int numCells = theMesh->GetNumberOfCells();
				        for(unsigned int i=0; i< numCells; i++)
                {
                    if (*cellsTypes->GetTuple(i) == VTK_TETRA || *cellsTypes->GetTuple(i) == VTK_HEXAHEDRON ||
                            *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TETRA || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_HEXAHEDRON)
                        if((*cellsData->GetTuple(i)) == id)
                        {
                            vtkSmartPointer<vtkIdList> pointIds = vtkIdList::New(); 
                            theMesh->GetCellPoints(i, pointIds);
                            for (int j =0; j <pointIds->GetNumberOfIds();j++)
                            {
                              indicesSet.insert(pointIds->GetId(j));
                            }
                            
                        }
                }
                indices.assign(indicesSet.begin(), indicesSet.end());
            }

            else if(type.compare("faces") == 0)
            {
                vtkCell* currentCell;
                vtkDataArray* cellsData = theMesh->GetCellData()->GetScalars();
                vtkUnsignedCharArray* cellsTypes = theMesh->GetCellTypesArray();
                vtkIdType numberOfPoints;
				int numCells = theMesh->GetNumberOfCells();
				for(unsigned int i=0; i< numCells; i++)
                {
                    if ((*cellsTypes->GetTuple(i) == VTK_TRIANGLE || (*cellsTypes->GetTuple(i) ==VTK_QUAD)) ||
                            *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TRIANGLE || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_QUAD)
                        if((*cellsData->GetTuple(i)) == id)
                        {
                            indices.push_back(i);
                        }
                }
            }

            else if(type.compare("elements") == 0)
            {
                vtkCell* currentCell;
                vtkDataArray* cellsData = theMesh->GetCellData()->GetScalars();
                vtkUnsignedCharArray* cellsTypes = theMesh->GetCellTypesArray();
                vtkIdType numberOfPoints;
				int numCells = theMesh->GetNumberOfCells();
                for(unsigned int i=0; i< numCells; i++)
                {
                    if (*cellsTypes->GetTuple(i) == VTK_TETRA || *cellsTypes->GetTuple(i) == VTK_HEXAHEDRON ||
                            *cellsTypes->GetTuple(i) == VTK_QUADRATIC_TETRA || *cellsTypes->GetTuple(i) == VTK_QUADRATIC_HEXAHEDRON)
                        if((*cellsData->GetTuple(i)) == id)
                        {
                            indices.push_back(i);
                        }
                }
            }

            else
            {
                log_info() <<"Error, this type is not supported" << endl;
            }

            return indices;
        }


        vector<double> PositionFromIndices(string filename, vector<unsigned int> indices, string type) {
            vector<double> points;
            vtkSmartPointer<vtkUnstructuredGrid> theMesh = MSML::IOHelper::VTKReadUnstructuredGrid(filename.c_str());
            vtkPoints* thePoints = theMesh->GetPoints();

            double* currentPoint = new double[3];

            if(type.compare("points") == 0)
            {
                int count = 0;

                vector<unsigned int>::iterator it = indices.begin();
                vector<unsigned int>::iterator end = indices.end();

                for(; it != end; it++)
                {
                    if(*it >= thePoints->GetNumberOfPoints()) {
                       log_error() << "ID to high" << endl;
                       continue;
                    }

		    thePoints->GetPoint(*it, currentPoint);
		    points.push_back(currentPoint[0]);
		    points.push_back(currentPoint[1]);
		    points.push_back(currentPoint[2]);
		}

                log_info() << count << " points found in box" << endl;
            }/* TODO implement this

            else if(type.compare("elements") == 0)
            {
                vtkCell* currentCell;
                vtkUnsignedCharArray* cellsTypes = reader->GetOutput()->GetCellTypesArray();
                vtkIdType numberOfPoints;
                double currentBounds[6];
                int count = 0;

                for(unsigned int i=0; i<reader->GetOutput()->GetNumberOfCells(); i++)
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
*/
            else
            {
                log_error() <<"Error, this type is not supported" << std::endl;
            }


            delete [] currentPoint;
            return points;

        }
    }
}
