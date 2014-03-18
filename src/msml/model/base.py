# -*- encoding: utf-8 -*-
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


"""

from collections import namedtuple
import re
import warnings

from path import path
from .exceptions import *







# from msml.model.alphabet import Argument cycle
from msml.sorts import get_sort


__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

Argument = namedtuple('Argument', 'name,format,type,required')


class struct(dict):
    def __getattr__(self, attr):
        a = self[attr]
        if isinstance(a, dict):
            return struct(a)
        return a

    #    __getattr__= dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def structure(name, field_names):
    class _allset(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    return type(name, (_allset,), {f: None for f in field_names.split('[ ,]')})


#Edge = namedtuple("Edge", "inarg outarg");


class MSMLFile(object):
    """
    
    """

    def __init__(self, variables=None, workflow=None, scene=None, env=None, output=None):
        if variables:
            self._variables = {v.name: v for v in variables}
        else:
            self._variables = dict()

        self._workflow = workflow if workflow else Workflow()
        self._scene = scene if scene else []
        self._env = env if env else MSMLEnvironment
        self._output = output if output else []
        self._exporter = None

        assert isinstance(self._env, MSMLEnvironment)

    @property
    def variables(self):
        return self._variables

    @property
    def workflow(self):
        return self._workflow

    @property
    def scene(self):
        return self._scene

    @property
    def env(self):
        return self._env

    @property
    def output(self):
        return self._output


    @property
    def exporter(self):
        return self._exporter

    @exporter.setter
    def exporter(self, exp):
        self._exporter = exp

    def exists_var(self, name):
        return name in self._variables

    def get_var(self, name):
        return self._variables[name]

    def validate(self, alphabet=None):
        if not alphabet:
            import msml.env

            alphabet = msml.env.current_alphabet

        self._workflow.bind_operators(alphabet)
        self._workflow.link(alphabet, self)

        # exporter can link his variables against msml file
        self._exporter.link()

        self._workflow.check_arguments()
        return True

    def lookup(self, ref, outarg=True):
        "lookup a reference, consists of task id and output arg"
        if isinstance(ref, str):
            ref = parse_attribute_value(ref)

        r = ref.task
        v = ref.slot

        task = self._workflow.lookup(r)
        if task:
            op = task.operator
            args = op.output if outarg else op.input + op.parameters
            if v:
                return task, args[ref]
            else:
                # choose first from output/input
                return task, args.values()[0]
        elif r in self._variables:
            return self._variables[r], self._variables[r]
        else:
            a = self._exporter.lookup(ref, outarg)
            if a: return a

        warnings.warn("could not bind %s to a slot" % ref)

    def add_variable(self, var):
        self._variables[var.name] = var;

    def find_simulation_step(self, name):
        name = name.strip("{$}")
        for env in self.env['environment']:
            if 'simulation' in env:
                for sstep in env['simulation']:
                    if sstep['@name'] == name:
                        return sstep
        #TODO WARNING! sim step not found
        return None


class Workflow(object):
    def __init__(self, tasks=[]):
        self._tasks = {t.id: t for t in tasks}

    def add_task(self, task):
        self._tasks[task.id] = task

    def lookup(self, id):
        return self._tasks.get(id, None)

    def bind_operators(self, alphabet):
        for t in self._tasks.values():
            t.bind(alphabet)

    def link(self, alphabet, msmlfile):
        for t in self._tasks.values():
            t.link(alphabet, msmlfile)

    def check_arguments(self):
        "checks if all tasks match the operator definition"
        return all(map(lambda x: x.validate(), self._tasks.values()))


class MSMLEnvironment(object):
    """<solver linearSolver="iterativeCG" processingUnit="CPU"
                timeIntegration="dynamicImplicitEuler"/>
        <simulation>
            <step name="initial" dt="0.05" iterations="100"/>
        </simulation>"""

    class Simulation(list):
        class Step(object):
            def __init__(self, name="initial", dt=0.05, iterations=100):
                self.name = name
                self.dt = dt
                self.iterations = iterations

        def __init__(self, *args):
            list.__init__(self, *args)

        def add_step(self, name="initial", dt=0.05, iterations=100):
            self.append(MSMLEnvironment.Simulation.Step(name, dt, iterations))

    class Solver(object):
        def __init__(self, linearSolver="iterativeCG", processingUnit="CPU", timeIntegration="dynamicImplicitEuler"):
            self.linearSolver = linearSolver
            self.processingUnit = processingUnit
            self.timeIntegration = timeIntegration


    def __init__(self):
        self.simulation = MSMLEnvironment.Simulation()
        self.solver = MSMLEnvironment.Solver()


class MSMLVariable(object):
    def __init__(self, name, format=None, typ=None, value=None):
        self.name = name
        self.format = format
        self.type = typ
        self.value = value
        self.sort = None

        self._find_sort()

    def _find_sort(self):
        if self.value is not None:
            self.type = type(self.value)
            self.sort = self.type
        elif self.format is not None and self.type is not None:
            self.sort = get_sort(self.format + self.type)
        elif self.format:
            self.sort = get_sort(self.format)
        elif self.type:
            self.sort = get_sort(self.type)
        else:
            self.sort = get_sort('*')

    def _dot(self):
        return {'label': self.name, 'color': 'orange'}

    def __str__(self):
        return "Var '%s' (%s)" % (self.name, self.sort)

    def __repr__(self):
        return "MSMLVariable(%s,%s,%s)" % (self.name, self.format, self.type)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['sort']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._find_sort()


class MSMLFileVariable(object):
    def __init__(self, name, format=None, typ=None, location=None):
        self.name = name
        self.sort = get_sort([format, type])
        self.format = format
        self.type = type
        self.location = path(location)

        if self.location is not None:
            self.type = 'file'
            self.format = "file." + self.location.ext()
            self.sort = get_sort([self.format, self.type])
        elif format is not None and type is not None:
            self.sort = get_sort([format, typ])

    def __str__(self):
        return "<Variable %s of (%s,%s)>" % (self.name, self.type, self.format)

    def __repr__(self):
        return "MSMLVariable(%s,%s,%s)" % (self.name, self.format, self.type)


class Constant(object):
    def __init__(self, value):
        self.value = value


class Reference(object):
    ref = namedtuple("ref", "task,name,arginfo")

    def __init__(self, task, out=None):
        self.task = task
        self.slot = out

        self.linked_from = None
        self.linked_to = None

    @property
    def linked(self):
        return self.linked_to and self.linked_from

    def link_from_task(self, task, outarg):
        self.linked_from = Reference.ref(task, outarg.name, outarg)

    def link_from_variable(self, variable):
        self.linked_from = Reference.ref(variable, variable.name, variable)

    def link_to_task(self, task, inarg):
        self.linked_to = Reference.ref(task, inarg.name, inarg)

    def validate(self):
        pass


    def _edge_dot(self):
        return {'taillabel': str(self.linked_to.arginfo.sort),
                'headlabel': str(self.linked_from.arginfo.sort)}

    def __str__(self):
        def _id(a):
            try:
                return a.id
            except:
                return a.name

        if self.linked:
            return "{Ref+: %s.%s -> %s.%s}" % (
                _id(self.linked_from.task), self.linked_from.name, _id(self.linked_to.task), self.linked_to.name)
        else:
            return "{Ref-: %s.%s}" % (self.task, self.slot)


def parse_attribute_value(value):
    expr = re.match(r'\${(.*)(\..*)?}', value)
    if expr:
        a = expr.group(1)
        try:
            b = expr.group(2)
        except:
            b = None
        return Reference(a, b)
    else:
        return Constant(value)


def random_var_name():
    import random

    return "_gen_%d_" % random.randint(100, 999)


class Task(object):
    ID_ATTRIB = "id"

    def __init__(self, name, attrib):
        self.name = name
        self.id = attrib[Task.ID_ATTRIB]
        del attrib[Task.ID_ATTRIB]

        self.attributes = {k: parse_attribute_value(value) for k, value in attrib.items()}
        self.operator = None
        self.arguments = {}

    def __str__(self):
        return "{Task %s (%s)}" % (self.id, self.name)

    def _dot(self):
        i = ["%s : %s" % (k, str(v))
             for k, v in self.arguments.items()]

        o = ("%s :  %s" % (k, v)
             for k, v in self.operator.output.items())

        LABEL_TPL = """<
            <TABLE>
            <tr><td>ID</td> 
                <td><B>{$ id}</B></td>
            </tr>
            <tr><td>OP</td> 
                <td><I>{$ operator}</I></td>
            </tr>
            {for o in input} 
                <tr><td>IN</td><td>{$ o}</td></tr>
            {end}

            {for o in output} 
                <tr><td>OUT</td><td>{$ o}</td></tr>
            {end}
            </TABLE>
            >
        """

        import msml.titen

        TPL = msml.titen.titen(LABEL_TPL)
        return {'label': TPL(id=self.id, operator=self.operator.name, input=i, output=o)}

    def bind(self, alphabet):
        self.operator = alphabet.get(self.name)

    def link(self, alphabet, msmlfile):
        self.arguments = {}
        for key, value in self.attributes.items():
            if isinstance(value, Reference):
                a = msmlfile.lookup(value)
                if a:
                    outtask, outarg = a
                    value.link_from_task(outtask, outarg)
                    try:
                        if key in self.operator.input:
                            value.link_to_task(self, self.operator.input[key])
                        else:
                            print self
                            print self.operator.parameters[key]
                            value.link_to_task(self, self.operator.parameters[key])
                    except KeyError, e:

                        f = str(a)
                        t = str(self.name)
                        i = key
                        op = str(self.operator)
                        inputs = ",".join(map(str, self.operator.acceptable_names()))

                        raise BindError(
                            "you try to connect {start} to Task '{target}' but slot {inputname} is unknown for {operator} (Inputs {inputs})".format(
                                start=f, target=t, inputname=i, operator=op, inputs=inputs
                            ))
                    except AttributeError:
                        raise MSMLError(
                            "the operator for Task {target} is {operator} ".format(
                                target=self.name, operator=self.operator
                            ))

                    self.arguments[key] = value
                else:
                    warnings.warn("Lookup after %s does not succeeded" % value)
            elif isinstance(value, Constant):
                var = MSMLVariable(random_var_name(), value=value.value);
                msmlfile.add_variable(var)
                ref = Reference(var.name, None)
                outtask, outarg = msmlfile.lookup(ref)
                ref.link_from_task(outtask, outarg)

                try:
                    #ref.link_to_task(self, self.operator.input[key])
                    if key in self.operator.input:
                        ref.link_to_task(self, self.operator.input[key])
                    else:
                        ref.link_to_task(self, self.operator.parameters[key])
                except KeyError, e:
                    f = str(var)
                    t = str(self.name)
                    i = key
                    op = str(self.operator)
                    inputs = ",".join(map(str, self.operator.acceptable_names()))

                    raise BindError(
                        "you try to connect {start} to Task '{target}' but slot {inputname} is unknown for {operator} (Inputs {inputs})".format(
                            start=f, target=t, inputname=i, operator=op, inputs=inputs
                        ))

                self.arguments[key] = ref
            else:
                raise MSMLError("no case %s : %s " % (value, str(type(value))))

    def validate(self):
        if not self.operator:
            raise BindError("self.operator is not bound to an operator (call Workflow.bind_operator?)")

            # if self.id:
            #    raise MSMLError("Task does not have an <id> attribute")

            # for arg in self.arguments.values():
            #    if arg.inarg.required and arg.outarg is None:
            #        raise MSMLError("task for operator %s misses attribute %s " % (self.operator.name, arg.attribute))

            #        for k in self.attrib:
            #            if k not in self.operator and k != Task.ID_ATTRIB:
            #                raise MSMLError("attrib %s is unknown for operator %s" % (k, self.operator.name))

    def get_default(self):
        pass


class SceneObject(object):
    def __init__(self, oid, mesh=None, body=[], material=[], constraints=[]):
        self._id = oid
        self._mesh = mesh
        self._material = material
        self._constraints = constraints
        self._sets = None
        self._output = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def sets(self):
        return self._sets

    @sets.setter
    def sets(self, value):
        self._sets = value

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, value):
        assert isinstance(value, Mesh)
        self._mesh = value

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    @property
    def constraints(self):
        return self._constraints

    @constraints.setter
    def constraints(self, c):
        self._constraints = c

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, mat):
        self._material = mat


from abc import abstractmethod


class SceneGroup(object):
    "unused"

    @abstractmethod
    def __init__(self):
        pass


class ObjectElement(object):
    def __init__(self, attrib={}, object_attrib=None):
        self.attributes = attrib
        self.object_attribute = object_attrib

    def __getattr__(self, item):
        try:
            return self.attributes[item]
        except KeyError as e:
            return None

    # TODO Check for valid against ObjectAttribute

    @property
    def tag(self):
        return self.attributes['__tag__']

    @tag.setter
    def tag(self, tag):
        self.attributes['__tag__'] = tag


class ObjectConstraints(object):
    def __init__(self, name, forStep="initial"):
        self._name = name
        self._forStep = forStep
        self._constraints = []


    @property
    def index_group(self):
        warn(DeprecationWarning, "This method will be removed at the next refactoring! /alexander weigl")
        for c in self._constraints:
            if c.attributes['__tag__'] == 'indexgroup': return c
        return None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def for_step(self):
        return self._forStep

    @for_step.setter
    def for_step(self, v):
        self._forStep = v

    @property
    def constraints(self):
        return self._constraints

    @constraints.setter
    def constraints(self, v):
        self._constraints = v


    def add_constraint(self, *constraints):
        self._constraints += constraints


class SceneSets(object):
    def __init__(self, nodes=list(), surfaces=list(), elements=list()):
        self.nodes = nodes
        self.surfaces = surfaces
        self.elements = elements


class IndexGroup(object):
    def __init__(self, id, indices):
        self.id = id
        self.indices = indices

class Mesh(object):
    def __init__(self, type, id, mesh):
        self.type = type
        self.id = id
        self.mesh = mesh


class MaterialRegion(list):
    def __init__(self, id, elements):
        self.id = id
        list.__init__(self, elements)

    def get_indices(self):
        for ele in self:
            if ele.attributes['__tag__'] == 'indexgroup':
                return ele