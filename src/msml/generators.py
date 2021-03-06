# encoding: utf-8
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


"""This module provide functions for generating names.


"""

__author__ = "Alexander Weigl"
__date__ = "2014-06-06"


class IdentifierGenerator(object):
    """Generates identifier with a given `prefix` and `suffx`.

    An instance can check, if the generated name was generated by him.

    The counter starts by 1.

    :param str prefix: prefix string
    :param str suffix: suffix string


    >>> g = IdentifierGenerator('a', 'b')
    >>> g()
    "a1b"
    >>> a = g()
    >>> a
    "a2b"
    >>> g.has_generated(a)
    True
    >>> g.has_generated('a3b')
    False

    """

    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix
        self._counter = 0

    def __repr__(self):
        return "msml.generators.IdentifierGenerator(%s, %s)" % (
            repr(self.prefix), repr(self.suffix))


    def __call__(self):
        """generates an (unused) identifier

        :returns: identifier
        :rtype: str
        """
        self._counter += 1
        return "%s%d%s" % (self.prefix, self._counter, self.suffix)

    def reset(self):
        """resets the counter to zero"""
        self._counter = 0

    def has_generated(self, value):
        """ checks if the value was generated by this instance

        :param value:
        :type value: str
        :return:
        :rtype: bool
        """

        if value.startswith(self.prefix) and value.endswith(self.suffix):
            try:
                cntval = int(value[len(self.prefix): - len(self.suffix)])
                return cntval <= self._counter
            except:
                pass
        return False


generate_task_id = IdentifierGenerator("converter_task_")
"""generator for converter task ids

:type: :py:class:`msml.generators.IdentifierGenerator`
"""

generate_variable = IdentifierGenerator("gen_", '_')
"""generator for converter task ids

:type: :py:class:`msml.generators.IdentifierGenerator`
"""

generate_identifier = IdentifierGenerator('id')
"""generator for converter task ids

:type: :py:class:`msml.generators.IdentifierGenerator`
"""


def reset_all():
    """reset all here defined generators

    .. warning::

       This function is for testing purpose.

    """
    generate_task_id.reset()
    generate_variable.reset()
    generate_identifier.reset()
