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
You only need this if you want create your own exporter.

An exporter is like an operator but with great power!
It is a cut-off in the execution of an msml file and can
read/manipulate the whole and processed memory content.


"""

__author__ = 'Alexander Weigl'
__version__ = "0.1"
__date__ = "2013-12-13"
__updated__ = "2014-02-26"

from .base import *
from .abaqusnew import AbaqusExporter as NAbaqusExporter
from .febio import FeBioExporter
from .sofanew import SofaExporter as NSofaExporter
from .hiflow3 import HiFlow3Exporter

# Register for common Exporters

__REGISTER = {'base': Exporter,
              "nabaqus": NAbaqusExporter, 'nsofa': NSofaExporter,
              "abaqus": NAbaqusExporter, 'sofa': NSofaExporter,
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


def get_exporter(name):
    """Find an Exporter under the given ``name``

    Args:
      name (str): common name of the Exporter, @see ``register_exporter``

    Returns:
      type: a factory function"""
    return __REGISTER[name]

    #from .abaqus_exporter import AbaqusExporter
    #from .base_exporter import BaseExporter
    #from .generic_exporter import GenericExporter
    #from .sofa_exporter import SOFAExporter