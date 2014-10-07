__author__ = 'suwelack'

import msml.frontend
import msml.env
from msml.model import *

class SimulationRunner(object):
    def __init__(self, file=None, exporter=None, output_dir = None):

        self._file = file
        self._exporter = exporter
        self._output_dir = output_dir

        #execOptions={}
        #execOptions['D'] = {'executor.class=run.ControllableExecutor'}

        self._theApp = msml.frontend.App(exporter=exporter, output_dir = output_dir)

        self._mfile = self._theApp._load_msml_file(file)

        #self._theApp.init_workflow(self._mfile)



    def update_variable(self,variable_name, variable_value):
        #this is a temporary hack

        updated = False
        for constraint in self._mfile._scene[0].constraints[0].constraints:
            if constraint.tag == 'displacementConstraint':
                if constraint.name == variable_name:
                    constraint.displacement = variable_value
                    updated = True
        if not updated:
            print('Error, no displacementConstraint with given name found, values could not be updated ')

        #update the variables

        #self._theApp.update_variable(variable_name, variable_value)

    #def run_preprocessing(self):
    #    self._theApp.process_workflow()

    #def run_simulation(self):
    #    self._theApp.launch_simulation()

    #def run_postprocessing(self):
    #    self._theApp.launch_postprocessing()


    def get_results(self, variableName, valueName):

        #try to get the variable from memory
        theDict = self._memory._internal

        if variableName in theDict:
            return theDict[variableName][valueName]
        else:
            print('Error, '+variableName+' is not in memory, please check your msml file!!')
        #pull points

        #fill datastructure

        #return it


    def run_full_workflow(self):
        #self.run_preprocessing()
        #self.run_simulation()
        #self.run_postprocessing()

        self._memory = self._theApp.execute_msml(self._mfile)



    #def executeMSML(self):
#
 #       self._memory = self._theApp.execute_msml(self._mfile)


