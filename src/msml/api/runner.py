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

__author__ = 'suwelack'

import msml.frontend
import msml.env
from msml.model import *

class Runner(object):
    def __init__(self, file=None, exporter=None, output_dir = None):

        self._file = file
        self._exporter = exporter
        self._output_dir = output_dir

        execOptions={}
        execOptions['D'] = {'executor.class=run.ControllableExecutor'}

        self._theApp = msml.frontend.App(exporter=exporter, output_dir = output_dir,options=execOptions)

        self._mfile = self._theApp._load_msml_file(file)


    def executeMSML(self):

        self._memory = self._theApp.execute_msml(self._mfile)


    def setDisplacements(self, indices, displacements):
        print('Setting displacements...')

        assert isinstance(self._mfile, MSMLFile)

        sceneobject = self._mfile.scene[0]
        cs = sceneobject.constraints[0]

        assert isinstance(cs, ObjectConstraints)

        for displacementConstraint in cs.constraints:
            assert isinstance(displacementConstraint, ObjectElement)

            if displacementConstraint.tag == 'displacementConstraint':
                break

        print displacementConstraint

        displacementConstraint.attributes['displacement'] = [1,1,1,1,1,1]
        displacementConstraint.attributes['indices'] = [2,2]




#    def init_msml_system(self):
#        msml.env.load_user_file()
#        self._load_alphabet()