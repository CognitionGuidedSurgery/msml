/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, VCGOperators
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

#ifndef __VCGOperators_h
#define __VCGOperators_h

// ****************************************************************************
// Includes
// ****************************************************************************
#include "../MSML_Operators.h"
#include <vector>
#include <limits>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>



#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>


using namespace std;



// ****************************************************************************
// Defines
// ****************************************************************************
#define USE_PROJEKTION 0
#define QUALITY_THRESHOLD 0.3;
#define FINENESS 0.5;
#define GRADING 0.3;
#define ELEMENTS_PER_CURVE 0.6;
#define ELEMENTS_PER_EDGE 0.3;



// ****************************************************************************
// VCGOperators
// ****************************************************************************



namespace MSML {




class VCGOperators
{
public:
	// constructor
	VCGOperators();

	// destructor
	~VCGOperators();

	// standard class typedefs


	// public methods
	LIBRARY_API static std::string CoarseSurfaceMeshPython(std::string infile, std::string outfile, int numberOfElements);
	LIBRARY_API static bool CoarseSurfaceMesh(const char* infile, const char* outfile, unsigned int numberOfElements);
	
	// member access


protected:



private:
	// private methods


	// private attributes





};

} // end namespace MediAssist


#endif /* __VCGOperators_h */
