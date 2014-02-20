__author__ = 'weigl'

import pprint

from ..model.base import parse_attribute_value


class MemoryError(Exception):
    pass


class MemoryTypeMismatchError(MemoryError):
    pass


class MemoryVariableUnknownError(MemoryError):
    pass


class Memory(object):
    def __init__(self, predefine_variables={}):
        self._internal = {}  # stores the variable value
        self._meta = {}  # stores the metadata for each variable name

    def __getitem__(self, item):
        return self._internal[item]

    def __setitem__(self, key, value):
        # TODO compatibility of variable and metadata (if meta is set)
        r = self._internal[key] = value
        return r

    def is_compatible(self, name):
        #TODO
        pass

    def load_memory_file(self, filename):
        mem = {}
        execfile(filename, mem)
        self._internal.update(mem)

    def show_content(self):
        pprint.pprint(self._internal)

    def lookup(self, reference):
        if isinstance(reference, str):
            reference = parse_attribute_value(reference)
        return self[reference.task][reference.slot]


