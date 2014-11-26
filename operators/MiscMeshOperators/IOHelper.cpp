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
#include <boost/graph/adjacency_list.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string.hpp> 
#include <boost/regex.hpp>

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

#include <vtkXMLImageDataWriter.h>
#include <vtkStructuredPointsWriter.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkXMLPolyDataWriter.h>
#include <vtkPolyDataWriter.h>

#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkImageData.h>

#include "MiscMeshOperators.h" //circular, should be refactored
#include "../vtk6_compat.h"
#include "../common/log.h"



#include "IOHelper.h"
using namespace std;

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
      std::istringstream lineStream(line);
      std::string field;
      std::vector<string> fields;
      fields.clear();
      while (getline(lineStream, field, delim)) 
      {
        if (field.size()>0)
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
  vtkSmartPointer<vtkImageData> aReturn;
  if (!boost::filesystem::exists(filePath))
    log_error() << filePath << " was not found." << endl;

  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (!reader->IsFileStructuredPoints())
      log_error() << filePath << " is not an .vtk image." << endl;
    aReturn = (vtkImageData*)reader->GetOutput();
  }
  else if (filePath.extension().string() == ".ctx")
  {
    aReturn = IOHelper::CTXReadImage(filename);
  }

  else if (filePath.extension().string() == ".gz")
  {
    boost::filesystem::path filePath_without_gz(filename);
    filePath_without_gz = filePath_without_gz.replace_extension("");
    string command = "gunzip -c \"" + filePath.string() + "\" >\"" + filePath_without_gz.string() + "\"";
    log_info() << command << std::endl;
    system(command.c_str());    
    aReturn = IOHelper::CTXReadImage(filePath_without_gz.string().c_str());
    boost::filesystem::remove(filePath_without_gz);
  }

  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (!reader->GetImageDataOutput())
      log_error() << filePath << " is not an .vti image." << endl;
    aReturn = reader->GetImageDataOutput();
  }
  return aReturn;
}

vtkSmartPointer<vtkUnstructuredGrid> IOHelper::VTKReadUnstructuredGrid(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkUnstructuredGrid> aReturn;

  if (!boost::filesystem::exists(filePath))
    log_error() << filePath << " was not found." << endl;
  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (!reader->IsFileUnstructuredGrid())
      log_error() << filePath << " is not an .vtk unstructured grid." << endl;
    aReturn = reader->GetUnstructuredGridOutput();
  }
  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (!reader->GetUnstructuredGridOutput() )
      log_error() << filePath << " is not an .vtu unstructured grid." << endl;
    aReturn = reader->GetUnstructuredGridOutput();
  }
  return aReturn;
}

vtkSmartPointer<vtkPolyData> IOHelper::VTKReadPolyData(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkPolyData> aReturn;
  if (!boost::filesystem::exists(filePath))
   log_error() << filePath << " was not found." << endl;

  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();

    if (reader->GetPolyDataOutput())
    {
       aReturn =  reader->GetPolyDataOutput();   
    }

    else 
    {
      log_error() << filePath << " is not a .vtk poly data file. Trying to use MiscMeshOperators::ExtractSurfaceMesh(IOHelper::VTKReadUnstructuredGrid(..)" << endl;
      vtkSmartPointer<vtkPolyData> poly = vtkSmartPointer<vtkPolyData>::New();
      MiscMeshOperators::ExtractSurfaceMesh(IOHelper::VTKReadUnstructuredGrid(filename), poly);
      aReturn = poly;
    }
  }
  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    if (reader->GetPolyDataOutput())
      aReturn =  reader->GetPolyDataOutput();
    else 
    {
      log_error() << filePath << "  is not a .ply poly data grid." << endl;
    }
  }
  return aReturn;
}

bool IOHelper::VTKWriteImage(const char* filename, vtkImageData* image)
{
  return VTKWriteImage(filename, image, false);
}

bool IOHelper::VTKWriteUnstructuredGrid(const char* filename, vtkUnstructuredGrid* grid)
{
  return VTKWriteUnstructuredGrid(filename, grid, false);
}

bool IOHelper::VTKWritePolyData(const char* filename, vtkPolyData* polyData)
{
  return VTKWritePolyData(filename, polyData, false);
}

bool IOHelper::VTKWriteImage(const char* filename, vtkImageData* image, bool asciiMode)
{
  bool aResult=false;
  //check if directory exists.
    boost::filesystem::path filePath(boost::filesystem::absolute(filename));
  if (!boost::filesystem::exists(filePath.parent_path()))
  {
    log_error() << filePath << " can not be written. Directory of" << filePath << " does not exist "<< endl;
  }
  else if (filePath.extension().string() == ".vti")
  {
    vtkSmartPointer<vtkXMLImageDataWriter> writer =  vtkSmartPointer<vtkXMLImageDataWriter>::New();
    writer->SetFileName(filename);
    __SetInput(writer, image);
    if (asciiMode)
    {
      writer->SetCompressorTypeToNone();
      writer->SetDataModeToAscii();
    }
    else
    {
      writer->SetCompressorTypeToZLib();
      writer->SetDataModeToBinary();
    }
    aResult = writer->Write() == 0; 
  }
  else 
  {
    if (filePath.extension().string() != ".vtk")
      log_error() << filePath.extension().string() << " is an unknown file extension for images. Fallback solution, the images is stored in vtk legacy format." << endl;
    
    vtkSmartPointer<vtkStructuredPointsWriter> writer =  vtkSmartPointer<vtkStructuredPointsWriter>::New();
    writer->SetFileName(filename);
    __SetInput(writer, image);
    if (asciiMode)
    {
      writer->SetFileTypeToASCII();
    }
    else
    {
      writer->SetFileTypeToBinary();
    }
    aResult = writer->Write() == 0; 
  }

  return aResult;
}

bool IOHelper::VTKWriteUnstructuredGrid(const char* filename, vtkUnstructuredGrid* grid, bool asciiMode)
{
  bool aResult=false;
  //check if directory exists.
  boost::filesystem::path filePath(boost::filesystem::absolute(filename));
  if (!boost::filesystem::exists(filePath.parent_path()))
  {
    log_error() << filePath << " can not be written. Directory of " << filePath << " does not exist "<< endl;
  }
  else if (filePath.extension().string() == ".vtu")
  {
    vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer =  vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New();
    writer->SetFileName(filename);
    __SetInput(writer, grid);
    if (asciiMode)
    {
      writer->SetCompressorTypeToNone();
      writer->SetDataModeToAscii();
    }
    else
    {
      writer->SetCompressorTypeToZLib();
      writer->SetDataModeToBinary();
    }
    aResult = writer->Write() == 0; 
  }
  else 
  {
    if (filePath.extension().string() != ".vtk")
      log_error() << filePath.extension().string() << " is an unknown file extension for UnstructuredGrid. Fallback solution, the UnstructuredGrid is stored in vtk legacy format." << endl;
    
    vtkSmartPointer<vtkUnstructuredGridWriter> writer =  vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    writer->SetFileName(filename);
    __SetInput(writer, grid);
    if (asciiMode)
    {
      writer->SetFileTypeToASCII();
    }
    else
    {
      writer->SetFileTypeToBinary();
    }
    aResult = writer->Write() == 0; 
  }

  return aResult;
}

bool IOHelper::VTKWritePolyData(const char* filename, vtkPolyData* polyData, bool asciiMode)
{
  bool aResult=false;
  //check if directory exists.
  boost::filesystem::path filePath(boost::filesystem::absolute(filename));
  if (!boost::filesystem::exists(filePath.parent_path()))
  {
    log_error() << filePath << " can not be written. Directory of " << filePath << " does not exist "<< endl;
  }
  else if (filePath.extension().string() == ".vtp")
  {
    vtkSmartPointer<vtkXMLPolyDataWriter> writer =  vtkSmartPointer<vtkXMLPolyDataWriter>::New();
    writer->SetFileName(filename);
    __SetInput(writer, polyData);
    if (asciiMode)
    {
      writer->SetCompressorTypeToNone();
      writer->SetDataModeToAscii();
    }
    else
    {
      writer->SetCompressorTypeToZLib();
      writer->SetDataModeToBinary();
    }
    aResult = writer->Write() == 0; 
  }
  else 
  {
    if (filePath.extension().string() != ".vtk")
      log_error() << filePath.extension().string() << " is an unknown file extension for polydata. Fallback solution, the polydata is stored in vtk legacy format." << endl;
    
    vtkSmartPointer<vtkPolyDataWriter> writer =  vtkSmartPointer<vtkPolyDataWriter>::New();
    writer->SetFileName(filename);
    __SetInput(writer, polyData);
    if (asciiMode)
    {
      writer->SetFileTypeToASCII();
    }
    else
    {
      writer->SetFileTypeToBinary();
    }
    aResult = writer->Write() == 0; 
  }

  return aResult;
}




//find all files with the same name (without digit postfix) and any digit postfix.
//TODO: move to Python
vector<pair<int, string> >* IOHelper::getAllFilesOfSeries(const char* filename)
{
    vector<pair<int, string> >* aReturn = new vector<pair<int, string> >();
    boost::filesystem::path aPath(boost::filesystem::absolute(filename));
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

std::vector< std::string > IOHelper::getAllFilesByMask(const char* filename)
{
  boost::filesystem::path aPath(filename);

  std::vector< std::string > all_matching_files;

  // check if parent directory exists, should fix:
  // https://github.com/CognitionGuidedSurgery/msml/issues/148
  if( ! boost::filesystem::exists( aPath.parent_path() )) {
      return all_matching_files;
  }

  std::string target_path( aPath.parent_path().string() );
  std::string filter =  aPath.filename().string();
  boost::replace_all(filter, "*", ".*\\");

  const boost::regex my_filter( filter );



  boost::filesystem::directory_iterator end_itr; // Default ctor yields past-the-end
  for( boost::filesystem::directory_iterator i( target_path ); i != end_itr; ++i )
  {
      // Skip if not a file
      if( !boost::filesystem::is_regular_file( i->status() ) ) continue;

      boost::smatch what;

      // Skip if no match
      if( !boost::regex_match( i->path().filename().string(), what, my_filter ) ) continue;

      // File matches, store it
      all_matching_files.push_back( i->path().string() );
  }
  return all_matching_files;
}


} // end namespace MSML

