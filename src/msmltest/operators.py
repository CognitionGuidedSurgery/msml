__author__ = 'weigl'


from msml.env import load_user_file

load_user_file()

import filecmp
from unittest import TestCase

from path import path
from msml.sorts import MSMLString

import TetgenOperatorsPython as P
import MiscMeshOperatorsPython as M


MSML_ROOT = (path(__file__).dirname() / '..' / '..').abspath()

REF_DIR = MSML_ROOT / "src/msmltest/references"
TMP_DIR = MSML_ROOT / "src/msmltest/tmp"
INP_DIR = MSML_ROOT / "src/msmltest/input"

import os

def fcmp(a,b):
    print ("diff -b %s %s" %(a,b))
    return os.system("diff -b %s %s" %(a,b)) == 0

class OperatorTest(TestCase):
    def test_tetgen(self):
        input_file = INP_DIR / 'Bunny6000Surface.vtk'
        ref_file = REF_DIR / 'test_tetgen_1.vtk'
        output_file = TMP_DIR / 'test_tetgen_1.vtk'

        P.CreateVolumeMeshPython(str(input_file),
                                 str(output_file), False)

        self.assertTrue(fcmp(ref_file, output_file),
                        "%s has not the same contents as %s" % (output_file, ref_file))

    def test_tetgen_sorts(self):
        input_file = INP_DIR / 'Bunny6000Surface.vtk'
        ref_file = REF_DIR / 'test_tetgen_2.vtk'
        output_file = TMP_DIR / 'test_tetgen_2.vtk'

        P.CreateVolumeMeshPython(MSMLString(input_file),
                                 MSMLString(output_file), False)

        self.assertTrue(filecmp.cmp(ref_file, output_file),
                        "%s has not the same contents as %s" % (output_file, ref_file))

    def test_boxROIToIndexOperators(self):
        input_file = str(INP_DIR / 'bunnyVolumeMesh.vtk')
        a = M.computeIndicesFromBoxROI(input_file,
                                       [-0.1, -0.03, -0.07, 0.06, 0.19, 0.06], 'elements')

        print type(a), len(a)


    def test_convertVTKtoVTU(self):
        input_file = INP_DIR / 'bunnyVolumeMesh.vtk'
        output_file = TMP_DIR / "vtu_test1.vtu"
        reference_file = REF_DIR / "vtu_test1.vtu"

        M.ConvertVTKToVTUPython(str(input_file), str(output_file))

        self.assertTrue(
            fcmp(output_file, reference_file),
            "%s has not the same contents as %s" % (output_file, reference_file)
        )