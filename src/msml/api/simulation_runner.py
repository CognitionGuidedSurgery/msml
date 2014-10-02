__author__ = 'suwelack'

import msml.frontend
import msml.env
from msml.model import *

class SimulationRunner(object):
    def __init__(self, file=None, exporter=None, output_dir = None):

        self._file = file
        self._exporter = exporter
        self._output_dir = output_dir

        execOptions={}
        execOptions['D'] = {'executor.class=run.ControllableExecutor'}

        self._theApp = msml.frontend.App(exporter=exporter, output_dir = output_dir,options=execOptions)

        self._mfile = self._theApp._load_msml_file(file)

        self._theApp.init_workflow(self._mfile)



    def update_variable(self,variable_name, variable_value):
        #update the variables

        self._theApp.update_variable(variable_name, variable_value)

    def run_preprocessing(self):
        self._theApp.process_workflow()

    def run_simulation(self):
        self._theApp.launch_simulation()

    def run_postprocessing(self):
        self._theApp.launch_postprocessing()


    def get_Results(self):
        print('test')
        #get the name of the disp output

        #pull points

        #fill datastructure

        #return it


    def run_full_workflow(self):
        self.run_preprocessing()
        self.run_simulation()
        self.run_postprocessing()

        #self._memory = self._theApp.execute_msml(self._mfile)


    #def executeMSML(self):
#
 #       self._memory = self._theApp.execute_msml(self._mfile)


