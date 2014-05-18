# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
# Medicine Meets Virtual Reality (MMVR) 2014
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


__author__ = "Alexander Weigl"
__date__ = "2014-01-26"

import warnings

from path import path

from .memory import Memory
from msml.model import *
from msml.model.dag import DiGraph
from msml.exporter.base import Exporter
from msml.run.GraphDotWriter import GraphDotWriter


class Executer(object):
    """Describe the interface of an Executer.

    An Executer is responsible for calling the operator with the right arguments and parameters in the right order.
    Additionally it invokes the Exporter.


    """
    # TODO define interface /weigl
    pass


def contains(a, b):
    if isinstance(b, type):
        b = b.__name__
    elif not isinstance(b, (str, unicode)):
        b = str(b)
    try:
        return b.index(a) >= 0
    except ValueError:
        return False


def initialize_file_literals(first_bucket):
    def var_is_file(var):
        if isinstance(var, MSMLVariable):
            # TODO better predicate if sort logic defined /weigl
            return contains("file", var.logical_type) or contains("file", var.physical_type)
        return False

    def abs_value(var):
        import os.path

        var.value = os.path.abspath(var.value)
        return var

    return map(abs_value, filter(var_is_file, first_bucket))


class LinearSequenceExecuter(Executer):
    """ The LinearSequenceExecuter executes the given MSMLFile  in one sequence with no parallelism in topological order.

    """

    def __init__(self, msmlfile):
        self._mfile = msmlfile
        self._memory = Memory()
        self._exporter = self._mfile.exporter
        self.working_dir = None

    def init_memory(self, content):
        if isinstance(content, str):
            self._memory.reset()
            self._memory.load_memory_file(content)
        elif content:
            warnings.warn("init_memory handles only filenames", MSMLWarning)


    def define_var(self, name, value=None):
        """defines a variable in the current memory.

        Args:
          name (str): variable identifier
          value (object): any value of variable

        """
        if name not in self._memory:  # do not override
            self._memory[name] = value

    def run(self):
        """starts the execution of the given MSMLFile
        """
        dag = DefaultGraphBuilder(self._mfile, self._exporter).dag

        # dag.show()

        buckets = dag.toporder()

        # make absolute paths for every string/file literal
        # wd is msml file dirname
        initialize_file_literals(buckets[0])

        # change to output_dir
        if self.working_dir:
            wd = path(self.working_dir)
            try:
                wd.mkdir()
            except:
                pass
            finally:
                wd.chdir()

        for bucket in buckets:
            for node in bucket:
                if isinstance(node, Task):
                    self._execute_operator_task(node)
                elif isinstance(node, MSMLVariable):
                    self._execute_variable(node)
                elif isinstance(node, Exporter):
                    self._execute_exporter(node)

        return self._memory

    def _execute_exporter(self, node):
        """executes the exporter behind node

        Args:
          node (Exporter): the exporter for the msml-file

        """
        self._exporter.init_exec(self)
        self._exporter.render()
        self._exporter.execute()


    def _execute_variable(self, node):
        """node is MSMLVariable

        """
        self.define_var(node.name, node.value)


    def _execute_operator_task(self, task):
        kwargs = self.gather_arguments(task)
        report('Executing operator of task {} with arguments {}'.format(task, kwargs), 'I', '001')
        result = task.operator(**kwargs)
        report('--Executing operator of task {} done'.format(task), 'I', '002')
        self._memory[task.id] = result


    def gather_arguments(self, task):
        """ Finds and collect all needed input and parameters variables from the current memory.

        Args:
          task (Task):

        """
        arguments = task.arguments

        vals = {}
        for ref in arguments.values():
            outname = ref.linked_from.arginfo.name
            inname = ref.linked_to.arginfo.name

            if isinstance(ref.linked_from.task, MSMLVariable):
                outid = ref.linked_from.task.name
                vals[inname] = self._memory[outid]
            else:
                outid = ref.linked_from.task.id
                vals[inname] = self._memory[outid][outname]

        return vals


def build_graph(tasks, exporter, variables):
    dag = DiGraph()

    nodes = dict(tasks)
    nodes.update(variables)

    for t in nodes.values():
        dag.add_node(t)

    dag.add_node(exporter)

    for t in tasks.values():
        for ta in t.arguments.values():
            dag.add_edge(ta.linked_from.task,
                         ta.linked_to.task,
                         ref=ta)

    for ta in exporter.arguments.values():
        dag.add_edge(ta.linked_from.task,
                     ta.linked_to.task, ref=ta)

    return dag


from ..log import report
from ..sorts import conversion


def inject_implict_conversion(dag):
    """Finds type mismatch and injects suitable conversion operators

    :param dag: a directed acyclic graph from `build_graph`
    :type dag: DiGraph
    :return: the given graph
    :rtype: DiGraph
    """
    for a, b, data in dag.edges(data=True):
        ref = data['ref']
        if not ref.valid:
            report("Reference %s is invalid. Try to implicit conversion" % ref, 'I', 1561)
            task = create_conversion_task(ref.linked_from, ref.linked_to)

            # add new task
            dag.add_node(task)

            #remove the old edge
            dag.remove_edge(a, b)

            # from Task to Converter
            _a_t = Reference(ref.task, ref.slot)
            _a_t.linked_from = ref.linked_from
            _a_t.link_to_task(task, task.operator.input['i'])

            _t_b = Reference(ref.task, ref.slot)
            _t_b.linked_to = ref.linked_to
            _t_b.link_from_task(task, task.operator.output[task.operator.output.keys()[0]])


            task.arguments['i'] = _a_t
            b.arguments[ref.linked_to.name] = _t_b

            dag.add_edge(a, task, ref=_a_t)
            dag.add_edge(task, b, ref=_t_b)

        else:
            report("Reference %s is valid" % ref, 'D', 1562)
    return dag


from ..model import PythonOperator, Task, Slot


def get_python_conversion_operator(slotA, slotB):
    r = {'function': '<automatic-converter>', 'module': '<module-name>'}

    pA = slotA.arginfo.sort.physical
    lA = slotA.arginfo.sort.logical

    pB = slotB.arginfo.sort.physical
    lB = slotB.arginfo.sort.logical

    pyop = PythonOperator(
        "converter_%s_%s" % (pA.__name__, pB.__name__),
        input=[Slot("i", pA, lA)],
        output=[Slot(slotB.name, pB, lB)], runtime=r)

    return pyop


def create_conversion_task(slotA, slotB):
    """

    :param slotA:
    :type slotA: Reference.Ref
    :param slotB:
    :type slotB: Reference.Ref
    :return:
    """

    fn = conversion(slotA.arginfo.sort, slotB.arginfo.sort)
    if fn is None:
        raise MSMLError("Could not find an automatic Converter for %s to %s" % (slotA, slotB))

    def get_id(slot):
        if isinstance(slot.task, Task):
            return slot.task.id
        if isinstance(slot.task, MSMLVariable):
            return slot.task.name


    pyop = get_python_conversion_operator(slotA, slotB)
    pyop._function = fn

    # the new task override the old one memory values
    attrib = {'id': get_id(slotA), 'i': None}
    task = Task(pyop.name, attrib)
    task.operator = pyop
    return task


class DefaultGraphBuilder(object):
    """ Builds the DAG for the given msmlfile and exporter

     Args:
       msmlfile (MSMLFile)
       exporter (Exporter)
        
    """

    def __init__(self, msmlfile, exporter):
        """
        :type msmlfile: msml.model.base.MSMLFile
        """

        assert isinstance(msmlfile, MSMLFile)
        self.mfile = msmlfile

        assert isinstance(exporter, Exporter)
        self.exporter = exporter

        self._dag = None


    @property
    def dag(self):
        if not self._dag:
            self._dag = inject_implict_conversion(
                build_graph(self.mfile.workflow._tasks, self.exporter, self.mfile.variables))
        return self._dag
