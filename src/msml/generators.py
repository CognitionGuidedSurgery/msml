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


"""This module provide basic logging facilities in color.
"""

__author__ = "Alexander Weigl"
__date__ = "2014-06-06"


class IdentifierGenerator(object):
    def __init__(self, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix
        self._counter = 0

    def __call__(self):
        self._counter += 1
        return "%s%d%s" % (self.prefix, self._counter, self.suffix)

    def reset(self):
        self._counter = 0

    def has_generated(self, value):
        """

        :param value:
        :type value: str
        :return:
        """
        if value.startswith(self.prefix) and value.endswith(self.suffix):
            try:
                cntval = int(value[len(self.prefix): - len(self.suffix)])
                return cntval <= self._counter
            except:
                pass
        return False


generate_task_id = IdentifierGenerator("converter_task_")
generate_variable = IdentifierGenerator("gen_", '_')
generate_identifier = IdentifierGenerator('id')

def reset_all():
    generate_task_id.reset()
    generate_variable.reset()