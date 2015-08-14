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
import MiscMeshOperatorsPython as MiscOps
from csv import reader
import multiprocessing
 
 
def createAndRunHnnSimulation(args_list): #create a simulation instance with given parameter and run it.
    aHeadneck_simulation = headneck(args_list['msml_file'], args_list['i'], args_list['scenarioDisp'], args_list['scenarioResultMesh'], args_list['resultImage'])
    return aHeadneck_simulation()
   
class headneck(object): 
    def __init__(self, msml_filename, id, scenarioDisp, scenarioResultMesh, resultImage):
        self.id = id
        self.app = App(seq_parallel=True, exporter='nsofa', output_dir= NAME + str(id), executor='sequential')
        self.mf = self.app._load_msml_file(msml_filename)
        self._scenarioDisp = scenarioDisp
        self._scenarioResultMesh = scenarioResultMesh
        self.resultImage = resultImage
   
    def __call__(self):
        self.app.memory_init_file = {
            "dispVar":self._scenarioDisp,
			"resultMesh":self._scenarioResultMesh,
            "resultImage":self.resultImage            
        }
        mem = self.app.execute_msml(self.mf, )
        return self._scenarioResultMesh
 
 
NAME = "OUT_MC__"
if __name__ == '__main__': #for parallel processing compatibility
   
    
    msml_file_name ='beamLinearDisp.msml.xml'
        
    args_list = []
    startDir = os.getcwd()
    headneck_simulations = []
    
    csv_file_name = "stdnorm_mc_10k.csv"
    scenarios = reader(open(csv_file_name, "rb"), delimiter=',', dialect='excel')
    result_vtus = list()
    result_vtis = list()
    
    #collect parameters for all simulation runs
    i=1
    for scenarioRow in scenarios: #one  scenario = one line in csv file = one simulation run = one simulation output folder
        if (i>0):
            vec = [0,0, float(scenarioRow[0])*0.01]
            args = { 'i':i, 'msml_file': msml_file_name, 'scenarioDisp': vec, 'scenarioResultMesh' : '../' + NAME + str(i) + '.vtu', 'resultImage': '../' + NAME + str(i) + '.vti'} 
            result_vtus.append( NAME + str(i) + '.vtu' )
            result_vtis.append( NAME + str(i) + '.vti' )
            args_list.append(dict(args)) #copy            
        i=i+1
        if i>10:
            break

    #run simulations
    results = []
    for j in range(0,i-1):  
        os.chdir( startDir )    
        createAndRunHnnSimulation(args_list[j])
    
    os.chdir( startDir )
    vtus = ['vtus', 'vtus2']
    weights =  [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    MiscOps.IsoContourOperator('', 'init.vtu', result_vtus, weights)
    
    MiscOps.ImageSum(NAME+'*' + '.vti', True, 'imgSum.vti');
    
        
		
   
    #num_of_workers =   multiprocessing.cpu_count() -1
    #pool = multiprocessing.Pool(5)
    #pool.map(createAndRunHnnSimulation, args_list)
   
    
 
   
