__author__ = 'Sarah Grimm'
__date__ = '2015-05-29'

from msml.frontend import App

from unittest import TestCase

import test_common


class MeshQuality(object):
    def __init__(self, msml_filename, facet_size, facet_distance, cell_radius, cell_size):
        self.app = App(exporter='nsofa', output_dir= test_common.SCENARIOS_DIR / "MeshQuality/out_vertebra", 
           executor='sequential', add_search_path=[test_common.MSML_ALPHABET_DIR])
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



class MeshQualityTest(TestCase):
    
    def test_quality(self):
        msml_file = test_common.SCENARIOS_DIR / "MeshQuality/MeshQuality.msml.xml"
        print("Test %s" % msml_file)
        for i in range(2,6):
            print(i)
            q1 = MeshQuality(msml_file, 10, 5, i, 30)
            q1()
        for i in range(1,31):
            print(i)
            q1 = MeshQuality(msml_file, i, i, 3, i)
            q1()
        
        
        
        #self.assertTrue( quality2 > quality2) 
