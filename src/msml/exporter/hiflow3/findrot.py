# -*- encoding: utf-8 -*-
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
# endregionvm

"""find rotation.


http://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d

"""
__authors__ = 'Alexander Weigl <uiduw@student.kit.edu>'
__license__ = 'GPLv3'

from numpy import array, matrix, cross, eye, inner, zeros
from numpy.linalg import norm

__all__ = ['find_rotation', 'conv'
                            '']

def convert4x4(mat):
    m = matrix(zeros((4,4)))
    m[0:3,0:3] = mat
    m[-1,-1] = 1
    return list(m)

def find_rotation(a, b):
    """find the rotation matrix between vector `a` and `b`.

    :param a:
    :param b:
    :return:
    """

    assert len(a) == 3
    assert len(b) == len(a)

    a = array(a, dtype=float)
    b = array(b, dtype=float)

    v = cross(a, b)
    s = norm(v)
    c = inner(a, b)

    R = eye(3) + skew(v) + skew(v) ** 2 * (1 - c) / s ** 2
    return R


def skew(v):
    v1, v2, v3 = v
    return matrix([[0, -v3, v2], [v3, 0, -v1], [-v2, v1, 0]])