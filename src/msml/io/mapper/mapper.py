__author__ = 'suwelack'

from msml.io.mapper.base_mapping import *
import inspect
import types
from msml.exporter.base import *
from msml.model.base import *

class Mapper(object):
    def __init__(self, mapping):
        self._mapping = mapping
        assert isinstance(self._mapping, BaseMapping)

    def map(self, source, target):

        self.map_recursively(source, source, target, source, target)


    def map_recursively(self,current_node, parent_source,parent_target ,source, target):


        #do not map root scene node, also do not map lists
        if type(current_node) != types.ListType:
            parent_target = self._mapping.map_element_pre( element=current_node, parent_source=parent_source,parent_target=parent_target, source=source, target=target)

        #if current_node is list, then iterate over list
        if isinstance(current_node, list):
            for sub_node in current_node:
                self.map_recursively(sub_node,parent_source,parent_target, source, target)
        elif not (isinstance(current_node, ObjectElement) or isinstance(current_node, Mesh) or isinstance(current_node, ContactGeometry) or isinstance(current_node, SceneObjectSets)):
            attributes = current_node.__dict__
            for key in attributes:
                #if inspect.isdatadescriptor(sub_node):

                sub_node = attributes[key]
                if not (type(sub_node) is type(None) or type(sub_node) is types.StringType):
                    self.map_recursively(sub_node,current_node,parent_target, source, target)
        #else iterate over all attributes



        if type(current_node) != types.ListType:
            parent_target = self._mapping.map_element_post( element=current_node, parent_source=parent_source,parent_target=parent_target, source=source, target=target)


class MSMLMapper(Mapper):

    def map_recursively(self,current_node, parent_source,parent_target ,source, target):

        #do not map root scene node, also do not map lists
        if type(current_node) != types.ListType:
            new_parent_target, successorClass = self._mapping.map_element_pre( element=current_node, parent_source=parent_source,parent_target=parent_target, source=source, target=target)
            if successorClass:
                successorType = successorClass.__name__
            else:
                successorType = None

        #if current_node is list, then iterate over list
        if isinstance(current_node, list):
            for sub_node in current_node:
                self.map_recursively(sub_node,parent_source,new_parent_target, source, target)
        else:
            unmapped_children = current_node.get_children()

            while unmapped_children:
                sub_node = None
                if successorType is not None:
                    sub_node = next(obj for obj in unmapped_children if type(obj).__name__ == successorType)
                else:
                    sub_node = next(iter(unmapped_children))

                successorType = self.map_recursively(sub_node,current_node,new_parent_target, source, target)
                unmapped_children.remove(sub_node)


        if type(current_node) != types.ListType:
            parent_target, successorClass  = self._mapping.map_element_post( element=current_node, parent_source=parent_source,parent_target=parent_target, source=source, target=target)
            if successorClass:
                successorType = successorClass.__name__

        return successorType

