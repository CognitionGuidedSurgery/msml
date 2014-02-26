# -*- encoding: utf-8 -*-
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
Sorts logic. 

Factory and Cache for Sorts in MSML.

Currently there are two disjoint sorts hierarchies. 

1. format
2. type

`format` describes the kind of storage (e.g. file format)
`type` is the definition of the ground data type (e.g. vector of ints)

## example

vector.int + file.vtk

result in: file_vtk__vector_int as subtype of file and vector 
 

sortsdef => name of a sort, characterize by multiple path, seperated with »+«
path     => name/path in the class hierarchy, each class is seperated with ».«
"""

import inspect

#__all__ = ["__author__", "__date__", "SortsDefinition", "get_sort", "default_sorts_definition"]


__author__ = "Alexander Weigl"
__date__   = "2014-01-25, 2014-02-23"

def _strip(iter):
    return map(lambda x: x.strip(), iter)
    

def _split_path(path):
    if isinstance(path, str):
        return _strip(path.split('.'))
    else: 
        return path

def _split_sortsdef(sortsdef):
    return _strip(sortsdef.split('+'))

def _path_to_classname(path):
    if type(path) is str:
        path = _split_path(path)
    return '_'.join(path)

def _parse_sortsdef(string):
    if type(string) is str:
        a = _split_sortsdef(string)
    else:
        a = string
    return list(map(_split_path, a))

def _sortsdef_to_classname(sortsdef):
    if type(sortsdef) is str:
        sortsdef = _parse_sortsdef(sortsdef)    
    sortsdef.sort()    
    return '__'.join(map(_path_to_classname, sortsdef))


class BaseSort(object):
    """
    
    """    
    pass

class SortsDefinition(object):
    def __init__(self):
        self.type_cache = {}
        self.format_cache = {}
        self.sort_cache = {}

    def get_sort(self, tp, fmt = None):
        if type(tp) is str:
            tp = self._find_type(tp)

        if type(fmt) is str:
            fmt = self._find_format(fmt)

        try:
            return self.sort_cache[tp, fmt]
        except:
            import msml.model.sortdef
            s = msml.model.sortdef.Sort(tp, fmt)
            self.sort_cache[tp, fmt] = s
            return s

    def _find_type(self, typestr):
        try:
            return self.type_cache[typestr]
        except:
            print "todo"

    def _find_format(self, fmtstr):
        try: return self.format_cache[fmtstr]
        except: print "todo2"


    def register_format(self, clazz, name = None):
        if not name: name = clazz.__name__
        self.format_cache[name] = clazz
        return clazz

    def register_type(self, clazz, name = None):
        if not name: name = clazz.__name__
        self.type_cache[name] = clazz
        return clazz

    def register_type_with_name(self, name):
        def fn(clazz):
            return self.register_type(clazz,name)
        return fn

DEFAULT_SORTSDEFINITION = SortsDefinition()

def default_sorts_definition(): 
    "return default sorts definition"
    return DEFAULT_SORTSDEFINITION

def get_sort(t, f = None):
    """    
    returns the type object for the given sort definition
    """
    return default_sorts_definition().get_sort(t, f)


def issort(x):
    import msml.model.sortdef
    return isinstance(x, type) or isinstance(x, msml.model.sortdef.Sort)

######################################################################################
# conversion
#
#
#
#
import networkx

class ConversionNetwork(networkx.DiGraph):

    def register_conversion(self, a, b, fn, precedence):
        assert issort(a)
        assert issort(b)
        assert callable(fn)

        self.add_node(a)
        self.add_node(b)

        self.add_edge(a,b, fn = fn, precedence = precedence)

    def converter(self, a, b):
        def c(n1, n2):
            data = self.get_edge_data(a,b)
            return data['fn']

        import itertools
        path = list(networkx.dijkstra_path(self, a, b, 'precedence'))
        edges =  zip(path[:-1], path[1:])
        converters = itertools.starmap(c , edges)

        def fn(val):
            return reduce(lambda val, convert: convert(val),
                          converters, val)

        return fn






DEFAULT_CONVERSION_NETWORK = ConversionNetwork()

def default_conversion_network():
    return DEFAULT_CONVERSION_NETWORK


register_conversion  = DEFAULT_CONVERSION_NETWORK.register_conversion
conversion = DEFAULT_CONVERSION_NETWORK.converter

# if __name__ == "__main__":
#     todo remove tests
#     a = "vector.int + file.vtk"
#     print _parse_sortsdef(a)
#     print _sortsdef_to_classname( _parse_sortsdef(a) )
#     print get_sort(a)
#     print get_sort(_parse_sortsdef(a))
#
#     a = ["vector.float", "file.vtk"]
#     print _parse_sortsdef(a)
#     print _sortsdef_to_classname( _parse_sortsdef(a) )
#     print get_sort(a)
#     print get_sort(_parse_sortsdef(a))
#
#
