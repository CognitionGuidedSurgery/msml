__author__ = 'Markus Stoll'

from unittest import TestCase

from path import path
import msml.env, msml.frontend

import test_common

msml.env.alphabet_search_paths = []



class Scenarios(TestCase):
    def setUp(self):
        self.app = msml.frontend.App(executor="phase", exporter="base", 
            output_dir=test_common.TMP_DIR / "mitral_nosetest_output", add_search_path=[test_common.MSML_ALPHABET_DIR])


    def test_mitral(self):
        msml_file = test_common.SCENARIOS_DIR / "mitral/mitralvalveMeshing.msml.xml"
        print("Test %s" % msml_file)

        memory = self.app.execute_msml_file(msml_file)
