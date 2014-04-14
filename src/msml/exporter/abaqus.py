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

# MODULE is DEPRECATED /Alexander Weigl
# consider abaqusnew.py
#      d)                                                   t)                d)
#      d)                                                 t)tTTT              d)
#  d)DDDD e)EEEEE p)PPPP   r)RRR  e)EEEEE  c)CCCC a)AAAA    t)   e)EEEEE  d)DDDD
# d)   DD e)EEEE  p)   PP r)   RR e)EEEE  c)       a)AAA    t)   e)EEEE  d)   DD
# d)   DD e)      p)   PP r)      e)      c)      a)   A    t)   e)      d)   DD
#  d)DDDD  e)EEEE p)PPPP  r)       e)EEEE  c)CCCC  a)AAAA   t)T   e)EEEE  d)DDDD
#                 p)
#                 p)



__authors__ = 'Stefan Suwelack'
__license__ = 'GPLv3'

from warnings import warn

import lxml.etree as etree
import os

#from ..ext import tetgen

from ..model import alphabet
from ..model import base
from ..model.alphabet import PythonOperator
from ..model.base import Task
from .base import XMLExporter, Exporter
from msml.model.exceptions import *
import msml.env


class MSMLAbaqusExporterWarning(MSMLWarning): pass


class AbaqusExporter(XMLExporter):
    def __init__(self, msml_file):
        """
      Args:
       executer (Executer)


      """
        self.name = 'AbaqusExporter'
        Exporter.__init__(self, msml_file)

    def init_exec(self, executer):
        """
     initialization by the executer, sets memory and executor member
     :param executer: msml.run.Executer
     :return:
     """
        self._executer = executer
        self._memory = self._executer._memory

    def render(self):
        """
     Builds the File (XML e.g) for the external tool
     """
        #scene = self.msml_file.scene

        #print os.getcwd()

        filename = self._msml_file.filename

        fileTree = etree.parse(filename)
        msmlRootNode = fileTree.getroot()

        print("Converting to abaqus input deck.")
        theAbaqusFilename = filename[0:-3] + 'inp'
        print theAbaqusFilename

        self.write_inp(msmlRootNode, theAbaqusFilename)


    def execute(self):
        "should execute the external tool and set the memory"

        print("Executing abaqus.")

        pass

    def write_inp(self, msmlRootNode, filename):
        sceneNode = msmlRootNode.find("scene")
        for msmlObject in sceneNode.iterchildren():
            if (msmlObject.tag == "object"):
                #create mesh
                #           physicsElementNode = msmlObject.find("physicsElements")
                currentMeshNode = msmlObject.find("mesh")[0]

                meshValue = currentMeshNode.attrib["mesh"]
                #if meshValue.star

                meshFilename = self.evaluate_node(meshValue)

                #theFilename = self.startDataNodeEvaluation( currentMeshNode)

                thealphabet = msml.env.current_alphabet
                abaqusConverter = thealphabet.get("vtk-mesh-to-abaqus-mesh-str")
                #testMesh = abaqusConverter.input["inputMesh"]
                #abaqusConverter.input["inputMesh"].value = meshFilename

                #create task
                attrib = {'inputMesh': meshFilename, 'mesh': 'result', 'partName': msmlObject.get("id"),
                          'materialName': 'Neo-Hooke', 'id': 'tempConverter'}
                name = 'vtk-mesh-to-abaqus-mesh-str'
                theTask = Task(name, attrib)
                theTask.bind(thealphabet)
                theOperator = theTask.operator
                #theOperator.bind_function()
                #result = theOperator()
                kwargs = {'inputMesh': meshFilename, 'mesh': 'result', 'partName': msmlObject.get("id"),
                          'materialName': 'Neo-Hooke'}
                theInpDict = theOperator(**kwargs)
                theInpString = theInpDict['mesh']

                #print result

                #print meshFilename
                #create node for operator processing
                #targetNode = etree.Element("convertVTKMeshToAbaqusMeshString", name="converter", partName=msmlObject.get("name"), materialName="Neo-Hooke")
                #inputValue = theFilename
                #targetNodeAlphabet = self.findNodeTypeInAlphabet(targetNode.tag)
                # theInpString = MiscMeshOperatorsPython.convertVTKMeshToAbaqusMeshString(meshFilename, msmlObject.get("name"), "Neo-Hooke")

                #       task = PythonOperator('converter', )
                #              Operator.__init__(self, name, input, output, parameters, runtime, meta)
                #   self.function_name = runtime['function']
                #   self.modul_name = runtime['module']
                #   self.function = None
                #       print theInpString


                #writing boundary conditions
                currentLine = [theInpString, "**\n", "** \n", "** ASSEMBLY \n", "**\n", "*Assembly, name=",
                               msmlObject.get("id"), "-Assembly\n"]
                currentLine += ["**\n", "*Instance, name=", msmlObject.get("id"), "-Instance, part=",
                                msmlObject.get("id"), "-Part\n"]
                currentLine += ["*End Instance\n", "**\n"]
                theInpString = ''.join(currentLine)

                globalIndices = []
                globalConstraintType = []
                globalDisplacements = []

                constraintRegionNode = msmlObject.find("constraints")

                for constraint in constraintRegionNode.iterchildren():
                    indices_key = constraint.get("indices")
                    indices_vec = self.evaluate_node(indices_key)
                    indices = '%s' % ', '.join(map(str, indices_vec))
                    indices = indices.split(",")
                    currentConstraintType = constraint.tag

                    if (currentConstraintType == "fixedConstraint"):
                        iter = 0
                        #print len(indices)
                        #print indices
                        for index in indices:
                            globalIndices.append(index);
                            globalConstraintType.append(0)
                            globalDisplacements.extend([0, 0, 0])
                            iter += 1
                    elif (currentConstraintType == "displacementConstraint"):
                        displacements = constraint.get("displacements")
                        displacements = displacements.split(" ")
                        #print displacements
                        #print indices
                        #print len(indices)
                        iter = 0
                        #print len(indices)
                        #print indices
                        for index in indices:
                            print iter
                            globalIndices.append(index);
                            globalConstraintType.append(1)
                            globalDisplacements.append(float(displacements[3 * iter + 0]))
                            globalDisplacements.append(float(displacements[3 * iter + 1]))
                            globalDisplacements.append(float(displacements[3 * iter + 2]))
                            iter += 1
                    else:
                        print(currentConstraintType)
                        print("Constraint Type not supported!!!!!!!!!!!")

            #print the sets for the bcs
            currentLine = [theInpString]
            #print len(indices)
            #print indices
            iter = 0
            for index in globalIndices:
                currentLine += ["*Nset, nset=_StaticPickedSet", str(iter), ", internal, instance=",
                                msmlObject.get("id"), "-Instance\n ,", str(int(index) + 1), "\n"]
                iter += 1

            theInpString = ''.join(currentLine)

            currentLine = [theInpString]
            currentLine += ["*End Assembly\n"]

            currentLine += ["**\n", "** MATERIALS\n", "**\n"]
            currentLine += ["*Material, name=Neo-Hooke\n"]
            currentLine += ["*Damping, beta=0.21\n"]
            currentLine += ["*Density\n1070.,\n"]
            currentLine += ["*Hyperelastic, neo hooke\n", "365., 0.000838\n"];

            currentLine += ["**\n", "** BOUNDARY CONDITIONS\n", "**\n"];

            iter = 0
            for index in globalIndices:
                if (globalConstraintType[iter] == 0):
                    currentLine += ["** Name: Fixed Type: Symmetry/Antisymmetry/Encastre\n", "*Boundary\n"];
                    currentLine += ["_StaticPickedSet", str(iter), ", PINNED \n"];
                iter += 1

            currentLine += ["** ----------------------------------------------------------------\n"];
            currentLine += ["**\n", "** STEP: CustomLoad", "**\n",
                            "*Step, name=CustomLoad, nlgeom=YES, inc=5000\n"];
            currentLine += ["DiaLoad\n", "*Dynamic,alpha=-0.05,haftol=0.1\n", "0.01,3.,3e-05,3.\n"];

            currentLine += ["**\n", "** BOUNDARY CONDITIONS\n", "**\n"];

            iter = 0
            for index in globalIndices:
                if (globalConstraintType[iter] == 1):
                    currentLine += ["** Name: Disp Type: Displacement/Rotation\n", "*Boundary\n"];
                    currentLine += ["_StaticPickedSet", str(iter), ", 1 , 1, ",
                                    str(globalDisplacements[3 * iter + 0]), "\n"];
                    currentLine += ["_StaticPickedSet", str(iter), ", 2 , 2, ",
                                    str(globalDisplacements[3 * iter + 1]), "\n"];
                    currentLine += ["_StaticPickedSet", str(iter), ", 3 , 3, ",
                                    str(globalDisplacements[3 * iter + 2]), "\n"];
                iter += 1

            theInpString = ''.join(currentLine)


            #print theInpString

            f = open(filename, 'w')
            f.write(theInpString)
