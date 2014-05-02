# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
# Medicine Meets Virtual Reality (MMVR) 2014
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

"""

__author__ = 'Alexander Weigl'
__date__ = '2014-02-21'


class Sort(object):
    def __init__(self, physical, logical=None):
        assert physical is not None
        self._physical = physical
        self._logical = logical

    def __eq__(self, other):
        if other is self:
            return True

        if isinstance(other, Sort):
            return other._logical == self._logical and self._physical == other._physical

        return False

    def __lt__(self, other):
        if other is self:
            return False

        a = issubclass(self._physical, other._physical)

        if self._logical is None and other._logical is None:
            return a
        else:
            b = issubclass(self._logical, other._logical)
            return a and b

        return False

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other

    def __str__(self):
        return "<Sort: %s %s>" % (self.physical, self._logical)

    @property
    def physical(self):
        return self._physical

    @physical.setter
    def physical(self, fmt):
        if not fmt:
            assert isinstance(fmt, type)
        self._physical = fmt


    @property
    def logical(self):
        return self._logical

    @logical.setter
    def logical(self, tp):
        assert isinstance(tp, type)
        self._logical = tp


# ################################################
# #  Logical Type Hierarchy
#

class MSMLTop(object): pass


class IndexSet(MSMLTop): pass


class NodeSet(IndexSet): pass


class FaceSet(IndexSet): pass


class ElementSet(IndexSet): pass


class Mesh(MSMLTop): pass


class Volume(Mesh): pass


class Tetrahedral(Volume): pass


class Hexahedral(Volume): pass


class QuadraticTetraHedral(Volume): pass


class Surface(Mesh): pass


class Triangular(Surface): pass


class Square(Surface): pass


class Image(MSMLTop): pass


class Image2D(Image): pass


class Image3D(Image): pass


class PhysicalQuantities(MSMLTop): pass


class Scalar(PhysicalQuantities): pass


class VonMisesStress(Scalar): pass


class Vector(PhysicalQuantities): pass


class Displacement(Vector): pass


class Force(Vector): pass


class Velocity(Vector): pass


class Tensor(PhysicalQuantities): pass


class Stress(PhysicalQuantities): pass


##########################################################
##
# Physical Hierarchy
class MSMLPhysicalTop(object): pass


class InMemory(MSMLPhysicalTop):
    pass


class MSMLFloat(float, MSMLPhysicalTop): pass


class MSMLInt(int, MSMLPhysicalTop): pass

class MSMLBool(int, MSMLPhysicalTop): pass


class MSMLUInt(int, MSMLPhysicalTop): pass


class MSMLString(str, MSMLPhysicalTop): pass


class MSMLListUI(list, MSMLPhysicalTop): pass


class MSMLListI(list, MSMLPhysicalTop): pass


class MSMLListFI(list, MSMLPhysicalTop): pass


class InFile(MSMLPhysicalTop):
    pass


class PNG(InFile):
    pass


class ContainerFile(InFile):
    def __init__(self, filename, partname = None):
        if not partname:
            self.filename, self.partname = filename.split(";")
        else:
            self.filename = filename
            self.partname = partname


class VTK(ContainerFile): pass


class STL(InFile): pass


class DICOM(ContainerFile): pass


class HDF5(ContainerFile): pass

