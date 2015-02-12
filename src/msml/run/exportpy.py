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

"""Transform MSML files into a equivalence Python file.

"""

from jinja2 import Template
from simplegeneric import generic

from ..run import *
from ..exporter import Exporter
from ..model import Task, MSMLVariable


T = Template("""#!/usr/bin/python

import msml.frontend

app = App()
alphabet = app.alphabet

memory = {}
""")

__all__ = ["exportpy"]


def exportpy(msml_file):
    graphb = DefaultGraphBuilder(msml_file, msml_file.exporter).dag
    print T.render()
    buckets = graphb.toporder()
    for bucket in buckets:
        for node in bucket:
            execute(node)


@generic
def execute():
    pass

import msml.exporter
from msml.model import *


@execute.when_type(Exporter)
def execute_exporter(exporter):
    ename = ""
    for ex in msml.exporter.get_known_exporters():
        if isinstance(exporter, msml.exporter.get_exporter(ex)):
            ename = ex
            break

    print "_exporter_clazz = msml.exporter.get_exporter('%s')" % ename
    print "msml_file = msml.xml.load_msml_file(%r)" % str(exporter._msml_file.filename)
    print "_exporter = _exporter_clazz(msml_file)"
    print "_exporter._memory = memory"


@execute.when_type(MSMLVariable)
def execute_variable(var):
    print "memory[%r] = '%s'" % (var.name, var.value)


from itertools import starmap


@execute.when_type(Task)
def execute_task(task):
    def refo(a):
        if isinstance(a.linked_from.task, MSMLVariable):
            return "memory[%r]" % a.linked_from.task.name
        return "memory[%r][%r]" % (a.linked_from.task.id, a.linked_from.task.name)


    # onames = ', '.join( map(lambda x: task.id +"_"+x , task.operator.output.keys()))

    inames = ', '.join(starmap(lambda name, ref:
                               "%s = %s" % (name, refo(ref)),
                               task.arguments.items()))

    opname = task.operator.name

    print "%s = alphabet.get(%r)" % (opname, task.operator.name)
    print "memory[%r] = %s(%s)" % (task.id, opname, inames)
    print
