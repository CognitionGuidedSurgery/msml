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

class SlidingContactTest(TestCase):
    def test_slidingContact(self):
        msml_file = os.path.abspath('../examples//SlidingContact/sliding_cycy.xml')
        self.app = App(exporter='nsofa', output_dir='slideout', executor='sequential', add_search_path=['../share/alphabet', 'share/alphabet'])
        self.mf = self.app._load_msml_file(msml_file)
        mem = self.app.execute_msml(self.mf, ) 
        
        