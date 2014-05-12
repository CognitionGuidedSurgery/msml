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

//#ifndef __IOHelper_h //ifdef does not work with function templates
//#define __IOHelper_h

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
#include <vtkSmartPointer.h>
#include <vtkDataObject.h>

#include <../MSML_Operators.h>

using namespace std;

/*MSMLDOC
IOHelper
^^^^^^^^

.. cpp:namespace:: MSML::IOHelper

.. cpp:function:: vtkSmartPointer\<vtkImageData> VTKReadImage(const char* filename)

    :param const char* filename:

    :returns:
    :rtype:




.. cpp:function:: vtkSmartPointer\<vtkUnstructuredGrid> VTKReadUnstructuredGrid(const char* filename)

    :param const char* filename:

    :returns:
    :rtype:




.. cpp:function:: vtkSmartPointer\<vtkPolyData> VTKReadPolyData(const char* filename)

    :param const char* filename:

    :returns:
    :rtype:


*/

namespace MSML {
    namespace IOHelper {

        LIBRARY_API vtkSmartPointer<vtkImageData> VTKReadImage(const char* filename);
        LIBRARY_API vtkSmartPointer<vtkUnstructuredGrid> VTKReadUnstructuredGrid(const char* filename);
        LIBRARY_API vtkSmartPointer<vtkPolyData> VTKReadPolyData(const char* filename);

    }
}


//#endif /* __IOHelper_h */
