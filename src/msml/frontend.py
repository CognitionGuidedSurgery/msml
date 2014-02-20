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
