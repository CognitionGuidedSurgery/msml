#!/usr/bin/python
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


import os, sys
from path import path

sys.path.insert(0, "../../src/")

import msml.exporter


"""
Example of a MSML pipeline without XML.


"""

__author__ = 'Alexander Weigl'
__date__ = "2014-03-20"

import msml.frontend
import msml.env
from msml.model import *


options = {'--alphabet': 'alphabet.cache',
           '--exporter': 'nsofa',
           '--output': None,
           '--start-script': '~/.config/msmlrc.py',
           '--verbose': True,
           '--xsd-file': False,
           '-S': True,
           '-w': False,
           '<file>': [file],
           '<paths>': [],
           'alphabet': False,
           'exec': True,
           'show': False}


def construct_msml_file():
    def _task(name, **kwargs):
        t = Task(name, kwargs)
        return t

    def valfrom(task, slot=None):
        if slot:
            return "${%s.%s}" % (task.id , slot)
        else:
            return "${%s}" % task.id

    clrmesh = _task("colormesh",
                    id="clrmesh",
                    coloredMesh="Colored/liverTet4ColoredIni.vtk",
                    mesh="ToColor/LiverXSTet4.vtk")

    pv = _task("paraview",
               id="pv",
               data=valfrom(clrmesh))

    wf = Workflow([clrmesh, pv])
    m = MSMLFile(workflow=wf, env=MSMLEnvironment())
    m.filename = "bunnypy.xml" # needed for generating export file name
    return m

def main():
    msml.env.load_user_file()
    msml.env.current_alphabet = msml.frontend.alphabet(options)
    msml.env.current_alphabet.validate()
    exporter = msml.exporter.get_exporter("nsofa")

    model = construct_msml_file()
    model.exporter = exporter(model)
    model.validate(msml.env.current_alphabet)

    fil = path(__file__)
    os.chdir(fil.dirname().abspath())

    exe = msml.run.LinearSequenceExecuter(model)
    mem = exe.run()

    mem.show_content()


__name__ == "__main__" and main()



