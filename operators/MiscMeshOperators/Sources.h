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

#ifndef SOURCES_H_
#define SOURCES_H_

#include "../MSML_Operators.h"
#include <vector>
#include <limits>
#include <map>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <exception>

#include <vtkSmartPointer.h>
#include <vtkPolyData.h>

using namespace std;

namespace MSML {
  namespace Sources {
  LIBRARY_API const char*  GenerateSpheres(vector<double> centers, double radius, int thetaResolution, int phiResolution, const char* targetFileName);
  LIBRARY_API vtkSmartPointer<vtkPolyData> GenerateSpheres(vector<double> centers, double radius, int thetaResolution, int phiResolution);
  }
} // end MSML

#endif /* SOURCES_H_ */
