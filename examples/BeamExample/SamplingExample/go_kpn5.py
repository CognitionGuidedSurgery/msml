__author__ = 'Markus Stoll, Chen Song'
import sys
sys.path.append('../../../src/');


 
import copy
from lxml import etree    
import os
import ntpath
import shutil
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
from csv import reader
import multiprocessing
 
 
def createAndRunHnnSimulation(args_list): #create a simulation instance with given parameter and run it.
    aHeadneck_simulation = headneck(args_list['msml_file'], args_list['i'], args_list['scenarioDisp'])
    return aHeadneck_simulation()
   
class headneck(object): 
    def __init__(self, msml_filename, id, scenarioDisp):
        self.id = id
        self.app = App(seq_parallel=True, exporter='nsofa', output_dir= NAME + str(id), executor='sequential')
        self.mf = self.app._load_msml_file(msml_filename)
        self._scenarioDisp = scenarioDisp
        self._scenarioResultMesh = '../' + NAME + str(id) + '.vtu'
   
    def __call__(self):
        self.app.memory_init_file = {
            "dispVar":self._scenarioDisp,
			"resultMesh":self._scenarioResultMesh
        }
        mem = self.app.execute_msml(self.mf, )
        return #mem._internal['volumeMeasure']['volume']
 
 
NAME = "OUT_KPN5__"
if __name__ == '__main__': #for parallel processing compatibility
   
    
    msml_file_name ='beamLinearDisp.msml.xml'
        
    args_list = []
    startDir = os.getcwd()
    headneck_simulations = []
    
    csv_file_name = "kpn5_sample.txt"
    scenarios = reader(open(csv_file_name, "rb"), delimiter=',', dialect='excel')

    #collect parameters for all simulation runs
    i=1
    for scenarioRow in scenarios: #one  scenario = one line in csv file = one simulation run = one simulation output folder
        if (i>0):
            vec = [0,0, scenarioRow[0]]
            args = { 'i':i, 'msml_file': msml_file_name, 'scenarioDisp': vec } 
            args_list.append(dict(args)) #copy            
        i=i+1
        if i>1000:
            break

    #run simulations
    for j in range(0,i-1):  
        os.chdir( startDir )    
        createAndRunHnnSimulation(args_list[j]) 
   
    #num_of_workers =   multiprocessing.cpu_count() -1
    #pool = multiprocessing.Pool(5)
    #pool.map(createAndRunHnnSimulation, args_list)
   
    
 
   
