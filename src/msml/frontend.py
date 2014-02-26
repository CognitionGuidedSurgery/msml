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
Frontend - cli interface of msml

"""

from __future__ import print_function

from collections import OrderedDict
import os

from docopt import docopt
from path import path

import msml
import msml.env
import msml.model
import msml.run
import msml.xml
import msml.exporter


__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

# please read: http://docopt.org/ for more information
OPTIONS = """
                                _
                               | | Medical
     _ __ ___   ___  _ __ ___  | | Simulation
    | '_ ` _ \ / __|| '_ ` _ \ | | Markup
    | | | | | |\__ \| | | | | || | Language
    |_| |_| |_||___/|_| |_| |_||_|

Usage:
  msml exec     [-w] [options] [<file>...]
  msml show     [options] [<file>...]
  msml alphabet [options] [-x XSDFile] [<paths>...] 

Options:  
 -v, --verbose              verbose information on stdout [default: false]
 -o, --output=FILE          output file
 --start-script=FILE        overwrite the default rc file [default: ~/.config/msmlrc.py]
 -a, --alphabet=FILE        loads a precalculated alphabet dump [default: alphabet.cache]
 -x, --xsd-file=FILE        xsd-file
 -S                         SKIP-loading alphabet dump, refresh alphabet on each start
 -e VALUE, --exporter=VALUE    set the exporter (base, sofa, abaqus) [default: base]

"""


def show(options):
    """
    """

    mfile = msml.xml.load_msml_file(fil)
    msml.env.current_alphabet.validate()
    mfile.validate(msml.env.current_alphabet)

    dag = mfile.get_dag()
    with open("test.dot", 'w') as w:
        w.write(dag.dot())
        print(dag.dot())


def execute_msml_file(fil, exporter_factory):
    mfile = msml.xml.load_msml_file(fil)
    msml.env.current_alphabet.validate()
    exporter = exporter_factory(mfile)
    mfile.exporter = exporter
    mfile.validate(msml.env.current_alphabet)

    print("Execute: %s in %s" % (fil, fil.dirname))
    fil = path(fil)
    os.chdir(fil.dirname().abspath())


    exe = msml.run.LinearSequenceExecuter(mfile)
    mem = exe.run()
    mem.show_content()


def execution(options):
    def trace(frame, event, arg):
        print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
        return trace

    #sys.settrace(trace)


    #debug msml.env._debug_install_operators()
    files = options['<file>']

    exporter_clazz = msml.exporter.get_exporter(options['--exporter'])

    for fil in files:
        thePath = path(fil)
        absPath = thePath.abspath()
        execute_msml_file(absPath, exporter_clazz)


def alphabet(options):
    "Create the alphabet from reading"

    print("READING alphabet...")

    if options['<paths>']:
        msml.env.alphabet_search_paths += options['<paths>']

    files = msml.env.gather_alphabet_files()
    print("found %d xml files in the alphabet search path" % len(files))

    # construct alphabet
    alphabet = msml.xml.load_alphabet(file_list=files)

    # debug
    print(alphabet)

    # save xsd file
    if options['--xsd-file']:
        with open(options['--xsd-file'], 'w') as xsd:
            xsd.write(alphabet._xsd())

    # save the alphabet dump (always set)
    if not options['-S'] and options['--alphabet']:
        alphabet.save(options['--alphabet'])

    return alphabet


COMMANDS = OrderedDict({'show': show, 'alphabet': alphabet, 'exec': execution})


def main():
    args = docopt(OPTIONS, version=msml.__version__)
    print(args)

    msml.env.load_user_file()

    if not args['-S']:
        msml.env.load_alphabet(args['--alphabet'])
    else:
        print("Skipping alphabet dump %s" % args['--alphabet'])
        msml.env.current_alphabet = alphabet(args)



    # dispatch to COMMANDS
    for cmd, fn in COMMANDS.items():
        if args[cmd]:
            fn(args)
            break;
    else:
        print("could not find a suitable command")
