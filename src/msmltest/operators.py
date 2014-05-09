__author__ = 'weigl'

from unittest import TestCase

from msml.sorts import MSMLString
import TetgenOperatorsPython as P
import MiscMeshOperatorsPython as M

class OperatorTest(TestCase):
    def test_tetgen(self):
        P.CreateVolumeMeshPython('/homes/students/weigl/workspace1/msml/examples/BunnyExample/Bunny6000Surface.vtk',
                                 '/homes/students/weigl/workspace1/msml/examples/BunnyExample/bunnyVolumeMesh.vtk',
                                 False)

    def test_tetgen_sorts(self):
        P.CreateVolumeMeshPython(MSMLString('/homes/students/weigl/workspace1/msml/examples/BunnyExample/Bunny6000Surface.vtk'),
                                 MSMLString('/homes/students/weigl/workspace1/msml/examples/BunnyExample/bunnyVolumeMesh.vtk'),
                                 False)


    def test_boxROIToIndexOperators(self):
        a = M.computeIndicesFromBoxROI('/homes/students/weigl/workspace1/msml/examples/BunnyExample/bunnyVolumeMesh.vtk',
                                   [-0.1, -0.03, -0.07, 0.06, 0.19, 0.06], 'elements')

        print type(a), len(a)
