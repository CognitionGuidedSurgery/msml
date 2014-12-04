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


"""
msml.exporter -- base functionality for all exporters.

An exporter is like an operator but with great power!
It is a cut-off in the execution of an msml file and can
read/manipulate the whole and processed memory content.

For more information: :py:class:`msml.exporter.Exporter`

"""

__author__ = 'Alexander Weigl'
__version__ = "0.1"
__date__ = "2013-12-13"
__updated__ = "2014-02-26"

from .base import *
from .abaqus import AbaqusExporter
#from .sofanew import SofaExporter
from .sofanew import SofaExporter
from .hiflow3 import HiFlow3Exporter
from .semantic_tools import OntologyParser
from .febio import FeBioExporter

__all__ = ['register_exporter', 'get_exporter',
           'Exporter', 'NAbaqusExporter', 'NSofaExporter',
           'AbaqusExporter', 'SofaExporter',
           'HiFlow3Exporter']


# Register for common Exporters
__REGISTER = {'base': Exporter,
              "nabaqus": AbaqusExporter, 'nsofa': SofaExporter,
              "abaqus": AbaqusExporter, 'sofa': SofaExporter,
              'hiflow3': HiFlow3Exporter, 'febio' : FeBioExporter,
}


def register_exporter(name, clazz):
    """
    Register an exporter class under the given name.

    Args:
      name (str): name to select the Exporter from the command line interface
      clazz (type): the type object or a factory function for the Exporter
    """
    __REGISTER[name] = clazz

def get_known_exporters():
    return __REGISTER.keys()


def get_exporter(name):
    """Find an Exporter under the given ``name``

    Args:
      name (str): common name of the Exporter,

    Returns:
      type: a factory function

    See Also:

       :py:func:`msml.exporter.register_exporter`


    """
    return __REGISTER[name]
