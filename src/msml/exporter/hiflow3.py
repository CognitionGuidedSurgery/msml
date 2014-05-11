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
import msml.ext.misc

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

        filename = self._msml_file.filename  # syntax wrong?! "_"msml_file????

        fileTree = etree.parse(filename)
        self.msmlRootNode = fileTree.getroot()

        print("Converting to HiFlow3 input formats (hiflow3Scene.xml-file & vtkMesh.vtu-file & BCdata.xml-file).")
        self.theHiFlow3SceneFilename = filename[0:-8] + 'hf3.xml'
        self.theHiFlow3VtuMeshFilename = filename[0:-8] + 'mesh.vtu'
        self.theHiFlow3BCxmlFilename = filename[0:-8] + 'bc.xml'
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

            # get and compute elasticity constants (i.e. material parameters):
            # therefore, iterate over "material" and "material's region"
            # (compare to: NewSofaExporter.createMaterialRegion().)
            youngs = {}
            poissons = {}
            density = {}

            for matregion in msmlObject.material:
                assert isinstance(matregion, MaterialRegion)

                indexGroupNode = matregion.get_indices() # needed for two or more materialregions only?!

                assert isinstance(indexGroupNode, ObjectElement) # needed for two or more materialregions only?!

                indices_key = indexGroupNode.attributes["indices"] # needed for two or more materialregions only?!
                indices_vec = self.evaluate_node(indices_key) # needed for two or more materialregions only?!
                indices = '%s' % ', '.join(map(str, indices_vec)) # needed for two or more materialregions only?!

                indices_int = [int(i) for i in indices.split(",")] # needed for two or more materialregions only?!

                #Get all materials
                for material in matregion:
                    assert isinstance(material, ObjectElement)

                    currentMaterialType = material.attributes['__tag__'] # what?!
                    if currentMaterialType == "indexgroup": # what?!
                        continue

                    if currentMaterialType == "linearElastic":
                        currentYoungs = material.attributes["youngModulus"]
                        currentPoissons = material.attributes["poissonRatio"]
                        for i in indices_int:   # needed for two or more materialregions only?! #TODO Performance (maybe generator should be make more sense)
                            youngs[i] = currentYoungs # needed for two or more materialregions only?!
                            poissons[i] = currentPoissons # needed for two or more materialregions only?!
                    elif currentMaterialType == "mass":
                        currentDensity = material.attributes["density"]
                        for i in indices_int: # needed for two or more materialregions only?!
                            density[i] = currentDensity # needed for two or more materialregions only?!
                    else:
                        warn(MSMLSOFAExporterWarning, "Material Type not supported %s" % currentMaterialType)

                # now we have: youngs[], poissons[], density[].
                # since HiFlow3 is currently dealing with one material only, the for-loop is to be ended here.

            # the thus obtained linearElasticityConstants for the (imposed) one given material are:
            NU = poissons[0] # by definition: set NU = poissons[0], so HiFlow3 can handle without weak material boundaries.
            E = youngs[0] # by definition: set E = youngs[0], so HiFlow3 can handle without weak material boundaries.
            # and hence
            lamelambda = (E * NU) / ((1 + NU)*(1 - 2 * NU))
            lamemu = E / (2*(1 + NU))

            maxtimestep = self._msml_file.env.simulation[0].iterations # is this right????? # if so, is the *.msml.xml notation to be changed?!

            if maxtimestep > 1:
                SolveInstationary = 1
            else:
                SolveInstationary = 0

            hf3xmlfile.write(tpl.render(
                # template arguments
                meshfilename=self.theHiFlow3VtuMeshFilename,  #vtufile
                bcdatafilename=self.theHiFlow3BCxmlFilename,  #bcxmlfile
                density=density[0],
                lamelambda=lamelambda,
                lamemu=lamemu,
                gravity=-9.81,
                SolveInstationary=SolveInstationary,
                DeltaT=self._msml_file.env.simulation[0].dt,
                maxtimestep=maxtimestep,
                linsolver=self._msml_file.env.solver.linearSolver,
                precond=self._msml_file.env.solver.preconditioner
                # in future, there may be some more?! # alternatively parsing by means of using *.get("...") possible?!
            ))


    # define function to create HiFlow3-compatible vtu-mesh-File:
    def write_MeshVTU(self, vtufile):
        assert isinstance(vtufile, file)

        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject) # this serves for TypeSafty and AutoCompletion...?

            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue)

            # for HIFLOW3: convert plain vtk to vtu-xml
            theVtuString = convertVTKToVTU(meshFilename, msmlObject.id)
            # TODO: check if other arguments needed?!

            vtufile.write(theVtuString)


    # define function to create HiFlow3-compatible BCdata-input-File:
    def write_BCdataXML(self, bcxmlfile):

        import jinja2

        bcdata_tpl_path = path(__file__).dirname() / "hiflow_bcdata.tpl.xml"
        tpl = jinja2.Template(open(bcdata_tpl_path).read())

        assert isinstance(bcxmlfile, file)

        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)

            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue) # is this needed here?!

            #prepare input for BCdataXML-Template:
            for roiBoxes in msmlObject.workflow: # TODO: stimmt das so?
                assert isinstance(roiBoxes, boxROI)

                indicesVector = computeIndicesFromBoxROI(string meshFilename, vector<double> roiBoxes, string type) # hier müssen die type-definitions wieder raus...
                # in "IndexRegionOperators.cpp"
                # TODO: what is type "tetrahedron"?
                pointsInBoxROIVector = extractPointPositions( std::vector<int> indicesVector, const char* meshFilename)
                # in "MiscMeshOperators.cpp"
                numfDpoints = len(pointsInBoxROIVector)/3
                zeroDisplacementVectors = ''
                for it in range(1, numfDpoints):
                    zeroDisplacementVectors.append('0,0,0;')
                zeroDisplacementVectors = zeroDisplacementVectors[0:-1]

            #writing boundary conditions
            bcxmlfile.write(tpl.render(
                # template arguments
                #---
                #TODO: Number of fDpoints
                numfDpoints=numfDpoints,

                #TODO: list of DPoints
                pointsInBoxROIVector=pointsInBoxROIVector,
                #TODO: transform MSML-ROIs/Boxes into (lists of) point coordinates:
                #TODO: use "getPointsInBoxROI()" (-> compare: abaqusnew.py, lines 129ff) and "extractPointPositions()".

                #TODO: list of zeroDisplacementVectors
                zeroDisplacementVectors=zeroDisplacementVectors,

                #---
                #TODO: Number of dDpoints

                #TODO: list of dDPoints getPointsInBoxROI()

                #TODO: list of displacementVectors getVectorsInBoxROI()

                #---
                #TODO: Number of ForceOrPressureBCPoints

                #TODO: list of ForceOrPressureBCPoints getPointsInBoxROI()

                #TODO: list of ForceOrPressureVectors

                #---
            ))

