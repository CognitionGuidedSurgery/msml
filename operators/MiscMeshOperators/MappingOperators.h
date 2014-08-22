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

#ifndef MAPPINGOPERATORS_H_
#define MAPPINGOPERATORS_H_

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

/*MSMLDOC
MappingOperators
^^^^^^^^^^^^^^^^



*/

namespace MSML {
    namespace MappingOperators {
        /*MSMLDOC
            .. cpp:function:: std::string MapMeshPython ( std::string meshIni, std::string meshDeformed, std::string meshToMap, std::string mappedMesh )

                :param std::string meshIni:
                :param std::string meshDeformed:
                :param std::string meshToMap:
                :param std::string mappedMesh:

                :rtype:
                :returns:
        */
        LIBRARY_API std::string MapMeshPython ( std::string meshIni, std::string meshDeformed, std::string meshToMap, std::string mappedMesh );

        /*MSMLDOC
            .. cpp:function:: bool MapMesh ( const char* meshIni, const char* meshDeformed, const char* meshToMap, const char* mappedMesh )

                :param const char* meshIni:
                :param const char* meshDeformed:
                :param const char* meshToMap:
                :param const char* mappedMesh:

                :rtype:
                :returns:
        */
        LIBRARY_API bool MapMesh ( const char* meshIni, const char* meshDeformed, const char* meshToMap, const char* mappedMesh );

        /*MSMLDOC
            .. cpp:function:: bool MapMesh ( vtkUnstructuredGrid* meshIni,vtkUnstructuredGrid* meshDeformed, vtkUnstructuredGrid* meshToMap, vtkUnstructuredGrid* mappedMesh )

                :param vtkUnstructuredGrid* meshIni:
                :param vtkUnstructuredGrid* meshDeformed:
                :param vtkUnstructuredGrid* meshToMap:
                :param vtkUnstructuredGrid* mappedMesh:

                :rtype:
                :returns:
        */
        LIBRARY_API bool MapMesh ( vtkUnstructuredGrid* meshIni,vtkUnstructuredGrid* meshDeformed, vtkUnstructuredGrid* meshToMap, vtkUnstructuredGrid* mappedMesh );

    }
} // end namespace MediAssist

#endif /* MAPPINGOPERATORS_H_ */
