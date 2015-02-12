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

from collections import OrderedDict
import msml.sorts as sorts

__author__ = 'Alexander Weigl'

def _list_to_dict(lis, attrib='name'):
    if not lis:
        return OrderedDict()

    d = OrderedDict()
    for e in lis:
        d[getattr(e, attrib)] = e
    return d


class Operator(object):
    """Operator hold all slots, runtime information and meta data"""

    def __init__(self,
                 name,
                 input=None,
                 output=None,
                 parameters=None,
                 runtime=None,
                 settings=None,
                 meta=None):
        """Constructs an operator from the given arguments.
        :type name: str
        :type input: list
        :type output: list
        :type:parameters: list
        :type runtime: dict
        :type meta: dict
        """
        self.name = name

        self.input = _list_to_dict(input)
        """:type: dict"""

        self.output = _list_to_dict(output)
        """:type: dict"""

        self.parameters = _list_to_dict(parameters)
        """:type: dict"""

        self.meta = meta
        """:type: dict"""

        self.runtime = runtime
        """:type: dict"""

        if settings is None:
            settings = dict()
        self.settings = settings
        """:type: dict"""

        self._filename = None
        """filename of the xml file, which defined this operator
        :type: str"""

    def __str__(self): return "{Operator %s}" % self.name

    def output_names(self):
        """:returns all names of the output slots
        :rtype: list[str]
        """
        return self.output.keys()

    def input_names(self):
        """:returns all names of the input slots
        :rtype: list[str]
        """
        return self.input.keys()

    def parameter_names(self):
        """:returns all names of the parameter slots
        :rtype: list[str]
        """
        return self.parameters.keys()

    def acceptable_names(self):
        """all names of input or parameter slots
        :rtype: list[str]
        """
        return self.input_names() + self.parameter_names()

    def settings(self):
        """all settingss
        :rtype: list[str]
        """
        return self.settings

    def __contains__(self, attrib):
        """checks if attrib is a valid input or parameter name"""
        return attrib in self.input or attrib in self.parameters

    def __call__(self, *args, **env):
        """execution of this operator, with the given arguments"""
        pass

    def get_targets(self):
        return [p.name for p in self.parameters.values()
                if p.target]

    def validate(self):
        """validation of this operator
        :returns: True iff. this operator is well-defined
        :rtype: bool"""
        return True

    def get_default_args(self):
        defaults = dict()
        for x in self.parameters.values():
            if x.default is not None:
                defaults[x.name] = sorts.conversion(str, x.sort)(x.default)
        return defaults

# def check_types(self, args, kwargs):
# sig = signature(self.func)
# type_bind = sig.bind(*self.args)
# val_bind = sig.bind(*args)
#
# T = type_bind.args
# V = val_bind.args
#
# return issubtype(V, T)
#
# def _execute(self, *args, **kwargs):
# sig = signature(self.func)
#         fargs = sig.bind_partial(*args)  # , **kwargs)
#
#         if self.check_types(args, kwargs):
#             a = self.func(*fargs.args)
#             if not issubtype(a, self.out):
#                 raise BaseException("return types mismatch")
#             return a
#         else:
#             raise BaseException("argument type does not match defined types")





