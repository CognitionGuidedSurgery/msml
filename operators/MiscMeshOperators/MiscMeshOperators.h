/*=========================================================================

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

// ****************************************************************************
// Includes
// ****************************************************************************
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

//#include <boost/python.hpp>


using namespace std;
//using namespace MediAssist;


// ****************************************************************************
// Defines
// ****************************************************************************





// ****************************************************************************
// MiscMeshOperators
// ****************************************************************************

/** \class AbsImageFilter
 * \brief This class does some really fancy stuff
 *
 * \ingroup Examples
 */


namespace MSML {




class MiscMeshOperators
{
public:
	// constructor
	MiscMeshOperators();

	// destructor
	~MiscMeshOperators();

	// standard class typedefs


	// public methods

	LIBRARY_API static std::string ConvertSTLToVTKPython(std::string infile, std::string outfile);
	LIBRARY_API static bool ConvertSTLToVTK(const char* infile, const char* outfile);
	LIBRARY_API static bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh);

	LIBRARY_API static std::string ConvertVTKToSTLPython(std::string infile, std::string outfile);
	LIBRARY_API static bool ConvertVTKToSTL(const char* infile, const char* outfile);

	LIBRARY_API static bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile);

	LIBRARY_API static std::string ConvertInpToVTKPython(std::string infile, std::string outfile);
	LIBRARY_API static bool ConvertInpToVTK(const char* infile, const char* outfile);
	LIBRARY_API static bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh);

	LIBRARY_API static std::string VTKToInpPython( std::string infile, std::string outfile);
	LIBRARY_API static bool VTKToInp( const char* infile, const char* outfile);
	LIBRARY_API static bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile);

	LIBRARY_API static std::string ExtractSurfaceMeshPython( std::string infile, std::string outfile);
	LIBRARY_API static bool ExtractSurfaceMesh( const char* infile, const char* outfile);
	LIBRARY_API static bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh);


	LIBRARY_API static std::string ExtractAllSurfacesByMaterial( const char* infile, const char* outfile, bool theCutIntoPieces);
  	LIBRARY_API static std::map<int,int>* createHist(vtkDataArray* theVtkDataArray);

	LIBRARY_API static bool AssignSurfaceRegion( const char* infile, const char* outfile,  std::vector<std::string> regionMeshes );
	LIBRARY_API static bool AssignSurfaceRegion( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, std::vector<vtkSmartPointer<vtkPolyData> > & regionMeshes);

	LIBRARY_API static std::string ConvertVTKMeshToAbaqusMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName, std::string materialName);
	LIBRARY_API static std::string ConvertVTKMeshToAbaqusMeshStringPython(std::string inputMesh,  std::string partName, std::string materialName);

	LIBRARY_API  static std::string ProjectSurfaceMeshPython(std::string infile, std::string outfile, std::string referenceMesh);
	LIBRARY_API  static bool ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh );
	LIBRARY_API  static bool ProjectSurfaceMesh(vtkPolyData* inputMesh, vtkPolyData* referenceMesh);


	LIBRARY_API  static std::string VoxelizeSurfaceMeshPython(std::string infile, std::string outfile, int resolution);
	LIBRARY_API  static bool VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution);
	LIBRARY_API  static bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int spacing);

	LIBRARY_API  static std::string ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile);
	LIBRARY_API  static bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile );
	LIBRARY_API  static bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh);

    LIBRARY_API  static std::string ConvertVTKToVTUPython(std::string infile, std::string outfile); // python: 'convertVTKToVTU()'
	LIBRARY_API  static bool ConvertVTKToVTU(const char* infile, const char* outfile );
//	LIBRARY_API  static bool ConvertVTKToVTU(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh); // is this needed at all?!

//	LIBRARY_API static boost::python::list ExtractPointPositionsPython( boost::python::list indices, std::string infile);
	LIBRARY_API static std::vector<double> ExtractPointPositions( std::vector<int> indices, const char* infile);
	LIBRARY_API static std::vector<double> ExtractPointPositions( std::vector<int> indices, vtkUnstructuredGrid* inputMesh);

	// member access


protected:


private:
	// private methods


	// private attributes





};

} // end namespace MediAssist


#endif /* __MiscMeshOperators_h */
