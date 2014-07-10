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

""" Directed Acyclic Graph for control and information flow.
"""

import networkx as nx

__author__ = "Alexander Weigl"


class DiGraph(nx.MultiDiGraph):
    """ A networkx.MultiDiGraph but extends this by to methods:

     * ``self.toporder``
     * ``self.show``

    """
    def toporder(self):
        """ Returns the topological order of the graph.

        Returns:
          list[set]: a list of buckets (set of nodes),
                     that has only predecessor from the previous bucket

        Raises:
          ValueError: iff. the graph is not acyclic
        """

        graph = nx.MultiDiGraph(self)
        amountnodes = len(self.nodes())
        nodes = 0
        buckets = []


        def independent_nodes():
            nodes = graph.nodes()
            pred = map(graph.predecessors, nodes)
            return [n for n, p in zip(nodes, pred) if len(p) == 0]

        i = 0
        while nodes < amountnodes and i < amountnodes:
            inodes = set(independent_nodes())
            nodes += len(inodes)
            buckets.append(inodes)
            graph.remove_nodes_from(inodes)
            i += 1

        if nodes < amountnodes:
            raise ValueError('graph is not acyclic')

        return buckets


    # def show(self):
    #     """ shows the graph withing matplotlib
    #     """
    #
    #     import matplotlib.pyplot as plt
    #
    #     try:
    #         from networkx import graphviz_layout, write_dot
    #     except ImportError:
    #         raise ImportError("This example needs Graphviz and either PyGraphviz or Pydot")
    #
    #     G = self
    #     #write_dot(G, '/tmp/test.dot')
    #     pos = nx.graphviz_layout(G, prog='neato', args='')
    #     plt.figure(figsize=(8, 8))
    #     nx.draw(G, pos, node_size=100, alpha=0.5, node_color="blue", with_labels=True)
    #     plt.axis('equal')
    #     #plt.savefig('circular_tree.png')
    #     #plt.show()


# region oldcode

'''
class DiGraph(object):
    """ Directed acyclic graph implementation. """

    def __init__(self):
        """ Construct a new DAG with no nodes or edges. """
        self._incoming = {}
        self._outgoing = {}
        self._edge_value = {}


    def add_node(self, node_name):
        """ Add a node if it does not exist yet, or error out. """
        if node_name in self._incoming:
            raise KeyError('node %s already exists' % node_name)
        self._incoming[node_name] = set()
        self._outgoing[node_name] = set()


    def delete_node(self, node_name):
        """ Deletes this node and all edges referencing it. """
        if node_name not in self._incoming:
            raise KeyError('node %s does not exist' % node_name)

        for lis in (self._incoming.iteritems(), self._outgoing.iteritems()):
            for node , edges in lis:
                if node_name in edges:
                    edges.remove(node_name)

        self._incoming.pop(node_name)
        self._outgoing.pop(node_name)


    def add_edge(self, fro, to, key = None):
        """ Add an edge (dependency) between the specified nodes. """
        if to not in self._incoming or fro not in self._outgoing:
            raise KeyError('one or more nodes do not exist in graph')
        self._outgoing[fro].add(to)
        self._incoming[to].add(fro)
        self._edge_value[(fro, to)] = key

    def delete_edge(self, fro, to):
        """ Delete an edge from the graph. """
        self._outgoing[fro].discard(to)
        self._incoming[to].discard(fro)


    def downstream(self, node):
        """ Returns a list of all nodes this node has edges towards. """
        if node not in self._incoming:
            raise KeyError('node %s is not in graph' % node)
        return list(self._incoming[node])

    def upstream(self, node):
        if node not in self._outgoing:
            raise KeyError('node %s is not in graph' % node)
        return list(self._outgoing[node])


    def reset_graph(self):
        """ Restore the graph to an empty state. """
        self._incoming = {}
        self._outgoing = {}


    def validate(self):
        """ Returns (Boolean, message) of whether DAG is valid. """
        if len(self.ind_nodes()) == 0:
            return (False, 'no independent nodes detected')
        try:
            self._topological_sort()
        except ValueError:
            return (False, 'failed topological sort')
        return (True, 'valid')


    def _dependencies(self, target_node, graph = None):
        """ Returns a list of all nodes from incoming edges. """

        if graph is None:
            graph = self.graph

        result = set()
        for node, outgoing_nodes in graph.iteritems():
            if target_node in outgoing_nodes:
                result.add(node)
        return list(result)


    def independent_nodes(self):
        return (node for node, items in self._incoming.items() if len(items) == 0)

    def toporder(self):
        """ Returns a topological ordering of the DAG.

        Raises an error if this is not possible (graph is not valid).
        """


        graph = copy(self)
        amountnodes = len(self._incoming.keys())
        nodes = 0
        buckets = []

        i = 0
        while nodes < amountnodes  and i < amountnodes:
            inodes = set(graph.independent_nodes())
            nodes += len(inodes)
            buckets.append(inodes)

            for b in inodes:
                graph.delete_node(b)

            i += 1

        if nodes < amountnodes:
            raise ValueError('graph is not acyclic')
        return buckets


if __name__ == "__main__":

    G = DiGraph()

    a, b, c, d, e = list("ABCDE")


    G.add_node(a)
    G.add_node(b)
    G.add_node(c)
    G.add_node(d)
    G.add_node(e)


    G.add_edge(a, b)
    G.add_edge(a, c)
    G.add_edge(c, d)
    G.add_edge(b, e)
    G.add_edge(b, d)

    print(G.toporder())
'''

#endregion