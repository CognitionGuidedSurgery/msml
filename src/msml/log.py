# encoding: utf-8
# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
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


"""This module provide basic logging facilities in color.
"""

__author__ = "Alexander Weigl"
__date__ = "2014-05-05"

import inspect
import os.path

try:
    import colorama
    colorama.init()
except:
    pass

__all__ = ['report', '_reported']

COLOR_TABLE = {'I': 94, 'W': 33, 'E': 31, 'D': 90, 'F': 35}

FORMAT = "{color}{type}-{number:04d}: {msg} {grey}(from {file}:{lineno}){nocolor}"

_reported = []

def report(msg, kind="W", number=0, filename=None, lineno=-1):
    """prints a report information on stdout

    if `filename` is empty, the method tries to find the source of the caller.

    :param msg: Message
    :type msg: str
    :param kind: I, W, E, D, F -- kind of message
    :param number: some random error number
    :param filename: a filename (location of event)
    :param lineno: a line number (location of event)
    :return:
    """
    if not filename:
        frame = inspect.stack()[1][0]
        info = inspect.getframeinfo(frame)

        color = COLOR_TABLE.get(kind, 0)

        filename = os.path.basename(info.filename)
        lineno = info.lineno
        if filename == "__init__.py":
            filename = os.path.join(os.path.basename(
                os.path.dirname(info.filename)), filename)

    _reported.append((kind, number, lineno, filename, msg))

    print FORMAT.format(
        type=kind,
        number=number,
        lineno=lineno,
        file=filename,
        msg=msg,
        color="\x1b[%dm" % color,
        nocolor="\x1b[0m",
        grey="\x1b[37m"
    )
