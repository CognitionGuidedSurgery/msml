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

#include "ACVDOperators.h"
#include <string>
using namespace MSML;

int main( int argc, char * argv[])
{                                            
	ACVDOperators::ReduceSurfaceMesh((std::string(TESTDATA_PATH) + "/TestACVD_cylinder_rough.vtk").c_str(), 
										   (std::string(TESTDATA_PATH) + "/TestACVD_cylinder_remeshed.vtk").c_str(), 	
											2000,true,true);
       
}
