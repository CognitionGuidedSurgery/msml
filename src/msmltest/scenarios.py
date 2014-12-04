__author__ = 'Alexander Weigl'
__date__ = '2014-06-06'

from unittest import TestCase

from path import path
import msml.env, msml.frontend

msml.env.alphabet_search_paths = []

ROOT = path(__file__).dirname() / "../../share/testdata"
ALPHABET_DIR = ROOT / 'alphabet'


class Scenarios(TestCase):
    def setUp(self):
        self.app = msml.frontend.App(executor="phase", exporter="sofa", output_dir=ROOT / "tmp",
                                     add_search_path=['../share/alphabet', 'share/alphabet'])


    def test_liver(self):
        msml_file = ROOT / "scenarios/Liver/liverLinear.msml.xml"
        print("Test %s" % msml_file)

        memory = self.app.execute_msml_file(msml_file)
        error = memory._internal['meanErrorOperator']['error']
        self.assertTrue( error < 3.14e-4)