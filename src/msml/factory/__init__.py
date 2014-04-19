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
API for easily creating workflows and msml models.
"""
__author__ = 'Alexander Weigl'
__date__ = "2014-04-19"
__version__ = "0.1"

import operator
import functools
import contextlib

from msml.model import *
from msml.frontend import *


active_app = App()
num = 0

def generate_name(prefix="", suffix=""):
    global num
    num += 1
    return "%s_%d_%s" % (prefix, num, suffix)

def parse_attrib(kwargs):
    attrib = {}
    for k,v in kwargs.items():
        attrib[k] = v
        if isinstance(v, Task):
            attrib[k] = v.output_default
    return attrib

class OperatorFactory(object):
    def __init__(self, msml_file):
        self.msml_file = msml_file

    def __getattr__(self, item):
        return self.get_operator(item)

    def __getitem__(self, item):
        return self.get_operator(item)

    def get_operator(self, name):
        return functools.partial(self.create_task, active_app.alphabet.operators[name])

    def create_task(self, operator, **kwargs):
        id = generate_name("task")
        kwargs["id"] = id

        task = Task(operator.name, parse_attrib(kwargs))
        for out in operator.output_names():
            setattr(task, out, "${%s.%s}" % (id, out))

        if operator.output_names():
            setattr(task, 'output_default', "${%s.%s}" % (id, operator.output_names()[0]))

        self.msml_file.workflow.add_task(task)
        return task

class SceneFactory(object):
    def __init__(self, msml_file):
        self.msml_file = msml_file

    def object(self, id = None):
        if not id:
            id = generate_name("object")
        o = SceneObject(id)
        self.msml_file.scene.append(o)
        return ObjectFactory(o)

class ObjectFactory(object):
    def __init__(self, scene_object):
        self.so = scene_object


    def mesh(self, data, typ):
        if isinstance(data, Task):
            data = data.output_default
        self.so.mesh.mesh = data
        self.so.mesh.type = typ
        return self

    def sets_nodes(self, *sets):
        #TODO create indexgroup
        self.so.sets.nodes = sets

    def sets_surfaces(self, *sets):
        #TODO create indexgroup
        self.so.sets.surfaces = sets

    def sets_elements(self, *sets):
        #TODO create indexgroup
        self.so.sets.elements = sets

    def material_region(self, name, *args):
        region = MaterialRegion(name,args)
        self.so.material.append(region)
        return self

    def constraints(self, name, for_step = "initial", *elements):
        oc = ObjectConstraints(name, for_step)
        oc._constraints = elements
        self.so.constraints.append(oc)
        return self

    def output(self,*elements):
        self.so.output = elements
        return self

@contextlib.contextmanager
def define_workflow_of(msml_file):
    yield OperatorFactory(msml_file)

@contextlib.contextmanager
def define_scene_of(msml_file):
    yield SceneFactory(msml_file)

def __list2dict(l, attribute):
    a = operator.attrgetter(attribute)
    return {a(i): i for i in l}


class _AttributeFactory(object):
    def __init__(self):
         pass

    def __getattr__(self, item):
        return self.get_element(item)

    def __getitem__(self, item):
        return self.get_element(item)

    def get_element(self, name):
        #active_app.alphabet._object_attributes[name]
        return functools.partial(self.create_element, name)

    def create_element(self, name, **kwargs):
        kwargs['__tag__'] = name
        oe = ObjectElement(parse_attrib(kwargs))
        oe.bind(active_app.alphabet)
        return oe

elements = _AttributeFactory()

def as_operator(input=[], output=[], parameters=[]):
    def construct(func):
        name = func.func_name
        op = PythonOperator(name, __list2dict(input), __list2dict(output), __list2dict(parameters))
        op.function_name = name
        op.modul_name = "<unknown>"
        op.function = func
        return op

    return construct












