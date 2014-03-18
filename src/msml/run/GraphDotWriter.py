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

__author__ = 'Alexander Weigl'

TMPL = """
digraph G {{
  //rankdir = LR;
  splines=ortho

  node [shape=box]

  {for n in nodes}
   {$ n.name } [ {$ n.spec} ]; {end}

  {for e in edges}
    {$ e.a } -> {$ e.b } [{$ e.spec }]; {end}

}
"""
import itertools

from collections import namedtuple


def kvstr(dic, noquote=False):
    return ', '.join(itertools.starmap(
        lambda k, v: '%s=%s' % (k, v.replace('"', "'")),
        dic.items()))


from msml.titen import titen as T

gen = T(text=TMPL)
N = namedtuple("NodeTP", "name spec")
E = namedtuple("EdgeTP", "a b spec")


class GraphDotWriter(object):
    def __init__(self, dag):
        self.edges = 0

        self.nodes = 0


    def __str__(self):
        nodes = [
            N(id(n), kvstr(n._dot()))
            for n in self._outgoing.keys()]

        def _edge(a, b):
            ref = self._edge_value[(a, b)]
            _a = "%d" % (id(a))
            _b = "%d" % (id(b))
            l = kvstr(ref._edge_dot())
            return E(_a, _b, l)

        edges = (_edge(a, b)
                 for a, to in self._outgoing.items()
                 for b in to)

        return gen(nodes=nodes, edges=edges)


from ..model import *
from ..exporter import Exporter

from simplegeneric import generic


@generic
def todot(obj):
    return {'label': str(obj), 'color': 'red'}


@todot.when_type(Exporter)
def todot_exporter(exporter):
    return {'label': str(exporter), 'color': 'yellow'}


@todot.when_type(MSMLVariable)
def todot(obj):
    return {'label': str(obj), 'color': 'green'}


#@todot.when_type(MSMLVariable)
def todot_task(task):
    return {'label': str(task), 'color': 'blue'}
