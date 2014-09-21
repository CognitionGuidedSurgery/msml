/*  =========================================================================

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

// ****************************************************************************
// Includes
// ****************************************************************************
#include <vector>
#include <limits>


#include <boost/filesystem.hpp>
#include <boost/algorithm/string/trim_all.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/lexical_cast.hpp>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sstream>      // std::istringstream
#include <iostream>
#include <map>


#include <vtkSmartPointer.h>
#include <vtkGenericDataObjectReader.h>
#include <vtkXMLGenericDataObjectReader.h>
#include <vtkImageReader.h>
#include <vtkImageFlip.h>

#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkImageData.h>

#include "MiscMeshOperators.h"


#include "IOHelper.h"
using namespace std;

// ****************************************************************************
// Defines
// ****************************************************************************


// ****************************************************************************
// PostProcessingOperators
// ****************************************************************************




namespace MSML {

vtkSmartPointer<vtkImageData> IOHelper::CTXReadImage(const char* filename)
{
  boost::filesystem::path filePath(filename);
  assert(filePath.extension().string() == ".ctx"); //legacy datat format
  boost::filesystem::path filePathHed = filePath.replace_extension("hed");
  std::map<std::string, std::string> hed_map = ReadTextFileToMap(filePathHed.string(), ' ');
  vtkSmartPointer<vtkImageReader2> reader = vtkSmartPointer<vtkImageReader2>::New();
  reader->SetFileName(filename);
  assert(hed_map["xoffset"] == "0"); 
  assert(hed_map["yoffset"] == "0"); 
  assert(hed_map["zoffset"] == "0");
  reader->SetDataSpacing(atof(hed_map["pixel_size"].c_str()), atof(hed_map["pixel_size"].c_str()), atof(hed_map["slice_distance"].c_str()));
  reader->SetDataExtent(0, atof(hed_map["dimx"].c_str())-1, 0, atof(hed_map["dimy"].c_str())-1, 0, atof(hed_map["slice_number"].c_str())-1);
  reader->SetDataOrigin(0.0, 0.0, atof(hed_map["1"].c_str())); //first slice
  reader->SetDebug(1);
  reader->SetFileDimensionality(3);
  reader->Update();
  assert(hed_map["data_type"] == "integer"); // data_type = interger  OR  data_type=float
  assert(hed_map["num_bytes"] == "2");
  reader->SetNumberOfScalarComponents(1);
  reader->SetDataScalarTypeToShort();
  reader->SetDataByteOrderToLittleEndian();
  reader->UpdateWholeExtent();

  vtkSmartPointer<vtkImageFlip> flipFilter = vtkSmartPointer<vtkImageFlip>::New();
  flipFilter->SetFilteredAxis(1); // flip y axis
  flipFilter->SetInputConnection(reader->GetOutputPort());
  flipFilter->Update();

  vtkSmartPointer<vtkImageData> aReturn = flipFilter->GetOutput();

  reader->SetFileName("");
  reader->Update();

  return aReturn;
}

std::map<std::string, std::string> IOHelper::ReadTextFileToMap(std::string file, char delim)
{
  std::map<std::string, std::string> keyValueMap;
	std::ifstream fileStream;
	fileStream.open(file.c_str(), std::ifstream::in);
  if (fileStream)
  {
	  std::string line;  
	  while(getline(fileStream, line))
	  {
      boost::algorithm::trim_all(line);
      std::istringstream lineStream(line);
      std::string field;
      std::vector<string> fields;
      fields.clear();
      while (getline(lineStream, field, delim)) 
      {
        fields.push_back(field);
      }
      if (fields.size() > 1)
      {
        keyValueMap[fields[0]] = fields[1] ;
      }
	  }
	  fileStream.close();
  }
  return keyValueMap;
}

vtkSmartPointer<vtkImageData> IOHelper::VTKReadImage(const char* filename)
{
  boost::filesystem::path filePath(filename);
  
  if (!boost::filesystem::exists(filePath))
    cerr << filePath << " was not found." << endl;

  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    vtkImageData* aReturn = (vtkImageData*)reader->GetOutput();
    if (!reader->IsFileStructuredPoints())
      cerr << filePath << " is not an .vtk image." << endl;
    return aReturn;
  }
  else if (filePath.extension().string() == ".ctx")
  {
    return IOHelper::CTXReadImage(filename);
  }

  else if (filePath.extension().string() == ".gz")
  {
    boost::filesystem::path filePath_without_gz(filename);
    filePath_without_gz = filePath_without_gz.replace_extension("");
    string command = "gunzip -c \"" + filePath.string() + "\" >\"" + filePath_without_gz.string() + "\"";
    cout << command << std::endl;
    system(command.c_str());    
    vtkSmartPointer<vtkImageData> tmp = IOHelper::CTXReadImage(filePath_without_gz.string().c_str());
    boost::filesystem::remove(filePath_without_gz);
    return tmp;
  }

  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    vtkSmartPointer<vtkImageData> aReturn = reader->GetImageDataOutput();
    if (!reader->GetImageDataOutput())
      cerr << filePath << " is not an .vti image." << endl;
    return aReturn;
  }
}

vtkSmartPointer<vtkUnstructuredGrid> IOHelper::VTKReadUnstructuredGrid(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkDataObject> aReturn;

  if (!boost::filesystem::exists(filePath))
    cerr << filePath << " was not found." << endl;
  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (!reader->IsFileUnstructuredGrid())
      cerr << filePath << " is not an .vtk unstructured grid." << endl;
    return reader->GetUnstructuredGridOutput();
  }
  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (!reader->GetUnstructuredGridOutput() )
      cerr << filePath << " is not an .vtu unstructured grid." << endl;
    return reader->GetUnstructuredGridOutput();
  }
}

vtkSmartPointer<vtkPolyData> IOHelper::VTKReadPolyData(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkDataObject> aReturn;
  if (!boost::filesystem::exists(filePath))
   cerr << filePath << " was not found." << endl;

  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();

    if (reader->GetPolyDataOutput())
    {
       return reader->GetPolyDataOutput();
       cerr << filePath << " is no poly data file. Trying to use MiscMeshOperators::ExtractSurfaceMesh(IOHelper::VTKReadUnstructuredGrid(..)" << endl;
    }

    else 
    {
      vtkSmartPointer<vtkPolyData> poly = vtkSmartPointer<vtkPolyData>::New();
      MiscMeshOperators::ExtractSurfaceMesh(IOHelper::VTKReadUnstructuredGrid(filename), poly);
      return poly;
    }
  }
  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (reader->GetPolyDataOutput())
      return reader->GetPolyDataOutput();
    else 
    {
      vtkSmartPointer<vtkPolyData> poly = vtkSmartPointer<vtkPolyData>::New();
      MiscMeshOperators::ExtractSurfaceMesh(IOHelper::VTKReadUnstructuredGrid(filename), poly);
      return poly;
    }
  }
}
/*
IOHelper::VTKWriteImage()
IOHelper::VTKWriteImage()
IOHelper::VTKWriteImage()*/


//find all files with the same name (without digit postfix) and any digit postfix.
//TODO: move to Python
vector<pair<int, string> >* IOHelper::getAllFilesOfSeries(const char* filename)
{
    vector<pair<int, string> >* aReturn = new vector<pair<int, string> >();
    boost::filesystem::path aPath(filename);
    boost::filesystem::path extension = aPath.extension();
    boost::filesystem::path file = aPath.filename().stem();
    std::string aFilename = file.string();
    
    //how many digits? 
    int i=aFilename.length()-1;
    int numberOfDigits=0;
    while(i>0 && aFilename[i] >='0' && aFilename[i] <='9')
    {
        numberOfDigits++;
        i--;
    }

    //find all files with the same name (without digit postfix) and any digit postfix.
    aFilename = aFilename.substr(0,aFilename.length()-numberOfDigits);
    for (int i=0; i<pow(10.0,(double)numberOfDigits); i++)
    {
        boost::filesystem::path curentPath = aPath.parent_path() / (aFilename + boost::lexical_cast<string>(i) + extension.string());

        if(boost::filesystem::exists(curentPath))
        {
            aReturn->push_back(std::make_pair(i, curentPath.string()));
        }
    }

    return aReturn;
}


//refactor with:

/*
template <typename T>
static vtkSmartPointer<T> IOHelper::VTKRead(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkDataObject> aReturn;
  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (reader->GetStructuredPointsOutput())
      return (*vtkImageData) (reader->GetStructuredPointsOutput());
    if (reader->GetPolyDataOutput())
      return reader->GetPolyDataOutput();
    if (reader->GetUnstructuredGridOutput())
      return reader->GetUnstructuredGridOutput();

  }
  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    aReturn.TakeReference(reader->GetOutput());
    if (reader->GetImageDataOutput())
      return reader->GetImageDataOutput();
    if (reader->GetPolyDataOutput())
      return reader->GetPolyDataOutput();
    if (reader->GetUnstructuredGridOutput())
      return reader->GetUnstructuredGridOutput();
  }
  throw();
  return 0;
}

*/

} // end namespace MSML

