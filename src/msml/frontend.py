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


"""
Frontend - cli interface of msml

This modules offers an easy way to interact with the
MSML system (Alphabet, Pipeline). You can see it as an
entry point, where you can access to various subsystem.


"""

from __future__ import print_function

from .env import *

# need first step caused of sys.path
# this is terrible to execute on module load
# but else we do not have chance for changing
# sys.path for initialization in msml.sorts

load_envconfig()

from .analytics.alphabet_analytics import *

from . import log

from collections import OrderedDict
from msml.run.GraphDotWriter import *
from msml.run import DefaultGraphBuilder

import os

import msml
import msml.env
import msml.model
import msml.run
import msml.xml
import msml.exporter
import argparse

__all__ = ["App", "main"]
__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

prolog = """
                             _
                            | | Medical
  _ __ ___   ___  _ __ ___  | | Simulation
 | '_ ` _ \ / __|| '_ ` _ \ | | Markup
 | | | | | |\__ \| | | | | || | Language
 |_| |_| |_||___/|_| |_| |_||_|
"""
from .package import *
from path import path

DEFAULT_REPOSITORIES = [MSML_REPOSITORY_FILENAME, "~/.config/msml/%s" % MSML_REPOSITORY_FILENAME]


def create_argument_parser():
    class KeyValueAction(argparse.Action):
        def __init__(self, option_strings, dest, nargs=None, **kwargs):
            if nargs is None:
                raise ValueError("KeyValue action is only for nargs!")

            super(KeyValueAction, self).__init__(option_strings, dest, nargs, **kwargs)

        def __call__(self, parser, namespace, values, option_string=None):
            if hasattr(namespace, self.dest):
                d = getattr(namespace, self.dest)
            else:
                d = {}

            for val in values:
                try:
                    k, v = val.split(":")
                    d[k] = v
                except:
                    raise ValueError("Can not split up %s. Expected 'key:value'" % val)

            setattr(namespace, self.dest, d)


    parser = argparse.ArgumentParser("msml.py",
                                     usage=None,
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=prolog)

    parser.add_argument("-v", '--verbose', dest="verbosity", action="count",
                        help="select the verbosity of this program")

    parser.add_argument('--rc', metavar='FILE', type=str,
                        default="~/.config/msmlrc.py",
                        help="overwrite the default rc file [default: ~/.config/msmlrc.py]")

    parser.add_argument('--alphabet-dir', metavar="PATH", nargs='*', type=str, dest='alphabet_dirs',
                        help="loads an specific alphabet dir")

    parser.add_argument('--operator-dir', metavar='FOLDER', nargs='*', type=str, dest='operator_dirs',
                        help="path to search for additional python modules")

    sub_parser = parser.add_subparsers(help="sub command help")

    # execution
    exec_parser = sub_parser.add_parser("exec", help="specifies the command to be executed")
    exec_parser.set_defaults(which="exec")

    exec_parser.add_argument('-o', '--output', metavar='FOLDER', dest='output_folder', action='store',
                             help="output directory for all generated data")

    exec_parser.add_argument('-e', '--exporter', dest='exporter', metavar='EXPORTER', action='store',
                             help='select the wanted exporter', choices=set(msml.exporter.get_known_exporters()))

    exec_parser.add_argument('-r', '--runner', dest='executor', metavar='EXECUTER', action='store',
                             default='sequential',
                             help='select the wanted executor', choices=set(msml.run.get_known_executors()))

    exec_parser.add_argument("-E", "--exopt", nargs="+", default=dict(), dest="exporter_options",
                             metavar='key:val', action=KeyValueAction)

    exec_parser.add_argument("-R", "--runopt", nargs="+", default=dict(), dest="executor_options",
                             metavar='key:val', action=KeyValueAction)

    exec_parser.add_argument("--repository", nargs="+", default=list(), dest="repositories",
                             metavar="FOLDER", action="store",
                             help="specifies msml user repositories with alphabet definition")

    exec_parser.add_argument("-p", "--package", nargs="+", default=list(), dest="packages",
                             metavar="FOLDER", action="store",
                             help="specifies msml user repositories with alphabet definition")

    exec_parser.add_argument('-m', '--variables', metavar="FILE", dest="memoryfile", action="store",
                             help="predefined memory content")

    exec_parser.add_argument('files', metavar="FILES", nargs='+', help="MSML files to be executed")

    # show
    show_parser = sub_parser.add_parser('show', help="prints out the build graph")
    show_parser.set_defaults(which="show")
    show_parser.add_argument('-e', '--exporter', dest='exporter', metavar='EXPORTER', action='store',
                             help='select the wanted exporter', choices=set(msml.exporter.get_known_exporters()))

    show_parser.add_argument('files', metavar="FILES", nargs='+', help="MSML files to be executed")

    show_parser = sub_parser.add_parser('show', help="prints out the build graph")
    show_parser.set_defaults(which="show")
    show_parser.add_argument('-e', '--exporter', dest='exporter', metavar='EXPORTER', action='store',
                             help='select the wanted exporter', choices=set(msml.exporter.get_known_exporters()))

    show_parser.add_argument('files', metavar="FILES", nargs='+', help="MSML files to be executed")

    # cli
    cli_parser = sub_parser.add_parser('cli', help="convert to cli")
    cli_parser.set_defaults(which="cli")
    cli_parser.add_argument('files', metavar="FILES", nargs='+', help="MSML files to be executed")
    cli_parser.add_argument('-e', '--exporter', dest='exporter', metavar='EXPORTER', action='store',
                            help='select the wanted exporter', choices=set(msml.exporter.get_known_exporters()))

    cli_parser.add_argument('-o', '--output', metavar='FOLDER', dest='output_folder', action='store',
                            help="output directory for all generated data")

    cli_parser.add_argument('-r', '--runner', dest='executor', metavar='EXECUTER', action='store',
                            default='sequential',
                            help='select the wanted executor', choices=set(msml.run.get_known_executors()))

    cli_parser.add_argument("-E", "--exopt", nargs="+", default=dict(), dest="exporter_options",
                            metavar='key:val', action=KeyValueAction)

    cli_parser.add_argument("-R", "--runopt", nargs="+", default=dict(), dest="executor_options",
                            metavar='key:val', action=KeyValueAction)

    cli_parser.add_argument("--repository", nargs="+", default=list(), dest="repositories",
                            metavar="FOLDER", action="store",
                            help="specifies msml user repositories with alphabet definition")

    cli_parser.add_argument("-p", "--package", nargs="+", default=list(), dest="packages",
                            metavar="FOLDER", action="store",
                            help="specifies msml user repositories with alphabet definition")

    cli_parser.add_argument('-m', '--variables', metavar="FILE", dest="memoryfile", action="store",
                            help="predefined memory content")

    # validate
    validate_parser = sub_parser.add_parser('validate', help="validates the current msml environment")
    validate_parser.set_defaults(which="validate")

    # expy
    expy_parser = sub_parser.add_parser('expy', help="transforms msml files into Python")
    expy_parser.set_defaults(which="expy")
    expy_parser.add_argument('-e', '--exporter', dest='exporter', metavar='EXPORTER', action='store',
                             help='select the wanted exporter', choices=set(msml.exporter.get_known_exporters()))
    expy_parser.add_argument('files', metavar="FILES", nargs='+', help="MSML files to be executed")
    return parser


def _parse_keyvalue_options(list_str):
    options = {}
    for s in list_str:
        if "=" in s:
            k, v = s.split("=")
            options[k] = v
        else:
            options[s] = True
    return options


def _load_class(cl):
    d = cl.rfind(".")
    classname = cl[d + 1:len(cl)]
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

    def __init__(self, novalidate=False, files=None, exporter="sofa", add_search_path=None,
                 add_operator_path=None, memory_init_file=None, output_dir=None, executor=None,
                 execution_options=None, exporter_options=None,
                 seq_parallel=True, repositories=None,
                 packages=None,
                 options=None, **kwargs):

        options = dict(options if options else {})  # create copy
        options.update(kwargs)
        self._options = options

        self._exporter = options.get("exporter") or exporter
        self._executor = executor or options.get('executor')

        self._files = options.get('files') or files or list()
        self._additional_alphabet_path = options.get('alphabetdir') or add_search_path or list()
        self._additional_operator_search_path = options.get('operatorpath') or add_operator_path or list()

        self.output_dir = output_dir or options.get('output')
        self._seq_parallel = seq_parallel or options.get('seqparallel')

        self._novalidate = novalidate

        self._memory_init_file = memory_init_file or options.get('memoryfile')

        self._executor_options = execution_options or options.get('executor_options', {})
        self._exporter_options = exporter_options or options.get('exporter_options', {})

        self._output_dir = output_dir or options.get('output_folder', None)

        self._repositories = repositories or options.get('repositories', [])
        self._packages = packages or options.get('repositories', [])

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

        self._init_repositories_and_packages()

        self._load_alphabet()

        if not self._novalidate:
            self.alphabet.validate()

    def _init_repositories_and_packages(self):
        # loading repositories incl. defaults
        effective_repositories = list(self._repositories)
        effective_repositories += DEFAULT_REPOSITORIES

        metarepo = Repository(path("."))
        metarepo.add_imports(*effective_repositories)
        packages = metarepo.resolve_packages()

        # include single packages, useful for testing
        for pth in self._packages:
            try:
                p = Package.from_file(pth)
                packages.insert(0, p)
            except FileNotFoundError:
                log.error("Explicit given package %s could not be loaded: Not found", pth)

        # msml default package at first place
        # weigl, it is now down in load
        #try:
        #    packages.insert(0, Package.from_file(MSML_DEFAULT_PACKAGE))
        #except FileNotFoundError:
        #    log.fatal("The MSML default operator are not available, the package file %s is missing",
        #              MSML_DEFAULT_PACKAGE)
        #    sys.exit(100)

        for p in packages:
            log.info("Activate %s", p)
        alpha, bin, py, rc = get_concrete_paths(packages)

        for f in rc:
            execfile(f, {'app': self})

        log.debug("Register alphabet dir: %s", alpha)
        self.additional_alphabet_dir += clean_paths(alpha)

        log.debug("Add to Python path: %s", py)
        sys.path += clean_paths(py)

        log.debug("Binary Path %s", bin)
        msml.env.binary_search_path += clean_paths(bin)

        log.debug("--")
        log.debug("Alphabet Path: %s", msml.env.alphabet_search_paths)
        log.debug("Python Path: %s", sys.path)
        log.debug("Binary Path: %s", msml.env.binary_search_path)
        log.debug("--")

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
    def executor(self):
        """returns a function that creates an
        :py:class:`msml.run.Executor`

        Currently is return :py:class:`msml.run.LinearSequenceExecutor`

        If you want an other executor, you should inherit this class
        and override this property.

        """
        return self._executor


    def get_executor(self, msml_file):
        self._prepare_msml_model(msml_file)

        execlazz = msml.run.get_executor(self.executor)

        # change to msml-file dirname
        os.chdir(msml_file.filename.dirname().abspath())
        _executor = execlazz(msml_file)
        _executor.options = self._executor_options
        _executor.working_dir = self.output_dir
        _executor.seq_parallel = self._seq_parallel
        _executor.init_memory(self.memory_init_file)

        return _executor


    def _load_msml_file(self, filename):
        mfile = msml.xml.load_msml_file(filename)
        return mfile

    def _prepare_msml_model(self, mfile):
        mfile.bind()
        exporter = self.exporter(mfile)
        mfile.exporter = exporter
        # validate is needed for simulation execution, removed if condition "if not self._novalidate:"
        mfile.validate(msml.env.CURRENT_ALPHABET)

        exporter._match_features()

    def show(self, msml_file=None):
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
        log.info("File %s written." % newname)

    def execute_msml_file(self, fil):
        mfile = self._load_msml_file(fil)
        log.info("Execute: %s in %s" % (fil, fil.dirname))
        return self.execute_msml(mfile)

    def execute_msml(self, msml_file):
        exe = self.get_executor(msml_file)
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
        log.info("READING alphabet...")

        msml.env.alphabet_search_paths += self._additional_alphabet_path
        log.info("Alphabet Paths: %s", msml.env.alphabet_search_paths)
        files = msml.env.gather_alphabet_files()
        log.info("found %d xml files in the alphabet search path" % len(files))
        alphabet = msml.xml.load_alphabet(file_list=files)

        msml.env.CURRENT_ALPHABET = alphabet
        self._alphabet = alphabet
        return alphabet

    def writexsd(self):
        """generation of a XSD for the current alphabet.

        The xsd is written  `'<XSDFile>` in the given `option` argument.
        """
        import msml.analytics.schema_creator

        content = msml.analytics.schema_creator.xsd(self.alphabet)
        with open(self._options['<XSDFile>'], 'w') as fp:
            fp.write(content)
            print(content)

    def check_file(self):
        for f in self.files:
            try:
                self._load_msml_file(f)
                log.info(f)
            except msml.model.MSMLError as e:
                log.error(f, e)

    def validate(self):
        """validation of the alphabet via the :py:mod:`msml.analytics`

        prints out a report of found warnings and errors
        """
        for r in check_element_completeness(self.alphabet, ELEMENT_DEFAULT_VALIDATORS):
            print(r)
            # print(export_alphabet_overview_rst(self.alphabet))


    def cli(self):
        from .api import clisupport

        for f in self.files:
            m = self._load_msml_file(f)
            self._prepare_msml_model(m)
            c = clisupport.GenerateCLIFromMSML(m)

            c.executor = self.executor
            c.executor_options = self._executor_options
            c.exporter_options = self._exporter_options
            c.exporter = self.exporter
            c.memory = self.memory_init_file
            c.packages = self._packages
            c.repositories = self._repositories

            c.generate(path(f).namebase + ".py", [])

    def _exec(self):
        COMMANDS = OrderedDict({'show': self.show,
                                'exec': self.execution,
                                'validate': self.validate,
                                'expy': self.expy,
                                'cli': self.cli,
                                'writexsd': self.writexsd,
                                'check': self.check_file})
        cmd = self._options["which"]
        if cmd in COMMANDS:
            COMMANDS[cmd]()
        else:
            log.error("Could not find application: %s" % cmd)


def main(args=None):
    """main entry of the `msml.py`

    You can all it with command line.
    For more control refer to :py:class:`App`.
    """

    if args is None:
        parser = create_argument_parser()
        ns = parser.parse_args()
        args = vars(ns)

    log.set_verbosity(
        "WARNING" if ns.verbosity == 1 else
        "INFO" if ns.verbosity == 2 else
        "DEBUG" if ns.verbosity == 3 else
        "ERROR")

    log.debug("cli arguments: %s", args)

    app = App(options=args)
    app._exec()
