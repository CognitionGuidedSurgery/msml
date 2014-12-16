# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
#   S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
#   The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#   Medicine Meets Virtual Reality (MMVR) 2014
#
# Copyright (C) 2013-2014 see Authors.txt
#
# If you have any questions please feel free to contact us at suwelack@kit.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# endregion
from __future__ import absolute_import

__author__ = 'Alexander Weigl <uiduw@student.kit.edu>'
__date__ = '2014-04-14'

from msml.exceptions import MSMLWarning, warn
import math
from itertools import starmap
from ..log import logger


class MSMLVTKImportWarning(MSMLWarning):
    pass

try:
    import vtk
except:
    logger.warn("Could not import vtk python module. Did you install python-vtk?")

def read_ugrid(filename):
    if filename.endswith(".pvtu"):
        reader = vtk.vtkXMLPUnstructuredGridReader()
    elif filename.endswith(".vtk"):
        reader = vtk.vtkUnstructuredGridReader()
    elif filename.endswith(".vtu"):
        reader = vtk.vtkXMLUnstructuredGridReader()
    else:
        raise BaseException("Illegal filename suffix %s" % filename)

    reader.SetFileName(filename)
    reader.Update()

    return reader.GetOutput()

def write_surface(ugrid, filename):
    surface_filter = vtk.vtkDataSetSurfaceFilter()
    surface_filter.SetInputData(ugrid)

    triangle_filter = vtk.vtkTriangleFilter()
    triangle_filter.SetInputConnection(surface_filter.GetOutputPort())

    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputConnection(triangle_filter.GetOutputPort())
    writer.Write()

def write_stl(ugrid, filename):
    surface_filter = vtk.vtkDataSetSurfaceFilter()
    surface_filter.SetInputConnection(ugrid)

    triangle_filter = vtk.vtkTriangleFilter()
    triangle_filter.SetInputConnection(surface_filter.GetOutputPort())

    writer = vtk.vtkSTLWriter()
    writer.SetFileName(filename)
    writer.SetInputConnection(triangle_filter.GetOutputPort())
    writer.Write()

def write_vtu(ugrid, filename, mode = 'ascii'):
    writer = vtk.vtkXMLUnstructuredGridWriter()
    if mode == 'ascii':
        writer.SetDataModeToAscii()
    elif mode == 'binary':
        writer.SetDataModeToBinary()
    elif mode == 'append':
        writer.SetDataModetoAppend()

    writer.SetFileName(filename)
    writer.SetInputData(ugrid)
    writer.Write()

def write_vtk(ugrid, filename):
    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(filename)
    writer.SetInputData(ugrid)
    writer.Write()

def closest_point(mesh, vector, radius = None):
    locator = vtk.vtkPointLocator()
    ugrid = read_ugrid(mesh)
    locator.SetDataSet(ugrid)

    vector = map(float, vector)
    assert len(vector) == 3

    if radius is None:
        index = locator.FindClosestPoint(vector)
    else:
        a = vtk.mutable(0.0)
        index = locator.FindClosestPointWithinRadius(radius, vector, a)

    point = ugrid.GetPoint(index)
    distance = math.sqrt(sum(starmap(lambda a, b: (b-a)**2, zip(vector, point))))
    return {'index': index, 'point': point, 'dist': distance}


def get_impact(ugrid, start, direction, factor = 1000):
    cl = vtk.vtkCellLocator()
    ugrid = read_ugrid(ugrid)
    cl.SetDataSet(ugrid)

    mult = lambda f, x: map(lambda a: f*a, x)
    end = mult(1000, direction)


    points = vtk.vtkPoints()
    cells = vtk.vtkIdList()

    cl.intersectWithLine(start, end, points, cells)

    ugrid.GetCell(cells.getId(0))






def view_stl(filename):
    """
    http://www.vtk.org/Wiki/VTK/Examples/Python/STLReader
    """
    reader = vtk.vtkSTLReader()
    reader.SetFileName(filename)

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(reader.GetOutput())
    else:
        mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a rendering window and renderer
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    # Create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Assign actor to the renderer
    ren.AddActor(actor)

    # Enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()


def  vtp_reader(filename):
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(reader.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

def unstructered_grid_reader(filename):
    # Read the source file.
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update() # Needed because of GetScalarRange
    output = reader.GetOutput()
    scalar_range = output.GetScalarRange()

    # Create the mapper that corresponds the objects of the vtk file
    # into graphics elements
    mapper =vtk.vtkDataSetMapper()
    mapper.SetInputData(output)
    mapper.SetScalarRange(scalar_range)

    # Create the Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create the Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1) # Set background to white

    # Create the RendererWindow
    renderer_window = vtk.vtkRenderWindow()
    renderer_window.AddRenderer(renderer)

    # Create the RendererWindowInteractor and display the vtk_file
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()
