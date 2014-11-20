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

/*MSMLDOC
MiscMeshOperators
==================

.. cpp:namespace:: MSML::MiscMeshOperators


.. cpp:function:: std::string ConvertSTLToVTKPython(std::string infile, std::string outfile)

    :param std::string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertSTLToVTK(const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh)

    :param const char* infile:
    :param vtkPolyData* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKToSTLPython(std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKToSTL(const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile)

    :param vtkPolyData* inputMesh:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertInpToVTK(const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh)

    :param const char* infile:
    :param vtkUnstructuredGrid* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKToVTUPython(std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool        ConvertVTKToVTU(const char* infile, const char* outfile )

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool VTKToInp( const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile)

    :param vtkUnstructuredGrid* inputMesh:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: std::string ExtractSurfaceMeshPython( std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ExtractSurfaceMesh( const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:

.. cpp:function:: bool DebugPrint(vector<int> to_print)

    :param vector<int> to_print:

    :returns:
    :rtype:
	
.. cpp:function:: vector<unsigned int> GetMaterialNumbersFromMesh( const char* infile)

    :param const char* infile:

    :returns:
    :rtype:

.. cpp:function:: bool SmoothMeshPython(const char* infile, const char* outfile, int iterations,
										  double feature_angle, double pass_band,bool boundary_smoothing,
										  bool feature_edge_smoothing, bool non_manifold_smoothing,
										  bool normalized_coordinates)

    :param const char* infile:
    :param const char* outfile:
	:param int iterations:
	:param double feature_angle:
	:param double pass_band:
	:param bool boundary_smoothing:
	:param bool feature_edge_smoothing:
	:param bool non_manifold_smoothing:
	:param bool normalized_coordinates:

    :returns:
    :rtype:


.. cpp:function:: bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)

    :param vtkUnstructuredGrid* inputMesh:
    :param vtkPolyData* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string ExtractAllSurfacesByMaterial( const char* infile, const char* outfile, bool theCutIntoPieces)

    :param const char* infile:
    :param const char* outfile:
    :param bool theCutIntoPieces:

    :returns:
    :rtype:




.. cpp:function:: std::map\<int,int>* createHist(vtkDataArray* theVtkDataArray)

    :param vtkDataArray* theVtkDataArray:

    :returns:
    :rtype:




.. cpp:function:: bool AssignSurfaceRegion( const char* infile, const char* outfile, std::vector\<std::string> regionMeshes )

    :param const char* infile:
    :param const char* outfile:
    :param std\:\:vector\<std::string> regionMeshes:

    :returns:
    :rtype:




.. cpp:function:: bool AssignSurfaceRegion( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, std::vector\<vtkSmartPointer\<vtkPolyData> > & regionMeshes)

    :param vtkUnstructuredGrid* inputMesh:
    :param vtkUnstructuredGrid* outputMesh:
    :param std\:\:vector\<vtkSmartPointer\<vtkPolyData> > & regionMeshes:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKMeshToAbaqusMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName, std::string materialName)

    :param vtkUnstructuredGrid* inputMesh:
    :param std\:\:string partName:
    :param std\:\:string materialName:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKMeshToAbaqusMeshStringPython(std::string inputMesh,  std::string partName, std::string materialName)

    :param std\:\:string inputMesh:
    :param std\:\:string partName:
    :param std\:\:string materialName:

    :returns:
    :rtype:




.. cpp:function:: std::string ProjectSurfaceMeshPython(std::string infile, std::string outfile, std::string referenceMesh)

    :param std\:\:string infile:
    :param std\:\:string outfile:
    :param std\:\:string referenceMesh:

    :returns:
    :rtype:




.. cpp:function:: bool ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh )

    :param const char* infile:
    :param const char* outfile:
    :param const char* referenceMesh:

    :returns:
    :rtype:




.. cpp:function:: bool ProjectSurfaceMesh(vtkPolyData* inputMesh, vtkPolyData* referenceMesh)

    :param vtkPolyData* inputMesh:
    :param vtkPolyData* referenceMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string VoxelizeSurfaceMeshPython(std::string infile, std::string outfile, int resolution)

    :param std\:\:string infile:
    :param std\:\:string outfile:
    :param int resolution:

    :returns:
    :rtype:




.. cpp:function:: bool VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution)

    :param const char* infile:
    :param const char* outfile:
    :param int resolution:

    :returns:
    :rtype:




.. cpp:function:: bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int spacing)

    :param vtkPolyData* inputMesh:
    :param vtkImageData* outputImage:
    :param int spacing:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile )

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh)

    :param vtkPolyData* inputPolyData:
    :param vtkUnstructuredGrid* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::vector\<double> ExtractPointPositions( std::vector\<int> indices, const char* infile)

    :param std\:\:vector\<int> indices:
    :param const char* infile:

    :returns:
    :rtype:




.. cpp:function:: std::vector\<double> ExtractPointPositions( std::vector\<int> indices, vtkUnstructuredGrid* inputMesh)

    :param std\:\:vector\<int> indices:
    :param vtkUnstructuredGrid* inputMesh:

    :returns:
    :rtype:

*/



namespace MSML {
    namespace MiscMeshOperators
    {
        LIBRARY_API  std::string ConvertSTLToVTKPython(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertSTLToVTK(const char* infile, const char* outfile);
        LIBRARY_API  bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh);

        LIBRARY_API  std::string ConvertVTKToSTLPython(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertVTKToSTL(const char* infile, const char* outfile);

        LIBRARY_API  bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile);

        //LIBRARY_API  std::string ConvertInpToVTKPython(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertInpToVTK(const char* infile, const char* outfile);
        LIBRARY_API  bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh);

        LIBRARY_API  std::string ConvertVTKToVTUPython(std::string infile, std::string outfile); // python: 'convertVTKToVTU()'
	    LIBRARY_API  bool        ConvertVTKToVTU(const char* infile, const char* outfile );
//	LIBRARY_API  static bool ConvertVTKToVTU(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh); // is this needed at all?!

        //LIBRARY_API  std::string VTKToInpPython( std::string infile, std::string outfile);
        LIBRARY_API  bool VTKToInp( const char* infile, const char* outfile);
        LIBRARY_API  bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile);

        LIBRARY_API  std::string ExtractSurfaceMeshPython( std::string infile, std::string outfile);
        LIBRARY_API  bool ExtractSurfaceMesh( const char* infile, const char* outfile);
        LIBRARY_API  bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);

		LIBRARY_API  bool SmoothMeshPython(const char* infile, const char* outfile, int iterations,
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
        LIBRARY_API  std::string ConvertVTKMeshToAbaqusMeshStringPython(std::string inputMesh,  std::string partName, std::string materialName);

        LIBRARY_API   std::string ProjectSurfaceMeshPython(std::string infile, std::string outfile, std::string referenceMesh);
        LIBRARY_API   bool ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh );
        LIBRARY_API   bool ProjectSurfaceMesh(vtkPolyData* inputMesh, vtkPolyData* referenceMesh);

        LIBRARY_API   std::string VoxelizeSurfaceMeshPython(const char* infile, const char* outfile, int resolution, double isotropicVoxelSize, const char* referenceCoordinateGrid, bool disableFillHole, double additionalIsotropicMargin);
        LIBRARY_API   bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int spacing, double isotropicVoxelSize, const char* referenceCoordinateGrid, bool disableFillHole, double additionalIsotropicMargin);

        LIBRARY_API   std::string ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile);
        LIBRARY_API   bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile );
        LIBRARY_API   bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh);

//	LIBRARY_API  boost::python::list ExtractPointPositionsPython( boost::python::list indices, std::string infile);
        LIBRARY_API  std::vector<double> ExtractPointPositionsPython( std::vector<int> indices, std::string inputMesh);
        LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, const char* infile);
        LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, vtkUnstructuredGrid* inputMesh);

        LIBRARY_API  bool ConvertLinearToQuadraticTetrahedralMesh(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertLinearToQuadraticTetrahedralMesh( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh);

        LIBRARY_API  bool ProjectSurfaceMesh(std::string inputVolumeMesh, std::string outputSurfaceMesh, std::string referenceMesh);
        LIBRARY_API  bool ProjectSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, vtkPolyData* referenceMesh);

        LIBRARY_API  std::vector<unsigned int> ExtractNodeSet(std::string inputVolumeMeshFile, std::string nodeSetName);
        LIBRARY_API  std::vector<unsigned int> ExtractNodeSet( vtkUnstructuredGrid* inputMeshFile, std::string nodeSetName);

        LIBRARY_API  std::vector<double> ExtractVectorField(std::string inputVolumeMeshFile, std::string vectorFieldName, std::vector<unsigned int> nodeList);
        LIBRARY_API  std::vector<double> ExtractVectorField( vtkUnstructuredGrid* inputMeshFile, std::string vectorFieldName, std::vector<unsigned int> nodeList);

        LIBRARY_API vtkSmartPointer<vtkImageData> ImageCreateWithMesh(vtkPointSet* grid, double resolution);
        LIBRARY_API vtkSmartPointer<vtkImageData> ImageCreate(vtkImageData* refImageGrid);
        LIBRARY_API void ImageChangeVoxelSize(vtkImageData* image, double voxelSize);
        LIBRARY_API void ImageChangeVoxelSize(vtkImageData* image, double* voxelSize);
        LIBRARY_API void ImageEnlargeIsotropic(vtkImageData* image, double enlargement);


    } //end namespace MiscMeshOperators
} // end namespace MSML


#endif /* __MiscMeshOperators_h */
