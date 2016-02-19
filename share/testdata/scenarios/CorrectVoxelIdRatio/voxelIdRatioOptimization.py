#requires SciPy: http://www.scipy.org/install.html


import sys
import copy
from lxml import etree     
import os
import ntpath
from path import path

import numpy as np
from scipy import optimize

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



class CorrectVoxelIdRatio(object):
    def __init__(self, msml_filename, facet_size, facet_distance, cell_radius, cell_size):

        self.app = App(exporter='nsofa', output_dir= 'C:/MSML/msml/share/testdata/scenarios/CorrectVoxelIdRatio/out_CorrectVoxelIdRatio', 
           executor='sequential')
        self.mf = self.app._load_msml_file(msml_filename)
        self._facet_size = facet_size
        self._facet_distance = facet_distance
        self._cell_radius = cell_radius
        self._cell_size = cell_size
    
    def __call__(self):
        self.app.memory_init_file = {
            "facet_size":float(self._facet_size),
            "facet_distance":float(self._facet_distance),
            "cell_radius":float(self._cell_radius),
            "cell_size":float(self._cell_size)
            
        }
        mem = self.app.execute_msml(self.mf, ) 
        return mem._internal['meshQuality']['quality']
      
def f_to_minimize(size_array):
    size = size_array[0]
    if (size < 1 or size > 35):  
        return 1 - (abs(size)/100)
    
    q = CorrectVoxelIdRatio(msml_file, size, size * 0.1, 3, size *3)
    quality = q()
    print quality 
    print abs(round(quality,2) - 0.95)
    return abs(round(quality,2) - 0.95)


msml_file = 'C:/MSML/msml/share/testdata/scenarios/CorrectVoxelIdRatio/CorrectVoxelIdRatio.msml.xml'
q0 = x0 = np.asarray((20))
qn = optimize.fmin_powell(f_to_minimize, x0,full_output=True, disp=1)
print qn
    
