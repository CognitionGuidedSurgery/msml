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


__author__ = "Alexander Weigl"
__date__ = "2014-01-26"

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


class LinearSequenceExecuter(Executer):
    """ The LinearSequenceExecuter executes the given MSMLFile  in one sequence with no parallelism in topological order.

    """

    def __init__(self, msmlfile):
        self._mfile = msmlfile
        self._memory = Memory()
        self._exporter = self._mfile.exporter

    def define_var(self, name, value=None):
        """defines a variable in the current memory.

        Args:
          name (str): variable identifier
          value (object): any value of variable

        """
        self._memory[name] = value

    def run(self):
        """starts the execution of the given MSMLFile
        """
        dag = DefaultGraphBuilder(self._mfile, self._exporter).dag

        #dag.show()

        buckets = dag.toporder()

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
        result = task.operator(**kwargs)
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

    def _build(self):
        dag = DiGraph()

        nodes = dict(self.mfile._workflow._tasks)
        nodes.update(self.mfile._variables)

        for t in nodes.values():
            dag.add_node(t)

        dag.add_node(self.exporter)

        for t in self.mfile._workflow._tasks.values():
            for ta in t.arguments.values():
                dag.add_edge(ta.linked_from.task,
                             ta.linked_to.task,
                             ref=ta)

        for ta in self.exporter.arguments.values():
            dag.add_edge(ta.linked_from.task,
                         ta.linked_to.task, ref=ta)

        return dag

    @property
    def dag(self):
        if not self._dag:
            self._dag = self._build()
        return self._dag
