# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
# Medicine Meets Virtual Reality (MMVR) 2014
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

__author__ = 'Alexander Weigl'

from stub import *

# #############################################


simulation = SimulationBuilder()


input_vol_mesh = simulation.Variable(value="bunnyVolumeMesh.vtk",
                          logical="Mesh",
                          physical="str")

input_surf_mesh = simulation.Variable(value="Bunny6000Surface.vtk", logical="Mesh",
                           physical="file.vtk")

wf = WorkflowBuilder()
bunnyVolumeMesher = wf.mesherTetgen(
    meshFilename=input_vol_mesh,
    surfaceMesh=input_surf_mesh,
    preserveBoundary=False)

bodyToIndexGroup = wf.boxROIToIndexOperator(
    box=(-0.1, -0.03, -0.07, 0.06, 0.19, 0.06),
    mesh=bunnyVolumeMesher.mesh,
    select="elements")

bottomToIndexGroup = wf.boxROIToIndexOperator(
    box=(-0.1, 0.03, -0.07, 0.07, 0.035, 0.06),
    mesh=bunnyVolumeMesher.mesh,
    select="points")

simulation.workflow = wf.workflow

## Scene
#
bunny = simulation.SceneObject(
    mesh=Mesh(type=MeshTypes.LinearTetraheder, value=bunnyVolumeMesher.mesh),
    material=Material(
        Region(bodyToIndexGroup.indices, None,
               linearElasticMaterial(0.49, 80000),
               mass(1000))
    ),
    constraints=[
        Constraints(0, fixedConstraint(bottomToIndexGroup.indices))
    ],
    output=[
        displacement(1)
    ]
)

env = simulation.Environment(None, Step(0.05, 100))

run(simulation.msml_file, filename = __file__)

# ############################################





