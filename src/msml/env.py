# -*- encoding: utf-8 -*-
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


"""
Environment things, such as defining alphabet search path, 
defining msml-wide options and user configuration
"""


__author__ = "Alexander Weigl"
__date__ = "2014-01-25"


from path import path
import os
from msml.model.alphabet import Alphabet, PythonOperator, Slot, SharedObjectOperator, ShellOperator

# msml alphabet search path
alphabet_search_paths = list()

# the current alphabet
current_alphabet = None

# path where the msml file resides
msml_file_path = None

def load_user_file(loc = "~/.config/msmlrc.py"):
    """load user rc file.

    The user can load custom python code into the msml workflow with the rc file.
    The rc file lies per default in `~/.config/msmlrc.py`, but can be given on the command line interface.

    The scope in the file is only `alphabet_search_path`

    :return: nothing
    :rtype: NoneType
    """
    global alphabet_search_paths
    loc = path(loc).expanduser()
    if loc.exists() and False:
        execfile(loc, {"alphabet_search_path" : alphabet_search_paths})
    else:
        env_path = path(__file__)
        alphabet__path = env_path.dirname() / '..' / '..' / 'share' / 'alphabet'
        alphabet_search_paths.append(alphabet__path)

        import msml.envconfig as C
        import sys
        #Import release and debug paths here?
        sys.path.append(C.operators_path)
        sys.path.append(C.operators_path_debug)
        sys.path.append(C.operators_path_release)

        #Add windows paths to python path - Python sometimes only checks this directories for dependencies (e.g. boost dlls)
        win_path = os.environ.get('path')
        if win_path is not None:
            win_paths = win_path.split(';')
            for currentPath in win_paths:
                sys.path.append(currentPath)

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
            files += loc.walkfiles("*.xml" , errors= 'warn')
    return files


def load_alphabet(fil = "alphabet.cache"):
    """Loads an alphabet from a pickled file
    :param fil:
    :return: Alphabet
    """
    p = path(fil).expanduser().expandvars()

    if p.exists():
        global current_alphabet
        current_alphabet = Alphabet.load(p);
        return current_alphabet
    else:
        print("WARNING: alphabet file »%s« not found, please run msml.py alphabet" % fil)
        return None

def _debug_install_operators():
    global current_alphabet
    current_alphabet = Alphabet()

    op_square = PythonOperator("square", [Slot('n', 'int', None, True)],
                                         [Slot('n', 'int', None, True)],
                                         runtime = {'exec':'python', 'module': 'test', 'function': 'square'})

    op_square.function = lambda n: int(n) ** 2

    op_output = PythonOperator("output", [Slot('object', '*', None, True)],
                                         runtime = {'exec':'python', 'module': 'pprint', 'function': 'pprint'})

    op_output.bind_function()
    
    op_ctype = SharedObjectOperator("ctime", None, [Slot('time', 'int', None, True)],
                        runtime = {'exec':'so', 'file': 'libc.so.6', 'symbol': 'time'})
    op_ctype.bind_function()

    op_id = ShellOperator("id", [Slot('name', 'string', None, True)],
                                         runtime = {'exec':'sh', 'template' : 'id {name}'})

    current_alphabet.append((op_square, op_output, op_ctype, op_id))

