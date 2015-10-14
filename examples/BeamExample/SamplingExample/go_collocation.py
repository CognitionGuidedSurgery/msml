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
 
 
NAME = "OUT_COLLOC6_DIRNEW_"
COUNTER = 6
DIR = './COLLOC6/'
#DIR = './Reference_solution/'

try :
	os.stat(DIR)
except:
	os.mkdir(DIR)

if __name__ == '__main__': #for parallel processing compatibility
   
    shutil.copy('./init.vtu', DIR + 'init.vtu')   
 
    msml_file_name ='beamLinearDisp.msml.xml'
        
    args_list = []
    startDir = os.getcwd()
    headneck_simulations = []
    
    csv_file_name = "./samples/collocation/gqu6_sample.csv"
    #csv_file_name = "./samples/reference/reference.csv"

    weight_name = './samples/collocation/gqu6_weight.csv'
    weights = []
    weights_reader = reader(open(weight_name, "rb"), delimiter=',', dialect='excel')
    for i in weights_reader :
        weights.append(float(i[0]))

    scenarios = reader(open(csv_file_name, "rb"), delimiter=',', dialect='excel')
    result_vtus = list()
    result_vtis = list()
    
    #collect parameters for all simulation runs
    i=1
    for scenarioRow in scenarios: #one  scenario = one line in csv file = one simulation run = one simulation output folder
        if (i>0):
	    # scaling is separated in two parts. "*0.01" is same as in monte-carlo case, and "(-0.5)*2" is rescale the samples in interval [-1,1]
            vec = [0,0, (float(scenarioRow[0])-0.5)*2.0*0.01]
            args = { 'i':i, 'msml_file': msml_file_name, 'scenarioDisp': vec, 'scenarioResultMesh' : '../' + DIR + NAME + str(i) + '.vtu', 'resultImage': '../' + DIR + NAME + str(i) + '.vti'} 
            result_vtus.append( NAME + str(i) + '.vtu' )
            result_vtis.append( NAME + str(i) + '.vti' )
            args_list.append(dict(args)) #copy            
        i=i+1
        if i>COUNTER:
            break

    #run simulations
    results = []
    for j in range(0,i-1):  
        os.chdir( startDir )    
        createAndRunHnnSimulation(args_list[j])
    
    os.chdir( startDir )

    MiscOps.IsoContourOperator(DIR, 'init.vtu', result_vtus, weights)
    
    shutil.move('./isocontour_initial.vtp', DIR + 'isocontour_initial.vtp')
    shutil.move('./isocontour_mean.vtp', DIR + 'isocontour_mean.vtp')
    shutil.move('./isocontour_inner.vtp', DIR + 'isocontour_inner.vtp')
    shutil.move('./isocontour_outer.vtp', DIR + 'isocontour_outer.vtp')
		
    #delet intermediate results folders
    for i in range(1, COUNTER+1) :
	    shutil.rmtree('./' + NAME + str(i))  
 
    #num_of_workers =   multiprocessing.cpu_count() -1
    #pool = multiprocessing.Pool(5)
    #pool.map(createAndRunHnnSimulation, args_list)
   
    
 
   
