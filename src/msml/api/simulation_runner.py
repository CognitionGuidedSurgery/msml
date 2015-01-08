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

__author__ = 'Stefan Suwelack and Alexander Weigl'

import msml.frontend
import msml.env
from msml.model import *
from collections import namedtuple

import numpy as np
from scipy import optimize


class SimulationRunner(object):
    ResultType = namedtuple('ResultRequest', 'variable_name value_name')

    def __init__(self, file=None, exporter=None, output_dir = None):

        self._file = file
        self._exporter = exporter
        self._output_dir = output_dir

        self._theApp = msml.frontend.App(exporter=exporter, output_dir = output_dir, executor='phase')

        self._mfile = self._theApp._load_msml_file(file)

        self._executer = self._theApp.get_executor(self._mfile)


    def update_variable(self,variable_name, variable_value):

        self._executer.update_variable(variable_name, variable_value)


    def get_results(self, variableName, valueName):

        #try to get the variable from memory
        theDict = self._memory._internal

        if variableName in theDict:
            return theDict[variableName][valueName]
        else:
            print('Error, '+variableName+' is not in memory, please check your msml file!!')



    def run(self):
        #self._executer._init_workflow()
        self._memory = self._executer.run()


    #future extensions for fine grain execution control
            #def run_preprocessing(self):
    #    self._theApp.process_workflow()

    #def run_simulation(self):
    #    self._theApp.launch_simulation()

    #def run_postprocessing(self):
    #    self._theApp.launch_postprocessing()


class SimulationSweeper(SimulationRunner):


    def __init__(self, file=None, exporter=None, output_dir = None):
        super(SimulationSweeper, self).__init__(file, exporter, output_dir)

    def set_sweep_variables(self, variable_dict):
        self._sweep_dict = variable_dict

    def set_result_logging(self, result_list):
        self._result_requests= result_list
        self._history = dict()
        for request in result_list:
            self._history[request] =list()


    def run(self):

        if self._sweep_dict is None:
            print('Error, please specify variables to sweep')
            return

        for key in self._sweep_dict:
            values = self._sweep_dict[key]
            for value in values:
                super(SimulationSweeper,self).update_variable(key, value)
                #TODO: Mechanism to save different output requests to hdd
                #if self._result_requests is not None:
                #    for request in self._result_requests:

                super(SimulationSweeper,self).run()

                if self._history is not None:
                    for historyKey in self._history:
                        #get the output value
                        variableName = historyKey.variable_name
                        valueName = historyKey.value_name
                        value = super(SimulationSweeper,self).get_results(variableName, valueName)
                        self._history[historyKey].append(value)


    def get_history(self):
        if self._history is None:
            print('Error, no history present, please enable result logging')
        return self._history

