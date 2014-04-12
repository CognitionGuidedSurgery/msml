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


__authors__ = 'Alexander Weigl <uiduw@student.kit.edu>'
__license__ = 'GPLv3'
__date__ = "2014-04-13"

import abc
from path import path

from ..model import *
from .base import Exporter


class Visitor(object):
    def __init__(self, exporter):
        self.exporter = exporter

    def msml_begin(self, msml_file):
        pass


    def environment_begin(self, _msml, env):
        pass

    def environment_simulation(self, _msml, _environment, simulation):
        pass

    def environment_solver(self, _msml, _environment, solver):
        pass

    def environment_end(self, _msml, _environment, environment):
        pass

    def scene_begin(self, _msml, scene):
        pass

    def object_begin(self, _msml, _scene, object):
        pass

    def object_mesh(self, _msml, _scene, _object, mesh):
        pass

    def object_sets_begin(self, _msml, _scene, _object, sets):
        pass

    def object_sets_nodes(self, _msml, _scene, _object, _object_sets, node):
        pass

    def object_sets_elements(self, _msml, _scene, _object, _object_sets, element):
        pass

    def object_sets_surfaces(self, _msml, _scene, _object, _object_sets, surface):
        pass

    def object_sets_end(self, _msml, _scene, _object):
        pass

    def object_material_begin(self, _msml, _scene, _object, materials):
        pass

    def object_material_region_begin(self, _msml, _scene, _object, _material, region):
        pass

    def object_material_region_element(self, _msml, _scene, _object, _material, _region, element):
        pass

    def object_material_region_end(self, _msml, _scene, _object, _material, _region):
        pass

    def object_material_end(self, _msml, _scene, _object, _material):
        pass

    def object_constraints_begin(self, _msml, _scene, _object, constraints):
        pass

    def object_constraint_begin(self, _msml, _scene, _object, _constraints, constraint):
        pass

    def object_constraint_element(self, _msml, _scene, _object, _constraints, _constraint, element):
        pass

    def object_constraint_end(self, _msml, _scene, _object, _constraints, _constraint):
        pass

    def object_constraints_end(self, _msml, _scene, _object, _constraints):
        pass

    def object_output_begin(self, _msml, _scene, _object, outputs):
        pass

    def object_output_element(self, _msml, _scene, _object, _output, output):
        pass

    def object_output_end(self, _msml, _scene, _object, _output):
        pass

    def object_end(self, _msml, _scene, _object, sceneobject):
        pass

    def scene_end(self, _msml, _scene, scene):
        pass

    def msml_end(self, _msml):
        pass

    @abc.abstractmethod
    def write_export_file(self, msml_file_path, product):
        pass


class VisitorExporterFramework(Exporter):
    def __init__(self, msml_file, visitor_clazz):
        """
        Args:
            executer (Executer)


        """
        self.name = 'VisitorSekeleton'
        Exporter.__init__(self, msml_file)
        self.visitor_clazz = visitor_clazz
        self.visitor = None

    def render(self):
        self.visitor = self.visitor_clazz(self)
        assert isinstance(self.visitor, Visitor)

        _msml = self.visitor.msml_begin(self._msml_file)

        _env = self.visitor.environment_begin(_msml, self._msml_file.env)
        self.visitor.environment_simulation(_msml, _env, self._msml_file.env.simulation)
        self.visitor.environment_solver(_msml, _env, self._msml_file.env.solver)
        self.visitor.environment_end(_msml, _env, self._msml_file.env)

        # begin scene
        _scene = self.visitor.scene_begin(self._msml_file.scene)

        for obj in self._msml_file.scene:
            #begin object
            assert isinstance(obj, SceneObject)
            _so = self.visitor.object_begin(_msml, _scene, obj)

            self.visitor.object_mesh(_msml, _scene, _so, obj.mesh)

            #begin material
            _mat = self.visitor.object_material_begin(_msml, _scene, _so)

            for region in obj.material:
                #begin region
                _mr = self.visitor.object_material_region_begin(_so, _mat, region)
                for mat in region:
                    self.visitor.object_material_region_element(_so, _mat, _mr, mat)
                self.visitor.object_material_region_end(_so, _mat, _mr, region)
                #end region

            self.visitor.object_material_end(_so, _mat)
            #end material

            #begin constraints
            _css = self.visitor.object_constraints_begin(_msml, _scene, _so)
            for cs in obj:
                #begin constraint set
                _set = self.visitor.object_constraint_begin(_msml, _scene, _so, _css, cs)

                for c in cs:
                    self.visitor.object_constraint_element(_msml, _scene, _so, _css, _set, c)

                self.visitor.object_constraint_end(_msml, _scene, _so, _css, _set, cs)
                #end constraint set

            self.visitor.object_constraints_end(_msml, _scene, _so, _css)
            #end constraints

            #begin output
            _o = self.visitor.object_output_begin(_msml, _scene, _so)
            for o in obj.output:
                self.visitor.object_output_element(_msml, _scene, _so, _o, o)
            self.visitor.object_output_end(_msml, _scene, _so, _o)
            #end output

            self.visitor.object_end(_msml, _scene, _so, obj)
            #end object

        self.visitor.scene_end(_msml, _scene, self._msml_file.scene)
        #end scene

        self.visitor.msml_end(_msml)
        #end file

        self.export_file = self.visitor.write_export_file(path(self._msml_file), product)

    @abc.abstractmethod
    def execute(self):
        pass
