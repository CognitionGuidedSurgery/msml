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

from unittest import TestCase

class Lungs(object):
    def __init__(self, msml_filename, p):
        self.app = App(exporter='nsofa', output_dir='batchedPressureNew' + str(p), executor='sequential')
        self.mf = self.app._load_msml_file(msml_filename)
        self._surface_pressure = p
    
    def __call__(self):
        self.app.memory_init_file = {
            "surface_pressure":str(self._surface_pressure) 
        }
        mem = self.app.execute_msml(self.mf, ) 
        return mem._internal['volumeMeasure']['volume']

class LungsTest(TestCase):
    def test_Lung(self):
        msml_file = os.path.abspath('../../examples//CGALi2vLungs/Lungs_new.xml')
        for p in range (20, 80, 20):
            l = Lungs(msml_file, p)
        volume = l()