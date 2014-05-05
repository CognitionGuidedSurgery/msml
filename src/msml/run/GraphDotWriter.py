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

from jinja2 import Template


TMPL = """
digraph G {
  splines=ortho
  node [shape=box]

  {% for n in nodes %}
   {{ n.name }} [ {{ n.spec }} ] ;
  {% endfor%}

  {%for e in edges%}
    {{ e.a }} -> {{ e.b }} [{{ e.spec }}] ;
  {%endfor%}
}
"""

template = Template(TMPL)

import itertools
from collections import namedtuple


def kvstr(dic, noquote=False):
    a = '%s=%s' if noquote else '%s="%s"'
    return ', '.join(itertools.starmap(
        lambda k, v:  a % (k, str(v).replace('"', "'")),
        dic.items()))

N = namedtuple("NodeTP", "name spec")
E = namedtuple("EdgeTP", "a b spec")

from msml.model.dag import DiGraph


class GraphDotWriter(object):
    def __init__(self, dag):
        self.dag = dag

    def __call__(self):
        dag = self.dag
        assert isinstance(dag, DiGraph)

        nodes = [N(id(n), kvstr(todot(n)))
                 for n in dag.nodes_iter()]

        def _edge(e):
            a,b, data = e
            ref = data['ref']
            _a = "%d" % (id(a))
            _b = "%d" % (id(b))
            l = kvstr(todot(ref))
            return E(_a, _b, l)

        edges = map(_edge, dag.edges_iter(data=True))
        return template.render(nodes=nodes, edges=edges)


from ..model import *
from ..exporter import Exporter

from simplegeneric import generic


@generic
def todot(obj):
    return {'label': str(obj), 'color': 'red'}

@todot.when_type(Task)
def todot_task(task):
    return {'label': "{%s|%s}" % (task.id, task.name), 'color': 'red', 'shape':'record'}


@todot.when_type(Exporter)
def todot_exporter(exporter):
    return {'label': str(exporter), 'color': 'yellow', 'shape':'house'}


@todot.when_type(MSMLVariable)
def todot_var(obj):
    return {'label': obj.value or obj.name, 'color': 'green', 'shape':'parallelogram'}

@todot.when_type(Reference)
def todot_ref(ref):
    return {'taillabel': str(ref.linked_to.arginfo.sort),
            'headlabel': str(ref.linked_from.arginfo.sort), 'fontsize':'8'}
