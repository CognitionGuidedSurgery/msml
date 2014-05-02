
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

from msml.model.base import *

__authors__ = 'Nicolai Schoch'
__license__ = 'GPLv3'

import lxml.etree as etree

from ..model.base import Task
from .base import XMLExporter, Exporter
from msml.model.exceptions import *
import msml.env

from msml.model import *


class MSMLHiFlow3ExporterWarning(MSMLWarning): pass


class HiFlow3Exporter(XMLExporter):
    def __init__(self, msml_file):
        """
      Args:
       executer (Executer)


      """
        self.name = 'HiFlow3Exporter'
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

        filename = self._msml_file.filename

        fileTree = etree.parse(filename)
        msmlRootNode = fileTree.getroot()

        print("Converting to HiFlow3 input formats (hiflow3Scene.xml-file & vtkMesh.vtu-file & BCdata.xml-file).")
        theHiFlow3SceneFilename = filename[0:-3] + 'hf3.xml'
        theHiFlow3VtuMeshFilename = filename[0:-3] + 'mesh.vtu'
        theHiFlow3BCxmlFilename = filename[0:-3] + 'bc.xml'
        print theHiFlow3SceneFilename
        print theHiFlow3VtuMeshFilename
        print theHiFlow3BCxmlFilename
        
        with open(theHiFlow3SceneFilename, "w") as hf3xmlfile: # TODO: check this!
            #self.write_inp(inpfile)
            self.write_HiFlow3Scene(hf3xmlfile)

        with open(theHiFlow3VtuMeshFilename, "w") as vtufile: # TODO: check this!
            #self.write_inp(inpfile)
            self.write_MeshVTU(vtufile)

        with open(theHiFlow3BCxmlFilename, "w") as bcxmlfile: # TODO: check this!
            #self.write_inp(inpfile)
            self.write_BCdataXML(bcxmlfile)


    def execute(self):
        "should execute the external tool and set the memory"
        print("Executing HiFlow3.")
        os.system("runHiFlow3 %s" % self.hf3xmlfile) # TODO: should this be "export_file"?!


    # define function to create basic HiFlow3-Scene-File:
    def write_HiFlow3Scene(self hf3xmlfile):
        assert isinstance(vtufile, file)
        
        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)
            
            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue)
            
            #import xml.etree.ElementTree as ET # double?! see above?!
            #tree = ET.parse(filename)
            #root = tree.getroot()
            
            hf3xmlfile.write("""<Param>
  <OutputPathAndPrefix> SimResults/elasticitySimulation_ </OutputPathAndPrefix>
  <Mesh>
    <Filename>""")
            hf3xmlfile.write(theHiFlow3VtuMeshFilename)
            hf3xmlfile.write("""</Filename>
    <BCdataFilename>""")
            hf3xmlfile.write(theHiFlow3BCxmlFilename)
            hf3xmlfile.write("""</BCdataFilename>
    <InitialRefLevel>0</InitialRefLevel>
  </Mesh>
  
  <LinearAlgebra>
    <Platform>CPU</Platform>
    <Implementation>Naive</Implementation>
    <MatrixFormat>CSR</MatrixFormat>
  </LinearAlgebra>
  
  <ElasticityModel>
    <density>""")
            density = material.get("density") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            hf3xmlfile.write(density)
            hf3xmlfile.write("""</density>
    <lambda>""")
            LameLambda = material.get("LameConstLAMBDA") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            hf3xmlfile.write(LameLambda)
            hf3xmlfile.write("""</lambda>
    <mu>""")
            LameMu = material.get("LameConstMU") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            hf3xmlfile.write(LameMu)
            hf3xmlfile.write("""</mu>
    <gravity>""")
            gravity = material.get("gravity") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            hf3xmlfile.write(gravity)
            hf3xmlfile.write("""</gravity>
  </ElasticityModel>
  
  <QuadratureOrder>2</QuadratureOrder>
  
  <FiniteElements>
    <DisplacementDegree>1</DisplacementDegree>
  </FiniteElements>
  
  <Instationary>
    <SolveInstationary>""")
            bool solveInstationary = 1
            if solveInstationary == 1
                hf3xmlfile.write("""1""")
                
                DeltaT = material.get("dt") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
                DeltaT = = msmlRootNode.environment.simulation.step.parse(dt) # get/read-function with xml-Tree?!
                MaxTimeStepIts = material.get("iterations") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
                MaxTimeStepIts = msmlRootNode.environment.simulation.step.parse(iterations) # get/read-function with xml-Tree?!
                
                hf3xmlfile.write("""</SolveInstationary>
    <DampingFactor>1.0</DampingFactor>
    <RayleighAlpha>0.0</RayleighAlpha> <!-- MassFactor -->
    <RayleighBeta>0.2</RayleighBeta> <!-- StiffnessFactor -->
    <Method>Newmark</Method>
    <DeltaT>""")
                hf3xmlfile.write(DeltaT)
                hf3xmlfile.write("""</DeltaT>
    <MaxTimeStepIts>""")
                hf3xmlfile.write(MaxTimeStepIts)
                hf3xmlfile.write("""</MaxTimeStepIts>
  </Instationary>""")
            else
                hf3xmlfile.write("""0""")
                hf3xmlfile.write("""</SolveInstationary>
  </Instationary>""")
            
            hf3xmlfile.write("""  <LinearSolver>
    <SolverName>""")
            linSolver = solver.get("linearSolver") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            hf3xmlfile.write(linSolver)
            hf3xmlfile.write("""</SolverName>
    <MaximumIterations>1000</MaximumIterations>
    <AbsoluteTolerance>1.e-8</AbsoluteTolerance>
    <RelativeTolerance>1.e-20</RelativeTolerance>
    <DivergenceLimit>1.e6</DivergenceLimit>
    <BasisSize>1000</BasisSize>
    <Preconditioning>1</Preconditioning>
    <PreconditionerName>""")
            preconditioner = solver.get("preconditioner") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            hf3xmlfile.write(preconditioner)
            hf3xmlfile.write("""</PreconditionerName>
    <Omega>2.5</Omega>
    <ILU_p>2.5</ILU_p>
  </LinearSolver>
  <ILUPP>
    <PreprocessingType>0</PreprocessingType>
    <PreconditionerNumber>11</PreconditionerNumber>
    <MaxMultilevels>20</MaxMultilevels>
    <MemFactor>0.8</MemFactor>
    <PivotThreshold>2.75</PivotThreshold>
    <MinPivot>0.05</MinPivot>
  </ILUPP>

</Param>""")


    # define function to create HiFlow3-compatible vtu-mesh-File:
    def write_MeshVTU(self, vtufile):
        assert isinstance(vtufile, file)

        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)

            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue)

            import msml.ext.misc
            theVtuString = msml.ext.misc.convertVTKPolydataToUnstructuredGrid(meshFilename, msmlObject.id) # HIFLOW3
            # TODO?! other arguments else needed?!
            #theInpString = msml.ext.misc.convertVTKMeshToAbaqusMeshString(meshFilename, msmlObject.id, 'Neo-Hooke') # ABAQUS

            vtufile.write(theVtuString)


    # define function to create HiFlow3-compatible BCdata-input-File:
    def write_BCdataXML(self, bcxmlfile):
        assert isinstance(bcxmlfile, file)

        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)

            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue)
            
            #writing boundary conditions
            bcxmlfile.write("""<BCData>
  <FixedConstraintsBCs>
    <NumberOfFixedDirichletPoints>""")
            #TODO: Number of fDpoints
            bcxmlfile.write("""</NumberOfFixedDirichletPoints>
    <fDPoints>""")
            #TODO: list of DPoints getPointsInBoxROI() -> compare: abaqusnew.py, lines 129ff
            #TODO: how to transform MSML-ROIs/Boxes into (lists of) point coordinates?!
            #TODO: -> maybe use MSML.miscOperators: computeIndicesFromBoxROI -> vtkIDs.
            #TODO: -> maybe use MSML.miscOperators: extractPointPositions.
            bcxmlfile.write("""</fDPoints>
    <fDisplacements>""")
            #TODO: list of zeroDisplacementVectors
            bcxmlfile.write("""</fDisplacements>
  </FixedConstraintsBCs>""")
            
            bcxmlfile.write("""  <DisplacementConstraintsBCs>
    <NumberOfDisplacedDirichletPoints>""")
            #TODO: Number of dDpoints
            bcxmlfile.write("""</NumberOfDisplacedDirichletPoints>
    <dDPoints>""")
            #TODO: list of dDPoints getPointsInBoxROI() -> compare: abaqusnew.py, lines 129ff
            #TODO: how to transform MSML-ROIs/Boxes into (lists of) point coordinates?!
            bcxmlfile.write("""</dDPoints>
    <dDisplacements>""")
            #TODO: list of displacementVectors getVectorsInBoxROI() -> compare: abaqusnew.py, lines 129ff
            #TODO: how to transform MSML-ROIs/Boxes into (lists of) point coordinates?!
            bcxmlfile.write("""</dDisplacements>
  </DisplacementConstraintsBCs>""")
            
            bcxmlfile.write("""  <ForceOrPressureBCs>
    <NumberOfForceOrPressureBCPoints>""")
            #TODO: Number of ForceOrPressureBCPoints
            bcxmlfile.write("""</NumberOfForceOrPressureBCPoints>
    <ForceOrPressureBCPoints>""")
            #TODO: list of ForceOrPressureBCPoints getPointsInBoxROI() -> compare: abaqusnew.py, lines 129ff
            #TODO: how to transform MSML-ROIs/Boxes into (lists of) point coordinates?!
            bcxmlfile.write("""</ForceOrPressureBCPoints>
    <ForcesOrPressures>""")
            #TODO: list of ForceOrPressureVectors -> compare: abaqusnew.py, lines 129ff
            #TODO: how to transform MSML-ROIs/Boxes into (lists of) point coordinates?!
            bcxmlfile.write("""</ForcesOrPressures>
  </ForceOrPressureBCs>""")
            
            bcxmlfile.write("""</BCData>""")

