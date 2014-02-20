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

#include <boost/python.hpp>
#include "MiscMeshOperators.h"
#include "PostProcessingOperators.h"
#include "IndexRegionOperators.h"
#include "MappingOperators.h"

#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include "string.h"
#include <iostream>
#include <sstream>

typedef std::vector<unsigned int> VecUInt;
typedef std::vector<double> VecDouble;

using namespace std;

//char const* greet()
//{
//   return "hello, world";
//}
//
//std::string greetString(std::string input)
//{
//	ostringstream stream;
//	stream<<input;
//	stream<<" and one";
//   return stream.str();
//}
//
//std::string greetString2(const VecUInt & list)
//{
//	ostringstream stream;
//	stream<<list[0]<<list[1]<<list[2];
//	stream<<" and one";
//   return stream.str();
//}



using namespace MSML;

//typedef std::vector<std::string> MyList;



//void   (*createVTKMeshFromSTLWrapped)(char* , char* , int , bool ) =  &MediAssist::MeshHandler::CreateVTKVolumeMeshFromSTL;

static boost::python::list ExtractPointPositionsPython( boost::python::list indices, std::string infile)
{
//	std::cout<<"ExtractPointPositionsPython called \n";

//	std::cout<<"Length of indices is "<<boost::python::len(indices)<<"\n";

	int currentIndex = boost::python::extract<int>(indices[0]);

//	std::cout<<"First extraction successfull called \n";



	unsigned int indicesSize = boost::python::len(indices);
	std::vector<int> c_indices;
	for(int i=0; i<indicesSize; i++)
	{
		unsigned int currentIndex = boost::python::extract<int>(indices[i]);
		c_indices.push_back(currentIndex);
//		std::cout<<"Current index "<<currentIndex;
	}

	std::vector<double> pointPositions = MiscMeshOperators::ExtractPointPositions( c_indices, infile.c_str());
	boost::python::list positionsPython;

	for(int i=0; i< pointPositions.size();i++)
	{
		positionsPython.append(pointPositions[i]);
	}

	return positionsPython;


}

static boost::python::list CompareMeshesPython(std::string referenceFilename, std::string testFilename)
{
	std::cout<<"Compare meshes called\n";
	boost::python::list errorsPython;


	double errorRMS, errorMax;

	PostProcessingOperators::CompareMeshes(errorRMS,errorMax, referenceFilename.c_str(), testFilename.c_str(), false);

	errorsPython.append(errorRMS);
	errorsPython.append(errorMax);

	PostProcessingOperators::CompareMeshes(errorRMS,errorMax, referenceFilename.c_str(), testFilename.c_str(), true);

	errorsPython.append(errorRMS);
	errorsPython.append(errorMax);


	return errorsPython;
}

static boost::python::list CompareMeshesFullErrorPython(std::string referenceFilename, std::string testFilename, bool surfaceOnly)
{
	std::cout<<"Compare meshes called\n";
	boost::python::list errorsPython;
	std::vector<double> errorVec;


	PostProcessingOperators::CompareMeshes(errorVec, referenceFilename.c_str(), testFilename.c_str(), surfaceOnly);

	for(unsigned int i=0; i<errorVec.size(); i++)
	{
		errorsPython.append(errorVec[i]);
	}

	return errorsPython;
}



BOOST_PYTHON_MODULE(MiscMeshOperatorsPython)
{

    using namespace boost::python;


    class_<VecUInt>("VecUInt")
        .def(vector_indexing_suite<VecUInt>() );

    class_<VecDouble>("VecDouble")
        .def(vector_indexing_suite<VecDouble>() );

	def("computeIndicesFromBoxROI", &IndexRegionOperators::computeIndicesFromBoxROI);
	def("computeIndicesFromMaterialId", &IndexRegionOperators::computeIndicesFromMaterialId);
	
	def("colorMeshOperator", &PostProcessingOperators::ColorMeshPython);
  def("GenerateDVF", &PostProcessingOperators::GenerateDVFPython);
  def("ApplyDVF", &PostProcessingOperators::ApplyDVFPython);

	def("ExtractAllSurfacesByMaterial", &MiscMeshOperators::ExtractAllSurfacesByMaterial);
  def("convertVTKMeshToAbaqusMeshString", &MiscMeshOperators::ConvertVTKMeshToAbaqusMeshStringPython);
	def("projectSurfaceMesh", &MiscMeshOperators::ProjectSurfaceMeshPython);
	def("extractSurfaceMesh", &MiscMeshOperators::ExtractSurfaceMeshPython);
	def("convertVtkToInp", &MiscMeshOperators::VTKToInpPython);
	def("voxelizeSurfaceMesh", &MiscMeshOperators::VoxelizeSurfaceMeshPython);
	def("convertSTLToVTK", &MiscMeshOperators::ConvertSTLToVTKPython);
	def("convertVTKToSTL", &MiscMeshOperators::ConvertVTKToSTLPython);
	def("convertVTKPolydataToUnstructuredGrid", &MiscMeshOperators::ConvertVTKPolydataToUnstructuredGridPython);

	def("compareMeshes", &CompareMeshesPython);
	def("compareMeshesFullError", &CompareMeshesFullErrorPython);
	def("extractPointPositions", &ExtractPointPositionsPython);
	def("colorMeshFromComparison", &PostProcessingOperators::ColorMeshFromComparisonPython);

	def("mapMesh", &MappingOperators::MapMeshPython);

}

