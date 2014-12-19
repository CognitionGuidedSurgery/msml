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
//modified example from: http://www.vtk.org/Wiki/VTK/Examples/Cxx/Medical/GenerateModelsFromLabels TODO: update this with correct link!
// Surface2VoxelsOperator
// reads in a PolyData File and converts it to an image.
//   Usage: Surface2VoxelsOperator InputSurfaceSegmentation.vtk OutputVTKImage.vti AccuracyLevel Smoothing
//          where
//          InputSurfaceSegmentation: is a vtkPolyData (.vtk) representing the segmentation.
//          OutputVTKImage: is the vtkImage (.vti) representing the segmentation;
//             it contains non-zero values at the points of the PolyData Surface.
//          AccuracyLevel: a scalar value, represents the resolution of the image (affects computational costs);
//             reasonable range: 1 - 10 (e.g. default: 8).
//          Smoothing: a scalar value, represents the Gaussian filter applied to broaden the non-zero values;
//             reasonable range: 1 - 10 (e.g. default: 2).
//          NOTE: The PolyData File has to consist of surface triangles.
// 

#include <SurfaceToVoxelDataOperator.h>
#include <MiscMeshOperators.h>
#include <vtkMetaImageReader.h>
#include <vtkImageData.h>
#include <vtkPointData.h>
#include <IOHelper.h>

#include <vtkVersion.h>
#include <vtkSmartPointer.h>
#include <vtkCellArray.h>
#include <vtkCell.h>
#include <vtkIdList.h>
#include <vtkSphereSource.h>
#include <vtkXMLImageDataWriter.h>
#include <vtkXMLPolyDataReader.h>
#include <vtkSTLReader.h>
#include <vtkDataSet.h>
#include <vtkImageGaussianSmooth.h>
#include <vtksys/SystemTools.hxx>

#include "../vtk6_compat.h"

namespace MSML
{
  namespace SurfaceToVoxelDataOperator
  {
	  
  std::string SurfaceToVoxelDataOperator(const char* infile, const char* outfile, float accuracy_level, float smoothing)
  {
    vtkSmartPointer<vtkPolyData> pd = IOHelper::VTKReadPolyData(infile);
    // Note: vtp (PolyData) as input required; if necessary use MSML STL2VTK-Converter.
    
    
    vtkSmartPointer<vtkImageData> image = MiscMeshOperators::ImageCreateWithMesh(pd, 100);
    MiscMeshOperators::ImageEnlargeIsotropic(image, 20.0); // adding marginExtension, cp. ImageCreator.
    // Note: this is properly tuned only for the mitral valve.
    
    float ref_fac = accuracy_level;
    float smooth_size = smoothing;
    
    const unsigned int zero_val = 0;
    const unsigned int non_zero_val = 1000;
    
    const int numberOfCells  = pd->GetNumberOfCells();
	const int numberOfPoints = pd->GetNumberOfPoints();

	// Print information on polydata
	std::cout << "The input data contains a "
			      << pd->GetClassName()
			      << " that has "    << numberOfCells  << " cells"
			      << " and "            << numberOfPoints << " points." << std::endl;
    
    double av_length = computeAvLengthCount(pd);
    
  	const double ispacing = av_length / ref_fac;

    // Datatype
#if VTK_MAJOR_VERSION <= 5
	image->SetScalarTypeToUnsignedInt();
	image->AllocateScalars();
#else
	image->AllocateScalars(VTK_UNSIGNED_INT,1);
#endif

    // Default values
	vtkIdType numIpoints = image->GetNumberOfPoints();
	for (vtkIdType i = 0; i < numIpoints; ++i)	{
		image->GetPointData()->GetScalars()->SetTuple1(i, zero_val);
	}

	// statistics
	unsigned long mem_size = image->GetActualMemorySize();
	vtkIdType iCells =         image->GetNumberOfCells();
	vtkIdType iPoints =        image->GetNumberOfPoints();
	double* iBounds =         image->GetBounds();
	double* iSpacings =       image->GetSpacing();
	double* iOrigin =         image->GetOrigin();
	int* iDim =               image->GetDimensions();

	// Print information on image
	std::cout << "Properties of the image:"       << std::endl;
	std::cout << "Cells:         "  << iCells     << std::endl;
	std::cout << "Points:        "  << iPoints    << std::endl;
	std::cout << "Mem size [kB]: "  << mem_size   << std::endl;
	std::cout << "Origin:        [" << iOrigin[0] << ", " << iOrigin[1]  << ", " << iOrigin[2] << "]" << std::endl;
	std::cout << "Extent:        [" << iBounds[0] << ","  << iBounds[1] << "]"
			                  << " x [" << iBounds[2] << ","  << iBounds[2] << "]"
			                  << " x [" << iBounds[4] << ","  << iBounds[5] << "]"  << std::endl;
	std::cout << "Spacing:       "  << ispacing   << std::endl;
	std::cout << "Dimensions     "  << iDim[0]    << ", " << iDim[1] << ", " << iDim[2] << std::endl;
    std::cout << std::endl;
    
  // ************************************************
  // Map poly data into image
  // ************************************************
	int poly_count = 0;
	double av_int = 0;
    // Iterate polydata
    pd->GetPolys()->InitTraversal();
    vtkSmartPointer<vtkIdList> idList = vtkSmartPointer<vtkIdList>::New();
	while(pd->GetPolys()->GetNextCell(idList))	{
		if(idList->GetNumberOfIds() == 3) {
		  // Get the three points (A,B,C) of the poly data cell
			double p[3][3];
			for(vtkIdType pointId = 0; pointId < idList->GetNumberOfIds(); pointId++)
			{
				double * point = pd->GetPoint(idList->GetId(pointId));
				for(int d = 0; d < 3; ++d){
					p[pointId][d] = point[d];
				}
			}
			// Compute vectors A to B and A to C and their length
			double a2b[3];
			double a2c[3];
			double length_b = 0;
			double length_c = 0;
			for(int dim = 0; dim < 3; ++dim){
				a2b[dim] = p[1][dim]-p[0][dim];
				a2c[dim] = p[2][dim]-p[0][dim];
				length_b += a2b[dim]*a2b[dim];
				length_c += a2c[dim]*a2c[dim];
			}
			length_b = sqrt(length_b);
			length_c = sqrt(length_c);
			// Determine accuracy
			int num_intervalls = std::max(1.,2*(length_b + length_c)/ispacing);
			av_int += num_intervalls;
			double intervall_b = length_b / num_intervalls;
			double intervall_c = length_c / num_intervalls;
			// Take a distribution of points in the triangle
			for(int s = 0; s <= num_intervalls; ++s){
				for(int t = 0; t <= num_intervalls - s; ++t){
					double tri_point[3];
					for(int dim = 0; dim < 3; ++dim){
						tri_point[dim] = p[0][dim] + s*intervall_b*a2b[dim]/length_b + t*intervall_c*a2c[dim]/length_c;
					}
					// Find the next image point of the triangle point
					vtkIdType pd_point = image->FindPoint(tri_point);
					if(pd_point >= 0){
					  // Mark the detected image point
						image->GetPointData()->GetScalars()->SetComponent(pd_point,0,non_zero_val);
					}
				}
			}
		}
		++poly_count;
	}
	av_int /= poly_count;
	std::cout << "Average number of points per cell mapped to image : " << av_int*(av_int+1.)/2. << std::endl;
    std::cout << std::endl;

	// ************************************************
    // Smooth the image
    // ************************************************
	vtkSmartPointer<vtkImageGaussianSmooth> smoother = vtkSmartPointer<vtkImageGaussianSmooth>::New(); // NEW.
#if VTK_MAJOR_VERSION <= 5
	smoother->SetInput(image); // NEW.
#else
	smoother->SetInputData(image); // NEW.
#endif
	smoother->SetStandardDeviation(smooth_size); // NEW.
	smoother->Update(); // NEW.

    //IOHelper::VTKWriteImage(outfile, image);  // OLD.
    IOHelper::VTKWriteImage(outfile, smoother->GetOutput()); // NEW.

    return outfile;
  }
  
  double computeAvLengthCount(vtkSmartPointer<vtkPolyData> pd) {
	  int edge_counter = 0;
	  double av_length = 0;
      // Iterate cells
	  pd->GetPolys()->InitTraversal();
	  vtkSmartPointer<vtkIdList> idList = vtkSmartPointer<vtkIdList>::New();
	  while(pd->GetPolys()->GetNextCell(idList))	{
		if(idList->GetNumberOfIds() != 3) {
	    std::cerr << "Error: Only triangle poly data is supported." << std::endl;
	    return EXIT_FAILURE;
		}
		  // Get two vertices of the cell
			double p[2][3];
			for(int pointId = 0; pointId < 2; pointId++) {
				double* point = pd->GetPoint(idList->GetId(pointId));
				for(int d = 0; d < 3; ++d) {
					p[pointId][d] = point[d];
				}
			}
			double length = 0;
			for(int dim = 0; dim < 3; ++dim){
			  length += (p[1][dim]-p[0][dim]) * (p[1][dim]-p[0][dim]);
			}
			av_length += sqrt(length);
			++edge_counter;
	  }
	  av_length /= (double) edge_counter;
	  
	  return av_length;
  }
  }
}
