__author__ = 'suwelack'

from msml.exceptions import *
import uuid

class ObjectAlreadyInInventoryError(MSMLError):
    pass

class Node(object):

    def __init__(self):
        self._children = list()
        self._parent = None
        self._root = None


    def get_children(self):
        return self._children

    def add_child(self,child):
        self._children.append(child)
        child.parent = self
        currentRoot = self._root
        if self._root is None:
            currentRoot = self

        child._root = currentRoot
        try:
            id = child.id
            currentRoot.add_to_inventory( child, id)
        except AttributeError:
            currentRoot.add_to_inventory( child)


    @property
    def parent(self):
       return self._parent

    @parent.setter
    def parent(self, value):
       self._parent = value




class ScenarioRoot(Node):

    def __init__(self):
        self._inventory = dict()
        Node.__init__(self)
        self._root = self

    def add_to_inventory(self, object, id=None):
        if id is not Node:
            if id not in self._inventory:
                self._inventory[id] = object
            else:
                raise ObjectAlreadyInInventoryError('id already exists in scenario inventory')
        else:
            #in this case generate random id
            id = uuid.uuid4()
            self._inventory[id] = object

    def get_object_by_type(self, objectType):
        returnList = list()
        for key in self._inventory:
            if type(self._inventory[key]) == objectType:
                returnList.append(self._inventory[key])
        return returnList

    def get_object_by_id(self, id):
        if id in self._inventory:
            return self._inventory[id]
        else:
            return None


