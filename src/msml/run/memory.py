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


__author__ = 'Alexander Weigl <uiduw@student.kit.edu>'

import pprint

from ..model import parse_attribute_value, MSMLVariable

class MemoryError(Exception):
    """Generic Memory Error.
    """
    pass


class MemoryTypeMismatchError(MemoryError):
    """Raises if the type of the given value does not match the pinned type in the memory"""
    pass


class MemoryVariableUnknownError(MemoryError):
    """Raises if given variable is not in the memory"""
    pass


class Memory(object):
    """The memory encapsulate dict helpers.

    :param predefine_variables: a dict of predefined values for
                                the internal memory

    :type predefine_variables: dict[str, object]

    """
    def __init__(self, predefine_variables={}):
        self._internal = {}  # stores the variable value
        self._meta = {}  # stores the metadata for each variable name

    def __getitem__(self, item):
        """get value from memory (raw access)"""
        return self._internal[item]

    def __setitem__(self, key, value):
        """set value into memory (raw access)"""
        # TODO compatibility of variable and metadata (if meta is set)
        r = self._internal[key] = value
        return r

    def __contains__(self, item):
        return self._internal.__contains__(item)

    def is_compatible(self, name):
        #TODO
        pass

    def reset(self):
        """empties the internal memory"""
        self._internal = {}

    def load_memory_file(self, filename):
        """load the given file into the internal dict.

        The given `filename` is executed and the defined
        variables will be set into the internal memory.

        :param filename: a path to a python (executable) file
        :type filename:" str

        """
        mem = {}
        execfile(filename, mem)
        self._internal.update(mem)

    def show_content(self):
        """pretty print the internal dict to console"""
        pprint.pprint(self._internal)

    def lookup(self, reference):
        """lookup a reference

        A refernce consists of task and slot name.
        This method handles:

        :str: e.g. "${taskA.slotB}" via
              :py:func:`msml.model.parse_attribute_value`
        :MSMLVariable:
        :Reference:


        :param reference: a reference to task and slot
        :type reference: str or msml.model.Reference

        """
        if isinstance(reference, str):
            reference = parse_attribute_value(reference)

        if isinstance(reference.linked_from.task, MSMLVariable):
            return self[reference.linked_from.task.name]

        return self[reference.linked_from.task.id][reference.linked_from.name]
