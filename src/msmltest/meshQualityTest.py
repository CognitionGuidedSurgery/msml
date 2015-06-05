__author__ = 'Sarah Grimm'
__date__ = '2015-05-29'

from msml.frontend import App

from unittest import TestCase

import test_common



class MeshQuality(TestCase):
    
    def test_quality(self):
        msml_file = test_common.SCENARIOS_DIR / "MeshQuality/MeshQuality.msml.xml"
        self.app = App(exporter='nsofa', output_dir= test_common.SCENARIOS_DIR / "MeshQuality/out_vertebra", 
                       executor='sequential', add_search_path=[test_common.MSML_ALPHABET_DIR])
        self.mf = self.app._load_msml_file(msml_file)
        memory = self.app.execute_msml(self.mf, ) 
        quality = memory._internal['meshQuality']['quality']
        print(memory._internal['meshQuality'])
        self.assertTrue( quality > 0.5) 
