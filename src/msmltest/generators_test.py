__author__ = 'weigl'

from unittest import  TestCase
from msml.generators import IdentifierGenerator

class IdentifierGeneatorTest(TestCase):
    def setUp(self):
        self.gen = IdentifierGenerator("a","b")

    def test_call(self):
        self.assertEqual("a1b", self.gen())
        self.assertEqual("a2b", self.gen())
        self.assertEqual("a3b", self.gen())
        self.assertEqual("a4b", self.gen())

    def test_reset(self):
        self.assertEqual("a1b", self.gen())
        self.assertEqual("a2b", self.gen())
        self.gen.reset()
        self.assertEqual("a1b", self.gen())
        self.assertEqual("a2b", self.gen())

    def test_has_generated(self):
        self.assertEqual("a1b", self.gen())
        self.assertEqual("a2b", self.gen())

        self.assertTrue(self.gen.has_generated("a1b"))
        self.assertTrue(self.gen.has_generated("a2b"))

        self.assertFalse(self.gen.has_generated("a3b"))
        self.assertFalse(self.gen.has_generated("a4b"))
        self.assertFalse(self.gen.has_generated("bc"))
        self.assertFalse(self.gen.has_generated("161"))
        self.assertFalse(self.gen.has_generated(""))
        self.assertFalse(self.gen.has_generated("afdlksfnba343252l31k6 231 4532432 434"))