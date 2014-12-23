import numpy
import unittest

__author__ = 'weigl'

from msml.exporter.hiflow3.findrot import find_rotation, convert4x4


class FindRotTest(unittest.TestCase):
    def test_findrot1(self):
        a = (0, 0, 1)
        b = (0, 1, 0)

        R = find_rotation(a, b)
        self.assertEqualDirection(b, R.dot(a))

    def test_findrot2(self):
        a = (10, 2, 6)
        b = (0, 0, -9.81)
        R = find_rotation(a, b)

        self.assertEqualDirection(b, R.dot(a))


    def assertEqualDirection(self, expected, got):
        e = numpy.array(expected, dtype=float)
        g = numpy.array(got, dtype=float)

        e = 1 / numpy.linalg.norm(e) * e
        g = 1 / numpy.linalg.norm(g) * g

        self.assertTrue(
            numpy.linalg.norm(e - g) < 1e-14,
            "got %s , expected %s" % (g, e)
        )


    def test_convert4x4(self):
        mat = numpy.matrix([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape((3, 3))

        ref = numpy.matrix([[1, 2, 3, 0], [4, 5, 6, 0], [7, 8, 9, 0], [0, 0, 0, 1]], dtype=float)
        n = convert4x4(mat)

        for i in range(4):
            for j in range(4):
                self.assertEquals(ref[i,j] == n[i,j])
