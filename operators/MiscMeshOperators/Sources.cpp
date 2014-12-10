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

#include "Sources.h"
#include "../vtk6_compat.h"
#include "IOHelper.h"
#include "MiscMeshOperators.h"

#include <vtkSmartPointer.h>
#include <vtkSphereSource.h>
#include <vtkAppendPolyData.h>
#include <vtkVector.h>

namespace MSML {
  namespace Sources 
  {
    const char* GenerateEmptyImage3D(vector<int> dimVec, vector<double> spacingVec, vector<double> originVec, const char* targetImageName)
    {
      vtkSmartPointer<vtkImageData> newVTKImage = vtkSmartPointer<vtkImageData>::New();

      int dims[3] = {dimVec[0], dimVec[1], dimVec[2]};
      double spacing[3] = {spacingVec[0], spacingVec[1], spacingVec[2]};
      double origin[3] = {originVec[0], originVec[1], originVec[2]};


      newVTKImage->SetDimensions(dims);
      newVTKImage->SetOrigin(origin);
      newVTKImage->SetSpacing(spacing);
      newVTKImage->SetExtent(0, dims[0] - 1, 0, dims[1] - 1, 0, dims[2] - 1);

      #if VTK_MAJOR_VERSION <= 5
        newVTKImage->SetNumberOfScalarComponents(1);
        newVTKImage->SetScalarTypeToDouble();
      #else
        newVTKImage->AllocateScalars(VTK_DOUBLE,1);
      #endif
      IOHelper::VTKWriteImage(targetImageName, newVTKImage);
      return targetImageName;
    }

    const char* GenerateSpheres(vector<double> centers, double radius, int thetaResolution, int phiResolution, const char* targetFileName)
    {
      vtkSmartPointer<vtkPolyData> aPoly = GenerateSpheres(centers, radius, thetaResolution, phiResolution);
      IOHelper::VTKWritePolyData(targetFileName, aPoly);
      return targetFileName;
    }

    //Generate sperhes with constant radius but different centers
    vtkSmartPointer<vtkPolyData> GenerateSpheres(vector<double> centers, double radius, int thetaResolution, int phiResolution)
    {
      if (centers.size()%3 !=0)
        throw "GenerateSpheres: vector<double> centers.size() % 3 != 0";

      vtkSmartPointer<vtkAppendPolyData> appendFilter = vtkSmartPointer<vtkAppendPolyData>::New();
      for (int i=0;i<centers.size();i=i+3)
      {
        vtkSmartPointer<vtkSphereSource> currentSphereSource = vtkSmartPointer<vtkSphereSource>::New();
        currentSphereSource->SetCenter(centers.at(i+0), centers.at(i+1), centers.at(i+2));
        currentSphereSource->SetRadius(radius);
        currentSphereSource->Update();
        currentSphereSource->SetThetaResolution(thetaResolution);
        currentSphereSource->SetPhiResolution(phiResolution);
        #if VTK_MAJOR_VERSION <= 5
          appendFilter->AddInputConnection(currentSphereSource->GetProducerPort());
        #else
          appendFilter->AddInputData(currentSphereSource->GetOutput());
        #endif
      }
      appendFilter->Update();
      return appendFilter->GetOutput();
    }
  }
}
