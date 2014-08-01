// Project: image2mesh (http://code.google.com/p/image2mesh)

// Copyright (c) 2008-2009  GeometryFactory (France).
// All rights reserved.
//
// This file is part of CGAL (www.cgal.org); you may redistribute it under
// the terms of the Q Public License version 1.0.
// See the file LICENSE.QPL distributed with CGAL.
//
// Licensees holding a valid commercial license may use this file in
// accordance with the commercial license agreement provided with the software.
//
// This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
// WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
//
//
// Author(s)     : Laurent Rineau
//               : Hamid Ghadyani (Added cell id support to generated vtk unstructured grid


#ifndef CGAL_COMPLEX_3_IN_TRIANGULATION_3_TO_VTK
#define CGAL_COMPLEX_3_IN_TRIANGULATION_3_TO_VTK

#include <map>

#include <vtkPoints.h>
#include <vtkUnstructuredGrid.h>
#include <vtkCellArray.h>
#include <vtkType.h>
#include <vtkDoubleArray.h>
#include <vtkFieldData.h>
#include <vtkCellData.h>

#include "CGAL/IO/File_medit.h"

namespace CGAL {

template <typename C3T3>
vtkUnstructuredGrid*
output_c3t3_to_vtk_unstructured_grid(const C3T3& c3t3,
                                     vtkUnstructuredGrid* grid = 0)
{
  typedef typename C3T3::Triangulation Triangulation;
  typedef typename Triangulation::Vertex_handle Vertex_handle;
  typedef CGAL::Mesh_3::Medit_pmap_generator<C3T3,true,true> Generator;
  typedef typename Generator::Cell_pmap Cell_pmap;

  const Triangulation& tr = c3t3.triangulation();
  Cell_pmap cell_pmap(c3t3);

  vtkPoints* const vtk_points = vtkPoints::New();
  vtkCellArray* const vtk_facets = vtkCellArray::New();
  vtkCellArray* const vtk_cells = vtkCellArray::New();

  vtk_points->Allocate(c3t3.triangulation().number_of_vertices());
  vtk_facets->Allocate(c3t3.number_of_facets_in_complex());
  vtk_cells->Allocate(c3t3.number_of_cells_in_complex());

  std::map<Vertex_handle, vtkIdType> V;
  vtkIdType inum = 0;

  for(typename Triangulation::Finite_vertices_iterator
        vit = tr.finite_vertices_begin(),
        end = tr.finite_vertices_end();
      vit != end;
      ++vit)
  {
    typedef typename Triangulation::Point Point;
    const Point& p = vit->point();
    vtk_points->InsertNextPoint(CGAL::to_double(p.x()),
                                CGAL::to_double(p.y()),
                                CGAL::to_double(p.z()));
    V[vit] = inum++;
  }
  for(typename C3T3::Facets_in_complex_iterator
        fit = c3t3.facets_in_complex_begin(),
        end = c3t3.facets_in_complex_end();
      fit != end; ++fit)
  {
    vtkIdType cell[3];
    int j=0;
    for (int i = 0; i < 4; ++i)
      if (i != fit->second)
        cell[j++] =  V[(*fit).first->vertex(i)];
    CGAL_assertion(j==3);
    vtk_facets->InsertNextCell(3, cell);
  }

  vtkIntArray *vtka = vtkIntArray::New();
  vtka->SetNumberOfTuples(c3t3.number_of_cells_in_complex());
  vtka->SetNumberOfComponents(1);
  vtka->SetName("Materials");

  inum = 0;
  for(typename C3T3::Cells_in_complex_iterator
        cit = c3t3.cells_in_complex_begin(),
        end = c3t3.cells_in_complex_end();
      cit != end; ++cit)
  {
    vtkIdType cell[4];
    for (int i = 0; i < 4; ++i)
      cell[i] =  V[cit->vertex(i)];
    vtkIdType _i = vtk_cells->InsertNextCell(4, cell);
    vtka->SetTuple1(_i, static_cast<int>(CGAL::Mesh_3::get(cell_pmap, cit)));
  }

  if(!grid) {
    grid = vtkUnstructuredGrid::New();
  }

  grid->SetPoints(vtk_points);
  vtk_points->Delete();


 grid->SetCells(VTK_TRIANGLE, vtk_facets);
  grid->SetCells(VTK_TETRA, vtk_cells);
#if VTK_MAJOR_VERSION <= 5
  grid->Update();
#endif

  grid->GetCellData()->SetScalars(vtka);

#if VTK_MAJOR_VERSION <= 5
  grid->Update();
#endif

  vtk_facets->Delete();
  vtk_cells->Delete();
  vtka->Delete();
//  fd->Delete();

  return grid;
}

} // end namespace CGAL

#endif // CGAL_COMPLEX_3_IN_TRIANGULATION_3_TO_VTK
