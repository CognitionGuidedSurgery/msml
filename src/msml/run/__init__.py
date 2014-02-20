__author__ = "Alexander Weigl"
__date__ = "2014-01-26"

from .memory import Memory

from msml.model import *
from msml.model.dag import DiGraph
from msml.exporter.base import Exporter
from msml.run.GraphDotWriter import GraphDotWriter


class Executer(object):
    pass


class LinearSequenceExecuter(Executer):
    def __init__(self, msmlfile):
        self._mfile = msmlfile
        self._memory = Memory()
        self._exporter = self._mfile.exporter

    def define_var(self, name, value=None):
        self._memory[name] = value

    def run(self):
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
        self._exporter.init_exec(self)
        self._exporter.render()


    def _execute_variable(self, node):
        "node is MSMLVariable"
        self.define_var(node.name, node.value)


    def _execute_operator_task(self, task):
        kwargs = self.gather_arguments(task)
        result = task.operator(**kwargs)
        self._memory[task.id] = result


    def gather_arguments(self, task):
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
