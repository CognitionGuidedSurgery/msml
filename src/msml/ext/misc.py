"""
Small wrapper around MiscMeshOperatorsPython.so
"""

__author__ = "Alexander Weigl"
__date__ = "2014-01-28"

from warnings import warn

from msml.model.exceptions import MSMLUnknownModuleWarning

try:
    import MiscMeshOperatorsPython as cpp
except ImportError, e:
    warn("Could not import MiscMeshOperatorsPython. "
         "This is the C++-Modul. Have you successfully compiled and installed it? "
         "Error is %s" % e,
         MSMLUnknownModuleWarning, 0)


class VecUInt(cpp.VecUInt):
    pass


class VecDouble(cpp.VecDouble):
    pass


__all__ = ['colorMeshFromComparison',
           'colorMeshOperator',
           'compareMeshes',
           'compareMeshesFullError',
           'computeIndicesFromBoxROI',
           'computeIndicesFromMaterialId',
           'convertSTLToVTK',
           'convertVTKMeshToAbaqusMeshString',
           'convertVTKPolydataToUnstructuredGrid',
           'convertVTKToSTL',
           'convertVtkToInp',
           'extractPointPositions',
           'extractSurfaceMesh',
           'projectSurfaceMesh',
           'voxelizeSurfaceMesh'
           'ApplyDVF',
           'ExtractAllSurfacesByMaterial',
           'GenerateDVF']

ApplyDVF = cpp.ApplyDVF
ExtractAllSurfacesByMaterial = cpp.ExtractAllSurfacesByMaterial
GenerateDVF = cpp.GenerateDVF


def colorMeshFromComparison(*args):
    return cpp.colorMeshFromComparison(*args )


def colorMeshOperator(*args ):
    import os, os.path

    print("pwd: %s" % os.getcwd())
    print("pid: %d" % os.getpid())

    args1 = os.path.join(os.getcwd(), args[0])
    args2 = os.path.join(os.getcwd(), args[1])

    return cpp.colorMeshOperator(args1, args2)


def compareMeshes(*args ):
    return cpp.compareMeshes(*args )


def compareMeshesFullError(*args ):
    return cpp.compareMeshesFullError(*args )


def _parse_points_triples(string):
    box = map(float, filter(lambda x: len(x) > 0, string.split(" ")))

    vd = cpp.VecDouble()
    for d in box: vd.append(d)
    return vd


def computeIndicesFromBoxROI(mesh, box, select):
    vd = _parse_points_triples(box)
    return cpp.computeIndicesFromBoxROI(mesh, vd, select)


def computeIndicesFromMaterialId(*args ):
    return cpp.computeIndicesFromMaterialId(*args )


def convertSTLToVTK(*args ):
    return cpp.convertSTLToVTK(*args )


def convertVTKMeshToAbaqusMeshString(*args ):
    return cpp.convertVTKMeshToAbaqusMeshString(*args )


def convertVTKPolydataToUnstructuredGrid(*args ):
    return cpp.convertVTKPolydataToUnstructuredGrid(*args )


def convertVTKToSTL(*args ):
    return cpp.convertVTKToSTL(*args )


def convertVtkToInp(*args ):
    return cpp.convertVtkToInp(*args )


def extractPointPositions(*args ):
    return cpp.extractPointPositions(*args )


def extractSurfaceMesh(*args ):
    return cpp.extractSurfaceMesh(*args )


def projectSurfaceMesh(*args ):
    return cpp.projectSurfaceMesh(*args )


def voxelizeSurfaceMesh(*args ):
    return cpp.voxelizeSurfaceMesh(*args )
