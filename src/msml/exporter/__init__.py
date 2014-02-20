#TODO LICSENCE

#TODO DOCS
"""
TODO
"""

__author__ = 'weigl'
__version__ = "0.1"
__date__ = "2013-12-13"

from .base import *
from .sofa import SofaExporter
from .abaqus import AbaqusExporter


__REGISTER = {'base': Exporter, 'sofa': SofaExporter, 'abaqus': AbaqusExporter}


def register_exporter(name, clazz):
    __REGISTER[name] = clazz


def get_exporter(name):
    return __REGISTER[name]





    #from .abaqus_exporter import AbaqusExporter
    #from .base_exporter import BaseExporter
    #from .generic_exporter import GenericExporter
    #from .sofa_exporter import SOFAExporter