/*  =========================================================================

    Program:   The Medical Simulation Markup Language
    Module:    Operators, MiscMeshOperators, FeBioSupport
    Authors:   Sarah Grimm, Alexander Weigl

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

#include "FeBioSupport.h"
#include "IOHelper.h"

#include <vtkCellData.h>
#include <vtkDataArray.h>
#include <vtkImageData.h>
#include <vtkSmartPointer.h>
#include <vtkPoints.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkUnstructuredGrid.h>

#include <fstream>

using namespace std;

namespace MSML {
	namespace FeBioSupport {


void ConvertFEBToVTK(const std::string modelFilename,
					 const std::string lastStep,
					 std::string inputMesh)
{
	vtkSmartPointer<vtkPoints> thePointsOutput =
		 vtkSmartPointer<vtkPoints>::New();

	vtkSmartPointer<vtkUnstructuredGrid> vtkGrid =
		vtkSmartPointer<vtkUnstructuredGrid>::New();

	vtkSmartPointer<vtkUnstructuredGrid> referenceGrid =
		MSML::IOHelper::VTKReadUnstructuredGrid(inputMesh.c_str());

	vtkGrid->DeepCopy(referenceGrid);

	fstream f;
	char cstring[256];
	f.open(modelFilename.c_str(), ios::in);
	std::string prefix = "*";
	bool start = false;
	bool started = false;

    while (!f.eof())
    {
		double arr [4];
        f.getline(cstring, sizeof(cstring));
        int i = 0;
		stringstream ssin(cstring);
		std::string temp;
		if(cstring[0] == '*'){
			if(started == true){
				break;
			}
			while (ssin >> temp) {
				if(temp == lastStep) {
					start = true;
				}
			}
		} else {
			if(start){
				started = true;
				bool end = false;
				while (ssin.good() && i < 4){
					if(!ssin.str().empty()){
						ssin>>arr[i];
						++i;
					} else {
						end = true;
						break;
					}
				}
				if(!end){
					thePointsOutput->InsertNextPoint(arr[1], arr[2], arr[3]);
				}
			}
		}

    }
    f.close();
	string::size_type idx = modelFilename.find('.');
	std::string vtkFile = modelFilename.substr(0, idx) + ".vtk";
	vtkGrid->SetPoints(thePointsOutput);
	vtkGrid->GetPoints()->Modified();
	vtkGrid->Modified();

#if VTK_MAJOR_VERSION < 6
	vtkGrid->Update();
#endif

	MSML::IOHelper::VTKWriteUnstructuredGrid(vtkFile.c_str(), vtkGrid);
}


std::string ConvertVTKMeshToFeBioMeshString(vtkUnstructuredGrid* inputMesh, std::string partName)
{
	std::stringstream out;
	//write Geometry
	out << "<Geometry>\n";
	//nodes
	out << "<Nodes>\n";
	double* currentPoint;
	for(int i=0; i<inputMesh->GetNumberOfPoints(); i++)
	{
		currentPoint = inputMesh->GetPoint(i);
		out<<"<node id=\""<<i+1<<"\">"<< std::setprecision(7) << std::scientific;
		if(currentPoint[0] < 0 ){ //!!
			out<<currentPoint[0] << ",";
		}else{
			out<< " " << currentPoint[0] << ",";
		}
		if(currentPoint[1] < 0 ){
			out<<currentPoint[1] << ",";
		}else{
			out<< " " << currentPoint[1] << ",";
		}
		if(currentPoint[2] < 0 ){
			out<<currentPoint[2];
		}else{
			out<< " " << currentPoint[2];
		}
		out<< "</node>"<<"\n";
	}
	out << "</Nodes>\n";
	//elements
	out << "<Elements>\n";
	vtkIdType* currentCellPoints;
	vtkIdType numberOfNodesPerElement;
	vtkIdType cellType = inputMesh->GetCellType(0);
	vtkDataArray* pd = inputMesh->GetCellData()->GetScalars();
	for(int i=0; i<inputMesh->GetNumberOfCells(); i++)
	{
		inputMesh->GetCellPoints(i, numberOfNodesPerElement, currentCellPoints);
		double* key = pd->GetTuple(i);
		if((int) *key == 100){ // !!
			*key = 5;
		}
		if(numberOfNodesPerElement == 4) {
			out<<"<tet4 id=\""<<i+1<< "\" mat=\"" << ((int) *key + 1) << "\">";
			for(int j=0;j<numberOfNodesPerElement;j++)
			{
				if(j == numberOfNodesPerElement-1){ //!!
					out<<currentCellPoints[j]+1;
				} else{
					out<<currentCellPoints[j]+1<<",";
				}
			}
			out<<"</tet4>\n";
		}
		/*if(numberOfNodesPerElement == 3) {
		  out<<"<tri3 id=\""<<i+1<< "\" mat=\"" << ((int) *key + 1) << "\">";
		  for(int j=0;j<numberOfNodesPerElement;j++)
		  {
		  if(j == numberOfNodesPerElement-1){
		  out<<currentCellPoints[j-1]+1;
		  } else if(j == numberOfNodesPerElement-2){
		  out<<currentCellPoints[j+1]+1<<",";
		  }else{
		  out<<currentCellPoints[j]+1<<",";
		  }
		  }
		  out<<"</tri3>\n";
		  }*/
	}
	out << "</Elements>\n";
	out << "</Geometry>\n";
	return out.str();
}

std::string createFeBioPressureOutput(vtkUnstructuredGrid* inputMesh, std::vector<double> indices, std::string id, std::string pressure)
{
	std::stringstream out;
	//elements
	out << "<pressure>\n";
	vtkIdType* currentCellPoints;
	vtkIdType numberOfNodesPerElement;
	vtkIdType cellType = inputMesh->GetCellType(0);
	vtkDataArray* pd = inputMesh->GetCellData()->GetScalars();
	for(int i=0; i<indices.size(); i++)
	{
		inputMesh->GetCellPoints(indices[i], numberOfNodesPerElement, currentCellPoints);
		if(numberOfNodesPerElement == 3) {
			out<<"<tri3 id=\""<<i+1<< "\" lc=\""<< id << "\" scale=\""<< pressure <<"\" >" ; // lc als Parameter übergeben
			for(int j=0;j<numberOfNodesPerElement;j++)
			{
				if(j == numberOfNodesPerElement-1){
					out<<currentCellPoints[j]+1;
				} else{
					out<<currentCellPoints[j]+1<<",";
				}
			}
			out<<"</tri3>\n";
		}
	}
	out << "</pressure>\n";
return out.str();
}




std::string ConvertVTKMeshToFeBioMeshStringPython(std::string inputMesh, std::string partName)
{
	//load the vtk mesh
	log_debug() << "Converting " << inputMesh << " part " << partName << std::endl;
	vtkSmartPointer<vtkUnstructuredGrid> grid = MSML::IOHelper::VTKReadUnstructuredGrid(inputMesh.c_str());
	std::string output = ConvertVTKMeshToFeBioMeshString(grid, partName);
	return output;

}

std::string createFeBioPressureOutputPython(std::string inputMesh, std::vector <double> indices, std::string id, std::string pressure)
{
	vtkSmartPointer<vtkUnstructuredGrid> grid = MSML::IOHelper::VTKReadUnstructuredGrid(inputMesh.c_str());
	std::string output = createFeBioPressureOutput(grid, indices, id, pressure);
	return output;

}

}}