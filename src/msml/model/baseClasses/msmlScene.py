__author__ = 'suwelack'


class Node(object):

    def __init__(self):
        self.__hasChild = list()

    @property
    def hasChild(self):
        return self.__hasChild

    @hasChild.setter
    def hasChild(self,value):
        self.__hasChild = value

