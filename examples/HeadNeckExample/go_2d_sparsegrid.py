__author__ = 'Markus Stoll, Chen Song'
import sys
import time
import csv
sys.path.append('../../src/');

sys.path.append('./tools/')
from nwspgr import nwspgr

import copy
from lxml import etree
import os
import ntpath
import shutil
from path import path
import random



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

import numpy as np


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
        "moving_points":self._scenarioDisp,
        "resultMesh":self._scenarioResultMesh,
        "resultImage":self.resultImage
        }
        mem = self.app.execute_msml(self.mf, )
        return self._scenarioResultMesh

if __name__ == '__main__': #for parallel processing compatibility

    samples, weights = nwspgr('GQN', 5,2, 'symmetric')   
 
    COUNTER = len(weights)
    NAME = "First_PatSparse_" + str(COUNTER) + "_DIRNEW_"
    DIR = './First_PatSparse_' + str(COUNTER) + '/'
    
    results_file_name = 'results__2d_test2016c_' + str(COUNTER) + '_' + str(time.time()) + '.csv'
    
    try :
        os.stat(DIR)
    except:
        os.mkdir(DIR)

    msml_file_name ='simulation.xml'

    args_list = []
    startDir = os.getcwd()
    headneck_simulations = []

    
    #csv_file_name = "./samples/2d/monte_carlo/mc_normal_"+ str(COUNTER) + ".csv"
    #csv_file_name = "mc_nosys_400samples_1_5_5_17_5__18-Feb-2015__onPublicHNN.csv"
    csv_file_name = "motionModels_separated_p1_d5.ppca.coeff.csv"
    coeff = np.genfromtxt(csv_file_name,delimiter=',',dtype='f8')
    
    ref_csv_file_name = "ref.csv"
    ref = np.genfromtxt(ref_csv_file_name,delimiter=',',dtype='f8')
    
    scenarios = []
    for i in range(0,COUNTER):
        tmp = np.dot(coeff[:, [0, 1, 2, 3, 4] ], samples[i]) #sample from 5d space to 72d
        tmp2 = np.add(tmp, ref) #center
        scenarios.append(tmp2)
        
    result_vtus = list()
    result_vtis = list()

    #collect parameters for all simulation runs
    i=1
    for scenarioRow in scenarios: #one  scenario = one line in csv file = one simulation run = one simulation output folder
        args = { 'i':i, 'msml_file': msml_file_name, 'scenarioDisp': scenarioRow, 'scenarioResultMesh' : '../' + DIR + NAME + str(i) + '.vtu', 'resultImage': '../' + DIR + NAME + str(i) + '.vti'} 
        result_vtus.append( NAME + str(i) + '.vtu' )
        result_vtis.append( NAME + str(i) + '.vti' )
        args_list.append(dict(args)) #copy            
        if i>=COUNTER:
            break
        i=i+1


    #run simulations
    results = []
    for j in range(0,i):  
        os.chdir( startDir )    
        createAndRunHnnSimulation(args_list[j])

    os.chdir( startDir )
    #vtus = ['vtus', 'vtus2']
    #weights =  [0.5, 0.5]


    weights = []
    for i in range(0, COUNTER):
        weights.append(1.0/COUNTER)


    #Chens IsoContour method with monte carlo
    MiscOps.IsoContourOperator(DIR, '../out_preprocessing/PTV_1_volmesh.vtu', result_vtus, weights); #creates 'isocontour_outer.vtp'
    MiscOps.VoxelizeSurfaceMesh('./isocontour_outer.vtp', './isocontour_outerTwoDVoxIsoContour.vti', 0, 0.000, 'ct.vti', False, 0.025)


    shutil.move('./isocontour_initial.vtp', DIR + 'isocontour_initial' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_mean.vtp', DIR + 'isocontour_mean' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_inner.vtp', DIR + 'isocontour_inner' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_outer.vtp', DIR + 'isocontour_outer' + str(COUNTER) +'.vtp')


    #Markus Image sum method (works only with monte carlo) 
    MiscOps.ImageSum(DIR + NAME+'*' + '.vti', True, 'imgSumTwoDVox.vti');
    MiscOps.vtkMarchingCube('./imgSumTwoDVox.vti', './imgSumIsoSurface.vtp', 12);    


    shutil.move('./imgSumTwoDVox.vti', DIR + 'imgSumTwoDVox' + str(COUNTER) +'.vti')
    shutil.move('./imgSumIsoSurface.vtp', DIR + 'imgSumIsoSurface' + str(COUNTER) +'.vtp')


    #delet intermediate results folders
    for i in range(1, COUNTER+1) :
        shutil.rmtree('./' + NAME + str(i))  

    #num_of_workers =   multiprocessing.cpu_count() -1
    #pool = multiprocessing.Pool(5)
    #pool.map(createAndRunHnnSimulation, args_list)