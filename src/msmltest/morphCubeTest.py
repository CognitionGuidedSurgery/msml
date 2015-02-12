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
        #compare volume of mesh before and after morphing, volume after morphing should be less than volume before morphing
        originalVolume = mem._internal['OriginalPistonSurfaceVolume']['volume']
        morphedVolume = mem._internal['MorphedPistonSurfaceVolume']['volume']
        self.assertTrue(morphedVolume<originalVolume)
        
        #now, check the dice coefficient (should be above 0.5, below 1) 
        diceCoefficient = mem._internal['computeDice']['diceCoefficient']
        self.assertTrue(diceCoefficient>0.5 and diceCoefficient<1)
        