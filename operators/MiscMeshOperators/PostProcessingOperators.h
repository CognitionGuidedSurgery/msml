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


#ifndef __PostProcessingOperators_h
#define __PostProcessingOperators_h

// ****************************************************************************
// Includes
// ****************************************************************************
#include <vector>
#include <limits>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>



#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkImageData.h>

#include <../MSML_Operators.h>

using namespace std;
//using namespace MediAssist;


// ****************************************************************************
// Defines
// ****************************************************************************






// ****************************************************************************
// PostProcessingOperators
// ****************************************************************************

/** \class AbsImageFilter
 * \brief This class does some really fancy stuff
 *
 * \ingroup Examples
 */


namespace MSML {




class PostProcessingOperators
{
public:
	// constructor
	PostProcessingOperators();

	// destructor
	~PostProcessingOperators();

	// standard class typedefs


	// public methods
//	static void CreateVTKVolumeMeshFromSTL(char* infile, char* outfileSurface, char* outfileVolume, int numberOfElements, bool isQuadratic);
//	static void CreateCoarseSTLMeshFromSTL(char* infile, char* outfile, int numberOfElements);
//	static void CreateCoarseOBJMeshFromSTL(char* infile, char* outfile, int numberOfElements);
//	static void ConvertToTet10(char* inFile, char* outFileTet10, char* infileReference);
//
//	static bool CoarseSurfaceMesh(const char* infile, const char* outfile, unsigned int numberOfElements, std::string * errorMessage );
//	static bool CoarseSurfaceMesh(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, unsigned int numberOfElements, std::string * errorMessage=0 );
	LIBRARY_API static std::string  ColorMeshPython(std::string modelFilename, std::string coloredModelFilename);
	LIBRARY_API static std::string ColorMeshFromComparisonPython(std::string modelFilename, std::string referenceFilename, std::string coloredModelFilename);
	//Returns 4-tuple: RMS Volume, Max Volume, RMS Surface, Max Surface
//	LIBRARY_API static std::vector<double> CompareMeshesPython(std::string referenceFilename, std::string testFilename);

	LIBRARY_API static void ColorMesh(const char* modelFilename, const char* coloredModelFilename);
	LIBRARY_API static void ColorMesh(vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);
	LIBRARY_API static void CompareMeshes(double & errorRMS, double & errorMax, const char* referenceFilename, const char* testFilename, bool surfaceOnly);
	LIBRARY_API static void CompareMeshes(double & errorRMS, double & errorMax, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly);

	//LIBRARY_API static void ComputeDiceCoefficient(const char* filename, const char* filename2);
	LIBRARY_API static void ComputeOrganVolume(const char* volumeFilename);
	LIBRARY_API static void ComputeOrganCrossSectionArea(const char* volumeFilename);
	
	LIBRARY_API static void CompareMeshes(std::vector<double> & errorVec, const char* referenceFilename, const char* testFilename, bool surfaceOnly);
	LIBRARY_API static void CompareMeshes(std::vector<double> & errorVec, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly);

	LIBRARY_API static void ColorMeshFromComparison(const char* modelFilename, const char* referenceFilename, const char* coloredModelFilename);
	LIBRARY_API static void ColorMeshFromComparison(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* referenceMesh,vtkUnstructuredGrid* coloredMesh);

	LIBRARY_API static void FeBioToVTKConversion(const std::string modelFilename, const std::string lastStep, std::string inputMesh);

  LIBRARY_API static void MergeMeshes(vtkUnstructuredGrid* pointsMesh, vtkUnstructuredGrid* cellsMesh, vtkUnstructuredGrid* outputMesh);
	LIBRARY_API static void MergeMeshes(const char* pointsMeshFilename, const char* cellsMeshFilename, const char* outputMeshFilename);
  
  LIBRARY_API static std::string GenerateDVFPython(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename, bool multipleReferenceGrids);
  LIBRARY_API static void GenerateDVF(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename);
  LIBRARY_API static void GenerateDVF(vtkUnstructuredGrid* referenceGrid, vtkImageData* outputDVF, vtkUnstructuredGrid* deformedGrid);
	
  LIBRARY_API static std::string ApplyDVFPython(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool multipleDVF, bool reverseDirection);
  LIBRARY_API static void ApplyDVF(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool reverseDirection);
  LIBRARY_API static void ApplyDVF(vtkImageData* refImage, vtkImageData* outputDefImage, vtkImageData* dvf, bool reverseDirection);
  // member access


protected:
//	static void CoarseMesh(MyMesh& currentMeshVCG, MyMesh &referenceMeshVCG, int numberOfSurfaceElements);
//	static void CreateVolumeMesh(vtkUnstructuredGrid* volumeMesh, char* surfaceMeshFilename, char* referenceFilename, bool isQuadratic, bool projectPoints);
	//static void ConvertToTet10Mesh(vtkUnstructuredGrid* volumeMesh, char* surfaceMeshFilename, char* referenceFilename, bool isQuadratic, bool projectPoints);


private:
	// private methods
  static std::string GenerateDVFMultipleRefGrids(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename);
  static std::string ApplyMultipleDVF(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool reverseDirection);

	// private attributes





};

} // end namespace MediAssist


#endif /* __PostProcessingOperators_h */
