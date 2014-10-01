# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
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
API for easily creating workflows and msml models.
"""
from path import path
from msml.model.base import (MSMLEnvironment, ObjectConstraints, MSMLVariable, SceneObject, Mesh, SceneObjectSets,
                             MaterialRegion, MSMLFile)

from .base import generate_name, ACTIVE_APP


__author__ = 'Alexander Weigl'
__date__ = "2014-04-19"
__version__ = "0.1"


class MeshTypes(object):
    LinearTetraheder = "linearTet"
    QuadraticTetraeder = "qt"
    LinearQuader = "lq"


Solver = MSMLEnvironment.Solver
Steps = MSMLEnvironment.Simulation
Step = MSMLEnvironment.Simulation.Step

def Material(*regions):
    assert all(map(lambda x: isinstance(x, MaterialRegion), regions))
    return regions

def Region(indices, id= None, *materials):
    return MaterialRegion(id or generate_name(), indices, materials)

def Constraints(for_step = 0, *constraints):
    o = ObjectConstraints(generate_name, for_step)
    o.constraints = constraints
    return o


def run(msml_file, filename, output_folder = None):
    assert isinstance(msml_file, MSMLFile)
    msml_file.filename = path(filename)
    return ACTIVE_APP.execute_msml(msml_file)


class SimulationBuilder(object):
    def __init__(self):
        self.msml_file = MSMLFile()

    def Variable(self, name=None, physical=None, logical=None, value=None):
        var = MSMLVariable(name or generate_name(), physical, logical, value)
        self.msml_file.add_variable(var)
        return "${%s}" % var.name

    @property
    def workflow(self):
        return self.msml_file.workflow

    @workflow.setter
    def workflow(self, value):
        self.msml_file._workflow = value

    def SceneObject(self, name = None, mesh = None, sets = None, material = None, constraints = None, output = None):
        obj =  SceneObject(name or generate_name(), mesh, sets,  material, constraints,output)
        self.msml_file.scene.append(obj)
        return obj

    def Environment(self, solver = None, *steps):
        env =  MSMLEnvironment(solver, Steps(*steps))
        self.msml_file._env = env
        return env