__author__ = 'Sarah Grimm'
__date__ = '2015-05-29'

from msml.frontend import App

from unittest import TestCase

import test_common


class HausdorffDistanceTest(TestCase):
    def test_hausdorffDistance(self):
        msml_file = test_common.SCENARIOS_DIR / 'HausdorffDistance/HausdorffDistance.msml.xml'
        self.app = App(exporter='nsofa', output_dir= test_common.SCENARIOS_DIR / "HausdorffDistance/out_HausdorffDistance.msml", 
                       executor='sequential', add_search_path=[test_common.MSML_ALPHABET_DIR])
        self.mf = self.app._load_msml_file(msml_file)
        mem = self.app.execute_msml(self.mf, ) 
        #compare volume of mesh before and after morphing, volume after morphing should be less than volume before morphing
        hausdorffDistance = mem._internal['hausdorffDistance']['hausdorffDistance']
        self.assertEqual(hausdorffDistance, 0)
        