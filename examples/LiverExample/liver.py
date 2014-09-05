#!/usr/bin/env python
#region gplv3
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
#endregion

from __future__ import print_function

from msml.frontend import App
import vtk

from pprint import pprint
from msml.ext.vtk import read_ugrid
from path import path

__author__ = 'Alexander Weigl <Alexander.Weigl@student.kit.edu>'
__date__ = "2014-09-03"


def get_points(obj):
    if not hasattr(obj, "GetPoints"):
        obj = read_ugrid(obj)

    p = obj.GetPoints()
    points = (p.GetPoint(i) for i in range(0, p.GetNumberOfPoints()))

    return points


def get_connectivity(obj):
    ""
    if not hasattr(obj, "GetPoints"):
        obj = read_ugrid(obj)

    connections = list()

    ids = vtk.vtkIdList()
    for i in range(obj.GetNumberOfCells()):
        obj.GetCellPoints(i, ids)
        connections.append(tuple(
            (ids.GetId(j) for j in range(0, ids.GetNumberOfIds()))
        ))
    return connections

class Liver(object):
    def __init__(self, msml_filename):
        self.app = App()
        self.mf = self.app._load_msml_file(msml_filename)
        self._fixed_contraint_indices = None
        self._force_constraint_indices = None
        self._force_constraint_pressure = [0.0, 0.0, 0.0]
        self._displacement_indices = []
        self._displacement_vector = [0.0, 0.0, 0.0]

    def __call__(self):
        self.app.memory_init_file = {
            "force_vector" : self._force_constraint_pressure,
            "force_indices" : self._force_constraint_indices,
            "fixed_indices" : self._fixed_contraint_indices,
            "disp_vector" : self._displacement_vector,
            "disp_indices" : self._displacement_indices,
            "all_indices" : range(0,106) #readed from LiverXSTet4.vtk
        }

        self.app.execute_msml(self.mf)

        # we now the name from the displacement output request
        return path(".").files("LiverXSTet4Def.vtu*.vtu")


    @property
    def displacement_indices(self):
        return self._displacement_indices

    @displacement_indices.setter
    def displacement_indices(self, value):
        self._displacement_indices = value

    @property
    def displacement_vector(self):
        return self._displacement_vector

    @displacement_vector.setter
    def displacement_vector(self, value):
        self._displacement_vector = value

    @property
    def force_constraint_indices(self):
        return self._force_constraint_indices

    @force_constraint_indices.setter
    def force_constraint_indices(self, value):
        self._force_constraint_indices = value

    @property
    def force_constraint_pressure(self):
        return self._force_constraint_pressure

    @force_constraint_pressure.setter
    def force_constraint_pressure(self, value):
        self._force_constraint_pressure = value

    @property
    def fixed_contraint_indices(self):
        return self._fixed_contraint_indices

    @fixed_contraint_indices.setter
    def fixed_contraint_indices(self, value):
        self._fixed_contraint_indices = value




l = Liver("liverLinear_py.msml.xml")

l.displacement_vector = [0.1, 0.2, 0.3]
l.displacement_indices  = range(0,4)
l.fixed_contraint_indices = range(4,7)

files = l()

pprint(files)
pprint(list(get_points(files[0]))) # Get points step in the list