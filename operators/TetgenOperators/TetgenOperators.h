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


#ifndef __TetgenOperators_h
#define __TetgenOperators_h

// ****************************************************************************
// Includes
// ****************************************************************************
#include <vector>
#include <limits>
#include "../MSML_Operators.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>


using namespace std;


// ****************************************************************************
// TetgenOperators
// ****************************************************************************

namespace MSML {
    namespace Tetgen {
    LIBRARY_API bool CreateVolumeMesh(const char* infile, const char* outfile, bool preserveBoundary, bool isQuadratic );
    LIBRARY_API std::string CreateVolumeMeshPython(std::string infile, std::string outfile, bool preserveBoundary);
    LIBRARY_API bool CreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh, bool preserveBoundary, bool isQuadratic );
    } //end namespace Tetgen
} // end namespace MediAssist


#endif /* __TetgenOperators_h */
