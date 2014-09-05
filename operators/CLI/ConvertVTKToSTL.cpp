/*=========================================================================

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

#include "PostProcessingOperators.h"
#include "MiscMeshOperators.h"
#include "TetgenOperators.h"
#include <vector>
#include <iostream>
#include <string>
#include <sstream>

#include <boost/program_options/options_description.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/variables_map.hpp>

using namespace MSML;
namespace po = boost::program_options;



int main( int argc, char * argv[])
{

    po::options_description description("ConvertVTKToSTL Usage");

    description.add_options()
        ("help,h", "Display this help message")
        ("inputVTKMesh,i", po::value<std::string>(),"Filename of the input VTK mesh")
        ("outputSTLMesh,o", po::value<std::string>(),"Filename of the output VTK mesh");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, description), vm);
    po::notify(vm);

    if (vm.count("help")) {
        cout << description << "\n";
        return 1;
    }

    if (vm.size() == 0) {
        cout << description << "\n";
        return 1;
    }

    std::string inputMesh = vm["inputVTKMesh"].as<std::string>();
    std::string outputMesh = vm["outputSTLMesh"].as<std::string>();

    std::cout<<"Starting coloring mesh "<<inputMesh<<" and writing colored mesh "<<outputMesh<<"\n";

    MiscMeshOperators::ConvertVTKToSTL(inputMesh.c_str(),outputMesh.c_str() );





	return EXIT_SUCCESS;
}
