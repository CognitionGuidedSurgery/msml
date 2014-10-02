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

#include "CGALOperators.h"
#include <string>
//#include <iostream>

using namespace MSML;

int main( int argc, char * argv[])
{                                                                                                                                                                        
  CGALOperators::CreateVolumeMeshs2v("G:/MSML_Data/pelvis/output_extractBladder_30.09.2014/PyDev_test/Calypso10000blase_surface_poly.vtk", "G:/MSML_Data/pelvis/output_extractBladder_30.09.2014/PyDev_test/TestCreateVolumeMeshs2v_with_Calypso10000blase_surface_poly.vtk", 
    false, 20, 5, 2, 3, 10, 0, 0, 0, 0);
  CGALOperators::CreateVolumeMeshi2v((std::string(TESTDATA_PATH) + "/ircad_segmentation.vti").c_str(), (std::string(TESTDATA_PATH) + "/TestCreateVolumeMeshi2v.vtk").c_str(), 20, 10, 5, 3, 30, 1, 1, 1, 1);
}
