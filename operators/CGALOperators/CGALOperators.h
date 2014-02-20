/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, CGALOperators
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

#include "../MSML_Operators.h"
#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>

namespace MSML
{

  class CGALOperators
  {
    public:
	    // constructor
	    CGALOperators();
	    // destructor
	    ~CGALOperators();

      //vtk polydata -> tetrahedron unstructured grid vtk
      LIBRARY_API static std::string CreateVolumeMeshs2v(const char* infile, const char* outfile, bool thePreserveFeatures, double theFacetAngle, double theFacetSize, double theFacetDistance,
        double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder);
           
      //image vtk => tetrahedron unstructured grid vtk
      LIBRARY_API static  std::string CreateVolumeMeshi2v(const char* infile, const char* outfile, double theFacetAngle, double theFacetSize, double theFacetDistance,
        double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder);
 
    protected:
  };
}


