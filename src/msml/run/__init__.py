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

"""This class summaries functions for executing the pipeline.


"""

__author__ = "Alexander Weigl"
__date__ = "2014-01-26"

import abc

from path import path

from .memory import Memory
from .GraphDotWriter import GraphDotWriter
from ..model import *
from ..generators import generate_task_id
from ..exporter import Exporter
from ..exceptions import *
from .. import log
from ..sorts import conversion
import msml.sortdef
from .reruncheck import ReRunCheck


__all__ = ['Executor', 'Memory',
           'build_graph', 'create_conversion_task',
           'get_python_conversion_operator', 'initialize_file_literals',
           'inject_implict_conversion',
           'GraphDotWriter', 'DefaultGraphBuilder',
           # 'MemoryError', 'MemoryTypeMismatchError',
           #'MemoryVariableUnknownError',
           'LinearSequenceExecutor']


class Executor(object):
    """Describes the interface of an Executer.

    An Executer is responsible for calling the operator with the
    right arguments and parameters in the right order.
    Additionally it invokes the :py:class:`msml.exporter.Exporter`.

    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, msmlfile):
        self._msmlfile = msmlfile
        self._options = None

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def init_memory(self, content):
        pass


class AbstractExecutor(Executor):
    def __init__(self, msmlfile):
        super(AbstractExecutor, self).__init__(msmlfile)
        self._memory = Memory()
        self._exporter = self._msmlfile.exporter
        self.working_dir = None

    def init_memory(self, content):
        if isinstance(content, str):
            self._memory.reset()
            self._memory.load_memory_file(content)
        elif isinstance(content, dict):
            self._memory._internal.update(content)
        elif content:
            log.fatal("init_memory handles only filenames")

    def define_var(self, name, value=None):
        """defines a variable in the current memory.

        Args:
          name (str): variable identifier
          value (object): any value of variable

        """
        if name not in self._memory:  # do not override
            self._memory[name] = value


class LinearSequenceExecutor(AbstractExecutor):
    """ The LinearSequenceExecuter executes the given MSMLFile
    in one sequence with no parallelism in topological order.
    """

    def _prepare(self):
        """prepares the exeuction of the workflow.

        * bulding dag
        * initialize file literals
        * changing into working dir

        :return: the buckets to be executed
        """

        dag = DefaultGraphBuilder(self._msmlfile, self._exporter).dag
        buckets = dag.toporder()

        # make absolute paths for every string/file literal
        # wd is msml file dirname
        initialize_file_literals(buckets[0])


        #if there is no working dir, infer one
        if self.working_dir is None:
            self.working_dir = "out_" + self._msmlfile.filename.namebase

        # change to output_dir
        if self.working_dir:
            wd = path(self.working_dir)
            try:
                wd.mkdir()
            except:
                pass
            finally:
                wd.chdir()

        return buckets

    def run(self):
        """starts the execution of the given MSMLFile
        """

        buckets = self._prepare()

        with ReRunCheck(path(".")) as self.rerun_check:
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
        ExecutorsHelper.render_exporter(self, self._exporter)
        update = ExecutorsHelper.execute_exporter(self._exporter)
        self._memory.update(update)

    def _execute_variable(self, node):
        log.info("Define variable %s := %r" % (node.name, node.value))
        self._memory.update(
            ExecutorsHelper.execute_variable(self._memory, node))

    def _execute_operator_task(self, task):
        new = ExecutorsHelper.execute_operator_task(self._memory, task)
        #new = ExecutorsHelper.execute_operator_task(self.rerun_check, self._memory, task)
        self._memory.update(new)


class PhaseExecutor(LinearSequenceExecutor):
    """ PhaseExecutor works similar to :py:class:`LinearSequenceExecutor`, but provides more control over the phases
    of pre-, postprocessing, render and execution of the exporter.

    **Options:**

    :PE.disable.variable:
        deactivates the execution of variable bucket

    :PE.disable.pre:
        deactivates the execution of preprocessing

    :PE.disable.sim:
        deactivates the rendering and execution of exporter (no output would be generated)

    :PE.disable.simexec:
        deactivates the execution of exporter

    :PE.disable.post:
        deactivates the execution of postprocessing

    """

    def __init__(self, msmlfile):
        super(PhaseExecutor, self).__init__(msmlfile)
        self.pre_bucket = list()
        self.var_bucket = list()
        self.sim_bucket = list()
        self.post_bucket = list()
        self._prepared = False


    def _prepare(self):
        buckets = super(PhaseExecutor, self)._prepare()

        is_pre = True

        for bucket in buckets:
            for node in bucket:
                if isinstance(node, Task):
                    if is_pre:
                        self.pre_bucket.append(node)
                    else:
                        self.post_bucket.append(node)

                elif isinstance(node, MSMLVariable):
                    self.var_bucket.append(node)
                elif isinstance(node, Exporter):
                    self.sim_bucket.append(node)
                    is_pre = False

        return buckets

    def run(self):
        """starts the execution of the given MSMLFile
        """

        self._prepare()

        if not bool(self.options.get('PE.disable.variable', False)):
            for node in self.var_bucket:
                self._execute_variable(node)

        if not bool(self.options.get('PE.disable.pre', False)):
            for node in self.pre_bucket:
                self._execute_operator_task(node)

        if not bool(self.options.get('PE.disable.sim', False)):
            for node in self.sim_bucket:
                self._execute_exporter(node)

        if not bool(self.options.get('PE.disable.post', False)):
            for node in self.post_bucket:
                self._execute_operator_task(node)

        return self._memory

    def update_variable(self, name, value):
        log.info("Update variable %s := %r" % (name, value))
        var = MSMLVariable(name, value=value)
        self._memory.update(
            ExecutorsHelper.execute_variable(self._memory, var, True))

    def _execute_operator_task(self, task):
        new = ExecutorsHelper.execute_operator_task(self._memory, task)
        self._memory.update(new)

    def _execute_exporter(self, node):
        ExecutorsHelper.render_exporter(self, self._exporter)
        if not bool(self.options.get('PE.disable.simexec', False)):
             update = ExecutorsHelper.execute_exporter(self._exporter)
             self._memory.update(update)



class ParallelExecutor(AbstractExecutor):
    """The `ParallelExecutor` makes everything faster,
    by burning your CPU to a new heat level.


    **Options:**

    :PaE.kind:
        select "thread" or "process" (uses threading or multiprocessing library)

    :PaE.cores:
        select maximal parallel threads.
    """

    def run(self):
        """

        :return:
        """

        kind = self.options.get('PaE.cores', 'thread')
        if kind == 'thread':
            from  multiprocessing.pool import ThreadPool as Pool
        elif kind == 'process':
            from multiprocessing import Pool
        else:
            log.fatal('You selected an unknown threading method: %s. Only "thread" or "process" are supported' % kind)
            return self._memory

        import multiprocessing

        max_threads = self.options.get('PaE.cores', multiprocessing.cpu_count())
        pool = Pool(max_threads)

        buckets = self._prepare()

        for b in buckets:
            updates = pool.map(self.execute_node, b)
            for update in updates:
                self._memory.update(update)

    def execute_node(self, b):
        for node in b:
            if isinstance(node, Task):
                return ExecutorsHelper.execute_operator_task(self._memory, node)
            elif isinstance(node, MSMLVariable):
                return ExecutorsHelper.execute_variable(self._memory, node)
            elif isinstance(node, Exporter):
                ExecutorsHelper.render_exporter(self, node)
                ExecutorsHelper.execute_exporter(node)


def build_graph(tasks, exporter, variables):
    """build the direct acyclic graph from the given arguments.

    :param list[Task] tasks: a list of :py:class:`msml.model.Task`
    :param Exporter exporter: the :py:class:`msml.exporter.Exporter`
       to be weaved int
    :param list[MSMLVariable] variables: :py:class:`MSMLVariable`

    :returns: a DAG for the execution
    :rtype: :py:class:`msml.model.DiGraph`

    .. warning::

       The graph building does not validate the dependencies or anything
       else. You have to do this before or after you used the function.
       E.g. :py:method:`msml.model.MSMLFile.validate`

    """

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


class ExecutorsHelper(object):
    """static methods needed by some executors

    """

    @staticmethod
    def render_exporter(executor, exporter):
        assert isinstance(exporter, Exporter)
        assert isinstance(executor, Executor)
        exporter.init_exec(executor)
        exporter.render()
        return dict()

    @staticmethod
    def execute_exporter(exporter):
        """You need to ensure, that `_render_exporter` is called, before this method.

        :param exporter:
        :return:
        """
        assert isinstance(exporter, Exporter)
        return exporter.execute()

    @staticmethod
    def execute_variable(memory, variable, overwrite=False):
        assert isinstance(memory, Memory)

        if (variable.name not in memory) or overwrite:
            return {variable.name: variable.value}


    @staticmethod
    def execute_operator_task(memory, task):
        kwargs = ExecutorsHelper.gather_arguments(memory, task)
        ExecutorsHelper.inject_target_filename(task, kwargs)
        log.info('Executing operator of task %s with arguments %r', task, kwargs)
        result = task.operator(**kwargs)
        log.info('--Executing operator of task %s done', task.id)

        return {task.id: result}

        # if task.id in memory and isinstance(memory[task.id], dict):
        # # converter case, only update the change values
        #   self._memory[task.id].update(result)
        # else:
        #    # set the values into memory
        #    self._memory[task.id] = result

    @staticmethod
    def execute_operator_task_if_needed(checker, memory, task):
        assert isinstance(checker, ReRunCheck)
        kwargs = ExecutorsHelper.gather_arguments(memory, task)
        ExecutorsHelper.inject_target_filename(task, kwargs)

        # quick shortcut for converter tasks
        if task.id.startswith("converter_task_"):
            result = task.operator(**kwargs)
        else:
            input_files = [kwargs[ifile] for ifile in task.operator.input_names()]
            try:
                output_files = task.operator.get_targets()[0]
                output_files = kwargs[output_files]
            except:
                output_files = None

            if checker.check(task.id, input_files, kwargs, output_files):
                log.info('Omitting execution of operator %s', task.id)
                result = checker.get_last_result(task.id)
            else:
                log.info('Executing operator of task %s with arguments %r', task, kwargs)
                result = task.operator(**kwargs)
                checker.set_last_result(task.id, result)
                log.info('--Executing operator of task %s done', task.id)

        return {task.id: result}

        # if task.id in memory and isinstance(memory[task.id], dict):
        #   # converter case, only update the change values
        #   self._memory[task.id].update(result)
        # else:
        #    # set the values into memory
        #    self._memory[task.id] = result


    @staticmethod
    def inject_target_filename(task, kwargs):
        targets = task.operator.get_targets()
        outputs = task.operator.output_names()

        for t,o in zip(targets, outputs):
            if t not in kwargs:    
                physical = task.operator.output[o].sort.physical        
                suffix = physical.__name__.lower()
                kwargs[t] = "{task_id}_{name}.{sfx}".format(
                    task_id=task.id, name=o, sfx=suffix)
                log.info("Output target generated of %s" % kwargs[t])

    @staticmethod
    def gather_arguments(memory, task):
        """ Finds and collect all needed input and parameters variables from the current memory.
        """
        arguments = task.arguments

        vals = {}
        for ref in arguments.values():
            outname = ref.linked_from.arginfo.name
            inname = ref.linked_to.arginfo.name

            if isinstance(ref.linked_from.task, MSMLVariable):
                outid = ref.linked_from.task.name
                vals[inname] = memory[outid]
            else:
                outid = ref.linked_from.task.id
                vals[inname] = memory[outid][outname]
        return vals


__EXECUTERS = {
    'parallel': ParallelExecutor,
    'sequential': LinearSequenceExecutor,
    'phase': PhaseExecutor,
}


def get_known_executors():
    return __EXECUTERS.keys()


def get_executor(name):
    return __EXECUTERS[name]


def inject_implict_conversion(dag):
    """Finds type mismatches on edges and injects suitable conversion operators

    .. warning::

       This function works and changes the given `dag`.

    :param dag: a directed acyclic graph from
                :py:func:`msml.run.build_graph`
    :type dag: :py:class:`msml.model.DiGraph`
    :return: the modified graph
    :rtype: msml.model.DiGraph
    """
    for a, b, data in dag.edges(data=True):
        ref = data['ref']
        if not ref.valid:
            log.info("Reference %s is invalid. Try to implicit conversion" % ref)
            task = create_conversion_task(ref.linked_from, ref.linked_to)

            # add new task
            dag.add_node(task)

            # remove the old edge
            dag.remove_edge(a, b)

            # from Task to Converter
            _a_t = Reference(ref.task, ref.slot)
            _a_t.linked_from = ref.linked_from
            _a_t.link_to_task(task, task.operator.input['i'])

            _t_b = Reference(ref.task, ref.slot)
            _t_b.linked_to = ref.linked_to
            _t_b.link_from_task(task, task.operator.output['o'])

            # override converted value
            # _t_b.link_from_task(task, task.operator.output[task.operator.output.keys()[0]])

            task.arguments['i'] = _a_t
            b.arguments[ref.linked_to.name] = _t_b

            dag.add_edge(a, task, ref=_a_t)
            dag.add_edge(task, b, ref=_t_b)

        else:
            log.debug("Reference %s is valid" % ref)
    return dag


def get_python_conversion_operator(slotA, slotB):
    """creates an :py:class:`msml.model.PythonOperator` for conversion
    from sort of `slotA` to sort of `slotB`

    :param slotA: slot on the outgoing side
    :type slotA: msml.model.Reference.Ref

    :param slotB: slot on the incoming side
    :type slotB: msml.model.Reference.Ref

    :returns: an callable conversion operator or none if types incompatible
    :rtype: msml.model.PythonOperator

    .. seealso::

       :py:class:`msml.sorts.ConversionNetwork`

    """
    r = {'function': '<automatic-converter>', 'module': '<module-name>'}

    pA = slotA.arginfo.sort.physical
    lA = slotA.arginfo.sort.logical

    pB = slotB.arginfo.sort.physical
    lB = slotB.arginfo.sort.logical

    pyop = PythonOperator(
        "converter_%s_%s" % (pA.__name__, pB.__name__),
        input=[Slot("i", pA, lA)],
        output=[Slot('o', pB, lB)], runtime=r)

    return pyop


def create_conversion_task(slotA, slotB):
    """creates a task (instance of operator) for the requested conversion.

    :param slotA:
    :type slotA: Reference.Ref
    :param slotB:
    :type slotB: Reference.Ref
    :return: a task, ready for embedding into the build graph
    :rtype: msml.model.Task
    """

    fn = conversion(slotA.arginfo.sort, slotB.arginfo.sort)
    if fn is None:
        raise MSMLError("Could not find an automatic Converter for %s to %s" % (slotA, slotB))

    pyop = get_python_conversion_operator(slotA, slotB)
    pyop._function = fn

    # the new task override the old one memory values
    attrib = {'id': generate_task_id(), 'i': None}
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
    """
    """

    def var_is_file(var):
        if isinstance(var, MSMLVariable):
            return issubclass(var.sort.physical, msml.sortdef.InFile)
            # return contains("file", var.logical_type) or contains("file", var.physical_type)
        return False

    def abs_value(var):
        import os.path

        var.value = os.path.abspath(var.value)
        return var

    return map(abs_value, filter(var_is_file, first_bucket))

