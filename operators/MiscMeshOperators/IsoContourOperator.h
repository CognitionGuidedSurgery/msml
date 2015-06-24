#include "../MSML_Operators.h"

#include <iostream>
#include <fstream>
#include <string>
#include <stdlib.h> 
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkUnstructuredGrid.h>
#include <vtkSmartPointer.h>
#include <vtkPoints.h>
#include <vtkDataSetSurfaceFilter.h>
#include <vtkPolyData.h>
#include <vtkXMLPolyDataWriter.h>
#include <cmath>
#include <vtkPolyDataNormals.h>
#include <vtkFloatArray.h>
#include <vtkPointData.h>

namespace MSML
{
	namespace IsoContourOperator
	{
		LIBRARY_API std::vector<std::string> IsoContourOperator(const char* data_directory, const char* initial_position, const char* final_position, const char* weight_table);
	}
}
