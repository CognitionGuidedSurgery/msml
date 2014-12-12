'''
Created on 12.12.2014

@author: Daniel Schaubach
'''
import sys
import copy
from lxml import etree     
import os
import ntpath




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

import test_common

class SlidingContactTest(TestCase):
    def test_slidingContact(self):
        msml_file = test_common.MSML_EXAMPLE_DIR / 'SlidingContact/sliding_cycy.xml'
        self.app = App(exporter='nsofa', output_dir= test_common.TMP_DIR / 'slideout', 
                       executor='sequential', add_search_path=[test_common.MSML_ALPHABET_DIR])
        self.mf = self.app._load_msml_file(msml_file)
        mem = self.app.execute_msml(self.mf, ) 
        
        