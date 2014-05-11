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
        LIBRARY_API  std::string ConvertSTLToVTKPython(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertSTLToVTK(const char* infile, const char* outfile);
        LIBRARY_API  bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh);

        LIBRARY_API  std::string ConvertVTKToSTLPython(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertVTKToSTL(const char* infile, const char* outfile);

        LIBRARY_API  bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile);

        //LIBRARY_API  std::string ConvertInpToVTKPython(std::string infile, std::string outfile);
        LIBRARY_API  bool ConvertInpToVTK(const char* infile, const char* outfile);
        LIBRARY_API  bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh);

    LIBRARY_API  static std::string ConvertVTKToVTUPython(std::string infile, std::string outfile); // python: 'convertVTKToVTU()'
	LIBRARY_API  static bool ConvertVTKToVTU(const char* infile, const char* outfile );
//	LIBRARY_API  static bool ConvertVTKToVTU(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh); // is this needed at all?!

        //LIBRARY_API  std::string VTKToInpPython( std::string infile, std::string outfile);
        LIBRARY_API  bool VTKToInp( const char* infile, const char* outfile);
        LIBRARY_API  bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile);

        LIBRARY_API  std::string ExtractSurfaceMeshPython( std::string infile, std::string outfile);
        LIBRARY_API  bool ExtractSurfaceMesh( const char* infile, const char* outfile);
        LIBRARY_API  bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);


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


        LIBRARY_API   std::string VoxelizeSurfaceMeshPython(std::string infile, std::string outfile, int resolution);
        LIBRARY_API   bool VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution);
        LIBRARY_API   bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int spacing);

        LIBRARY_API   std::string ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile);
        LIBRARY_API   bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile );
        LIBRARY_API   bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh);

//	LIBRARY_API  boost::python::list ExtractPointPositionsPython( boost::python::list indices, std::string infile);
        LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, const char* infile);
        LIBRARY_API  std::vector<double> ExtractPointPositions( std::vector<int> indices, vtkUnstructuredGrid* inputMesh);

    } //end namespace MiscMeshOperators
} // end namespace MSML


#endif /* __MiscMeshOperators_h */
