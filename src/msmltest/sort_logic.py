from msml.sorts import *
from pprint import  pprint

__author__ = "Alexander Weigl"
__date__ = "2014-05-05"

from unittest import  TestCase

class SortLogicTest(TestCase):
    def test_basic_sorts(self):
        S = get_sort("str")
        I = get_sort(int)
        F = get_sort(float)

        self.assertEqual(MSMLString, S._physical)
        self.assertEqual(None, S.logical)
        self.assertEqual(MSMLInt, I._physical)
        self.assertEqual(MSMLFloat, F._physical)

    def test_compatibility(self):

        S1 = Sort(MSMLString, Mesh)
        S2 = Sort(str, Mesh)
        I = get_sort(int)
        F = get_sort(float)

        self.assertTrue(S2 == S2)
        self.assertTrue(S1 == S1)
        self.assertTrue(I == I)
        self.assertTrue(F == F)

        self.assertTrue(S1 < S2)
        self.assertTrue(S2 > S1)
        self.assertTrue(S1 != S2)
        self.assertFalse(S2 < S1)
        self.assertTrue(S2 != S1)
        self.assertFalse(S1 < I)
        self.assertFalse(I < S1)
        self.assertFalse(S1 > I)
        self.assertFalse(S1 == I)
        self.assertTrue(S1 != I)
        self.assertFalse(S1 == I)
