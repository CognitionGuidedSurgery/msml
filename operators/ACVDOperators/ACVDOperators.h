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


#ifndef __MiscExtOperators_h
#define __MiscExtOperators_h

#include "../MSML_Operators.h"
#include "vtkPolyData.h"
#include <string.h>



using namespace std;


namespace MSML {
    namespace ACVDOperators
    {
        LIBRARY_API  std::string ReduceSurfaceMeshPython(std::string infile, std::string outfile, int verticesCount, bool forceManifold, bool asciiOutput);
        LIBRARY_API  bool ReduceSurfaceMesh(vtkPolyData* in, vtkPolyData* out, int verticesCount, bool forceManifold);


    } //end namespace MiscExtOperators
} // end namespace MSML


#endif /* __MiscExtOperators_h */
