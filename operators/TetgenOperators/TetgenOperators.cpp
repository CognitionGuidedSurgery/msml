/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, TetgenOperators
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
#include "TetgenOperators.h"
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

#include "tetgen.h"

#include "../common/log.h"

using namespace std;

namespace MSML {
    namespace Tetgen {

TetgenSettings::TetgenSettings(): // Set default values as they are in Tetgen 1.5
		preserveBoundary(false),
		maxEdgeRadiusRatio(2.0),
		minDihedralAngleDegrees(0),
		maxTetVolumeOrZero(0),
		optimizationLevel(2),
		optimizationUseEdgeAndFaceFlips(true),
		optimizationUseVertexSmoothing(true),
		optimizationUseVertexInsAndDel(true) {
}

std::string TetgenCreateVolumeMesh(std::string infile, std::string outfile,
        bool preserveBoundary,
        double maxEdgeRadiusRatio,
        int minDihedralAngleDegrees,
        double maxTetVolumeOrZero,
        int optimizationLevel, // 0 to disable optimizations, 10 for maximum number of optimization iterations.
        bool optimizationUseEdgeAndFaceFlips,
        bool optimizationUseVertexSmoothing,
        bool optimizationUseVertexInsAndDel)
{
	log_info() << "Creating volume mesh with Tetgen..." << std::endl;

	TetgenSettings settings;
	settings.preserveBoundary = preserveBoundary;
	settings.maxEdgeRadiusRatio = maxEdgeRadiusRatio;
	settings.minDihedralAngleDegrees = minDihedralAngleDegrees;
	settings.maxTetVolumeOrZero = maxTetVolumeOrZero;
	settings.optimizationLevel = optimizationLevel;
	settings.optimizationUseEdgeAndFaceFlips = optimizationUseEdgeAndFaceFlips;
	settings.optimizationUseVertexSmoothing = optimizationUseVertexSmoothing;
	settings.optimizationUseVertexInsAndDel = optimizationUseVertexInsAndDel;

	TetgenCreateVolumeMesh(infile.c_str(), outfile.c_str(), settings, false);
	return outfile;
}

bool TetgenCreateVolumeMesh(const char* infile, const char* outfile, TetgenSettings settings, bool isQuadratic )
{

	vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(infile);
	reader->Update();

	//deep copy
	vtkPolyData* inputMesh = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGrid> outputMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
	TetgenCreateVolumeMesh(inputMesh, outputMesh, settings, isQuadratic);


	vtkSmartPointer<vtkUnstructuredGridWriter> writer = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	writer->SetFileName(outfile);

#if VTK_MAJOR_VERSION <= 5
	writer->SetInput(outputMesh);
#else
	writer->SetInputData(outputMesh);
#endif

	writer->Write();



	return true;
}

static tetgenbehavior tetgenbehaviorForSettings(const TetgenSettings &settings) {
    tetgenbehavior params;
    params.plc = 1; // -p
    params.nobisect = settings.preserveBoundary ? 1 : 0; // -Y
    params.quality = 1; // -q
    params.minratio = settings.maxEdgeRadiusRatio; // -q[X]/[] [sic] this variable seems to have changed semantics during the evolution of tetgen.
    params.mindihedral = settings.minDihedralAngleDegrees; // -q[]/[X]
    if(settings.maxTetVolumeOrZero > 0) {
        params.fixedvolume = 1; // -a[]
        params.maxvolume = settings.maxTetVolumeOrZero; // -a[X]
    }
    params.optlevel = settings.optimizationLevel; // -O[X]/[]
    // The optimization options are a 3 bit bitmap with a flag for each option.
    // Set the respective bits to 1 for the enabled options:
    params.optscheme = (0
            | (settings.optimizationUseEdgeAndFaceFlips ? (1 << 0) : 0)
            | (settings.optimizationUseVertexSmoothing ? (1 << 1) : 0)
            | (settings.optimizationUseVertexInsAndDel ? (1 << 2) : 0));

    return params;
}

bool TetgenCreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh, TetgenSettings settings, bool isQuadratic )
{
	tetgenio in, out;

	tetgenio::facet *f;
	tetgenio::polygon *p;

	inputMesh->BuildCells();

	int numberOfPoints = inputMesh->GetNumberOfPoints();
	int numberOfFaces = inputMesh->GetNumberOfCells();

	log_info() << "Starting tetgen with "<< numberOfPoints <<" points and "<< numberOfFaces <<" faces" << std::endl;
	in.numberofpoints = numberOfPoints;
	in.pointlist = new REAL[numberOfPoints*3];

	vtkPoints* thePoints = inputMesh->GetPoints();
	//vtkCellArray* theCells = inputMesh->GetCells();

	 double* currentPoint;
	 for(int i=0; i<numberOfPoints; i++)
	 {
		 currentPoint = thePoints->GetPoint(i);
		 in.pointlist[3*i] = currentPoint[0];
		 in.pointlist[3*i+1] = currentPoint[1];
		 in.pointlist[3*i+2] = currentPoint[2];
	 }

	  in.numberoffacets = numberOfFaces;
	  in.facetlist = new tetgenio::facet[in.numberoffacets];
	  in.facetmarkerlist = new int[in.numberoffacets];

		vtkIdType* currentCellPoints;
		vtkIdType numberOfNodes=3;


		for(int i=0; i<numberOfFaces; i++)
		{

			inputMesh->GetCellPoints(i,numberOfNodes, currentCellPoints);
			f = &in.facetlist[i];
			tetgenio::init(f);
			// In .mesh format, each facet has one polygon, no hole.
			f->numberofpolygons = 1;
			f->polygonlist = new tetgenio::polygon[1];
			f->numberofholes = 0;
			f->holelist = NULL;
			p = &f->polygonlist[0];
			tetgenio::init(p);
			p->numberofvertices = 3;
			p->vertexlist = new int[p->numberofvertices];

			for(int faceIter=0; faceIter<3; faceIter++)
			{
				p->vertexlist[faceIter] = currentCellPoints[faceIter];
			}

		}

		tetgenbehavior params = tetgenbehaviorForSettings(settings);

		tetrahedralize(&params, &in, &out);


		int numberOfPointsOutput = out.numberofpoints;
		int numberOfCellsOutput = out.numberoftetrahedra;

		log_info() << "Mesh generated by tetgen with " << numberOfPointsOutput <<" points and "<< numberOfCellsOutput << " tetras \n";

		//outputMesh->Reset();
		vtkSmartPointer<vtkPoints> thePointsOutput = vtkSmartPointer<vtkPoints>::New();

		vtkSmartPointer<vtkCellArray> theCellsOutput = vtkSmartPointer<vtkCellArray>::New();

		//vtkPoints* thePointsOutput = outputMesh->GetPoints();
		unsigned int numberOfElementNodes = 4;
		if(isQuadratic)
			numberOfElementNodes = 10;


		 for(int i=0; i<numberOfPointsOutput; i++)
		 {
			 thePointsOutput->InsertNextPoint(out.pointlist[3*i], out.pointlist[3*i+1], out.pointlist[3*i+2]);
		 }

		 outputMesh->SetPoints(thePointsOutput);

		 vtkIdType* currentElementPoints;

		 if(isQuadratic)
			 currentElementPoints = new vtkIdType[10];
		 else
			 currentElementPoints = new vtkIdType[4];

		 for(int i=0; i<numberOfCellsOutput; i++)
		 {
			 for(int nodeIter=0; nodeIter<numberOfElementNodes; nodeIter++)
			 {
				 currentElementPoints[nodeIter] = out.tetrahedronlist[4*i+nodeIter];
			 }

			 theCellsOutput->InsertNextCell(numberOfElementNodes,currentElementPoints);
		 }

		 if(isQuadratic)
			outputMesh->SetCells(24, theCellsOutput);
		 else
			 outputMesh->SetCells(10, theCellsOutput);

		 delete [] currentElementPoints;



	return true;
}
}
}
