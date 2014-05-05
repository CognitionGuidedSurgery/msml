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

__authors__ = 'Nicolai Schoch, Alexander Weigl <uiduw@student.kit.edu>'
__license__ = 'GPLv3'

import lxml.etree as etree
import os
from .base import XMLExporter, Exporter
from msml.exceptions import *
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

    def render(self):
        """
     Builds the File (XML e.g) for the external tool
     """

        filename = self._msml_file.filename

        fileTree = etree.parse(filename)
        self.msmlRootNode = fileTree.getroot()

        print("Converting to HiFlow3 input formats (hiflow3Scene.xml-file & vtkMesh.vtu-file & BCdata.xml-file).")
        self.theHiFlow3SceneFilename = filename[0:-3] + 'hf3.xml'
        self.theHiFlow3VtuMeshFilename = filename[0:-3] + 'mesh.vtu'
        self.theHiFlow3BCxmlFilename = filename[0:-3] + 'bc.xml'
        print self.theHiFlow3SceneFilename, self.theHiFlow3VtuMeshFilename, self.theHiFlow3BCxmlFilename
        
        with open(self.theHiFlow3SceneFilename, "w") as hf3xmlfile:
            self.write_HiFlow3Scene(hf3xmlfile)

        with open(self.theHiFlow3VtuMeshFilename, "w") as vtufile:
            self.write_MeshVTU(vtufile)

        with open(self.theHiFlow3BCxmlFilename, "w") as bcxmlfile:
            self.write_BCdataXML(bcxmlfile)


    def execute(self):
        "should execute the external tool and set the memory"
        print("Executing HiFlow3.")
        os.system("runHiFlow3 %s" % self.hf3xmlfile)

    # define function to create basic HiFlow3-Scene-File:
    def write_HiFlow3Scene(self, hf3xmlfile):
        import jinja2
        tpl_path = path(__file__).dirname() / "hiflow_scene.tpl.xml"
        tpl = jinja2.Template(open(tpl_path).read())

        assert isinstance(hf3xmlfile, file)
        
        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)
            
            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue)

            DeltaT = material.get("dt") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            DeltaT = self._msml_file.env.simulation[0].dt # get/read-function with xml-Tree?!
            MaxTimeStepIts = material.get("iterations") # hard-coded in "abaqus.py", how to include from "*.msml.xml"?!
            MaxTimeStepIts = self._msml_file.env.simulation[0].iterations # get/read-function with xml-Tree?!


            hf3xmlfile.write(tpl.render(
                # TODO template arguments
            ))

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
