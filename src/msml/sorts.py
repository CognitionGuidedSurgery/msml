# -*- encoding: utf-8 -*-
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


__all__ = ["__author__", "__date__", "SortsDefinition", "get_sort", "default_sorts_definition"]


__author__ = "Alexander Weigl"
__date__   = "2014-01-25"

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
    def __init__(self, start_classes=None, start_sorts=None):        
        self.sorts_cache = {}
        self.class_cache = {}
        
        if type(start_classes) is dict:
            self.class_cache.update(start_classes)
        elif type(start_classes) in (tuple, list):
            for sc in start_classes:
                name = sc.__name__
                self.class_cache[name] = sc

        if start_sorts:
            for ss in start_sorts:
                self.get_sort(ss)

    def get_sort(self, sortsdef):
        """
        
        """        

        sortsdef = _parse_sortsdef(sortsdef)
            
        sname = _sortsdef_to_classname(sortsdef)
        
        if self.is_defined(sname):
            return self.sorts_cache[sname]
        
        classes = map(self._resolve_class, sortsdef)        

        if len(classes) == 1:
            sort = classes[0]
        else:
            sort = self._factory(classes, sname);
        self.sorts_cache[sname] = sort
        return sort

    def is_defined(self, sortname):
        try:
            return self.sorts_cache[sortname]
        except:
            return None

    def _factory(self, supertype, name):
        if not supertype:
            u = (BaseSort,)
        elif type(supertype) not in (list, tuple):
            u = (supertype, BaseSort) 
        else:
            u = list(supertype) + [BaseSort]

        t = type(name, tuple(u), {})
        return t

    def _resolve_class(self, path):
        if type(path) is str:
            path = _split_path(path)
    
        classname = _path_to_classname(path)
        try:
            return self.class_cache[classname]
        except:
            supertype = None
            if len(path) > 1:
                supertype = self._resolve_class(path[:-1])
    
            clazz = self._factory(supertype, classname)
            self.class_cache[classname] = clazz
            self.class_cache[path[-1]] = clazz

            assert clazz is not None
            return clazz

#default sort hierarchy (hidden by __all__)
DEFAULT_CLASSES = {'*' : object, 'str': str, 'int': int, 'float': float, 'file': file }
DEFAULT_SORTSDEFINITION = SortsDefinition(DEFAULT_CLASSES)

def default_sorts_definition(): 
    "return default sorts definition"
    return DEFAULT_SORTSDEFINITION

def get_sort(sortsdef):
    """    
    returns the type object for the given sort definition
    """
    return default_sorts_definition().get_sort(sortsdef)


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
