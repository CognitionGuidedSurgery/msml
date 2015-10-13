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
 
 
DIR_ref = './Reference_solution/'
DIR = './MC100/'

reference = DIR_ref + 'isocontour_mean.vtp'
outfilename = DIR + 'isocontour_outer.vtp'
intersect_name = 'intersect.vtk'

MiscOps.ComputeDiceCoefficientPolydata(reference, outfilename, intersect_name)   

shutil.move('./' + intersect_name, DIR + intersect_name)
