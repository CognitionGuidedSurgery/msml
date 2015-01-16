# -*- encoding: utf-8 -*-
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


"""
Environment things, such as defining alphabet search path, 
defining msml-wide options and user configuration
"""

__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

import os
import sys

from path import path

from . import log

# msml alphabet search path
alphabet_search_paths = list()

# the current alphabet
CURRENT_ALPHABET = None

# path where the msml file resides
msml_file_path = None

def load_envconfig():
    """

    :return:
    """
    env_path = path(__file__)

    import msml.envconfig as C
    import sys

    #Add windows paths to python path - Python sometimes only checks this directories for dependencies (e.g. boost dlls)
    win_path = os.environ.get('path')
    if win_path is not None:
        win_paths = win_path.split(';')
        for currentPath in win_paths:
            sys.path.append(currentPath)


def load_user_file(loc="~/.config/msmlrc.py"):
    """load user rc file.

    The user can load custom python code into the msml workflow with the rc file.
    The rc file lies per default in `~/.config/msmlrc.py`, but can be given on the command line interface.

    The scope in the file is only `alphabet_search_path`

    :return: nothing
    :rtype: NoneType
    """
    global alphabet_search_paths
    loc = path(loc).expanduser()
    if loc.exists():
        execfile(loc, {"alphabet_search_path": alphabet_search_paths})


def gather_alphabet_files():
    """finds all xml files in the `alphabet_search_paths`
    :return: list of all xml files in the `alphabet_search_paths`
    :rtype: list[path.path]
    """
    files = []
    for loc in alphabet_search_paths:
        loc = path(loc)
        if loc.isfile():
            files.append(loc)
        else:
            files += loc.walkfiles("*.xml", errors='ignore')
    return files


def load_alphabet(fil="alphabet.cache"):
    """Loads an alphabet from a pickled file
    :param fil:
    :return: Alphabet
    """
    import msml.model.alphabet.Alphabet

    filename = path(fil).expanduser().expandvars()

    if filename.exists():
        global CURRENT_ALPHABET
        CURRENT_ALPHABET = msml.model.alphabet.Alphabet.load(filename)
        return CURRENT_ALPHABET
    else:
        log.warn("WARNING: alphabet file »%s« not found, please run msml.py alphabet" % fil)
        return None


class _BinarySearchPath(list):
    def __init__(self):
        super(_BinarySearchPath, self).__init__()
        self.add_paths(os.environ['PATH'])

    def _ensure_paths(self):
        for i in len(self):
            self[i] = path(self[i])

    def __str__(self):
        return ':'.join(self)

    def add_paths(self, string):
        """append all paths given as a string
        Seperator is ":" on linux, windows ";"
        """
        sep = ';' if sys.platform == 'win32' else ':'
        for p in string.split(sep):
            self.append(path(p))

    def find_executable(self, name):
        """finds the absolute executable path for the given `name

        If names contains spaces, the first token is taken.

        :param name:
         :type name: str
        :return:
        """
        name = name.strip()
        pos = name.find(' ')
        if pos > 0:
            name = name[:pos+1]

        for p in self:
            test = p/name
            test_win = p/name + '.exe'
            if test.exists() or test_win.exists():
                return test.abspath()
        return None

binary_search_path = _BinarySearchPath()
