/*  =========================================================================

    Program:   The Medical Simulation Markup Language
    Module:    Operators, MiscMeshOperators
    Authors:   Markus Stoll, Stefan Suwelack, Nicolai Schoch

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
//modified example from: http://www.vtk.org/Wiki/VTK/Examples/Cxx/Medical/GenerateModelsFromLabels
// GenerateModelsFromLabels
//   Usage: GenerateModelsFromLabels InputVolume Startlabel Endlabel
//          where
//          InputVolume is a meta file containing a 3 volume of
//            discrete labels.
//          StartLabel is the first label to be processed
//          EndLabel is the last label to be processed
//          NOTE: There can be gaps in the labeling. If a label does
//          not exist in the volume, it will be skipped.
//      
//

#include <vtkMetaImageReader.h>
#include <vtkImageAccumulate.h>
#include <vtkDiscreteMarchingCubes.h>
#include <vtkWindowedSincPolyDataFilter.h>
#include <vtkMaskFields.h>
#include <vtkThreshold.h>
#include <vtkGeometryFilter.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkAppendFilter.h>
 
#include <vtkImageData.h>
#include <vtkPointData.h>
#include <vtkUnstructuredGrid.h>
#include <vtkAppendFilter.h>
#include <vtksys/ios/sstream>
#include <IOHelper.h>
#include <VTKMeshgen.h>
namespace MSML
{
  namespace VTKMeshgen {
    std::string DiscreteMarchingCube(const char* infile, const char* outfile)
    {
 
    // Create all of the classes we will need
    vtkSmartPointer<vtkImageData> imageIn = IOHelper::VTKReadImage(infile);
    vtkSmartPointer<vtkImageAccumulate> histogram = vtkSmartPointer<vtkImageAccumulate>::New();
    vtkSmartPointer<vtkDiscreteMarchingCubes> discreteCubes = vtkSmartPointer<vtkDiscreteMarchingCubes>::New();
    vtkSmartPointer<vtkWindowedSincPolyDataFilter> smoother = vtkSmartPointer<vtkWindowedSincPolyDataFilter>::New();
    vtkSmartPointer<vtkThreshold> selector = vtkSmartPointer<vtkThreshold>::New();
    vtkSmartPointer<vtkMaskFields> scalarsOff = vtkSmartPointer<vtkMaskFields>::New();
    vtkSmartPointer<vtkGeometryFilter> geometry = vtkSmartPointer<vtkGeometryFilter>::New();
    vtkSmartPointer<vtkAppendFilter> appendFilter = vtkSmartPointer<vtkAppendFilter>::New(); //polydata to vtu
    vtkSmartPointer<vtkUnstructuredGridWriter> writer = vtkSmartPointer<vtkUnstructuredGridWriter>::New();

    vtkSmartPointer<vtkAppendFilter> appendFilterSingleFile = vtkSmartPointer<vtkAppendFilter>::New();
    vtkSmartPointer<vtkUnstructuredGridWriter> writerSingleFile = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
 
    // Define all of the variables
    unsigned int startLabel = atoi("0");
    unsigned int endLabel = atoi("25");
    unsigned int smoothingIterations = 15;
    double passBand = 0.001;
    double featureAngle = 120.0;
 
    // Generate models from labels
    // 1) Read the meta file
    // 2) Generate a histogram of the labels
    // 3) Generate models from the labeled volume
    // 4) Smooth the models
    // 5) Output each model into a separate file
 

 
    histogram->SetInput(imageIn);
    histogram->SetComponentExtent(0, endLabel, 0, 0, 0, 0);
    histogram->SetComponentOrigin(0, 0, 0);
    histogram->SetComponentSpacing(1, 1, 1);
    histogram->Update();
 
    discreteCubes->SetInput(imageIn);
    discreteCubes->GenerateValues(endLabel - startLabel + 1, startLabel, endLabel);
 
    smoother->SetInputConnection(discreteCubes->GetOutputPort());
    smoother->SetNumberOfIterations(smoothingIterations);
    smoother->BoundarySmoothingOff();
    smoother->FeatureEdgeSmoothingOff();
    smoother->SetFeatureAngle(featureAngle);
    smoother->SetPassBand(passBand);
    smoother->NonManifoldSmoothingOn();
    smoother->NormalizeCoordinatesOn();
    smoother->Update();
 
    selector->SetInputConnection(smoother->GetOutputPort());
    selector->SetInputArrayToProcess(0, 0, 0,
                                     vtkDataObject::FIELD_ASSOCIATION_CELLS,
                                     vtkDataSetAttributes::SCALARS);
 
    // Strip the scalars from the output
    scalarsOff->SetInputConnection(selector->GetOutputPort());
    scalarsOff->CopyAttributeOff(vtkMaskFields::POINT_DATA,
                                 vtkDataSetAttributes::SCALARS);
    scalarsOff->CopyAttributeOff(vtkMaskFields::CELL_DATA,
                                 vtkDataSetAttributes::SCALARS);
 
    geometry->SetInputConnection(scalarsOff->GetOutputPort());
    #if VTK_MAJOR_VERSION <= 5
      appendFilter->AddInput(geometry->GetOutput());
      appendFilterSingleFile->AddInput(smoother->GetOutput());
    #else
      appendFilter->AddInputData(geometry->GetOutput());
      appendFilterSingleFile->AddInputData(smoother->GetOutput());
    #endif
    appendFilter->Update();

    writer->SetInputConnection(appendFilter->GetOutputPort());
    writerSingleFile->SetInputConnection(appendFilterSingleFile->GetOutputPort());
    vtksys_stl::stringstream ss;
    ss << outfile << "all" << ".vtk";
    writerSingleFile->SetFileName(ss.str().c_str());
    writerSingleFile->Write();

    for (unsigned int i = startLabel; i <= endLabel; i++)
    {
      // see if the label exists, if not skip it
      double frequency =
        histogram->GetOutput()->GetPointData()->GetScalars()->GetTuple1(i);
      if (frequency == 0.0)
        {
        continue;
        }
 
      // select the cells for a given label
      selector->ThresholdBetween(i, i);
 
      // output the polydata
      ss << outfile << i << ".vtk";

 
      writer->SetFileName(ss.str().c_str());
      writer->Write();
      }
    return outfile;
  }

  std::string MarchingCube(const char* infile, const char* outfile, float isoValue)
  {
    vtkSmartPointer<vtkImageData> imageIn = IOHelper::VTKReadImage(infile);
    vtkSmartPointer<vtkMarchingCubes> surface = vtkSmartPointer<vtkMarchingCubes>::New();
    #if VTK_MAJOR_VERSION <= 5
      surface->SetInput(imageIn);
    #else
      surface->SetInputData(volume);
    #endif
    surface->ComputeNormalsOn();
    surface->SetValue(0, isoValue);

    vtkSmartPointer<vtkWindowedSincPolyDataFilter> smoother = vtkSmartPointer<vtkWindowedSincPolyDataFilter>::New();
    unsigned int smoothingIterations = 15;
    double passBand = 0.001;
    double featureAngle = 120.0;
    smoother->SetInputConnection(surface->GetOutputPort());
    smoother->SetNumberOfIterations(smoothingIterations);
    smoother->BoundarySmoothingOff();
    smoother->FeatureEdgeSmoothingOff();
    smoother->SetFeatureAngle(featureAngle);
    smoother->SetPassBand(passBand);
    smoother->NonManifoldSmoothingOn();
    smoother->NormalizeCoordinatesOn();
    smoother->Update();

    vtkSmartPointer<vtkAppendFilter> appendFilter = vtkSmartPointer<vtkAppendFilter>::New();
    #if VTK_MAJOR_VERSION <= 5
      appendFilter->AddInput(smoother->GetOutput());
    #else
      appendFilter->AddInputData(geometry->GetOutput());
    #endif
    appendFilter->Update();

    vtkSmartPointer<vtkUnstructuredGridWriter> writer = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    writer->SetInputConnection(appendFilter->GetOutputPort());
    writer->SetFileName(outfile);
    writer->Write();

    return outfile;
  }
  }
}