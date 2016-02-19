__author__ = 'Sarah Grimm'
__date__ = '2015-05-29'

from msml.frontend import App

from unittest import TestCase

import test_common


class CorrectVoxelIdRatio(object):
    def __init__(self, msml_filename, facet_size, facet_distance, cell_radius, cell_size):
        self.app = App(exporter='nsofa', output_dir= test_common.SCENARIOS_DIR / "CorrectVoxelIdRatio/out_CorrectVoxelIdRatio", 
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



class CorrectVoxelIdRatioTest(TestCase):
    
    def test_quality(self):
        msml_file = test_common.SCENARIOS_DIR / "CorrectVoxelIdRatio/CorrectVoxelIdRatio.msml.xml"
        print("Test %s" % msml_file)
        q1 = CorrectVoxelIdRatio(msml_file, 8, 8, 3, 8)
        q2 = CorrectVoxelIdRatio(msml_file, 30, 30, 3, 30)
        quality1 = q1()
        quality2 = q2()
        self.assertTrue( quality1 > quality2)
        