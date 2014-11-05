__author__ = 'suwelack'

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

        self._theApp = msml.frontend.App(exporter=exporter, output_dir = output_dir, execution_options='FULL')

        self._mfile = self._theApp._load_msml_file(file)

        self._executer = self._theApp.get_executor(self._mfile)
        self._executer._init_workflow()




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
        self._executer._init_workflow()
        self._memory = self._theApp.execute_msml(self._mfile)


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

