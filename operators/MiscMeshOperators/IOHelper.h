#include <stdio.h>/*  =========================================================================

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

//#ifndef __IOHelper_h //ifdef does not work with function templates
//#define __IOHelper_h

// ****************************************************************************
// Includes
// ****************************************************************************
#include <vector>
#include <limits>
#include <map>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>



#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkImageData.h>
#include <vtkSmartPointer.h>
#include <vtkDataObject.h>

#include <../MSML_Operators.h>

using namespace std;

namespace MSML {
    namespace IOHelper {

        LIBRARY_API vtkSmartPointer<vtkImageData> VTKReadImage(const char* filename);
        LIBRARY_API vtkSmartPointer<vtkUnstructuredGrid> VTKReadUnstructuredGrid(const char* filename);
        LIBRARY_API vtkSmartPointer<vtkPolyData> VTKReadPolyData(const char* filename);
        LIBRARY_API vtkSmartPointer<vtkImageData> CTXReadImage(const char* filename);
        LIBRARY_API std::map<std::string, std::string> ReadTextFileToMap(std::string file, char delim);
        LIBRARY_API vector<pair<int, string> >* getAllFilesOfSeries(const char* filename);
        LIBRARY_API std::vector< std::string > getAllFilesByMask(const char* filename);
 
        LIBRARY_API bool VTKWriteImage(const char* filename, vtkImageData* image, bool asciiMode);
        LIBRARY_API bool VTKWriteUnstructuredGrid(const char* filename, vtkUnstructuredGrid* grid, bool asciiMode);
        LIBRARY_API bool VTKWritePolyData(const char* filename, vtkPolyData* image, bool asciiMode);
        LIBRARY_API bool VTKWriteImage(const char* filename, vtkImageData* image);
        LIBRARY_API bool VTKWriteUnstructuredGrid(const char* filename, vtkUnstructuredGrid* grid);
        LIBRARY_API bool VTKWritePolyData(const char* filename, vtkPolyData* polyData);
    }
}


//#endif /* __IOHelper_h */