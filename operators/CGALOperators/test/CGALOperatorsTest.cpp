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
#include "../common/test_common.h"

#define BOOST_TEST_MODULE CGALOperatorsTest
#include <boost/test/unit_test.hpp>

#include <string>

BOOST_AUTO_TEST_CASE( TestCGALMeshVolumeFromVoxels)
{
  CGALOperators::CGALMeshVolumeFromVoxels(INPUT("ircad_segmentation.vti"), OUTPUT("TestCGALMeshVolumeFromVoxels.vtk"), 20, 10, 5, 3, 30, 1, 1, 1, 1);
}


BOOST_AUTO_TEST_CASE( TestCGALMeshVolumeFromSurface)
{
  CGALOperators::CGALMeshVolumeFromSurface(INPUT("bunny_polydata.vtk"), OUTPUT("TestCGALMeshVolumeFromSurface.vtk"), false, 20, 0.01, 5, 3, 0.03, 1, 1, 1, 1);
}

