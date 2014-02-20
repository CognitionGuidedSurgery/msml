/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, TetgenOperators
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

#include <boost/python.hpp>
#include "TetgenOperators.h"
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include "string.h"
#include <iostream>
#include <sstream>

typedef std::vector<unsigned int> VecUInt;
typedef std::vector<double> VecDouble;

using namespace std;




using namespace MSML;

//typedef std::vector<std::string> MyList;



//void   (*createVTKMeshFromSTLWrapped)(char* , char* , int , bool ) =  &MediAssist::MeshHandler::CreateVTKVolumeMeshFromSTL;


BOOST_PYTHON_MODULE(TetgenOperatorsPython)
{

    using namespace boost::python;

//    class_<MyList>("MyList")
//        .def(vector_indexing_suite<MyList>() );

//	class_<IndexRegionOperators::IndicesListType>("IndicesListType")
//			.def(vector_indexing_suite<IndexRegionOperators::IndexListType>() );

    class_<VecUInt>("VecUInt")
        .def(vector_indexing_suite<VecUInt>() );

    class_<VecDouble>("VecDouble")
        .def(vector_indexing_suite<VecDouble>() );
//
//    class_<MyClass>("MyClass")
//        .def("myFuncGet", &MyClass::myFuncGet)
//        .def("myFuncSet", &MyClass::myFuncSet)
//        ;


	def("createVolumeMeshTetgen", &TetgenOperators::CreateVolumeMeshPython);



}

