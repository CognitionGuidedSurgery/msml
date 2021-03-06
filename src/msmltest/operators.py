__author__ = 'weigl'

from msml.env import load_user_file
import test_common

load_user_file()

from unittest import TestCase

from msml.sorts import MSMLString

import TetgenOperatorsPython as P
import MiscMeshOperatorsPython as M

import msml.ext.msmlvtk as vtk

import filecmp


def fcmp(a, b):
    return filecmp.cmp(a, b, shallow=False)


# Just some Tetgen paramters
preserveBoundary = True
maxEdgeRadiusRatio = 10
minDihedralAngleDegrees = 10
maxTetVolumeOrZero = 0
optimizationLevel = 1
optimizationUseEdgeAndFaceFlips = False
optimizationUseVertexSmoothing = False
optimizationUseVertexInsAndDel = False


class OperatorTest(TestCase):
    def test_tetgen(self):
        # input_file = INP_DIR / 'Bunny6000Surface.vtk'
        input_file = test_common.MSML_ROOT / 'examples/BunnyExample/Bunny6000Surface.vtk'
        ref_file = test_common.REF_DIR / 'test_tetgen_1.vtk'
        output_file = test_common.TMP_DIR / 'test_tetgen_2.vtk'

        P.TetgenCreateVolumeMesh(str(input_file),
                                 str(output_file),
                                 preserveBoundary,
                                 maxEdgeRadiusRatio,
                                 minDihedralAngleDegrees,
                                 maxTetVolumeOrZero,
                                 optimizationLevel,
                                 optimizationUseEdgeAndFaceFlips,
                                 optimizationUseVertexSmoothing,
                                 optimizationUseVertexInsAndDel)

        self.assertTrue(fcmp(ref_file, output_file),
                        "%s has not the same contents as %s" % (output_file, ref_file))

    def test_tetgen_sorts(self):
        # input_file = INP_DIR / 'Bunny6000Surface.vtk'
        input_file = test_common.MSML_ROOT / 'examples/BunnyExample/Bunny6000Surface.vtk'
        ref_file = test_common.REF_DIR / 'test_tetgen_1.vtk'
        output_file = test_common.TMP_DIR / 'test_tetgen_1.vtk'

        P.TetgenCreateVolumeMesh(MSMLString(input_file),
                                 MSMLString(output_file),
                                 preserveBoundary,
                                 maxEdgeRadiusRatio,
                                 minDihedralAngleDegrees,
                                 maxTetVolumeOrZero,
                                 optimizationLevel,
                                 optimizationUseEdgeAndFaceFlips,
                                 optimizationUseVertexSmoothing,
                                 optimizationUseVertexInsAndDel)

        self.assertTrue(filecmp.cmp(ref_file, output_file),
                        "%s has not the same contents as %s" % (output_file, ref_file))

    def test_boxROIToIndexOperators(self):
        input_file = str(test_common.REF_DIR / 'test_tetgen_1.vtk')
        a = M.ComputeIndicesFromBoxROI(input_file,
                                       [-0.1, -0.03, -0.07, 0.06, 0.19, 0.06], 'elements')

        print type(a), len(a)

#tests disabled, see msml issue #204
#===============================================================================
#     def test_closestPoints_without_radius(self):
#         input_file = test_common.REF_DIR / 'bunny_tets.vtk'
#         result = vtk.closest_point(input_file, vector=(0, 0, 0))
#         self.assertDictEqual(
#            result,
#            {'index': 4943L, 'dist': 0.03453012740706179, 'point': (0.004991060122847557, 0.034084200859069824, 0.002384589985013008)})
# 
#     def test_closestPoints_with_radius(self):
#         input_file = test_common.REF_DIR / 'bunny_tets.vtk'
#         result = vtk.closest_point(input_file, vector=(0.0, 0.0, 0.0), radius=10.0)
#         self.assertDictEqual(
#             result,
#             {'index': 4943L, 'dist': 0.03453012740706179, 'point': (0.004991060122847557, 0.034084200859069824, 0.002384589985013008)})
#===============================================================================



    def test_convertVTKtoVTU(self):
        input_file = test_common.REF_DIR / 'test_tetgen_1.vtk'
        output_file = test_common.TMP_DIR / "vtu_test1.vtu"
        reference_file = test_common.REF_DIR / "vtu_test1.vtu"

        M.ConvertVTKToVTU(str(input_file), str(output_file))

        # self.assertTrue(
        #    fcmp(output_file, reference_file),
        #    "%s has not the same contents as %s" % (output_file, reference_file)
        #)

