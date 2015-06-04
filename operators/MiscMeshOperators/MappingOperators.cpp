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

#include "vtkMatrix3x3.h"
#include "vtkSTLWriter.h"
#include "vtkPolyDataWriter.h"
#include "vtkPolyDataReader.h"
#include "vtkPolyData.h"
#include "vtkPoints.h"
#include "vtkCellArray.h"
#include <vtkCellData.h>
#include "vtkCleanPolyData.h"
#include "vtkUnsignedIntArray.h"
#include "IOHelper.h"

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
#include "vtkQuadraticTetra.h"
#include "vtkGenericCell.h"
#include "vtkCellLocator.h"

#include <vtkThreshold.h>
#include <vtkMergeCells.h>

#include "../vtk6_compat.h"
#include "../common/log.h"

using namespace std;

namespace MSML {
    namespace MappingOperators {

        std::string MapMesh ( std::string meshIni, std::string meshDeformed,
                                    std::string meshToMap, std::string mappedMesh )
        {
            std::cout<<"MapMeshOperator started\n";
            MapMesh ( meshIni.c_str(), meshDeformed.c_str(),meshToMap.c_str(), mappedMesh.c_str() );
            return mappedMesh;
        }

        bool MapMesh ( const char* meshIni, const char* meshDeformed,
                       const char* meshToMap, const char* mappedMeshFilename )
        {
            vtkSmartPointer<vtkUnstructuredGrid> meshIniGrid = IOHelper::VTKReadUnstructuredGrid(meshIni);
            vtkSmartPointer<vtkUnstructuredGrid> meshDeformedGrid = IOHelper::VTKReadUnstructuredGrid(meshDeformed);
            vtkSmartPointer<vtkUnstructuredGrid> meshToMapGrid = IOHelper::VTKReadUnstructuredGrid(meshToMap);


            vtkSmartPointer<vtkUnstructuredGrid> mappedMesh =
                vtkSmartPointer<vtkUnstructuredGrid>::New();
            std::cout<<"Meshes loaded\n";

            bool result = MapMesh ( meshIniGrid , meshDeformedGrid,meshToMapGrid, mappedMesh );

            //save the subdivided polydata
            vtkSmartPointer<vtkUnstructuredGridWriter> gridWriter =	vtkSmartPointer<vtkUnstructuredGridWriter>::New();
            gridWriter->SetFileName ( mappedMeshFilename );
            __SetInput ( gridWriter,  mappedMesh );
            gridWriter->Write();
            return result;
        }

        void CalculateGlobalCoords(double* localCoords, double* globalCoords, double* nodes)
        {
            double fx = localCoords[0];
			double fy = localCoords[1];
			double fz = localCoords[2];

			double tempExp = 1-fx-fy-fz;

			for(int i=0;i<3;i++)
			{
				globalCoords[i] = 0;

				globalCoords[i] += ((double*)nodes)[10*i+0]*(2*fx-1)*fx;
				globalCoords[i] += ((double*)nodes)[10*i+1]*(2*fy-1)*fy;
				globalCoords[i] += ((double*)nodes)[10*i+2]*(2*tempExp-1)*tempExp;
				globalCoords[i] += ((double*)nodes)[10*i+3]*(2*fz-1)*fz;
				globalCoords[i] += ((double*)nodes)[10*i+4]*4*fx*fy;
				globalCoords[i] += ((double*)nodes)[10*i+5]*4*tempExp*fy;
				globalCoords[i] += ((double*)nodes)[10*i+6]*4*tempExp*fx;
				globalCoords[i] += ((double*)nodes)[10*i+7]*4*fx*fz;
				globalCoords[i] += ((double*)nodes)[10*i+8]*4*fy*fz;
				globalCoords[i] += ((double*)nodes)[10*i+9]*4*tempExp*fz;

				//globalCoords[i]=10;
			}

        }

        bool MapMesh ( vtkUnstructuredGrid* meshIni, vtkUnstructuredGrid* meshDeformed,
                       vtkUnstructuredGrid* meshToMap, vtkUnstructuredGrid* mappedMesh )
        {
            vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
            cellLocatorRef->SetDataSet ( meshIni );
            cellLocatorRef->BuildLocator();

            vtkSmartPointer<vtkMatrix3x3> currentBases = vtkSmartPointer<vtkMatrix3x3>::New();
            vtkSmartPointer<vtkMatrix3x3> currentInvertBases = vtkSmartPointer<vtkMatrix3x3>::New();



            vtkPoints* pointsToBeMapped = meshToMap->GetPoints();

            vtkSmartPointer<vtkPoints> mappedPoints = vtkSmartPointer<vtkPoints>::New();

            double currentPoint[3];
            double currentClosestPoint[3];

            double currentDeformedPoint[3];


            std::cout<<"Determining cell type \n";
            int cellType = meshIni->GetCellType(1);
            bool isQuadratic = false;



            if(cellType == 24)
            {
                isQuadratic = true;
                std::cout<<"Quadratic mesh found!\n";
            }



            vtkSmartPointer<vtkGenericCell> currentTetra = vtkSmartPointer<vtkGenericCell>::New();
            if(isQuadratic)
                currentTetra->SetCellTypeToQuadraticTetra();
            else
                currentTetra->SetCellTypeToTetra();

            vtkIdType currentCellId;
            int currentSubId;
            double currentDistance;

            std::cout<<"Begin mapping\n";

            for ( unsigned int i=0; i<pointsToBeMapped->GetNumberOfPoints(); i++ )
            {
                pointsToBeMapped->GetPoint ( i, currentPoint );

                //first find closes point
                cellLocatorRef->FindClosestPoint ( currentPoint, currentClosestPoint,
                                                   currentTetra, currentCellId,currentSubId,currentDistance );

                if(isQuadratic)
                {
                    double pcoords[3];
                    double bcords[3];
                    double r[3];
                    double x[3];
                    double xtemp[3];
                    double x0[3];
                    double x1[3];
                    double x2[3];
                    double x3[3];
                    double x4[3];
                    double x5[3];
                    double x6[3];
                    double x7[3];
                    double x8[3];
                    double x9[3];

                    double weights[4];
                    double dist2;
                    dist2 = 1;

                   // int in = currentTetra->EvaluatePosition(currentPoint, currentClosestPoint, currentSubId, pcoords, dist2, &weights[0]);

                   // if(in==0)
                    //    std::cout<<"MappingOeprator:: Warning, point is outside cell.";

                    vtkPoints* cellPoints = currentTetra->GetPoints();
                    cellPoints->GetPoint ( 0, x0 );
                    cellPoints->GetPoint ( 1, x1 );
                    cellPoints->GetPoint ( 2, x2 );
                    cellPoints->GetPoint ( 3, x3 );

                    currentBases->SetElement(0,0,x0[0]-x2[0]);
                    currentBases->SetElement(0,1,x1[0]-x2[0]);
                    currentBases->SetElement(0,2,x3[0]-x2[0]);

                    currentBases->SetElement(1,0,x0[1]-x2[1]);
                    currentBases->SetElement(1,1,x1[1]-x2[1]);
                    currentBases->SetElement(1,2,x3[1]-x2[1]);

                    currentBases->SetElement(2,0,x0[2]-x2[2]);
                    currentBases->SetElement(2,1,x1[2]-x2[2]);
                    currentBases->SetElement(2,2,x3[2]-x2[2]);

                    currentBases->Invert(currentBases, currentInvertBases);

                    xtemp[0] = currentPoint[0]-x2[0];
                    xtemp[1] = currentPoint[1]-x2[1];
                    xtemp[2] = currentPoint[2]-x2[2];

                    currentInvertBases->MultiplyPoint(xtemp, pcoords);



                    vtkQuadraticTetra*  deformedTetra = ( vtkQuadraticTetra*) meshDeformed->GetCell ( currentCellId );



                    deformedTetra->GetPoints()->GetPoint ( 0,x0 );
                    deformedTetra->GetPoints()->GetPoint ( 1,x1 );
                    deformedTetra->GetPoints()->GetPoint ( 2,x2 );
                    deformedTetra->GetPoints()->GetPoint ( 3,x3 );
                    deformedTetra->GetPoints()->GetPoint ( 4,x4 );
                    deformedTetra->GetPoints()->GetPoint ( 5,x5 );
                    deformedTetra->GetPoints()->GetPoint ( 6,x6 );
                    deformedTetra->GetPoints()->GetPoint ( 7,x7 );
                    deformedTetra->GetPoints()->GetPoint ( 8,x8 );
                    deformedTetra->GetPoints()->GetPoint ( 9,x9 );

                    double nodes[30];

                    for(int i=0; i<3;i++)
                    {
                        nodes[10*i+0] =   x0[i];
                        nodes[10*i+1] =   x1[i];
                        nodes[10*i+2] =   x2[i];
                        nodes[10*i+3] =   x3[i];
                        nodes[10*i+4] =   x4[i];
                        nodes[10*i+5] =   x5[i];
                        nodes[10*i+6] =   x6[i];
                        nodes[10*i+7] =   x7[i];
                        nodes[10*i+8] =   x8[i];
                        nodes[10*i+9] =   x9[i];

                    }

                    CalculateGlobalCoords(&pcoords[0], &currentDeformedPoint[0], &nodes[0]);

                    /*double fx = pcoords[0];
                    double fy = pcoords[1];
                    double fz = pcoords[2];


                    globalCoords[i] += ((double*)nodes)[10*i+0]*(2*fx-1)*fx;
		//		globalCoords[i] += ((double*)nodes)[10*i+1]*(2*fy-1)*fy;
		//		globalCoords[i] += ((double*)nodes)[10*i+2]*(2*tempExp-1)*tempExp;
		//		globalCoords[i] += ((double*)nodes)[10*i+3]*(2*fz-1)*fz;
		//		globalCoords[i] += ((double*)nodes)[10*i+4]*4*fx*fy;
		//		globalCoords[i] += ((double*)nodes)[10*i+5]*4*tempExp*fy;
		//		globalCoords[i] += ((double*)nodes)[10*i+6]*4*tempExp*fx;
		//		globalCoords[i] += ((double*)nodes)[10*i+7]*4*fx*fz;
		//		globalCoords[i] += ((double*)nodes)[10*i+8]*4*fy*fz;
		//		globalCoords[i] += ((double*)nodes)[10*i+9]*4*tempExp*fz;

                    currentDeformedPoint[0] = ( x0[0]*fx + x1[0]*fy +
                                                x2[0]*(1-fx-fy-fz) + x3[0]*fz );
                    currentDeformedPoint[1] = ( x0[1]*fx + x1[1]*fy +
                                                x2[1]*(1-fx-fy-fz) + x3[1]*fz );
                    currentDeformedPoint[2] = ( x0[2]*fx + x1[2]*fy +
                                                x2[2]*(1-fx-fy-fz) + x3[2]*fz );

                   /* std::cout<<"QuadraticPoint\n";

                    double pcoords[3];
                    double weights[10];
                    double dist2;

                    double x0[3];
                    double x1[3];
                    double x2[3];
                    double x3[3];
                    double x4[3];
                    double x5[3];
                    double x6[3];
                    double x7[3];
                    double x8[3];
                    double x9[3];

                    //dist2 = 1e-6;

                    int in = currentTetra->EvaluatePosition(currentPoint, currentClosestPoint, currentSubId, pcoords, dist2, &weights[0]);

                    if(in==0)
                        std::cout<<"MappingOeprator:: Warning, point is outside cell.";

                    vtkQuadraticTetra*  deformedTetra = ( vtkQuadraticTetra*) meshDeformed->GetCell ( currentCellId );

                    //deformedTetra->EvaluateLocation(currentSubId, pcoords, currentDeformedPoint,  &weights[0]);

                    deformedTetra->GetPoints()->GetPoint ( 0,x0 );
                    deformedTetra->GetPoints()->GetPoint ( 1,x1 );
                    deformedTetra->GetPoints()->GetPoint ( 2,x2 );
                    deformedTetra->GetPoints()->GetPoint ( 3,x3 );
                    deformedTetra->GetPoints()->GetPoint ( 4,x4 );
                    deformedTetra->GetPoints()->GetPoint ( 5,x5 );
                    deformedTetra->GetPoints()->GetPoint ( 6,x6 );
                    deformedTetra->GetPoints()->GetPoint ( 7,x7 );
                    deformedTetra->GetPoints()->GetPoint ( 8,x8 );
                    deformedTetra->GetPoints()->GetPoint ( 9,x9 );


                    currentDeformedPoint[0] = ( x0[0]*weights[0] + x1[0]*weights[1] +  x2[0]*weights[2] + x3[0]*weights[3]
                                                + x4[0]*weights[4] + x5[0]*weights[5] +  x6[0]*weights[6] + x7[0]*weights[7]
                                                +x8[0]*weights[8] + x9[0]*weights[9]  );
                    currentDeformedPoint[1] = ( x0[1]*weights[0] + x1[1]*weights[1] +  x2[1]*weights[2] + x3[1]*weights[3]
                                                + x4[1]*weights[4] + x5[1]*weights[5] +  x6[1]*weights[6] + x7[1]*weights[7]
                                                +x8[1]*weights[8] + x9[1]*weights[9]  );
                    currentDeformedPoint[2] = ( x0[2]*weights[0] + x1[2]*weights[1] +  x2[2]*weights[2] + x3[2]*weights[3]
                                                + x4[2]*weights[4] + x5[2]*weights[5] +  x6[2]*weights[6] + x7[2]*weights[7]
                                                +x8[2]*weights[8] + x9[2]*weights[9]  );

                                                currentDeformedPoint[0] = ( x0[0]*weights[0] + x1[0]*weights[1] +  x2[0]*weights[2] + x3[0]*weights[3]
                                                + x4[0]*weights[4] + x5[0]*weights[5] +  x6[0]*weights[6] + x7[0]*weights[7]
                                                +x8[0]*weights[8] + x9[0]*weights[9]  );*/





                    mappedPoints->InsertNextPoint ( currentDeformedPoint );

                }
                else
                {
                    double pcoords[3];
                    double bcords[3];
                    double r[3];
                    double x[3];
                    double xtemp[3];
                    double x0[3];
                    double x1[3];
                    double x2[3];
                    double x3[3];

                    double weights[4];
                    double dist2;
                    dist2 = 1;

                   // int in = currentTetra->EvaluatePosition(currentPoint, currentClosestPoint, currentSubId, pcoords, dist2, &weights[0]);

                   // if(in==0)
                    //    std::cout<<"MappingOeprator:: Warning, point is outside cell.";

                    vtkPoints* cellPoints = currentTetra->GetPoints();
                    cellPoints->GetPoint ( 0, x0 );
                    cellPoints->GetPoint ( 1, x1 );
                    cellPoints->GetPoint ( 2, x2 );
                    cellPoints->GetPoint ( 3, x3 );

                    currentBases->SetElement(0,0,x0[0]-x2[0]);
                    currentBases->SetElement(0,1,x1[0]-x2[0]);
                    currentBases->SetElement(0,2,x3[0]-x2[0]);

                    currentBases->SetElement(1,0,x0[1]-x2[1]);
                    currentBases->SetElement(1,1,x1[1]-x2[1]);
                    currentBases->SetElement(1,2,x3[1]-x2[1]);

                    currentBases->SetElement(2,0,x0[2]-x2[2]);
                    currentBases->SetElement(2,1,x1[2]-x2[2]);
                    currentBases->SetElement(2,2,x3[2]-x2[2]);

                    currentBases->Invert(currentBases, currentInvertBases);

                    xtemp[0] = currentPoint[0]-x2[0];
                    xtemp[1] = currentPoint[1]-x2[1];
                    xtemp[2] = currentPoint[2]-x2[2];

                    currentInvertBases->MultiplyPoint(xtemp, pcoords);



                    vtkTetra*  deformedTetra = ( vtkTetra*) meshDeformed->GetCell ( currentCellId );



                    deformedTetra->GetPoints()->GetPoint ( 0,x0 );
                    deformedTetra->GetPoints()->GetPoint ( 1,x1 );
                    deformedTetra->GetPoints()->GetPoint ( 2,x2 );
                    deformedTetra->GetPoints()->GetPoint ( 3,x3 );

                    double fx = pcoords[0];
                    double fy = pcoords[1];
                    double fz = pcoords[2];



                    currentDeformedPoint[0] = ( x0[0]*fx + x1[0]*fy +
                                                x2[0]*(1-fx-fy-fz) + x3[0]*fz );
                    currentDeformedPoint[1] = ( x0[1]*fx + x1[1]*fy +
                                                x2[1]*(1-fx-fy-fz) + x3[1]*fz );
                    currentDeformedPoint[2] = ( x0[2]*fx + x1[2]*fy +
                                                x2[2]*(1-fx-fy-fz) + x3[2]*fz );


                    //deformedTetra->EvaluateLocation(currentSubId, pcoords, currentDeformedPoint,  &weights[0]);

                    /*vtkPoints* cellPoints = currentTetra->GetPoints();
                    cellPoints->GetPoint ( 0, x0 );
                    cellPoints->GetPoint ( 1, x1 );
                    cellPoints->GetPoint ( 2, x2 );
                    cellPoints->GetPoint ( 3, x3 );


                    vtkTetra*  deformedTetra = ( vtkTetra*) meshDeformed->GetCell ( currentCellId );
                    deformedTetra->BarycentricCoords ( currentPoint, x0, x1, x2, x3, bcords );

                    //InterpolateFunctions
                    deformedTetra->GetPoints()->GetPoint ( 0,x0 );
                    deformedTetra->GetPoints()->GetPoint ( 1,x1 );
                    deformedTetra->GetPoints()->GetPoint ( 2,x2 );
                    deformedTetra->GetPoints()->GetPoint ( 3,x3 );

                    currentDeformedPoint[0] = ( x0[0]*bcords[0] + x1[0]*bcords[1] +
                                                x2[0]*bcords[2] + x3[0]*bcords[3] );
                    currentDeformedPoint[1] = ( x0[1]*bcords[0] + x1[1]*bcords[1] +
                                                x2[1]*bcords[2] + x3[1]*bcords[3] );
                    currentDeformedPoint[2] = ( x0[2]*bcords[0] + x1[2]*bcords[1] +
                                                x2[2]*bcords[2] + x3[2]*bcords[3] );*/

                    mappedPoints->InsertNextPoint ( currentDeformedPoint );

                }


            }

            std::cout<<"Mapping finished\n";

            vtkSmartPointer<vtkUnstructuredGrid> tempMappedMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
            tempMappedMesh->SetPoints ( mappedPoints );
            tempMappedMesh->SetCells ( meshToMap->GetCellType ( 1 ),meshToMap->GetCells() );
            mappedMesh->DeepCopy ( tempMappedMesh );
            return true;
        }
    }
}
