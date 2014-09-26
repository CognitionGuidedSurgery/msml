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

This modules offers an easy way to interact with the
MSML system (Alphabet, Pipeline). You can see it as an
entry point, where you can access to various subsystem.


"""

from __future__ import print_function

from .env import *
from msml.log import report

# need first step caused of sys.path
# this is terrible to execute on module load
# but else we do not have chance for changing
# sys.path for initialization in msml.sorts
load_envconfig()

from .analytics.alphabet_analytics import *


from collections import OrderedDict
from msml.run.GraphDotWriter import *
from msml.run import DefaultGraphBuilder

import os
from docopt import docopt
from path import path

import msml
import msml.env
import msml.model
import msml.run
import msml.xml
import msml.exporter


__all__ = ["App", "main"]
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
  msml exec [(-D D)...] [-w] [options] <file>...
  msml show     [options] <file>
  msml writexsd <XSDFile>
  msml check    [<file>...]
  msml validate
  msml expy     [options] [<file>...]

Options:
 -v, --verbose              verbose information on stdout [default: false]
 -o, --output=DIR           output directory
 --start-script=FILE        overwrite the default rc file [default: ~/.config/msmlrc.py]
 -a, --alphabet-dir=DIR     loads an specific alphabet dir
 --operator-dir             path to search for additional python modules
 -x, --xsd-file=FILE        xsd-file
 -e VALUE, --exporter=VALUE    set the exporter (base, nsofa, nabaqus) [default: base]
 -m FILE, --vars=FILE       predefined the memory content

"""

def _parse_keyvalue_options(list_str):
    options = {}
    for s in list_str:
        if "=" in s:
            k,v = s.split("=")
            options[k] = v
        else:
            options[s] = True
    return options

def _load_class(cl):
    d = cl.rfind(".")
    classname = cl[d+1:len(cl)]
    m = __import__(cl[0:d], globals(), locals(), [classname])
    return getattr(m, classname)



class App(object):
    """MSML App - interface for execute MSML files

    :param novalidate: if `True`, the validation of the loaded alphabet
                       is suppressed
    :type novalidate: bool

    :param files: list of msml files to be executed or `None`
    :type files: list[str]

    :param exporter: the name of the export,
                see also :py:func:`msml.exporter.get_exporter`
    :type exporter: str

    :param add_search_path: additional paths for the  alphabet search path
    :type add_search_path: list[str]

    :param add_operator_path: additional paths to
                        add into the :py:member:`sys.path`
    :type add_operator_path: list[str]

    :param memory_init_file: filename for initialize of
                            :py:class:`msml.run.memory.Memory`
    :type memory_init_file: str or path.path

    :param output_dir: set the given path as output dir
    :type output_dir: str

    :param options: options given by the command line (docopt).
    This values are only taken if the named argument is unset.
    :type options: dict[str, T]

    """
    def __init__(self, novalidate=False, files=None, exporter=None, add_search_path=None,
                 add_operator_path=None, memory_init_file=None, output_dir = None, options={}):
        self._exporter = options.get("--exporter") or exporter or "sofa"
        self._files = options.get('<file>') or files or list()
        self._additional_alphabet_path = options.get('--alphabet-dir') or add_search_path or list()
        self._additional_operator_search_path = options.get('--operator-path') or add_operator_path or list()
        self._options = options
        self.output_dir = output_dir or options.get('--output')
        self._novalidate = novalidate
        self._memory_init_file = memory_init_file
        self._executor_options = _parse_keyvalue_options(options.get('D', list()))

        assert isinstance(self._files, (list, tuple))
        self._alphabet = None
        self.init_msml_system()

    def init_msml_system(self):
        """initialize the msml system

        * called bye the constructor
        * loads the user file
        * load the alphabet
        * if `not self.novalidate` then the alphabet will be validated.
        """

        msml.env.load_user_file()
        self._load_alphabet()

        if not self._novalidate:
            self.alphabet.validate()

    @property
    def output_dir(self):
        """the output dir for all executions"""
        return self._output_dir

    @output_dir.setter
    def output_dir(self, o):
        if o:
            self._output_dir = path(o)
        else:
            self._output_dir = None

    @property
    def alphabet(self):
        """the used alphabet for all executions, *read-only*

           :type: msml.model.Alphabet
        """
        return self._alphabet

    @property
    def additional_alphabet_dir(self):
        """additional directory for loading the alphabet,
        only evaluated on :py:func:`App._load_alphabet`

        :type: list[str]
        """
        return self._additional_alphabet_path

    @additional_alphabet_dir.setter
    def additional_alphabet_dir(self, a):
        self._additional_alphabet_path = a

    @property
    def memory_init_file(self):
        """memory init file for initalization of the :py:class:`msml.run.Memory`.
        """
        return self._memory_init_file

    @memory_init_file.setter
    def memory_init_file(self, v):
        self._memory_init_file = v

    @property
    def exporter(self):
        return msml.exporter.get_exporter(self._exporter)

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files):
        self._files = files

    @property
    def executer(self):
        """returns a function that creates an
        :py:class:`msml.run.Executor`

        Currently is return :py:class:`msml.run.LinearSequenceExecutor`

        If you want an other executor, you should inherit this class
        and override this property.

        """
        if 'executor.class' in self._executor_options:
            return _load_class(self._executor_options['executor.class'])
        else:
            return msml.run.LinearSequenceExecutor

    def _load_msml_file(self, filename):
        mfile = msml.xml.load_msml_file(filename)
        return mfile

    def _prepare_msml_model(self, mfile):
        exporter = self.exporter(mfile)
        mfile.exporter = exporter
        #validate is needed for simulation execution, removed if condition "if not self._novalidate:"
        mfile.validate(msml.env.CURRENT_ALPHABET) 

    def show(self, msml_file = None):
        if not msml_file:
            msml_file = self._load_msml_file(self.files[0])
        elif isinstance(msml_file, str) or \
             isinstance(msml_file, unicode):
            msml_file = self._load_msml_file(msml_file)

        self._prepare_msml_model(msml_file)
        graphb = DefaultGraphBuilder(msml_file, msml_file.exporter)
        writer = GraphDotWriter(graphb.dag)

        newname = "%s.dot" % path(msml_file.filename).namebase
        newname = path(newname).abspath()
        with open(newname, 'w') as w:
            w.write(writer())
        report("File %s written." % newname)

    def execute_msml_file(self, fil):
        mfile = self._load_msml_file(fil)
        report("Execute: %s in %s" % (fil, fil.dirname),'I',20)
        return self.execute_msml(mfile)


    def execute_msml(self, msml_file):
        self._prepare_msml_model(msml_file)
        execlazz = self.executer

        # change to msml-file dirname
        os.chdir(msml_file.filename.dirname().abspath())
        exe = execlazz(msml_file)
        exe.options = self._executor_options
        exe.working_dir = self.output_dir
        exe.init_memory(self.memory_init_file)
        mem = exe.run()
        return mem

    def execution(self):
        files = self.files
        for fil in files:
            self.execute_msml_file(path(fil))

    def expy(self):
        """Transforms the given msml files into python scripts.

        ..seealso::
            :py:mod:`msml.run.exportpy`

        .. warning::

            The expy subsystem is not ready for production and will be moved
            to `msmllab`.


        """

        import msml.run.exportpy
        for fil in self.files:
            msml_file = self._load_msml_file(fil)
            self._prepare_msml_model(msml_file)
            msml.run.exportpy.exportpy(msml_file)

    def _load_alphabet(self):
        report("READING alphabet...", 'I')

        msml.env.alphabet_search_paths += self._additional_alphabet_path
        files = msml.env.gather_alphabet_files()
        report("found %d xml files in the alphabet search path" % len(files), 'I')
        alphabet = msml.xml.load_alphabet(file_list=files)

        # debug
        #        alphabet.print_nice()

        msml.env.CURRENT_ALPHABET = alphabet
        self._alphabet = alphabet
        return alphabet

    def writexsd(self):
        """generation of a XSD for the current alphabet.

        The xsd is written  `'<XSDFile>` in the given `option` argument.
        """
        import msml.analytics.schema_creator

        content = msml.analytics.schema_creator.xsd(self.alphabet)
        with open(self._options['<XSDFile>'],'w') as fp:
            fp.write(content)
            print(content)

    def check_file(self):
        for f in self.files:
            try:
                self._load_msml_file(f)
                print(f, "ok")
            except msml.model.MSMLError as e:
                print(f, "error")
                print("\t", e)

    def validate(self):
        """validation of the alphabet via the :py:mod:`msml.analytics`

        prints out a report of found warnings and errors
        """
        for r in check_element_completeness(self.alphabet, ELEMENT_DEFAULT_VALIDATORS):
            print(r)
        #print(export_alphabet_overview_rst(self.alphabet))


    def _exec(self):
        COMMANDS = OrderedDict({'show': self.show, 'exec': self.execution,
                                'validate': self.validate,
                                'expy':self.expy,
                                'writexsd': self.writexsd,
                                'check': self.check_file})

        # dispatch to COMMANDS
        for cmd, fn in COMMANDS.items():
            if self._options[cmd]:
                fn()
                break
        else:
            print("could not find a suitable command")


def main(args=None):
    """main entry of the `msml.py`

    You can call it with command line.
    For more control refer to :py:class:`App`.
    """

    if args is None:
        args = docopt(OPTIONS, version=msml.__version__)

    app = App(options=args)
    app._exec()
