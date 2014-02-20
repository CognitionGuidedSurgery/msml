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

#ifndef MAPPINGOPERATORS_H_
#define MAPPINGOPERATORS_H_




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
// MappingOperators
// ****************************************************************************


namespace MSML {




class MappingOperators
{
public:
	// constructor
	MappingOperators();

	// destructor
	~MappingOperators();

	// standard class typedefs


	// public methods
	LIBRARY_API static std::string MapMeshPython( std::string meshIni, std::string meshDeformed, std::string meshToMap, std::string mappedMesh);
	LIBRARY_API static bool MapMesh( const char* meshIni, const char* meshDeformed, const char* meshToMap, const char* mappedMesh );
	LIBRARY_API static bool MapMesh( vtkUnstructuredGrid* meshIni,vtkUnstructuredGrid* meshDeformed, vtkUnstructuredGrid* meshToMap, vtkUnstructuredGrid* mappedMesh);

	// member access


protected:


private:
	// private methods


	// private attributes





};

} // end namespace MediAssist





#endif /* MAPPINGOPERATORS_H_ */
