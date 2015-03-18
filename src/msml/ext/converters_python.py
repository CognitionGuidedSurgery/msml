__author__ = 'suwelack'

from msml.sortdef import *
from ..log import logger


try:
    import msml.ext.misc as ops

    def vtk_mesh2generic_mesh(vtkMesh):



        vertVec = ops.vectord()
        cellSizeVec = ops.vectorui()
        conVec = ops.vectorui()
        flag = ops.ConvertVTKToGenericMesh(vertVec, cellSizeVec, conVec, vtkMesh)

        vertList = []
        for i in range(0,vertVec.size()):
            vertList.append(vertVec[i])

        cellSizeList = []
        for i in range(0,cellSizeVec.size()):
            cellSizeList.append(cellSizeVec[i])

        conList = []
        for i in range(0,conVec.size()):
            conList.append(conVec[i])

        genMesh = GenericMesh(vertList, cellSizeList, conList)

        return genMesh
except:
    logger.fatal("Could not import vtk python module. Did you install python-vtk?")