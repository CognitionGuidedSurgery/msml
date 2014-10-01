import operator
import functools
import contextlib
from msml import generators

from msml.model import *
from msml.frontend import *

ACTIVE_APP = App()

generate_name = generators.IdentifierGenerator("gen_")

def parse_attrib(kwargs):
    attrib = {}
    for k,v in kwargs.items():
        attrib[k] = v
        if isinstance(v, Task):
            attrib[k] = v.output_default
    return attrib

class WorkflowBuilderBase(object):
    def __init__(self):
        self._wf = Workflow()

    def __getattr__(self, item):
        return self.get_operator(item)

    def __getitem__(self, item):
        return self.get_operator(item)

    def get_operator(self, name):
        return functools.partial(self.create_task, ACTIVE_APP.alphabet.operators[name])

    def create_task(self, operator, **kwargs):
        if 'id' not in kwargs:
            kwargs["id"] = generate_name()

        task = Task(operator.name, parse_attrib(kwargs))
        for out in operator.output_names():
            setattr(task, out, "${%s.%s}" % (id, out))

        if operator.output_names():
            setattr(task, 'output_default', "${%s.%s}" % (id, operator.output_names()[0]))

        self.workflow.add_task(task)
        return task

    @property
    def workflow(self):
        return self._wf

def create_object_element(name, **kwargs):
    kwargs['__tag__'] = name
    oe = ObjectElement(parse_attrib(kwargs))
    oe.bind(ACTIVE_APP.alphabet)
    return oe


def __list2dict(l, attribute):
    a = operator.attrgetter(attribute)
    return {a(i): i for i in l}

def as_operator(input=[], output=[], parameters=[]):
    def construct(func):
        name = func.func_name
        op = PythonOperator(name, __list2dict(input), __list2dict(output), __list2dict(parameters))
        op.function_name = name
        op.modul_name = "<unknown>"
        op.function = func
        return op

    return construct


class TaskDummyResult(object):
    """Base class for return task id and output slot names.

    """
    def __init__(self, task):
        self._task = task

    @property
    def task_id(self):
        return self._task.id