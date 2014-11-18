import sys
import copy
from lxml import etree     
import os
import ntpath
from path import path



from msml import frontend 
import msml
import msml.env
import msml.model
import msml.run
import msml.xml
import msml.exporter
import msml.exceptions
from msml.exceptions import *
from msml.frontend import App
import multiprocessing

class Lungs(object):
    def __init__(self, msml_filename, p):
        self.app = App(exporter='nsofa', output_dir='batchedPressureNew' + str(p), executor='sequential')
        self.mf = self.app._load_msml_file(msml_filename)
        self._surface_pressure = p
    
    def __call__(self):
        self.app.memory_init_file = {
            "surface_pressure":self._surface_pressure 
        }
        mem = self.app.execute_msml(self.mf, ) 
        return mem._internal['volumeMeasure']['volume']


def createAndRunSimulation(args_list):
    aLungs_simulation = Lungs(args_list['msml_file'], args_list['p'])
    return aLungs_simulation()

if __name__ == '__main__':
    currentDIr = os.getcwd()
    msml_file = os.path.abspath('../CGALi2vLungs/Lungs_new.xml')
    
    #create arguments for all simulations
    args_list = []
    for p in range (5, 80, 5):
        os.chdir(currentDIr)
        args = { 'p':p, 'msml_file':msml_file}
        args_list.append(dict(args)) #copy
    
    #createAndRunSimulation(args_list)
    
    num_of_workers =   multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_of_workers-1)
    pool.map(createAndRunSimulation, args_list)