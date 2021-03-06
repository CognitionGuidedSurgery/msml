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

#ifndef __IndexRegionOperators_h
#define __IndexRegionOperators_h

#include <vector>
#include <vtkUnstructuredGrid.h>
#include <vtkSmartPointer.h>
#include "string.h"
#include "../MSML_Operators.h"

using namespace std;

namespace MSML {
    namespace IndexRegionOperators {
        typedef std::vector<unsigned int> IndicesListType;

        LIBRARY_API vector<unsigned int> ComputeIndicesFromBoxROI(string filename, vector<double> box, string type);
        LIBRARY_API vector<unsigned int> ComputeIndicesFromMaterialId(string filename, int id, string type);
        LIBRARY_API vector<double> PositionFromIndices(string filename, vector<unsigned int> indices, string type);

    }
}

#endif /* __PostProcessingOperator_h */
