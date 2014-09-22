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
  
  //CGALOperators::CreateVolumeMeshFromImage("../../testdata/liver_kidney_gallbladder.inr", "../../testdata/liver_kidney_gallbladder_tri_tet.vtu", false);
  CGALOperators::CreateVolumeMeshi2v((std::string(TESTDATA_PATH) + "3Dircadb0101Labeled.vti").c_str(), "E:\\GIT\\msml\\testdata\\3Dircadb0101Labeled.vtk", 20, 10, 5, 3, 30, 1, 1, 1, 1);
}
