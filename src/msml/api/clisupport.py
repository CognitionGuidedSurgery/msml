import jinja2
import sys

from msml.frontend import App
from msml.sortdef import InFile, MSMLListF, MSMLListI, Image


__author__ = 'Alexander Weigl'

PYTHON = """
from msml.api.clisupport import *
import sys

MSMLFILE = '{{ filename }}'

def main():
    cli_app(MSMLFILE,
        exporter="sofa", memory_init_file={{ memory_init_file }},
        packages = {{ packages }},
        repositories = {{ repositories }},
        exporter_options= {{ exporter_options }},
        executor_options = {{ executor_options }}
    )

if __name__ == "__main__": main()
"""

XML = """<?xml version="1.0" encoding="utf-8"?>
<executable>
  <category>MSML.XXX</category>
  <title></title>
  <description><![CDATA[]]></description>
  <version>0.0.1</version>
  <documentation-url></documentation-url>
  <license></license>
  <contributor></contributor>
  <parameters>
    {% for p in parameters %}
        <{{ p.tag }}>
            <name>{{ p.name }}</name>
            <longflag>{{ p.longflag }}</longflag>
            <default>{{p.default}}</default>
        </{{ p.tag }}>
    {% endfor %}
  </parameters>
</executable>
"""

import argparse

from ..sorts import conversion

env = jinja2.Environment()


def cli_app(msmlfile, **kwargs):
    app = App(**kwargs)
    mfile = app._load_msml_file(msmlfile)
    app._prepare_msml_model(mfile)

    variables = get_arguments(mfile)
    if isinstance(app.memory_init_file, dict):
        app.memory_init_file.update(variables)
    else:
        app.memory_init_file = variables

    memory = app.execute_msml_file(msmlfile)

    return memory


def get_arguments(msmlfile):
    p = argparse.ArgumentParser()
    mutual = p.add_mutually_exclusive_group()
    grp = mutual.add_argument_group()
    for n, t in msmlfile.variables.items():
        grp.add_argument("--%s" % n, metavar=t.physical_type, dest=n)

    mutual.add_argument("--xml", action="store_true", dest="xml", help="show cli xml", default=False)

    ns = p.parse_args()

    if ns.xml:
        print_cli(msmlfile)
        sys.exit(0)

    args = {}

    for n, t in msmlfile.variables.items():
        args[n] = conversion(str, t.sort)(getattr(ns, n))

    return args


def print_cli(msmlfile):
    te = env.from_string(XML)
    p = []
    for n, t in msmlfile.variables.items():

        physcial = t.physical_type
        if isinstance(physcial, Image):
            tag = 'image'
        elif isinstance(physcial, InFile):
            tag = "file"
        elif physcial == str:
            tag = "string"
        elif physcial == int:
            tag = "integer"
        elif physcial == float:
            tag = "float"
        elif physcial == MSMLListF:
            tag = "float-vector"
        elif physcial == MSMLListI:
            tag = "integer-vector"
        else:
            tag = "string"

        a = {
            'name': n,
            'longflag': n,
            'tag': tag,
        }
        p.append(a)
    print te.render(parameters=p)


class GenerateCLIFromMSML(object):
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
        with open(filename, 'w') as fp:
            kwargs = dict(self.__dict__)
            kwargs[filename] = self.msmlfile.filename
            fp.write(template.render(**kwargs))

