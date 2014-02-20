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

// ****************************************************************************
// Includes
// ****************************************************************************
#include <vector>
#include <limits>

#include <boost/filesystem.hpp>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#include <vtkSmartPointer.h>
#include <vtkGenericDataObjectReader.h>
#include <vtkXMLGenericDataObjectReader.h>
#include <vtkImageReader.h>

#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkImageData.h>


#include "IOHelper.h"
using namespace std;

// ****************************************************************************
// Defines
// ****************************************************************************


// ****************************************************************************
// PostProcessingOperators
// ****************************************************************************




namespace MSML {

vtkSmartPointer<vtkImageData> IOHelper::VTKReadImage(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkDataObject> aReturn;
  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    vtkImageData* aReturn = (vtkImageData*)reader->GetOutput();
    return aReturn;
  }

  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    vtkSmartPointer<vtkImageData> aReturn = reader->GetImageDataOutput();
    return aReturn;
  }
}

vtkSmartPointer<vtkUnstructuredGrid> IOHelper::VTKReadUnstructuredGrid(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkDataObject> aReturn;
  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    return reader->GetUnstructuredGridOutput();
  }

  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    return reader->GetUnstructuredGridOutput();
  }
}

vtkSmartPointer<vtkPolyData> IOHelper::VTKReadPolyData(const char* filename)
{
  boost::filesystem::path filePath(filename);
  vtkSmartPointer<vtkDataObject> aReturn;
  if (filePath.extension().string() == ".vtk") //legacy datat format
  {
    vtkSmartPointer<vtkGenericDataObjectReader > reader = vtkSmartPointer<vtkGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    return reader->GetPolyDataOutput();
  }

  else
  {
    vtkSmartPointer<vtkXMLGenericDataObjectReader > reader = vtkSmartPointer<vtkXMLGenericDataObjectReader >::New();
    reader->SetFileName(filename);
    reader->Update();
    return reader->GetPolyDataOutput();
  }
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

