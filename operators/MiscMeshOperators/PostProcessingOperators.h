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


#ifndef __PostProcessingOperators_h
#define __PostProcessingOperators_h


#include <vector>
#include <limits>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkImageData.h>
#include <vtkCellLocator.h>
#include <vtkSmartPointer.h>

#include <../MSML_Operators.h>

using namespace std;


namespace MSML {
namespace PostProcessingOperators {

// void CreateVTKVolumeMeshFromSTL(char* infile, char* outfileSurface, char* outfileVolume, int numberOfElements, bool isQuadratic);
// void CreateCoarseSTLMeshFromSTL(char* infile, char* outfile, int numberOfElements);
// void CreateCoarseOBJMeshFromSTL(char* infile, char* outfile, int numberOfElements);
// void ConvertToTet10(char* inFile, char* outFileTet10, char* infileReference);
//
// bool CoarseSurfaceMesh(const char* infile, const char* outfile, unsigned int numberOfElements, std::string * errorMessage );
// bool CoarseSurfaceMesh(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, unsigned int numberOfElements, std::string * errorMessage=0 );

LIBRARY_API  std::string ColorMeshPython(std::string modelFilename, std::string coloredModelFilename);
LIBRARY_API  std::string ColorMeshFromComparisonPython(std::string modelFilename, std::string referenceFilename, std::string coloredModelFilename);

LIBRARY_API void ComputeOrganVolume(const char* volumeFilename);
LIBRARY_API void ComputeOrganCrossSectionArea(const char* volumeFilename);
LIBRARY_API void ComputeDiceCoefficient(const char* filename, const char* filename2);
	
//Returns 4-tuple: RMS Volume, Max Volume, RMS Surface, Max Surface
// LIBRARY_API  std::vector<double> CompareMeshesPython(std::string referenceFilename, std::string testFilename);

LIBRARY_API void ColorMesh(const char* modelFilename, const char* coloredModelFilename);
LIBRARY_API void ColorMesh(vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);
LIBRARY_API void CompareMeshes(std::vector<double> & errorVec, const char* referenceFilename, const char* testFilename, bool surfaceOnly);
LIBRARY_API void CompareMeshes(std::vector<double> & errorVec, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly);
LIBRARY_API void CompareMeshes(double& errorRMS, double& errorMax, const char* referenceFilename, const char* testFilename, bool surfaceOnly);
LIBRARY_API void CompareMeshes(double& errorRMS, double& errorMax, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly);

LIBRARY_API double ComputeRelativeMeanErrorOfSolution( const char* initialMeshFilename, const char* referenceMeshFilename, const char* testMeshFilename, bool surfaceOnly);

LIBRARY_API void ColorMeshFromComparison(const char* modelFilename, const char* referenceFilename, const char* coloredModelFilename);
LIBRARY_API void ColorMeshFromComparison(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* referenceMesh,vtkUnstructuredGrid* coloredMesh);

LIBRARY_API void MergeMeshes(vtkUnstructuredGrid* pointsMesh, vtkUnstructuredGrid* cellsMesh, vtkUnstructuredGrid* outputMesh);
LIBRARY_API void MergeMeshes(const char* pointsMeshFilename, const char* cellsMeshFilename, const char* outputMeshFilename);

LIBRARY_API std::string GenerateDVF(const char* referenceGridFilename, const char* deformedGridFilename, const char* outputDVFFilename, float spacingParam, const char* referenceCoordinateGrid, float interpolateOutsideDistance);
LIBRARY_API void GenerateDVFImp(vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkSmartPointer<vtkImageData> outputDVF, float interpolateOutsideDistance);

LIBRARY_API std::string ApplyDVF(const char* referenceImage, const char* DVF, const char* outputDeformedImage, bool reverseDirection, float voxelSize);
LIBRARY_API void ApplyDVF(vtkImageData* refImage, vtkImageData* DVF, vtkImageData* outputDefImage, bool reverseDirection, double voxelSize);

LIBRARY_API std::string TransformMeshBarycentric(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* out_meshPath, float interpolateOutsideDistance);
LIBRARY_API void TransformMeshBarycentric(vtkUnstructuredGrid* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* out_mesh, vtkUnstructuredGrid* deformedGrid, float interpolateOutsideDistance);

LIBRARY_API std::string TransformSurfaceBarycentric(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* out_meshPath, float interpolateOutsideDistance);
LIBRARY_API void TransformSurfaceBarycentric(vtkPolyData* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkPolyData* out_mesh, float interpolateOutsideDistance);

LIBRARY_API std::string ImageWeightedSum(const char* polydataFilePattern, bool normalize, const char* outfile);

// member access


// void CreateVolumeMesh(vtkUnstructuredGrid* volumeMesh, char* surfaceMeshFilename, char* referenceFilename, bool isQuadratic, bool projectPoints);
// void ConvertToTet10Mesh(vtkUnstructuredGrid* volumeMesh, char* surfaceMeshFilename, char* referenceFilename, bool isQuadratic, bool projectPoints);



void CalcVecBarycentric(double* p_mm, vtkUnstructuredGrid* referenceGrid, vtkCellLocator* cellLocatorRef, vtkUnstructuredGrid* deformedGrid, float interpolateOutsideDistance, float* vec_out);

} //end namespace PostProcessingOperators
} // end namespace MediAssist


#endif /* __PostProcessingOperators_h */
