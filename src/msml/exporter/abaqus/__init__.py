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

__authors__ = 'Stefan Suwelack, Alexander Weigl'
__license__ = 'GPLv3'

import lxml.etree as etree
from jinja2 import Template


from path import path
from ..base import XMLExporter, Exporter
from msml.exceptions import *
import msml.env

import rdflib
from msml.exporter.semantic_tools import OntologyParser
from rdflib import URIRef
from rdflib.namespace import RDF


from msml.model import *

from ...log import error, warn, info, fatal, critical, debug

class MSMLAbaqusExporterWarning(MSMLWarning): pass


class AbaqusExporter(XMLExporter):
    def __init__(self, msml_file):
        """
        """
        self.name = 'AbaqusExporter'
        Exporter.__init__(self, msml_file)

    def init_exec(self, executer):
        """initialization by the executer, sets memory and executor member
         :param executer: msml.run.Executer
         :return:
        """
        self._executer = executer
        self._memory = self._executer._memory

    def render(self):
        """Builds the File (XML e.g) for the external tool
        """
        filename = self._msml_file.filename

        fileTree = etree.parse(filename)
        msmlRootNode = fileTree.getroot()

        error("Converting to abaqus input deck.")
        theAbaqusFilename = filename[0:-3] + 'inp'
        print theAbaqusFilename

        with open(theAbaqusFilename, "w") as inpfile:
            self.write_inp(inpfile)


    def execute(self):
        "should execute the external tool and set the memory"

        info("Executing abaqus.")

        pass

    def write_inp(self, inpfile):
        assert isinstance(inpfile, file)
        info(" and rdf lib testing")

        modulepath = path(__file__).dirname()


        parser = OntologyParser(modulepath / 'MSMLOnto.rdf-xml.owl')
        parser.parse_ontology_from_python_memory(
            URIRef('http://www.msml.org/ontology/msmlRepresentation#pythonModelRep'), self._msml_file)

        #g=rdflib.Graph()
        #g.load('/home/suwelack/git/MSMLExtended/msml/share/ontology/MSMLOnto.rdf-xml.owl')

        #for s,p,o in g:
         # print s,p,o


        # for msmlObject in self._msml_file.scene:
        #     assert isinstance(msmlObject, SceneObject)
        #
        #     meshObj = msmlObject.mesh
        #     meshValue = meshObj.mesh
        #     meshFilename = self.evaluate_node(meshValue)
        #
        #     # TODO this should be obselete with automical converters
        #     #
        #     import msml.ext.misc
        #
        #     theInpString = msml.ext.misc.convertVTKMeshToAbaqusMeshString(meshFilename, msmlObject.id, 'Neo-Hooke')
        #
        #     inpfile.write(theInpString)
        #
        #     #writing boundary conditions
        #     inpfile.write("""**
# **
# ** ASSEMBLY
# **
# *Assembly, name={id}-Assembly
# **
# *Instance, name={id}-Instance, part={id}-Part
# *End Instance
# **
# """.format(id=msmlObject.id))
#
#             globalIndices = []
#             globalConstraintType = []
#             globalDisplacements = []
#
#             for constraint_step in msmlObject.constraints:
#                 assert isinstance(constraint_step, ObjectConstraints)
#
#                 for constraint in constraint_step._constraints:
#                     assert  isinstance(constraint, ObjectElement)
#                     indices_key = constraint.attributes['indices']
#                     indices_vec = self.evaluate_node(indices_key)
#                     indices = '%s' % ', '.join(map(str, indices_vec))
#                     indices = indices.split(",")
#                     currentConstraintType = constraint.attributes['__tag__']
#
#                     if currentConstraintType == "fixedConstraint":
#                         iter = 0
#                         for index in indices:
#                             globalIndices.append(index);
#                             globalConstraintType.append(0)
#                             globalDisplacements.extend([0, 0, 0])
#                             iter += 1
#                     elif currentConstraintType == "displacementConstraint":
#                         displacements = constraint.get("displacements")
#                         displacements = displacements.split(" ")
#                         #print displacements
#                         #print indices
#                         #print len(indices)
#                         iter = 0
#                         #print len(indices)
#                         #print indices
#                         for index in indices:
#                             print iter
#                             globalIndices.append(index);
#                             globalConstraintType.append(1)
#                             globalDisplacements.append(float(displacements[3 * iter + 0]))
#                             globalDisplacements.append(float(displacements[3 * iter + 1]))
#                             globalDisplacements.append(float(displacements[3 * iter + 2]))
#                             iter += 1
#                     else:
#                         print(currentConstraintType)
#                         print("Constraint Type not supported!!!!!!!!!!!")
#
#         #print the sets for the bcs
#         currentLine = [theInpString]
#         #print len(indices)
#         #print indices
#         for i, index in enumerate(globalIndices):
#             inpfile.write(
#                 "*Nset, nset=_StaticPickedSet{i}, internal, instance={id}-Instance\n ,{index}\n"\
#                 .format(id=msmlObject.id, index=int(index) + 1, i=i))
#
#         inpfile.write("""*End Assembly
# **
# ** MATERIALS
# **
# *Material, name=Neo-Hooke
# *Damping, beta=0.21
# *Density
# 1070.,
# *Hyperelastic, neo hooke
# 365., 0.000838
# **
# ** BOUNDARY CONDITIONS
# **
# """)

#         for iter, index in enumerate(globalIndices):
#             if globalConstraintType[iter] == 0:
#                 inpfile.write(
#                     "** Name: Fixed Type: Symmetry/Antisymmetry/Encastre\n*Boundary\n_StaticPickedSet{i}, PINNED \n".
#                     format(i=iter)
#                 )
#
#         inpfile.write("""** ----------------------------------------------------------------
# **
# ** STEP: CustomLoad**
# *Step, name=CustomLoad, nlgeom=YES, inc=5000
# DiaLoad
# *Dynamic,alpha=-0.05,haftol=0.1
# 0.01,3.,3e-05,3.
# **
# ** BOUNDARY CONDITIONS
# **
# """)
#
#         for iter, index in enumerate(globalIndices):
#             if globalConstraintType[iter] == 1:
#                 inpfile.write(
#                     """** Name: Disp Type: Displacement/Rotation
#                     *Boundary
#                     _StaticPickedSet{i}, 1, 1, {disp1}
#                     _StaticPickedSet{i}, 2, 2, {disp2}
#                     _StaticPickedSet{i}, 3, 3, {disp3}
#                     """.format(
#                         i=iter,
#                         disp1=globalDisplacements[3 * iter + 0],
#                         disp2=globalDisplacements[3 * iter + 1],
#                         disp3=globalDisplacements[3 * iter + 2]
#                     ))
