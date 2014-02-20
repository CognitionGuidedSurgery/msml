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

    po::options_description description("TetgenMesher Usage");

    description.add_options()
        ("help,h", "Display this help message")
        ("surfaceMesh,s", po::value<std::string>(),"Filename of the input surface mesh")
        ("volumeMesh,v", po::value<std::string>(),"Filename of the output volume mesh")
        ("preserveBoundary,p", po::value<bool>()->default_value(true),"Flag if surface should be preserved");

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

    std::string surfaceMesh = vm["surfaceMesh"].as<std::string>();
    std::string volumeMesh = vm["volumeMesh"].as<std::string>();
    bool preserveBoundary = vm["preserveBoundary"].as<bool>();

    std::cout<<"Starting meshing with tetgen on surface mesh "<<surfaceMesh<<" and writing volume mesh "<<volumeMesh;
    if(preserveBoundary)
    	std::cout<<" boundary preserve on";
    std::cout<<"\n";

    TetgenOperators::CreateVolumeMesh(surfaceMesh.c_str(),volumeMesh.c_str(), preserveBoundary, false );





	return EXIT_SUCCESS;
}
