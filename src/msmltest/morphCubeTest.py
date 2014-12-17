'''
Created on 17.12.2014

@author: Daniel Schaubach
'''

from msml.frontend import App

from unittest import TestCase

import test_common

class MorphCubeTest(TestCase):
    def test_morphCube(self):
        msml_file = test_common.MSML_EXAMPLE_DIR / 'MorphCube/morphtest.xml'
        self.app = App(exporter='nsofa', output_dir= test_common.TMP_DIR / 'morphout', 
                       executor='sequential', add_search_path=[test_common.MSML_ALPHABET_DIR])
        self.mf = self.app._load_msml_file(msml_file)
        mem = self.app.execute_msml(self.mf, ) 
        originalVolume = mem._internal['OriginalPistonSurfaceVolume']['volume']
        morphedVolume = mem._internal['MorphedPistonSurfaceVolume']['volume']
        self.assertTrue(morphedVolume<originalVolume)
        