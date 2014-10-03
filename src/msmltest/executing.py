__author__ = 'Alexander Weigl'
__date__ = '2014-06-06'

from unittest import TestCase

from path import path

import msml.env
from msml.frontend import App
from  msml.log import _reported
from  operator import itemgetter

msml.env.alphabet_search_paths = []

ROOT = path(__file__).dirname()
ALPHABET_DIR = ROOT / 'alphabet'

import msml.generators


class ExecutingWithTestAlphabet(TestCase):
    def setUp(self):
        msml.generators.reset_all()
        self.app = App(add_search_path=[ALPHABET_DIR], exporter='base')


    def test_simple_case_01(self):
        self.app.show(ROOT / 'msmlfiles/simple_case_01.msml.msml_xml')

        mem = self.app.execute_msml_file(ROOT / 'msmlfiles/simple_case_01.msml.msml_xml')
        self.assertEqual(
            {'a': {'o': 4}, 'converter_task_2': {'o': 2}, 'gen_2_': 2, 'i': '2'},
            mem._internal)

    def test_double_use_var_01(self):
        mem = self.app.execute_msml_file(ROOT / 'msmlfiles/double_use_variable_01.msml.msml_xml')
        self.assertEqual(
            {'a': {'o': 4}, 'gen_1_': 2, 'p': None, 'gen_4_': 'a = ', 'gen_3_': 'W', 'gen_2_': 'i = ', 'i': '2',
             'r': None, 'gen_5_': 'W', 'converter_task_1': {'o': '4'}, 'converter_task_2': {'o': 2}},
            mem._internal)


    def test_double_use_var_01(self):
        mem = self.app.execute_msml_file(ROOT / 'msmlfiles/double_use_variable_01.msml.msml_xml')
        self.assertEqual(
            {'a': {'o': 4}, 'gen_1_': 2, 'p': None, 'gen_4_': 'a = ', 'gen_3_': 'W', 'gen_2_': 'i = ', 'i': '2',
             'r': None, 'gen_5_': 'W', 'converter_task_1': {'o': '4'}, 'converter_task_2': {'o': 2}},
            mem._internal)


    def test_multiple_ids_01(self):
        mem = self.app.execute_msml_file(ROOT / 'msmlfiles/multiple_id_01.msml.msml_xml')
        self.assertReported(696)


    def assertReported(self, no):
        getnumber = itemgetter(1)
        numbers = set(map(getnumber, _reported))
        self.assertTrue(no in numbers, "Number %d was not reported.\nReported: %s" % (no,numbers))
