__author__ = 'suwelack'

from base_mapping import *

class Mapper(object):
    def __init__(self, mapping):
        self._mapping = mapping
        assert isinstance(self._mapping, BaseMapping)

    def map(self, source, target):

        self.map_recursively(source, source, target)


    def map_recursively(self,current_node, source, target):

        current_node = current_node[0]
        self._mapping.map_element_pre( element=current_node,  source=source, target=target)

        self._mapping.map_element_post( element=current_node,  source=source, target=target)
