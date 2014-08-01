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

"""
A exporter framework based upon the Visitor Pattern.

This package consists of following important parts:

 - Visitor
 - VisitorDispatchable
 - VisitorExporterFramework.

*Visitor* defines the events that are called during traversing by VisitorExporterFramework.
*VisitorDispatchable* provides additional mechanism to differ between
types and tags of Meshes and ObjectElements.

"""

__authors__ = 'Alexander Weigl <uiduw@student.kit.edu>'
__license__ = 'GPLv3'
__date__ = "2014-04-13"

from collections import defaultdict
from ..exceptions import *
import abc
from path import path

from ..model import *
from .base import Exporter


class DispatcherWarning(MSMLWarning):
    pass


class DispatchError(MSMLError):
    pass


class Visitor(object):
    """
    Visitor should be inherited by the user to get events during traversing the msml scene graph.
    The Visitor follows this rules:

        * every list of elements are introduced with an *_begin
        * every *_begin is closed by a matching *_end
        * every list element as name *_element
        * every begin event can deliver a product object that is delivered for every element event
          and the matching event (sub contexts inclusive)

    The processing order (bunny.msml.xml):

      * msml_begin
        * environment_begin
          * environment_simulation
          * environment_solver
        * environment_end
        * scene_begin
          * object_begin
            * object_mesh
            * object_material_begin
              * object_material_region_begin
                * object_material_region_element
                * object_material_region_element
                * object_material_region_element
              * object_material_region_end
            * object_material_end
            * object_constraints_begin
              * object_constraint_begin
                * object_constraint_element
              * object_constraint_end
            * object_constraints_end
            * object_output_begin
              * object_output_element
            * object_output_end
          * object_end
        * scene_end
      * msml_end
      * write_export_file
    """


    def __init__(self, exporter):
        self.exporter = exporter

    def msml_begin(self, msml_file):
        pass

    def variables_begin(self, _msml, variables):
        pass

    def variables_element(self, _msml, _variables, variable):
        pass

    def variables_end(self, _msml, _variables, variables):
        pass

    def workflow_begin(self, _msml, workflow):
        pass

    def workflow_element(self, _msml, _workflow, task):
        pass

    def workflow_end(self, _msml, _workflow, workflow):
        pass

    def environment_begin(self, _msml, env):
        pass

    def environment_simulation_begin(self, _msml, _environment, simulation):
        pass

    def environment_simulation_element(self, _msml, _environment, _simulation, step):
        pass

    def environment_simulation_end(self, _msml, _environment, _simulation, simulation):
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

    def object_sets_nodes_begin(self, _msml, _scene, _object, _object_sets, nodes):
        pass

    def object_sets_nodes_element(self, _msml, _scene, _object, _object_sets, _nodes, node):
        pass

    def object_sets_nodes_end(self, _msml, _scene, _object, _object_sets, _nodes, nodes):
        pass


    def object_sets_elements_begin(self, _msml, _scene, _object, _object_sets, elements):
        pass

    def object_sets_elements_element(self, _msml, _scene, _object, _object_sets, _elements, element):
        pass

    def object_sets_elements_end(self, _msml, _scene, _object, _object_sets, _elements, elements):
        pass


    def object_sets_surfaces_begin(self, _msml, _scene, _object, _object_sets, surfaces):
        pass

    def object_sets_surfaces_element(self, _msml, _scene, _object, _object_sets, _surfaces, surface):
        pass

    def object_sets_surfaces_end(self, _msml, _scene, _object, _object_sets, _surfaces, surfaces):
        pass

    def object_sets_end(self, _msml, _scene, _object):
        pass

    def object_material_begin(self, _msml, _scene, _object, materials):
        pass

    def object_material_region_begin(self, _msml, _scene, _object, _material, region):
        pass

    def object_material_region_element(self, _msml, _scene, _object, _material, _region, element):
        pass

    def object_material_region_end(self, _msml, _scene, _object, _material, _region, region):
        pass

    def object_material_end(self, _msml, _scene, _object, _material, material):
        pass

    def object_constraints_begin(self, _msml, _scene, _object, constraints):
        pass

    def object_constraint_begin(self, _msml, _scene, _object, _constraints, constraint):
        pass

    def object_constraint_element(self, _msml, _scene, _object, _constraints, _constraint, element):
        pass

    def object_constraint_end(self, _msml, _scene, _object, _constraints, _constraint, constraint):
        pass

    def object_constraints_end(self, _msml, _scene, _object, _constraints, constraints):
        pass

    def object_output_begin(self, _msml, _scene, _object, outputs):
        pass

    def object_output_element(self, _msml, _scene, _object, _output, output):
        pass

    def object_output_end(self, _msml, _scene, _object, _output, output):
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


class MethodDispatcherMeta(type):
    """
    If you do not know about metaclasses see http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/
    first.

    This metaclass discovers methods in the class that are marked for
    dispatching and gathered them with category and names.

    """

    def __new__(cls, name, bases, d):
        #       print cls, name, bases, d

        categories = defaultdict(dict)

        for name, func in d.items():
            if callable(func) and hasattr(func, '_dispatching'):
                if func._dispatching:
                    categories[func._dispatch_category][func._dispatch_name] = func

                    #      print "Found:", categories

        d["_dispatching"] = categories

        def get_func(self, category, name, *args, **kwargs):
            try:
                f = self._dispatching[category][name]
            except KeyError as e:
                raise DispatchError(e)

            return f(self, *args, **kwargs)

        d['_dispatcher'] = get_func
        return type.__new__(cls, name, bases, d)


def disp_cat(category):
    """
    Provides a function dispatch marker for the given category.
    """

    def register_name(name):
        """ Decorator for registering a function with a given name"""

        def register_fn(func):
            setattr(func, "_dispatching", True)
            setattr(func, "_dispatch_category", category)
            setattr(func, "_dispatch_name", name)
            return func

        return register_fn

    return register_name


##
# Dispatch Marker
disp_constraint = disp_cat("C")
disp_mesh = disp_cat("M")
disp_material = disp_cat("m")
disp_output = disp_cat("O")
#
##


class VisitorDispatchable(Visitor):
    """
    This class extends the Visitor by dispatching on mesh, constraint, output and material elements.
    The dispatching happens on the tag or type attribute of ObjectElement or Mesh class.,


    This creates a class that calls `object_constraint_element_fixedConstraint`
    for every ObjectElement that is a constraint and has the tag `fixedConstraint`:

    >>> class MyVisitor(VisitorDispatchable):
    >>>     @disp_constraint('fixedConstraint')
    >>>     def object_constraint_element_fixedConstraint(self, _msml, _scene, _object, _constraints, _constraint, element):
    >>>         Printer.object_constraint_element_fixedConstraint(self, _msml, _scene, _object, _constraints, _constraint, element)

    Use the dispatch markers: `disp_constraint, disp_mesh, disp_material, disp_output`

    **DON'T** override the corresponding *_element functions (e.g. object_constraint_element). Every function should
    have a different name.

    Inheritance should not work.

    """
    __metaclass__ = MethodDispatcherMeta

    def __init__(self, exporter):
        Visitor.__init__(self, exporter)

    def object_mesh(self, _msml, _scene, _object, mesh):
        try:
            return self._dispatcher('M', mesh.type, _msml, _scene, _object, mesh)
        except DispatchError as e:
            warn("return to default implementation for mesh type %s" % mesh.type, DispatcherWarning)
            self.object_mesh_default(_msml, _scene, _object, mesh)

    def object_mesh_default(self, _msml, _scene, _object, mesh):
        pass

    def object_output_element(self, _msml, _scene, _object, _output, output):
        try:
            return self._dispatcher('O', output.tag, _msml, _scene, _object, _output, _output)
        except DispatchError as e:
            warn("return to default implementation for output type %s" % output.tag, DispatcherWarning)
            self.object_output_element_default(_msml, _scene, _object, _output, output)

    def object_output_element_default(self, _msml, _scene, _object, _output, output):
        pass

    def object_constraint_element(self, _msml, _scene, _object, _constraints, _constraint, element):
        try:
            return self._dispatcher('C', element.tag, _msml, _scene, _object, _constraints, _constraint, element)
        except DispatchError:
            warn("return to default implementation for constraint type %s" % element.tag, DispatcherWarning)
            self.object_constraint_element_default(_msml, _scene, _object, _constraints, _constraint, element)

    def object_constraint_element_default(self, _msml, _scene, _object, _constraints, _constraint, element):
        pass

    def object_material_region_element(self, _msml, _scene, _object, _material, _region, element):
        try:
            return self._dispatcher('m', element.tag, _msml, _scene, _object, _material, _region, element)
        except DispatchError:
            warn("return to default implementation for material type %s" % element.tag, DispatcherWarning)
            self.object_material_region_element_default(_msml, _scene, _object, _material, _region, element)

    def object_material_region_element_default(self, _msml, _scene, _object, _material, _region, element):
        pass


class VisitorExporterFramework(Exporter):
    def __init__(self, msml_file, visitor_clazz):
        self.name = 'VisitorSekeleton'
        Exporter.__init__(self, msml_file)
        self.visitor_clazz = visitor_clazz
        self.visitor = None

    def render(self):
        self.visitor = self.visitor_clazz(self)
        assert isinstance(self.visitor, Visitor)
        self.visit()

    def visit(self):
        _msml = self.visitor.msml_begin(self._msml_file)

        ## Variables
        _variables = self.visitor.variables_begin(_msml, self._msml_file.variables)
        for var in self._msml_file.variables.values():
            self.visitor.variables_element(_msml, _variables, var)
        self.visitor.variables_end(_msml, _variables, self._msml_file.variables)

        ##Workflow
        _workflow = self.visitor.workflow_begin(_msml, self._msml_file.workflow)
        for task in self._msml_file.workflow._tasks.values():
            self.visitor.workflow_element(_msml, _workflow, task)
        self.visitor.workflow_end(_msml, _workflow, self._msml_file.workflow)

        _env = self.visitor.environment_begin(_msml, self._msml_file.env)
        _simulation = self.visitor.environment_simulation_begin(_msml, _env, self._msml_file.env.simulation)
        for s in self._msml_file.env.simulation:
            self.visitor.environment_simulation_element(_msml, _env,_simulation, s)
        self.visitor.environment_simulation_end(_msml, _env, _simulation, self._msml_file.env.simulation)

        self.visitor.environment_solver(_msml, _env, self._msml_file.env.solver)
        self.visitor.environment_end(_msml, _env, self._msml_file.env)

        # begin scene
        _scene = self.visitor.scene_begin(_msml, self._msml_file.scene)

        for obj in self._msml_file.scene:
            #begin object
            assert isinstance(obj, SceneObject)
            _so = self.visitor.object_begin(_msml, _scene, obj)

            self.visitor.object_mesh(_msml, _scene, _so, obj.mesh)

            #begin material
            _mat = self.visitor.object_material_begin(_msml, _scene, _so, obj.material)

            for region in obj.material:
                #begin region
                _mr = self.visitor.object_material_region_begin(_msml, _scene, _so, _mat, region)
                for mat in region:
                    self.visitor.object_material_region_element(_msml, _scene, _so, _mat, _mr, mat)
                self.visitor.object_material_region_end(_msml, _scene, _so, _mat, _mr, region)
                #end region

            self.visitor.object_material_end(_msml, _scene, _so, _mat, obj.material)
            #end material

            #begin constraints
            _css = self.visitor.object_constraints_begin(_msml, _scene, _so, obj.constraints)
            for cs in obj.constraints:
                #begin constraint set
                _set = self.visitor.object_constraint_begin(_msml, _scene, _so, _css, cs)

                for c in cs.constraints:
                    self.visitor.object_constraint_element(_msml, _scene, _so, _css, _set, c)

                self.visitor.object_constraint_end(_msml, _scene, _so, _css, _set, cs)
                #end constraint set

            self.visitor.object_constraints_end(_msml, _scene, _so, _css, obj.constraints)
            #end constraints

            #begin output
            _o = self.visitor.object_output_begin(_msml, _scene, _so, obj.output)
            for o in obj.output:
                self.visitor.object_output_element(_msml, _scene, _so, _o, o)
            self.visitor.object_output_end(_msml, _scene, _so, _o, obj.output)
            #end output

            self.visitor.object_end(_msml, _scene, _so, obj)
            #end object

        self.visitor.scene_end(_msml, _scene, self._msml_file.scene)
        #end scene

        self.visitor.msml_end(_msml)
        #end file

        self.export_file = self.visitor.write_export_file(path(self._msml_file), _msml)
        return _msml

    @abc.abstractmethod
    def execute(self):
        pass
