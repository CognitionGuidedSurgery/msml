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

    
    COUNTER = 800
    NAME = "BATCH_OUT_MC_UNIFORM_2d_test2016_" + str(COUNTER) + "_DIRNEW_"
    DIR = './BATCH_MC_UNIFORM_2d_test2016_' + str(COUNTER) + '/'
    
    results_file_name = 'results__2d_MC_test2016_' + str(COUNTER) + '_' + str(time.time()) + '.csv'
    
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

    #csv_file_name = "./samples/2d/ref_095.csv"
    #csv_file_name = "./samples/2d/monte_carlo/mc_uniform_" + str(COUNTER) + ".csv"
    
    csv_file_name = "./samples/2d/monte_carlo/mc_normal_"+ str(COUNTER) + ".csv"
    
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


    #reference preprocessing
    #MiscOps.VoxelizeVolumeMesh('./init.vtu', './initSurfaceVoxelized2D.vti', 0, 0.001, '', False, 0)
    #MiscOps.VoxelizeVolumeMesh('./dispSurfaceRefZeroPoisson2D.vtu', './dispSurfaceRefZeroPoissonTwoDVox.vti', 0, 0.000, 'initSurfaceVoxelized2D.vti', False, 0.025)
    #MiscOps.VoxelizeVolumeMesh('./dispSurfaceRefZeroPoisson2D.vtu', './dispSurfaceRefZeroPoissonTwoDVoxIsoContour.vti', 0, 0.000, 'initSurfaceVoxelized2D.vti', False, 0.025)

    #run simulations
    results = []
    for j in range(0,i-1):  
        os.chdir( startDir )    
        createAndRunHnnSimulation(args_list[j])

    os.chdir( startDir )
    #vtus = ['vtus', 'vtus2']
    #weights =  [0.5, 0.5]

    weights = []
    for i in range(0, COUNTER):
        weights.append(1.0/COUNTER)


    #DICE evaluation (voxel based)

    #reference 
    count_ref = float(MiscOps.CountVoxelsAbove('./dispSurfaceRefZeroPoissonTwoDVox.vti', 127));

    #Chens IsoContour method with monte carlo
    MiscOps.IsoContourOperator(DIR, 'init.vtu', result_vtus, weights); #creates 'isocontour_outer.vtp'
    MiscOps.VoxelizeSurfaceMesh('./isocontour_outer.vtp', './isocontour_outerTwoDVoxIsoContour.vti', 0, 0.000, 'initSurfaceVoxelized.vti', False, 0.025)
    count_result_mc_IsoContour = float(MiscOps.CountVoxelsAbove('./isocontour_outerTwoDVoxIsoContour.vti', 127));
    MiscOps.ImageSum('*' + 'TwoDVoxIsoContour.vti', True, 'SumIsoContourAndRef.vti');
    count_intersect_mc_IsoContour = float(MiscOps.CountVoxelsAbove('./SumIsoContourAndRef.vti', 127+127));
    
    dice_mc_IsoContour = (2 * count_intersect_mc_IsoContour) / (count_result_mc_IsoContour+count_ref)

    shutil.move('./isocontour_initial.vtp', DIR + 'isocontour_initial' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_mean.vtp', DIR + 'isocontour_mean' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_inner.vtp', DIR + 'isocontour_inner' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_outer.vtp', DIR + 'isocontour_outer' + str(COUNTER) +'.vtp')
    shutil.move('./isocontour_outerTwoDVoxIsoContour.vti', DIR + 'isocontour_outerTwoDVoxIsoContour' + str(COUNTER) +'.vti')
    shutil.move('./SumIsoContourAndRef.vti', DIR + 'SumIsoContourAndRef' + str(COUNTER) +'.vti')


    #Markus Image sum method (works only with monte carlo) 
    MiscOps.ImageSum(DIR + NAME+'*' + '.vti', True, 'imgSumTwoDVox.vti');
    MiscOps.vtkMarchingCube('./imgSumTwoDVox.vti', './imgSumIsoSurface.vtp', 12);    
    count_result_mc_imgsum = float(MiscOps.CountVoxelsAbove('./imgSumTwoDVox.vti', 12));
    MiscOps.ImageSum('*' + 'TwoDVox.vti', True, 'SumResultAndRef.vti');
    count_intersect_mc_imgsum = float(MiscOps.CountVoxelsAbove('./SumResultAndRef.vti', 134)); #127 + 6 + 1
    dice_mc_imgsum = (2 * count_intersect_mc_imgsum) / (count_result_mc_imgsum+count_ref)

    shutil.move('./imgSumTwoDVox.vti', DIR + 'imgSumTwoDVox' + str(COUNTER) +'.vti')
    shutil.move('./imgSumIsoSurface.vtp', DIR + 'imgSumIsoSurface' + str(COUNTER) +'.vtp')
    shutil.move('./SumResultAndRef.vti', DIR + 'SumResultAndRef' + str(COUNTER) +'.vti')


    results_file = open(results_file_name, 'a')
    csv_writer = csv.writer(results_file)
    csv_writer.writerow( (COUNTER, NAME, count_ref, count_result_mc_IsoContour, count_intersect_mc_IsoContour, dice_mc_IsoContour, count_ref, count_result_mc_imgsum, count_intersect_mc_imgsum, dice_mc_imgsum) )
    results_file.close()


    #delet intermediate results folders
    for i in range(1, COUNTER+1) :
        shutil.rmtree('./' + NAME + str(i))  

    #num_of_workers =   multiprocessing.cpu_count() -1
    #pool = multiprocessing.Pool(5)
    #pool.map(createAndRunHnnSimulation, args_list)
