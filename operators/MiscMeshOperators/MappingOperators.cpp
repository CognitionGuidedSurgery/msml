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

#include "MappingOperators.h"
#include <iostream>
#include <sstream>

#include <string.h>

#include <stdio.h>
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkTetra.h>
#include <vtkCellArray.h>
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
#include <vtkPolyDataToImageStencil.h>
#include <vtkImageStencil.h>
#include "vtkFeatureEdges.h"
#include "vtkFillHolesFilter.h"
#include "vtkCleanPolyData.h"
#include "vtkAppendFilter.h"

#include "vtkTetra.h"
#include "vtkGenericCell.h"
#include "vtkCellLocator.h"

#include <vtkThreshold.h>
#include <vtkMergeCells.h>

#include "../vtk6_compat.h"

using namespace std;

namespace MSML {
    namespace MappingOperators {

        std::string MapMeshPython ( std::string meshIni, std::string meshDeformed,
                                    std::string meshToMap, std::string mappedMesh )
        {
            MapMesh ( meshIni.c_str(), meshDeformed.c_str(),meshToMap.c_str(), mappedMesh.c_str() );
            return mappedMesh;
        }

        bool MapMesh ( const char* meshIni, const char* meshDeformed,
                       const char* meshToMap, const char* mappedMeshFilename )
        {
            //load the vtk  meshes
            vtkSmartPointer<vtkUnstructuredGridReader> reader =
                vtkSmartPointer<vtkUnstructuredGridReader>::New();
            reader->SetFileName ( meshIni );
            reader->Update();

            vtkSmartPointer<vtkUnstructuredGridReader> reader2 =
                vtkSmartPointer<vtkUnstructuredGridReader>::New();
            reader2->SetFileName ( meshDeformed );
            reader2->Update();

            vtkSmartPointer<vtkUnstructuredGridReader> reader3 =
                vtkSmartPointer<vtkUnstructuredGridReader>::New();
            reader3->SetFileName ( meshToMap );
            reader3->Update();

            vtkSmartPointer<vtkUnstructuredGrid> mappedMesh =
                vtkSmartPointer<vtkUnstructuredGrid>::New();

            bool result = MapMesh ( reader->GetOutput(), reader2->GetOutput(),reader3->GetOutput(), mappedMesh );

            //save the subdivided polydata
            vtkSmartPointer<vtkUnstructuredGridWriter> gridWriter =	vtkSmartPointer<vtkUnstructuredGridWriter>::New();
            gridWriter->SetFileName ( mappedMeshFilename );
            __SetInput ( gridWriter,  mappedMesh );
            gridWriter->Write();
            return result;
        }

        bool MapMesh ( vtkUnstructuredGrid* meshIni, vtkUnstructuredGrid* meshDeformed,
                       vtkUnstructuredGrid* meshToMap, vtkUnstructuredGrid* mappedMesh )
        {
            vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
            cellLocatorRef->SetDataSet ( meshIni );
            cellLocatorRef->BuildLocator();


            vtkPoints* pointsToBeMapped = meshToMap->GetPoints();

            vtkSmartPointer<vtkPoints> mappedPoints = vtkSmartPointer<vtkPoints>::New();

            double currentPoint[3];
            double currentClosestPoint[3];

            double currentDeformedPoint[3];

            vtkSmartPointer<vtkGenericCell> currentTetra = vtkSmartPointer<vtkGenericCell>::New();
            currentTetra->SetCellTypeToTetra();

            vtkIdType currentCellId;
            int currentSubId;
            double currentDistance;

            for ( unsigned int i=0; i<pointsToBeMapped->GetNumberOfPoints(); i++ )
            {
                pointsToBeMapped->GetPoint ( i, currentPoint );

                //first find closes point
                cellLocatorRef->FindClosestPoint ( currentPoint, currentClosestPoint,
                                                   currentTetra, currentCellId,currentSubId,currentDistance );

                double bcords[4];
                double x0[3];
                double x1[3];
                double x2[3];
                double x3[3];
                vtkPoints* cellPoints = currentTetra->GetPoints();
                cellPoints->GetPoint ( 0, x0 );
                cellPoints->GetPoint ( 1, x1 );
                cellPoints->GetPoint ( 2, x2 );
                cellPoints->GetPoint ( 3, x3 );


                vtkTetra*  deformedTetra = ( vtkTetra*) meshDeformed->GetCell ( currentCellId );
                deformedTetra->BarycentricCoords ( currentPoint, x0, x1, x2, x3, bcords );

                deformedTetra->GetPoints()->GetPoint ( 0,x0 );
                deformedTetra->GetPoints()->GetPoint ( 1,x1 );
                deformedTetra->GetPoints()->GetPoint ( 2,x2 );
                deformedTetra->GetPoints()->GetPoint ( 3,x3 );

                currentDeformedPoint[0] = ( x0[0]*bcords[0] + x1[0]*bcords[1] +
                                            x2[0]*bcords[2] + x3[0]*bcords[3] );
                currentDeformedPoint[1] = ( x0[1]*bcords[0] + x1[1]*bcords[1] +
                                            x2[1]*bcords[2] + x3[1]*bcords[3] );
                currentDeformedPoint[2] = ( x0[2]*bcords[0] + x1[2]*bcords[1] +
                                            x2[2]*bcords[2] + x3[2]*bcords[3] );

                mappedPoints->InsertNextPoint ( currentDeformedPoint );
            }

            vtkSmartPointer<vtkUnstructuredGrid> tempMappedMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
            tempMappedMesh->SetPoints ( mappedPoints );
            tempMappedMesh->SetCells ( meshToMap->GetCellType ( 1 ),meshToMap->GetCells() );
            mappedMesh->DeepCopy ( tempMappedMesh );
            return true;
        }
    }
}
