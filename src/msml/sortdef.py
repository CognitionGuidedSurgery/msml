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

"""


__author__ = 'Alexander Weigl'
__date__ = '2014-02-21'

from path import path

class Sort(object):
    def __init__(self, type, format = None):
        self._type, self._format = None, None

        self.type = type
        self.format = format

    def __eq__(self, other):
        if other is self:
            return True

        if isinstance(other, Sort):
            return other.format == self.format and self.type == other.type

        return False

    def __lt__(self, other):
        if other is self:
            return False

        a = issubclass(self.type, other.type)

        if self._format is None and other.format is None:
            return a
        else:
            b = issubclass(self.format,  other.format)
            return a and b

        return False

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other

    def __str__(self):
        return "<Sort: %s %s>" % (self.type, self.format)

    @property
    def format(self): return self._format

    @format.setter
    def format(self, fmt):
        assert fmt is None or isinstance(fmt, type)
        self._format = fmt


    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, tp):
        assert isinstance(tp, type)
        self._type = tp

#################################################
class IndexGroup(object):
    pass

class Vertice(object):
    def __init__(self, x= 0, y = 0, z = 0):
        self.x, self.y, self.z = x,y,z

    def __str__(self):
        return str( (self.x,self.y,self.z) )

    def __repr__(self):
        return "msml.model.sortdef.Vertice(%s,%s,%s)" % (self.x, self.y, self.z)

class Vertices(object):
    def __init__(self, h):
        self.list = h

    def __str__(self):
        return str(self.list)

class Filename(path):
    pass

class MeshFile(Filename):
    pass

class TriangularMeshFile(MeshFile):
    pass

class QuadraticMeshFile(MeshFile):
    pass

class LinearMeshFile(MeshFile):
    pass

###


class Format(object):
    pass

class VTI(Format): pass


class VTK(Format): pass


class VTU(Format): pass


class Image(Format): pass


class PNG(Image): pass


class JPG(Image): pass

