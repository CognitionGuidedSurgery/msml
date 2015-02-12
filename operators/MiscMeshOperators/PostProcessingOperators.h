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

LIBRARY_API  std::string ColorMesh(std::string modelFilename, std::string coloredModelFilename);
LIBRARY_API  std::string ColorMeshFromComparison(std::string modelFilename, std::string referenceFilename, std::string coloredModelFilename);

LIBRARY_API void ComputeOrganVolume(const char* volumeFilename);
LIBRARY_API void ComputeOrganCrossSectionArea(const char* volumeFilename);
LIBRARY_API void ComputeDiceCoefficient(const char* filename, const char* filename2);
LIBRARY_API double ComputeDiceCoefficientPolydata(const char* filename, const char* filename2,const char *intersectionFile);


LIBRARY_API void ColorMesh(const char* modelFilename, const char* coloredModelFilename);
LIBRARY_API void ColorMesh(vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);

//Returns 4-tuple: RMS Volume, Max Volume, RMS Surface, Max Surface
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

LIBRARY_API std::string TransformMeshBarycentric(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* outMeshPath, float interpolateOutsideDistance);
LIBRARY_API void TransformMeshBarycentric(vtkUnstructuredGrid* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* outMesh, vtkUnstructuredGrid* deformedGrid, float interpolateOutsideDistance);

LIBRARY_API std::string TransformSurfaceBarycentric(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* outMeshPath, float interpolateOutsideDistance);
LIBRARY_API void TransformSurfaceBarycentric(vtkPolyData* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkPolyData* outMesh, float interpolateOutsideDistance);

LIBRARY_API std::string ImageSum(const char* imagedataFilePattern, bool normalize, const char* outfile);

LIBRARY_API void CalcVecBarycentric(double* pInMM, vtkUnstructuredGrid* referenceGrid, vtkCellLocator* cellLocatorRef, vtkUnstructuredGrid* deformedGrid, float interpolateOutsideDistance, float* vecOut);

} //end namespace PostProcessingOperators
} // end namespace MediAssist


#endif /* __PostProcessingOperators_h */
