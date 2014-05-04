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
MSML -- Meta model.

defines classes for:

* operators 
* environments
* scene elements
* msml-files    

"""

__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

from .exceptions import *

from .alphabet import Alphabet, Operator, PythonOperator, SharedObjectOperator, ShellOperator, \
    OperatorSlot, ObjectAttribute, OAMaterial, OAConstraint, OAIndexGroup, OAMesh

from .base import MSMLFile, MSMLVariable, struct, \
    MSMLFileVariable, Workflow, Task, ObjectElement, SceneObject, \
    ObjectConstraints, SceneSets, IndexGroup, Mesh, MaterialRegion, \
    Reference, parse_attribute_value, random_var_name, Constant, MSMLEnvironment



