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

msml_file = os.path.abspath('../CGALi2vLungs/lungs_new.xml')

p_v_history = dict()

def f(p_array):
    p = p_array[0]
    if (p<-50 or p > 70): 
        return 8119088*2 
    app = frontend.App(exporter='nsofa', output_dir='batchedPressure' + str(p))
    mfile = app._load_msml_file(msml_file)
    mfile.scene[0].constraints[0].constraints[1].pressure = str(p)
    mfile.scene[0].constraints[0].constraints[1].attributes['pressure'] =  str(p)
    mfile.scene[0].constraints[0].constraints[2].pressure =  str(p)
    mfile.scene[0].constraints[0].constraints[2].attributes['pressure'] =  str(p)
    mem = app.execute_msml(mfile)
    aReturn = abs(mem._internal['volumeMeasure']['volume'] - 8400000)
    p_v_history[p] = mem._internal['volumeMeasure']['volume']
    return aReturn

p0 = x0 = np.asarray((20))
optimize.fmin_cg(f, x0)
p_v_history
    
