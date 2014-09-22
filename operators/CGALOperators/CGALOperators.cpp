/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, CGALOperators
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

#include <map>
#include <assert.h>

//CGAL Includes:
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Mesh_triangulation_3.h>
#include <CGAL/Mesh_complex_3_in_triangulation_3.h>
#include <CGAL/Mesh_criteria_3.h>
#include <CGAL/Polyhedral_mesh_domain_3.h>
#include <CGAL/make_mesh_3.h>
#include <CGAL/refine_mesh_3.h>
#include <CGAL/Image_3.h>
#include <CGAL/Labeled_image_mesh_domain_3.h>

// IO
#include <CGAL/IO/Polyhedron_iostream.h>



//Polyhedral domain:
// Domain poly
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Polyhedron_3<K> Polyhedron;
typedef CGAL::Polyhedral_mesh_domain_3<Polyhedron, K> Mesh_domain_poly;
// Triangulation poly
typedef CGAL::Mesh_triangulation_3<Mesh_domain_poly>::type Tr_poly;
typedef CGAL::Mesh_complex_3_in_triangulation_3<Tr_poly> C3t3_poly;
// Criteria poly
typedef CGAL::Mesh_criteria_3<Tr_poly> Mesh_criteria_poly;

//Labled image domain
// Domain lable
typedef CGAL::Labeled_image_mesh_domain_3<CGAL::Image_3,K> Mesh_domain_img; //the third type parameter could allow to change image data type. More than 255 segmentation classes may be possible.
// Triangulation
typedef CGAL::Mesh_triangulation_3<Mesh_domain_img>::type Tr_img;
typedef CGAL::Mesh_complex_3_in_triangulation_3<Tr_img> C3t3_img;
// Criteria
typedef CGAL::Mesh_criteria_3<Tr_img> Mesh_criteria_img;

// To avoid verbose function and named parameters call
using namespace CGAL::parameters;

//VTK includes
#include <vtkXMLGenericDataObjectReader.h>
#include <vtkGenericDataObjectReader.h>
#include <vtkPolyData.h>
#include <vtkTetra.h>
#include <vtkCellArray.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkPolyDataReader.h>
#include <vtkImageReader.h>
#include <vtkImageData.h>
#include <vtkXMLImageDataReader.h>
#include <vtkImageCast.h>
#include <vtkDataArray.h>
#include <vtkPointData.h>
#include <vtkTransformFilter.h>
#include <vtkTransform.h>


//MSML includes
#include "MiscMeshOperators.h"
#include "IOHelper.h"

//local includes
#include "CGALOperators.h"
#include "cgal_tet_to_vtk.h"
#include "../vtk6_compat.h"



namespace MSML{
    namespace CGALOperators {
    //local helper methods
  CGAL::Image_3 read_vtk_image_data_char(vtkImageData* vtk_image);
  C3t3_poly mesh_polyhedral_Domain(Polyhedron thePolyhedron,
                                   bool thePreserveFeatures, double theFacetAngle,
                                   double theFacetSize, double theFacetDistance,
                                   double theCellRadiusEdgeRatio, double theCellSize,
                                   bool theOdtSmoother, bool theLloydSmoother,
                                   bool thePerturber, bool theExuder);

    C3t3_img mesh_image_domain(CGAL::Image_3 theImage, double theFacetAngle, double theFacetSize, double theFacetDistance,
                               double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder);
    Polyhedron OpenOffSurface(const char* infile_off);
    map<int,int>*  CompressImageData(vtkImageData* theImageData);


  std::string CreateVolumeMeshi2v(const char* infile, const char* outfile, double theFacetAngle, double theFacetSize, double theFacetDistance,
     double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder)
  {
    vtkSmartPointer<vtkImageData> imageIn = IOHelper::VTKReadImage(infile);
    vtkSmartPointer<vtkImageData> image_compact = vtkSmartPointer<vtkImageData>::New();
    image_compact->DeepCopy(imageIn);

    //compress pixel values to [0...255]. (CGAL seems to need unsigned char) - more than 255 difference segmentation classes are supported.
    map<int,int>* aLUT = CompressImageData(image_compact);

    //cast image pixel data array to unsigned char
    vtkSmartPointer<vtkImageCast > image_caster = vtkSmartPointer<vtkImageCast>::New();
    __SetInput(image_caster, image_compact);
    image_caster->SetOutputScalarTypeToUnsignedChar();
    image_caster->Update();
    vtkSmartPointer<vtkImageData > image_data_byte =  image_caster->GetOutput();
#if VTK_MAJOR_VERSION <= 5
    image_data_byte->SetScalarTypeToUnsignedChar(); //does not work as expected. read_vtk_image_data will find double in image_data_byte->GetScalarType()
#else
    image_data_byte->AllocateScalars(VTK_UNSIGNED_CHAR,3);
#endif
    //convert vtk image to INRIA Image_3 and mesh it.
    CGAL::Image_3 image = read_vtk_image_data_char(image_data_byte);
    //image.read_vtk_image_data(image_data_byte); //read_vtk_image_data is undocumented (see http://cgal-discuss.949826.n4.nabble.com/VTK-support-td2531799.html)
    C3t3_img c3t3 = mesh_image_domain(image, theFacetAngle, theFacetSize, theFacetDistance, theCellRadiusEdgeRatio, theCellSize, theOdtSmoother, theLloydSmoother, thePerturber, theExuder);

    // Debug Output - MEDIT .msh format.
	  //std::ofstream medit_file("E:\\GIT\\msml\\Testdatadebug_out_medit.msh");
	  //c3t3.output_to_medit(medit_file);
	  //medit_file.close();

    //convert "cgals mesh cube" to "vtk unsructured grid" and translate grid to image origin.
    vtkUnstructuredGrid* outputMesh = vtkUnstructuredGrid::New();
    output_c3t3_to_vtk_unstructured_grid(c3t3, outputMesh);
    vtkSmartPointer<vtkTransform> transform = vtkSmartPointer<vtkTransform>::New();
    transform->Translate( image_compact->GetOrigin() );
    vtkSmartPointer<vtkTransformFilter> transformFilter = vtkSmartPointer<vtkTransformFilter>::New();
    __SetInput(transformFilter, outputMesh);
    transformFilter->SetTransform(transform);
    transformFilter->Update();
    outputMesh = (vtkUnstructuredGrid*) transformFilter->GetOutput();


    //check if any materials were removed
    map<int,int>* hist_img = MiscMeshOperators::createHist(image_data_byte->GetPointData()->GetScalars());
    map<int,int>*  hist_cells = MiscMeshOperators::createHist(outputMesh->GetCellData()->GetScalars());

    int countOfRemoved = hist_img->size()-1 - hist_cells->size();

    //If materials were removed guess which and adapt the LUT.
    for (int i=0; i<countOfRemoved; i++)
    {
      //find index of rarest pixel value
      int aMinKey = hist_img->begin()->first;
      for (map<int,int>::iterator it = hist_img->begin(); it!=hist_img->end(); it++)
      {
        if (it->second < hist_img->at(aMinKey))
        {
          aMinKey = it->first;
        }
      }
      hist_img->erase(aMinKey); //dont find the minimum again

      hist_cells->erase(aMinKey); //remove entry for material, which has not created any cells.
      //adapt all entries.
      for (map<int,int>::iterator it = hist_img->begin(); it!=hist_img->end(); it++)
      {
        if (it->first >= aMinKey)
        {
          it->second = it->second -1;
        }
      }
      cout << "Warning: CGAL generated cells of less material types than the image input. I guess image material of index=" <<
        aLUT->at(aMinKey) <<" did not create any cells. The LUT was adpated." << std::endl;
    }

    //replace the reduced material values using the LUT
    vtkDataArray* pd = outputMesh->GetCellData()->GetScalars();
    for (int i=0; i<pd->GetNumberOfTuples();i++)
    {
      double* key = pd->GetTuple(i);
      float value = aLUT->at((int) *key);
      pd->SetTuple(i,  &value);
    }

    //write vtk
    vtkSmartPointer<vtkUnstructuredGridWriter > aVtkUnstructuredGridWriter =
	  vtkSmartPointer<vtkUnstructuredGridWriter >::New();
    string tmp_file = string(outfile);
	  aVtkUnstructuredGridWriter->SetFileName(tmp_file.c_str());
	  __SetInput(aVtkUnstructuredGridWriter, outputMesh);
	  aVtkUnstructuredGridWriter->Write();


    return outfile;
  }

  map<int,int>* CompressImageData(vtkImageData* theImageData)
  {
    map<int,int>*   hist = MiscMeshOperators::createHist(theImageData->GetPointData()->GetScalars());

    if (hist->size() >= 253)
    {
      cout << "Error: Too many image value classes for unsigned char representation";
      exit(2);
    }

    //generate replacements LUT
    map<int,int>*  inverseLUT = new map<int,int>();
    map<int,int>*  aLUT = new map<int,int>();
    int counter = 0; //replacement image values 0...253
    for (map<int,int>::iterator it = hist->begin(); it!=hist->end(); it++) //iterates in order std::less<Key>
    {
      inverseLUT->insert(pair<int,int>(it->first,counter));//    old_value => new_value
      aLUT->insert(pair<int,int>(counter, it->first));  //new_Value => old_value
      counter++;
    }

    if (counter <= 1)
    {
      cout << "Error: The image has the same value in each voxel.";
      exit(2);
    }

    //Use LUT the replace values in the image
    vtkDataArray* pd = theImageData->GetPointData()->GetScalars();
    for (int i=0; i<pd->GetNumberOfTuples();i++)
    {
      double* value = pd->GetTuple(i);
      float key = inverseLUT->at(*value);
      pd->SetTuple(i,  &key);
    }
    return aLUT;
  }


  C3t3_img mesh_image_domain(CGAL::Image_3 theImage, double theFacetAngle, double theFacetSize, double theFacetDistance,
    double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder)
  {
    assert(theFacetAngle<=30);
    assert(theCellRadiusEdgeRatio>2);

    CGAL::parameters::internal::Features_options featuresParameter=no_features();

    CGAL::parameters::internal::Odt_options odtParameter = 0;
    if (theOdtSmoother)
      odtParameter=odt();
    else
      odtParameter=no_odt();

    CGAL::parameters::internal::Lloyd_options LloydParameter=0;
    if (theLloydSmoother)
      LloydParameter=lloyd();
    else
      LloydParameter=no_lloyd();

    CGAL::parameters::internal::Perturb_options PertubeParameter=0;
    if (thePerturber)
      PertubeParameter=perturb();
    else
      PertubeParameter=no_perturb();

    CGAL::parameters::internal::Exude_options ExudeParameter = 0;
    if (theExuder)
      ExudeParameter=exude();
    else
      ExudeParameter=no_exude();

    CGAL::Labeled_image_mesh_domain_3<CGAL::Image_3,K> domain(theImage);
    //Mesh_criteria_img criteria(facet_angle=20, facet_size=10, facet_distance=6,
       //                  cell_radius_edge_ratio=theCellRadiusEdgeRatio, cell_size=14);
    Mesh_criteria_img criteria(facet_angle=theFacetAngle, facet_size=theFacetSize, facet_distance=theFacetDistance,
                        cell_radius_edge_ratio=theCellRadiusEdgeRatio, cell_size=theCellSize);
    C3t3_img c3t3 = CGAL::make_mesh_3<C3t3_img>(domain, criteria, featuresParameter, odtParameter, PertubeParameter, ExudeParameter);
	  return c3t3;
  }



  /// <summary>
  /// Creates the volume mesh.
  /// </summary>
  /// <param name="infile">The infile.</param>
  /// <param name="outfile">The outfile.</param>
  /// <param name="preserveBoundary">The preserve boundary.</param>
  /// <returns></returns>
  std::string CreateVolumeMeshs2v(const char* infile, const char* outfile, bool thePreserveFeatures, double theFacetAngle, double theFacetSize, double theFacetDistance,
        double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder)
  {

	  std::cout<<" Calling CGAL Mesher with infile "<<infile<<" and outfile "<<outfile<<"\n";

    //read VTK Polydata
    vtkSmartPointer<vtkPolyDataReader> reader = vtkSmartPointer<vtkPolyDataReader>::New();
	  reader->SetFileName(infile);
	  reader->Update();

    //mesh polydata->vtu
    vtkUnstructuredGrid* outputMesh = vtkUnstructuredGrid::New();
    string errorMessage;
    MiscMeshOperators::ConvertVTKToOFF(reader->GetOutput(), "CreateVolumeMeshs2v__TEMP.off");
    C3t3_poly c3t3 = mesh_polyhedral_Domain(OpenOffSurface("CreateVolumeMeshs2v__TEMP.off"), thePreserveFeatures, theFacetAngle, theFacetSize, theFacetDistance,
      theCellRadiusEdgeRatio, theCellSize, theOdtSmoother, theLloydSmoother, thePerturber, theExuder);
    output_c3t3_to_vtk_unstructured_grid(c3t3, outputMesh);
    remove("CreateVolumeMeshs2v__TEMP.off");

    //write vtu
    vtkSmartPointer<vtkUnstructuredGridWriter > aVtkUnstructuredGridWriter =
	  vtkSmartPointer<vtkUnstructuredGridWriter >::New();
	  aVtkUnstructuredGridWriter->SetFileName(outfile);
	  __SetInput(aVtkUnstructuredGridWriter, outputMesh);
	  aVtkUnstructuredGridWriter->Write();
    return outfile;
  }

  Polyhedron OpenOffSurface(const char* infile_off)
	{
	  // Create input polyhedron
	  Polyhedron polyhedron;
	  std::ifstream input(infile_off);
	  input >> polyhedron;
    return polyhedron;
  }


  C3t3_poly mesh_polyhedral_Domain(Polyhedron thePolyhedron, bool thePreserveFeatures, double theFacetAngle, double theFacetSize, double theFacetDistance,
     double theCellRadiusEdgeRatio, double theCellSize, bool theOdtSmoother, bool theLloydSmoother, bool thePerturber, bool theExuder)
	{
	  assert(theFacetAngle<=30);
    assert(theCellRadiusEdgeRatio>2);

    CGAL::parameters::internal::Features_options featuresParameter = no_features();
    if (thePreserveFeatures)
      featuresParameter=features();

    CGAL::parameters::internal::Odt_options odtParameter = no_odt();
    if (theOdtSmoother)
      odtParameter=odt();

    CGAL::parameters::internal::Lloyd_options LloydParameter=no_lloyd();
    if (theLloydSmoother)
      LloydParameter=lloyd();

    CGAL::parameters::internal::Perturb_options PertubeParameter = no_perturb();
    if (thePerturber)
      PertubeParameter=perturb();

    CGAL::parameters::internal::Exude_options ExudeParameter = no_exude();
    if (theExuder)
      ExudeParameter=exude();

    CGAL::Polyhedral_mesh_domain_3<Polyhedron, K> domain(thePolyhedron);

	  Mesh_criteria_poly criteria(facet_angle=theFacetAngle, facet_size=theFacetSize, facet_distance=theFacetDistance,
							 cell_radius_edge_ratio=theCellRadiusEdgeRatio, cell_size=theCellSize);
	  C3t3_poly c3t3 = CGAL::make_mesh_3<C3t3_poly>(domain, criteria, featuresParameter, odtParameter, LloydParameter, PertubeParameter, ExudeParameter);

    return c3t3;
	}

//     taken form CGAL 4.1 Image_3, adapted by ms.
//
// Copyright (c) 2005-2008  INRIA Sophia-Antipolis (France).
//               2008 GeometryFactory, Sophia Antipolis (France)
// All rights reserved.
//
// This file is part of CGAL (www.cgal.org); you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License as
// published by the Free Software Foundation; either version 3 of the License,
// or (at your option) any later version.
//
// Licensees holding a valid commercial license may use this file in
// accordance with the commercial license agreement provided with the software.
//
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
//
// $URL: svn+ssh://scm.gforge.inria.fr/svn/cgal/branches/releases/CGAL-4.1-branch/CGALimageIO/src/CGALImageIO/Image_3.cpp $
// $Id: Image_3.cpp 67093 2012-01-13 11:22:39Z lrineau $
//
// Author(s)     : Laurent Rineau, Pierre Alliez

#include <assert.h>
#include <CGAL/Image_3.h>
#include <CGAL/gl.h>
#include <vtkImageData.h>
#include <vtkPointData.h>
#include <CGAL/Image_3_vtk_interface.h>

CGAL::Image_3 read_vtk_image_data_char(vtkImageData* vtk_image)
{

  if(!vtk_image)
    return false;

  point_image* image = new point_image();

  const int* dims = vtk_image->GetDimensions();
  const double* spacing = vtk_image->GetSpacing();
  image->vectMode = VM_SCALAR;
  image->xdim = dims[0];
  image->ydim = dims[1];
  image->zdim = dims[2];
  image->vdim = 1;
  image->vx = spacing[0];
  image->vy = spacing[1];
  image->vz = spacing[2];

#if VTK_MAJOR_VERSION <= 5
  vtk_image->Update();
#endif

  image->endianness = ::_getEndianness();
  int vtk_type = vtk_image->GetPointData()->GetScalars()->GetDataType();
  if(vtk_type != VTK_UNSIGNED_CHAR)
  {
    cerr << "read_vtk_image_data_char can only handle VTK_UNSIGNED_CHAR";
    exit(2);
  }
  image->wdim = 1;
  image->wordKind = WK_FIXED;
  image->sign = SGN_UNSIGNED;
  image->data = ::ImageIO_alloc(dims[0]*dims[1]*dims[2]* 1);
  std::cerr << "GetNumberOfTuples()=" << vtk_image->GetPointData()->GetScalars()->GetNumberOfTuples()
            << "\nimage->size()=" << dims[0]*dims[1]*dims[2]
            << "\nwdim=" << image->wdim << '\n';
  assert(vtk_image->GetPointData()->GetScalars()->GetNumberOfTuples() == dims[0]*dims[1]*dims[2]);
  vtk_image->GetPointData()->GetScalars()->ExportToVoidPointer(image->data);
  CGAL::Image_3 aReturn = CGAL::Image_3(image);
  return aReturn;
}
//end of taken form CGAL Image_3

    } //end of namespace CGALOperators
} // end of namespace MSML
