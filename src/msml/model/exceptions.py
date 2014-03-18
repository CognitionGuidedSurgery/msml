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

# region modul-doc
"""This module gather all global warnings, errors and exceptions:

  * Exception Hierarchy:
    for ``exception`` that are not allowed to happen regularly iff. the program was correct.
    Like type/format errors that should be checked by caller.

  * Error Hierarchy:
    for signaling mis-behaviour to the user. (e.g. missing files)

  * Warning hierarchy
    Things that should be an exception but, should not interrupt program flow.
    See: http://docs.python.org/2/library/warnings.html#warnings.warn for more information.
"""
# endregion

__author__ = 'Alexander Weigl'

##
# Exception

class MSMLException(Exception):
    pass


##
# Error

class MSMLError(Exception):
    pass


class BindError(Exception):
    pass


class MSMLXMLParseError(MSMLError):
    pass

##
# Warning

class MSMLWarning(Warning):
    pass


class MSMLXMlWarning(MSMLWarning):
    pass


class MSMLXMLUnknownTagWarning(MSMLWarning):
    pass


class MSMLOperatorWarning(MSMLWarning):
    pass


class MSMLUnknownFunctionWarning(MSMLOperatorWarning):
    pass


class MSMLUnknownModuleWarning(MSMLOperatorWarning):
    pass
