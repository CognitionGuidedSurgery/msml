__author__ = 'Markus Stoll, Chen Song'
import sys
import time
import csv
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
        "dispVar":self._scenarioDisp[0],
        "dispVar2":self._scenarioDisp[1],
        "resultMesh":self._scenarioResultMesh,
        "resultImage":self.resultImage
        }
        mem = self.app.execute_msml(self.mf, )
        return self._scenarioResultMesh

if __name__ == '__main__': #for parallel processing compatibility

    
    COUNTER = 1
    NAME = "BATCH_OUT_MC_UNIFORM_2d_test1_" + str(COUNTER) + "_DIRNEW_"
    DIR = './REFERENCE' + str(COUNTER) + '/'
    
    results_file_name = 'results__2d_MC_' + str(COUNTER) + '_' + str(time.time()) + '.csv'
    
    try :
        os.stat(DIR)
    except:
        os.mkdir(DIR)


    shutil.copy('./init.vtu', DIR + 'init.vtu')   

    #msml_file_name ='beamLinearDisp.msml.xml'
    msml_file_name ='beamLinearDisp_2d.msml.xml'

    args_list = []
    startDir = os.getcwd()
    headneck_simulations = []

    csv_file_name = "./samples/2d/ref_095.csv"

    scenarios = reader(open(csv_file_name, "rb"), delimiter=',', dialect='excel')
    result_vtus = list()
    result_vtis = list()

    #collect parameters for all simulation runs
    i=1
    for scenarioRow in scenarios: #one  scenario = one line in csv file = one simulation run = one simulation output folder
        if (i>0):
            vec = [ [0,0, float(scenarioRow[0])*0.005], [0,0,float(scenarioRow[1])*0.005] ]
            args = { 'i':i, 'msml_file': msml_file_name, 'scenarioDisp': vec, 'scenarioResultMesh' : '../' + DIR + NAME + str(i) + '.vtu', 'resultImage': '../' + DIR + NAME + str(i) + '.vti'} 
            result_vtus.append( NAME + str(i) + '.vtu' )
            result_vtis.append( NAME + str(i) + '.vti' )
            args_list.append(dict(args)) #copy            
            i=i+1
        if i>COUNTER:
            break

 
    results = []
    for j in range(0,i-1):
        os.chdir( startDir )
        createAndRunHnnSimulation(args_list[j])

    os.chdir( startDir )

    shutil.move(DIR + NAME + str(COUNTER) + '.vtu', './' + 'dispSurfaceRefZeroPoisson2D.vtu')

    #reference preprocessing
    MiscOps.VoxelizeVolumeMesh('./init.vtu', './initSurfaceVoxelized2D.vti', 0, 0.001, '', False, 0)
    MiscOps.VoxelizeVolumeMesh('./dispSurfaceRefZeroPoisson2D.vtu', './dispSurfaceRefZeroPoissonTwoDVox.vti', 0, 0.000, 'initSurfaceVoxelized2D.vti', False, 0.025)
    MiscOps.VoxelizeVolumeMesh('./dispSurfaceRefZeroPoisson2D.vtu', './dispSurfaceRefZeroPoissonTwoDVoxIsoContour.vti', 0, 0.000, 'initSurfaceVoxelized2D.vti', False, 0.025)

    #delet intermediate results folders
    for i in range(1, COUNTER+1) :
	shutil.rmtree('./' + NAME + str(i))
