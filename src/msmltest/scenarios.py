__author__ = 'Alexander Weigl'
__date__ = '2014-06-06'

from unittest import TestCase

from path import path
import msml.env, msml.frontend

import test_common

msml.env.alphabet_search_paths = []



class Scenarios(TestCase):
    def setUp(self):
        self.app = msml.frontend.App(executor="phase", exporter="sofa", 
            output_dir=test_common.TMP_DIR / "Scenarios_Resultsp", add_search_path=[test_common.MSML_ALPHABET_DIR])


    def test_liver(self):
        msml_file = test_common.SCENARIOS_DIR / "Liver/liverLinear.msml.xml"
        print("Test %s" % msml_file)

        memory = self.app.execute_msml_file(msml_file)
        error = memory._internal['meanErrorOperator']['error']
        self.assertTrue( error < 3.14e-4) 
