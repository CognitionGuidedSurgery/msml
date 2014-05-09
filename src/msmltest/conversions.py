__author__ = 'Alexander Weigl'

from unittest import TestCase

import msml.sorts as S


class ConversionTest(TestCase):
    def test_bool(self):
        self.assertTrue(S._bool("on"))
        self.assertTrue(S._bool("yes"))
        self.assertTrue(S._bool("true"))
        self.assertTrue(S._bool("True"))
        self.assertTrue(S._bool("ON"))
        self.assertTrue(S._bool("YES"))

        self.assertFalse(S._bool("no"))
        self.assertFalse(S._bool("off"))
        self.assertFalse(S._bool("OFF"))
        self.assertFalse(S._bool("false"))
        self.assertFalse(S._bool("False"))


    def test_vector_int(self):
        self.assertEqual([1, 2, 3], S._list_integer("1 2 3"))
        self.assertEqual([1, 2, 3], S._list_integer("1 2.3 3.0"))

    def test_vector_float(self):
        self.assertEqual([1.0, 2.0, 3.0], S._list_float("1 2 3"))
        self.assertEqual([1.0, 2.3, 3.0], S._list_float("1 2.3 3.0"))


    # def test_container_file(self):
    #     cf = S.ContainerFile("test.vtk;part")
    #     self.assertEqual('test.vtk', cf.filename)
    #     self.assertEqual('part', cf.partname)

    def test_str_MSMLString(self):
        cvt = S.conversion(str, S.MSMLString)
        self.assertEqual(S.MSMLString("abc"), cvt("abc"))

    def test_MSMLString_float(self):
        cvt = S.conversion(S.MSMLString, S.MSMLFloat)
        self.assertEqual(3.5, cvt("3.5"))