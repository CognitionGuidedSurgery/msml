__author__ = 'weigl'

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
