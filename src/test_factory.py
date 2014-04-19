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

__author__ = 'weigl'

from msml.factory import *

input_vol_mesh = ""
surface_mesh = ""

msml_file = MSMLFile()

with define_workflow_of(msml_file) as operator:
    bunnyVolumeMesher = operator.mesherTetgen(
        meshFilename=input_vol_mesh,
        surfaceMesh=surface_mesh,
        preserveBoundary=0
    )

    bodyToIndexGroup = operator.boxROIToIndexOperator(
        box="-0.1 -0.03  -0.07 0.06 0.19 0.06",
        mesh=bunnyVolumeMesher,
        select="elements")

    bottomToIndexGroup = operator.boxROIToIndexOperator(
        mesh=bunnyVolumeMesher,
        box="-0.1 0.03 -0.07 0.07 0.035 0.06",
        select="points")

with define_scene_of(msml_file) as scene:
    bunny = scene.object("bunny").mesh(bunnyVolumeMesher, 'linearType')  # get type from output slot

    bunny.sets_nodes(
        bottomToIndexGroup
    )

    bunny.sets_elements(
        bottomToIndexGroup
    )

    bunny.sets_surfaces(
        bottomToIndexGroup
    )

    bunny.material_region("bunnyMaterial",
                          elements.linearElastic(youngModulus=80000, poissonRatio=0.49),
                          elements.mass(density=1000)
    )

    bunny.constraints("test", "${initial}",
                      elements.fixedConstraint(indices=bottomToIndexGroup))

    bunny.output(
        elements.displacement(id="liver", timestep=1)
    )

if __name__ == "__main__":
    import msml.model.writer, sys, lxml.etree

    tree = msml.model.writer.to_xml(msml_file)
    root = lxml.etree.ElementTree(tree)
    root.write(sys.stdout, pretty_print=True)