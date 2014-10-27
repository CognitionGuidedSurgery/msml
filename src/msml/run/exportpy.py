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

from ..run import *

from ..exporter import Exporter
from ..model import Task, MSMLVariable

from jinja2 import Environment, FileSystemLoader, Template

from simplegeneric import generic


T = Template("""#!/usr/bin/python

import msml.frontend

app = App()
alphabet = app.alphabet

""")

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

@execute.when_type(Exporter)
def execute_exporter(exporter):
    print "_exporter_clazz = msml.exporter.get_exporter('%s')" % exporter.name
    print "_exporter = _exporter_clazz(mem)"


@execute.when_type(MSMLVariable)
def execute_variable(var):
    print "%s = '%s'" % (var.name, var.value)

from itertools import starmap

@execute.when_type(Task)
def execute_task(task):
    def refo(a):
        if isinstance(a.linked_from.task, MSMLVariable):
            return a.linked_from.task.name
        return a.linked_from.task.id + "_"  +a.linked_from.task.name


    onames = ', '.join( map(lambda x: task.id +"_"+x , task.operator.output.keys()))

    inames = ', '.join( starmap(lambda name, ref:
                                "%s = %s" %(name, refo(ref)),
                                task.arguments.items()) )

    opname = task.operator.name

    print "%s = alphabet.get('%s')" % (opname, task.operator.name)
    print "%s = %s(%s)" % (onames,opname,inames)
