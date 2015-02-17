__author__ = 'suwelack'

from collections import defaultdict
from msml.exceptions import *

class MappingNotCompleteWarning(MSMLWarning):
    pass


class MappingNotAvailableError(MSMLError):
    pass


class MappingMeta(type):
    """
    If you do not know about metaclasses see http://eli.thegreenplace.net/2011/08/14/python-metaclasses-by-example/
    first.

    This metaclass discovers all mapping methods in the class and gathers them.

    """

    def __new__(cls, name, bases, d):
        #       print cls, name, bases, d

        categories = defaultdict(dict)
        completeness = defaultdict(dict)

        for name, func in d.items():
            if callable(func) and hasattr(func, '_mapping'):
                if func._mapping:
                    categories[func._mapping_category][func._node_name] = func
                    completeness[func._mapping_category][func._node_name] = func._mapping_complete

                    #      print "Found:", categories

        d["_mapping"] = categories
        d["_mapping_completeness"] = completeness

        def get_func(self, category, name, *args, **kwargs):
            try:
                f = self._mapping[category][name]
                if not self._mapping_completeness[category][name]:
                    warn("Only partial mapping implemented for element %s" % name, MappingNotCompleteWarning)
            except KeyError as e:
                raise MappingNotAvailableError(e)


            return f(self, *args, **kwargs)

        d['_element_mapper'] = get_func
        return type.__new__(cls, name, bases, d)


def mapping_cat(category, is_complete):
    """
    Provides a function mapping marker for the given category.
    """

    def register_name(instance):
        """ Decorator for registering a function with a given name"""

        def register_fn(func):
            setattr(func, "_mapping", True)
            setattr(func, "_mapping_complete", is_complete)
            setattr(func, "_mapping_category", category)
            setattr(func, "_node_name", instance.__class__.__module__+'.'+instance.__class__.__name__)
            return func

        return register_fn

    return register_name


##
# Mapping Marker
complete_map_pre = mapping_cat('pre', True)
complete_map_post = mapping_cat('post', True)
partial_map_pre = mapping_cat('pre', False)
partial_map_post = mapping_cat('post', False)

#
##

class BaseMapping(object):
    __metaclass__ = MappingMeta

    def __init__(self):
        object.__init__(self)


    def map_element_pre(self,   *args, **kwargs):
        self._element_mapper('pre', kwargs['element'].__class__.__module__+'.'+kwargs['element'].__class__.__name__, *args, **kwargs)

    def map_element_post(self,  *args, **kwargs):
        self._element_mapper('post', kwargs['element'].__class__.__module__+'.'+kwargs['element'].__class__.__name__, *args, **kwargs)