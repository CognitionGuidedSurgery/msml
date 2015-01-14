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

__author__ = 'Alexander Weigl <uiduw@student.kit.edu>'

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

__all__ = ["GraphDotWriter"]


def kvstr(dic, noquote=False):
    a = '%s=%s' if noquote else '%s="%s"'
    return ', '.join(itertools.starmap(
        lambda k, v:  a % (k, str(v).replace('"', "'")),
        dic.items()))

N = namedtuple("NodeTP", "name spec")
E = namedtuple("EdgeTP", "a b spec")

from msml.model.dag import DiGraph


class GraphDotWriter(object):
    """Export the given `dag` into the graphviz format.

    :param dag: directed acyclic graph
    :type dag: msml.model.DiGraph


    """
    def __init__(self, dag):
        self.dag = dag

    def __call__(self):
        """returns the graph in dot format

        :rtype: str
        """
        dag = self.dag
        assert isinstance(dag, DiGraph)

        nodes = [N(id(n), todot(n))
                 for n in dag.nodes_iter()]

        def _edge(e):
            a,b, data = e
            ref = data['ref']
            _a = "%d:outlink" % (id(a))
            link_to = ref.linked_to.name
            _b = "%d:%s:n" % (id(b),link_to)
           
            l = kvstr(todot(ref))
            return E(_a, _b, l)

        edges = map(_edge, dag.edges_iter(data=True))
        return template.render(nodes=nodes, edges=edges)


from ..model import *
from ..exporter import Exporter

from simplegeneric import generic


@generic
def todot(obj):
    return kvstr({'label': str(obj), 'color': 'red'})

@todot.when_type(Task)
def todot_task(task):
    print task.arguments    
    inputs = task.arguments.keys()    
     
     #all inputs in first row of table
    inputs_row = "".join(map(lambda inp: '<TD port="f1">' + inp + '</TD>',inputs))    
    #name of task in second raw
    task_name = '<TD align="center">'+task.id+':'+task.name+'</TD>'
    #outputs in third row
    task_out = '<TD align="center">out</TD>'
    
    table_str = """<<table border="1" cellborder="1" cellspacing="0" bgcolor="white">
                      <TR>%s</TR>
                      <TR>%s</TR>  
                      <TR>%s</TR>
                   </table>>                     
                """ % (inputs_row,task_name,task_out)
                     
    return kvstr({'label': table_str},True)
    
    
    #return {'label': "{{ %s }| %s:%s |{ <%s> %s }}" % (inputs_label,task.name,task.id,"outlink","out"), 'color': 'red', 'shape':'record'}
    #return {'label': "{%s|%s}" % (task.id, task.name), 'color': 'red', 'shape':'record'}


@todot.when_type(Exporter)
def todot_exporter(exporter):
    return kvstr({'label': '<outlink> ' + str(exporter), 'color': 'yellow', 'shape':'house'})


@todot.when_type(MSMLVariable)
def todot_var(obj):
    return kvstr({'label': "{%s|<outlink> %s}" % (obj.name,obj.value) , 'color': 'green', 'shape':'record'})

@todot.when_type(Reference)
def todot_ref(ref):
    return {'taillabel': str(ref.linked_to.arginfo.sort),
            'headlabel': str(ref.linked_from.arginfo.sort), 
            'fontsize':'8'}
