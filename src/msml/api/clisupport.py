# -*- encoding: utf8 -*-

"""This module provides functionalities for using a MSML workflow as an CLI executable

Getting Started
===============

1. Test your workflow against MSML::

   $ msml.py exec [options] [workflows]

2. Create the »executables« with::

   $ msml.py cli [options] [workflows]

   with the same options as with `exec`

3. Add the executables to MITK or something else.


API
====

.. note::

    This module should not be used outside CLI invocations, because it changes the stdout and stderr on loading.

"""

__author__ = 'Alexander Weigl'
__date__ = "2015-03-21"

import sys
import os
from cStringIO import StringIO


class ConsoleCatcher(object):
    def __init__(self):
        self._active = not os.environ.get("MSML_DEBUG", False)
        self._true_channels = (sys.stdout, sys.stderr)
        if self._active:
            self._renew_cache()

    def _renew_cache(self):
        self._cached_channels = (StringIO(), StringIO())

    def _reset_stdio(self):
        """restores stdout and stderr, that were active while :py:func:`_overwrite_stdio` was called.

        Before restoring the both channels the catched values
        """
        if self._active:
            for real, cache in zip(self._true_channels, self._cached_channels):
                real.write(cache.getvalue())
            sys.stdout, sys.stderr = self._true_channels


    def _overwrite_stdio(self):
        """overwrites stdout and stderr with an :py:class:`StringIO.StringIO`
        file object if `MSML_DEBUG` is set in the environment.

        ugly hack for catching every output (logging) from this application during startup.
        If `--xml` arg is omitted we can print out the logging information.
        """
        if self._active:
            sys.stdout, sys.stderr = self._cached_channels


consolecatcher = ConsoleCatcher()
consolecatcher._overwrite_stdio()

# loading delayed
import jinja2, clictk
from msml.frontend import App
from msml.sortdef import InFile, MSMLListF, MSMLListI, Image
from msml import log

PYTHON = """#!{{python}} -W ignore

# Choose the right interpreter above for python dependencies
# given by the requirements of MSML

# This will load the ugly stdout hack and functionalities
# for producing cli xml + argument parsing
import sys
sys.path.append("{{msml_src}}")
from msml.api.clisupport import *


# absolute path to MSMLFILE
MSMLFILE = '{{ filename }}'

def main():
    cli_app(MSMLFILE,
        exporter="{{exporter}}",
        {% if memory_init_file %}
        memory_init_file={{ memory_init_file }},
        {% endif %}
        packages = {{ packages }},
        repositories = {{ repositories }},
        exporter_options= {{ exporter_options }},
        executor_options = {{ executor_options }}
    )

if __name__ == "__main__":
    main()
"""

# # <?xml version="1.0" encoding="utf-8"?>
# xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="/home/weigl/ctkCmdLineModule.xsd">
# XML = """<executable>
# <category>MSML.XXX</category>
#   <title>Test</title>
#   <description><![CDATA[]]></description>
#   <version>0.0.1</version>
#   <documentation-url>http://abc.de</documentation-url>
#   <license>abc</license>
#   <contributor>weigl</contributor>
#   <parameters>
#       <label>Parameters</label>
#       <description>...</description>
#     {% for p in parameters %}
#         <{{ p.tag }}>
#             <name>{{ p.name }}</name>
#             <longflag>{{ p.longflag }}</longflag>
#             <description>{{p.description}}</description>
#             <label>{% if p.label %}{{ p.label }}{%else%}{{ p.name }}{%endif%}</label>
#             {% if p.default%}<default>{{p.default}}</default>{% endif %}
#         </{{ p.tag }}>
#     {% endfor %}
#   </parameters>
# </executable>
# """

from ..sorts import conversion
from path import path

env = jinja2.Environment()


def make_executable(filename):
    return os.chmod(filename, 0755)


def cli_app(msmlfile, **kwargs):
    """Calls the workflow behind `msmlfile`like an CLI app.

    CLI apps

    * ... takes arguments from the command.
    * ...  provide an `--xml` for providing an XML description of the command line arguments


    :param msmlfile: path to the MSML workflow file (*.xml)
    :type msmlfile: str or path.path
    :param kwargs: various options from :py:class:`msml.frontend.App`

    :return: the memory from the executor
    :rtype: msml.run.memory.Memory
    """

    msmlfile = path(msmlfile)
    app = App(**kwargs)
    mfile = app._load_msml_file(msmlfile)
    app._prepare_msml_model(mfile)

    # grab arguments
    try:
        variables = get_arguments(mfile)

        if isinstance(app.memory_init_file, dict):
            app.memory_init_file.update(variables)
        else:
            app.memory_init_file = variables

        memory = app.execute_msml_file(msmlfile)

        return memory
    except SystemExit:
        pass
    except:
        consolecatcher._reset_stdio()
        raise


def get_arguments(msmlfile):
    """Parses the command line arguments for the given `msmlfile`.

    1. Generate an argument parser with :py:mod:`clictk`
    2. Parses the command line
    3. Check for `--xml`
        1. if `--xml` is set, abort execution and generate CLI XML
        2. else restore stdio channels

    ns = p.parse_args()

    .. note: only non-generated variables are exported as cli arguments

    :param msmlfile:
    :return: a dictionary of MSML variables
    """

    exe = generate_cli(msmlfile)
    parser = clictk.build_argument_parser(exe)
    ns = parser.parse_args()

    if ns.__xml__:  # if `--xml` is set
        xml = clictk.prettify(exe.as_xml())
        # write to real stdout
        consolecatcher._true_channels[0].write(xml)
        sys.exit(0)
    else:
        # we do not need stdout sanity further more
        consolecatcher._reset_stdio()


    args = {}

    for n, t in msmlfile.variables.items():
        if hasattr(ns, n):
            value = getattr(ns, n)

            # file arguments are relative to the current working dir
            if issubclass(t.sort.physical, InFile):
                value = os.path.abspath(value)

            try:
                args[n] = conversion(str, t.sort)(value)
            except TypeError as e:
                print("Parameter %s missing" % n)
                log.error("Parameter %s missing: Error", n)
                sys.exit(1)
                raise

    return args


def generate_cli(msmlfile, category="MSML", title=None, description=None,
                 version=None, contributor=None, license=None,
                 filter_generated_vars=True):
    """Generates the CLI XML from an MSML workflow object.

    :param msmlfile:
    :param category:
    :param title:
    :param description:
    :param version:
    :param contributor:
    :param license:
    :param filter_generated_vars:
    :return:
    """

    exe = clictk.Executable(
        category=category,
        title=title or os.path.basename(msmlfile.filename),
        description=description or "...",
        version=version,
        license=license,
        contributor=contributor,
        acknowledgements=None,
        documentation_url=None)

    grp = clictk.ParameterGroup(
        label="Offered Parameters",
        description="n/a",
        advanced=False
    )

    for var in msmlfile.variables.values():
        # over jump generated variables
        if var.name.startswith("gen_") and filter_generated_vars:
            continue

        if var.role == ("input"):
            ch = "input"
        elif var.role = ("output"):
            ch = "output"
        elif var.role = ("param"):
            ch = "None"
        else:
            continue

        p = clictk.Parameter(
            var.name,
            get_cli_tag(var.sort.physical),
            default=var.value,
            description=None,
            channel=ch,
            longflag=var.name
        )

        grp.append(p)

    exe.parameter_groups.append(grp)

    return exe

# If a sort is missing please add here
SORT_TO_CLI_TAG = [
    (Image, 'image'),
    (InFile, "file"),
    (int, "integer"),
    (float, "float"),
    (MSMLListF, "float-vector"),
    (MSMLListI, "integer-vector"),
    (object, "string"),  #fallback
]


def get_cli_tag(physical_type):
    """Lookup the cli tag name for an physical msml type

    :param physical_type: type
    :return:
    """
    for sort, tag in SORT_TO_CLI_TAG:
        #print(physical_type)
        if issubclass(physical_type, sort):
            return tag
    assert "No CLI tag found, but <object> => <string> is fallback, hä?"


class GenerateCLIFromMSML(object):
    """This class generates the CLI stub executable file.

    """
    def __init__(self, msmlfile):
        self.msmlfile = msmlfile

        self.inputs = []
        self._outputs = []

        self.exporter_options = {}
        self.executor_options = {}
        self.executor = "phase"
        self.repositories = []
        self.packages = []
        self.memory = {}

        self._getdata()

    def _getdata(self):
        for var in self.msmlfile.variables.values():
            if not var.name.startswith("gen"):
                self.inputs.append(
                    (var.name, var.physical_type)
                )

        for task in self.msmlfile.workflow.tasks.values():
            for name, slot in task.operator.output.items():
                self._outputs.append(
                    ("%s.%s" % (task.id, name),
                     slot.physical_type)
                )

    def generate(self, filename, outputfilter):
        template = env.from_string(PYTHON)

        msml_path = os.path.abspath(os.path.dirname(__file__) + "/../../")
        print filename
        with open(filename, 'w') as fp:
            kwargs = dict(self.__dict__)
            kwargs['msml_src'] = msml_path
            kwargs["filename"] = os.path.abspath(self.msmlfile.filename)
            kwargs["python"] = sys.executable
            fp.write(template.render(**kwargs))
        make_executable(filename)
