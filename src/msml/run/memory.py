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


__author__ = 'Alexander Weigl'

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

    def __contains__(self, item):
        return self._internal.__contains__(item)


    def is_compatible(self, name):
        #TODO
        pass

    def reset(self):
        self._internal = {}

    def load_memory_file(self, filename):
        mem = {}
        execfile(filename, mem)
        self._internal.update(mem)

    def show_content(self):
        pprint.pprint(self._internal)

    def lookup(self, reference):
        if isinstance(reference, str):
            reference = parse_attribute_value(reference)
        return self[reference.linked_from.task.id][reference.linked_from.name]


