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


#ifndef __MiscMeshOperators_h
#define __MiscMeshOperators_h

#include "../MSML_Operators.h"
#include <vector>
#include <limits>
#include <map>
#include <set>
#include <utility>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <exception>

#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkSmartPointer.h>
#include <vtkImageData.h>

using namespace std;

namespace MSML {
namespace MiscMeshOperators
{
  LIBRARY_API  std::string ConvertSTLToVTK(std::string infile, std::string outfile);
  LIBRARY_API  bool ConvertSTLToVTK(const char* infile, const char* outfile);
  LIBRARY_API  bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh);

  LIBRARY_API  std::string ConvertVTKToSTL(std::string infile, std::string outfile);
  LIBRARY_API  bool ConvertVTKToSTL(const char* infile, const char* outfile);

  LIBRARY_API  bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile);

  LIBRARY_API  bool ConvertInpToVTK(const char* infile, const char* outfile);
  LIBRARY_API  bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh);

  LIBRARY_API  std::string ConvertVTKToVTU(std::string infile, std::string outfile); 
  LIBRARY_API  bool ConvertVTKToVTU(const char* infile, const char* outfile );

  
  LIBRARY_API  bool VTKToInp( const char* infile, const char* outfile);
  LIBRARY_API  bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile);

  LIBRARY_API  std::string ExtractSurfaceMesh( std::string infile, std::string outfile);
  LIBRARY_API  bool ExtractSurfaceMesh( const char* infile, const char* outfile);
  LIBRARY_API  bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);

  LIBRARY_API  const char* vtkSmoothMesh(const char* infile, const char* outfile, int iterations,
				  double feature_angle, double pass_band,bool boundary_smoothing,
				  bool feature_edge_smoothing, bool non_manifold_smoothing,
				  bool normalized_coordinates);
								  
  LIBRARY_API  vector<unsigned int> GetMaterialNumbersFromMesh( const char* infile);
		
  LIBRARY_API  bool DebugPrint(vector<int> to_print);
        

  LIBRARY_API  std::string ExtractAllSurfacesByMaterial( const char* infile, const char* outfile, bool theCutIntoPieces);
  LIBRARY_API  std::map<int,int>* createHist(vtkDataArray* theVtkDataArray);

  LIBRARY_API  bool AssignSurfaceRegion( const char* infile, const char* outfile,
          std::vector<std::string> regionMeshes );
  LIBRARY_API  bool AssignSurfaceRegion( vtkUnstructuredGrid* inputMesh,
  vtkUnstructuredGrid* outputMesh, std::vector<vtkSmartPointer<vtkPolyData> > & regionMeshes);

  LIBRARY_API  std::string ConvertVTKMeshToAbaqusMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName, std::string materialName);
  LIBRARY_API  std::string ConvertVTKMeshToAbaqusMeshString(std::string inputMesh,  std::string partName, std::string materialName);

  LIBRARY_API  std::string ProjectSurfaceMesh(std::string infile, std::string outfile, std::string referenceMesh);
  LIBRARY_API  bool ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh );
  LIBRARY_API  bool ProjectSurfaceMesh(vtkPolyData* inputMesh, vtkPolyData* referenceMesh);
  
  LIBRARY_API  bool ProjectVolumeMesh(std::string inputVolumeMesh, std::string outputSurfaceMesh, std::string referenceMesh);
  LIBRARY_API  bool ProjectVolumeMesh( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, vtkPolyData* referenceMesh);

  LIBRARY_API   std::string VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, bool disableFillHole, double additionalIsotropicMargin);
  LIBRARY_API   bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int spacing, double isotropicVoxelSize, const char* referenceCoordinateGrid, bool disableFillHole, double additionalIsotropicMargin);

  LIBRARY_API   bool VoxelizeVolumeMesh(vtkUnstructuredGrid* inputMesh, vtkImageData* outputImage, int spacing, double isotropicVoxelSize, const char* referenceCoordinateGrid, bool disableFillHole, double additionalIsotropicMargin);
  LIBRARY_API   std::string VoxelizeVolumeMesh(const char* infile, const char* outfile, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, bool disableFillHoles, double additionalIsotropicMargin);

  LIBRARY_API   std::string ConvertVTKPolydataToUnstructuredGrid(std::string infile, std::string outfile);
  LIBRARY_API   bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile );
  LIBRARY_API   bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh);

  LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, std::string inputMesh);
  LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, const char* infile);
  LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, vtkUnstructuredGrid* inputMesh);

  LIBRARY_API  bool ConvertVTKToGenericMesh(std::vector<double> &vertices , std::vector<unsigned int> &cellSizes, std::vector<unsigned int> &connectivity, std::string inputMesh);
  LIBRARY_API  bool ConvertVTKToGenericMesh( std::vector<double> &vertices , std::vector<unsigned int> &cellSizes, std::vector<unsigned int> &connectivity,  const char* infile);
  LIBRARY_API  bool ConvertVTKToGenericMesh( std::vector<double> &vertices , std::vector<unsigned int> &cellSizes, std::vector<unsigned int> &connectivity,  vtkUnstructuredGrid* inputMesh);

  LIBRARY_API  bool ConvertLinearToQuadraticTetrahedralMesh(std::string infile, std::string outfile);
  LIBRARY_API  bool ConvertLinearToQuadraticTetrahedralMesh( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh);



  LIBRARY_API  std::vector<unsigned int> ExtractNodeSet(std::string inputVolumeMeshFile, std::string nodeSetName);
  LIBRARY_API  std::vector<unsigned int> ExtractNodeSet( vtkUnstructuredGrid* inputMeshFile, std::string nodeSetName);

  LIBRARY_API  std::vector<double> ExtractVectorField(std::string inputVolumeMeshFile, std::string vectorFieldName, std::vector<unsigned int> nodeList);
  LIBRARY_API  std::vector<double> ExtractVectorField( vtkUnstructuredGrid* inputMeshFile, std::string vectorFieldName, std::vector<unsigned int> nodeList);

  LIBRARY_API std::string GenerateDistanceMap(const char* inputUnstructuredGrid, const char*  targetImage, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, double additionalIsotropicMargin );
  LIBRARY_API vtkSmartPointer<vtkImageData> GenerateDistanceMap(vtkUnstructuredGrid* unstructuredGrid, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, double additionalIsotropicMargin);

  LIBRARY_API std::string GenerateDistanceMap3d(const char* inputUnstructuredGrid, const char*  targetImage, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, double additionalIsotropicMargin );
  LIBRARY_API vtkSmartPointer<vtkImageData> GenerateDistanceMap3d(vtkUnstructuredGrid* unstructuredGrid, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, double additionalIsotropicMargin);

  LIBRARY_API vtkSmartPointer<vtkImageData> ImageCreateGeneric(vtkPointSet* grid, double resolution, float isotropicVoxelSize, const char* referenceCoordinateGrid, float additionalIsotropicMargin);
  LIBRARY_API vtkSmartPointer<vtkImageData> ImageCreateWithMesh(vtkPointSet* grid, double resolution);
  LIBRARY_API vtkSmartPointer<vtkImageData> ImageCreate(vtkImageData* refImageGrid);
  LIBRARY_API void ImageChangeVoxelSize(vtkImageData* image, double voxelSize);

  LIBRARY_API void ImageChangeVoxelSize(vtkImageData* image, double* voxelSize);
  LIBRARY_API void ImageEnlargeIsotropic(vtkImageData* image, double enlargement);

  LIBRARY_API std::string MorphCube(const char *infile, const char *outfile, double toDilate, 
			            double toErode, std::vector<double> morph_kernel);    
  
  LIBRARY_API std::string SelectVolumesByMaterialID(const char* infile,const char* oufile, std::vector<int> group);
 
  LIBRARY_API std::string ReplaceMaterialID(const char* infile, const char* outfile, std::vector<int> toReplace, int replaceBy);
  LIBRARY_API std::vector<double> BoundsFromMaterialID(const char* infile, int materialID);

  LIBRARY_API std::string SurfaceFromVolumeAndNormalDirection(const char* infile, const char* outfile, 
															  std::vector<double> desiredNormalDir, 
															  double margin);
  
  LIBRARY_API std::string ExtractBoundarySurfaceByMaterials(const char* infile, const char* outfile, 
										 int baseMeshMaterial, std::vector<int> otherMeshesMaterial);

  LIBRARY_API std::vector<double> GradientOnSurface(const char* inFile, std::vector<double> values, int steps);
  LIBRARY_API std::string CombineMeshes(const char* infileA, const char* infileB, const char* outfile);

  LIBRARY_API int CountVoxelsAbove(const char* inputImage, float threshold);


} //end namespace MiscMeshOperators
} // end namespace MSML


#endif /* __MiscMeshOperators_h */
