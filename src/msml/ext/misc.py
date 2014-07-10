# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
#   S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
#   The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#   Medicine Meets Virtual Reality (MMVR) 2014
#
# Copyright (C) 2013-2014 see Authors.txt
#
# If you have any questions please feel free to contact us at suwelack@kit.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# endregion


"""
Small wrapper around MiscMeshOperatorsPython.so
"""

__author__ = "Alexander Weigl"
__date__ = "2014-01-28"

from warnings import warn

from msml.exceptions import MSMLUnknownModuleWarning

try:
    from MiscMeshOperatorsPython import *
except ImportError, e:
    import sys
    warn("Could not import MiscMeshOperatorsPython. "
         "This is a C++-Modul. "
         "Have you successfully compiled and installed it? "
         "Error is %s, Current sys.path: %s" % (e, sys.path),
         MSMLUnknownModuleWarning, 0)

__all__ = ['colorMeshFromComparison',
           'colorMeshOperator',
           'compareMeshes',
           'compareMeshesFullError',
           'computeIndicesFromBoxROI',
           'computeIndicesFromMaterialId',
           'convertSTLToVTK',
           'convertVTKMeshToAbaqusMeshString',
           'convertVTKMeshToFeBioMeshString',
           'createFeBioPressureOutput',
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


def _bool(s):
    return s in ("on", "True", "true", "yes")

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


def computeIndicesFromMaterialId(mesh, num, type):
    return cpp.computeIndicesFromMaterialId(mesh, int(num), type)


def convertSTLToVTK(*args ):
    return cpp.convertSTLToVTK(*args )


def convertVTKMeshToAbaqusMeshString(*args ):
    return cpp.convertVTKMeshToAbaqusMeshString(*args )


def convertVTKMeshToFeBioMeshString(*args ):
    return cpp.convertVTKMeshToFeBioMeshString(*args )

def convertFeBioMeshStringToVTKMesh(*args ):
    return cpp.FeBioToVTKConversion(*args )

def createFeBioPressureOutput(*args ):
    return cpp.createFeBioPressureOutput(*args )

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

def ExtractAllSurfacesByMaterial(meshin, meshout, cut):
    return cpp.ExtractAllSurfacesByMaterial(meshin, meshout, _bool(cut) )


def projectSurfaceMesh(*args ):
    return cpp.projectSurfaceMesh(*args )


def voxelizeSurfaceMesh(a,b,c):
    return cpp.voxelizeSurfaceMesh(a,b, int(c))

def GenerateDVF(ref_mesh, DVFFilename, DeformedMesh, multipleReferenceGrids):
    return cpp.GenerateDVF(str(ref_mesh), DVFFilename, DeformedMesh, _bool(multipleReferenceGrids))
