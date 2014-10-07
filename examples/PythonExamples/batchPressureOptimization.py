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


class Lungs(object):
    def __init__(self, msml_filename, p):
        self.app = App(exporter='nsofa', output_dir='batchedPressureNew' + str(p))
        self.mf = self.app._load_msml_file(msml_filename)
        self._surface_pressure = p
    
    def __call__(self):
        self.app.memory_init_file = {
            "surface_pressure":self._surface_pressure 
        }
        mem = self.app.execute_msml(self.mf, ) 
        return mem._internal['volumeMeasure']['volume']


def f_to_minimize(p_array):
    p = p_array[0]
    if (p<-50 or p > 70): # 
        print p
        return 8119088+100*(abs(p)+1)
    l = Lungs(msml_file, p)
    volume = l() 
    return abs(volume- 8400000)

msml_file = os.path.abspath('../CGALi2vLungs/lungs_new.xml')


p0 = x0 = np.asarray((20))
pn = optimize.fmin_cg(f_to_minimize, x0, epsilon=0.1)
print pn
    
