import sys
import copy
from lxml import etree     
import os
import ntpath
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

import test_common
from unittest import TestCase

class Lungs(object):
    def __init__(self, msml_filename, p):
        self.app = App(exporter='nsofa', output_dir=test_common.TMP_DIR / 'batchedPressureNew' + str(p), executor='sequential', 
                       add_search_path=[test_common.MSML_ALPHABET_DIR])
        self.mf = self.app._load_msml_file(msml_filename)
        self._surface_pressure = p
    
    def __call__(self):
        self.app.memory_init_file = {
            "surface_pressure":float(self._surface_pressure)
        }
        mem = self.app.execute_msml(self.mf, ) 
        return mem._internal['volumeMeasure']['volume']

class LungsTest(TestCase):
    def test_Lung(self):
        #run 2 lung expanded by pressure simulations with difference pressure values p0=1 and p1=100.
        #assert that end volume of simulation with p0 is lower than in simulation with p1.
        msml_file = test_common.MSML_EXAMPLE_DIR / 'CGALi2vLungs/Lungs_simple.xml'
        l1 = Lungs(msml_file, 1)
        l2 = Lungs(msml_file, 100) #large pressure difference needed as CGAl meshes non-deterministic
        volume1 = l1()
        volume2 = l2()
        self.assertTrue( volume1 < volume2)
        
        