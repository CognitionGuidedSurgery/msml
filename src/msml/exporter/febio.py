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


__author__ = 'Stefan Suwelack, Alexander Weigl, Markus Stoll, Sarah Grimm'
__license__ = 'GPLv3'
__date__ = "2014-05-26"

import os

from path import path
import lxml.etree as etree

from ..model import *
from .base import XMLExporter, Exporter
from msml.exceptions import *
from msml.ext.misc import *


class MSMLSOFAExporterWarning(MSMLWarning): pass


class FeBioExporter(XMLExporter):
    def __init__(self, msml_file):
        """
          Args:
           executor (Executer)
        """
        self.name = 'FeBioExporter'
        self.id = 'FeBioExporter'
        Exporter.__init__(self, msml_file)
        self.export_file = None
        self.working_dir = path()

    def init_exec(self, executer):
        """initialization by the executor, sets memory and executor member

        :param executer: msml.run.Executer
        :return:
        """
        self._executer = executer
        self._memory = self._executer._memory

    def render(self):
        """Builds the File (XML e.g) for the external tool
        """
        print("Converting to febio feb")
        self.file_name = path(self._msml_file.filename).namebase
        self.export_file = self.file_name + ".feb"
        print self.export_file

        import codecs

        with codecs.open(self.export_file, 'w', 'iso-8859-1') as febfile:  #should be open with codecs.open
            rootelement = self.write_feb()
            rootelement.write(febfile, pretty_print=True, encoding='iso-8859-1', xml_declaration=True)

    def execute(self):
        import msml.envconfig
        cmd = msml.envconfig.FEBIO_EXECUTABLE + " -i " + self.export_file
        print(os.getcwd());
        print cmd
        print("Executing FeBio.")
        os.system(cmd)
        print("Converting FeBio to VTK.")
        self.convertToVTK(str(self.meshFile))
        xplt = self.file_name + ".xplt"
        cmd = "%s  %s" % (msml.envconfig.FEBIO_POSTVIEW_EXECUTABLE, xplt)
        os.system(cmd)

    def write_feb(self):
        self.node_root = self.createScene()
        print(self._msml_file.scene)
    
        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)

            meshFilename = self.get_value_from_memory(msmlObject.mesh)
            self.meshFile = meshFilename

            self.createControl(self.node_root, msmlObject)

            self.createMaterialRegions(self.node_root, msmlObject)

            self.createMeshTopology(meshFilename, msmlObject)

            self.createConstraintRegions(msmlObject, meshFilename)

            self.createOutput()

        return etree.ElementTree(self.node_root)

    def createMeshTopology(self, meshFilename, msmlObject):
        assert isinstance(msmlObject, SceneObject)
        
        theInpString = ConvertVTKMeshToFeBioMeshString(meshFilename, msmlObject.id, self.materialList)
        self.node_root.append(etree.fromstring(theInpString))

    def createMaterialRegions(self, objectNode, msmlObject):
        assert isinstance(msmlObject, SceneObject)
        maxLength = 0
        materialNode = self.sub("Material", self.node_root)
        for k in range(len(msmlObject.material)):
            assert isinstance(msmlObject.material[k], MaterialRegion)
            indices_key = msmlObject.material[k].indices
            matregionId = msmlObject.material[k].id

            indices_vec = self.get_value_from_memory(msmlObject.material[k])
            max_vec = max(indices_vec)
            if max_vec >= maxLength:
                maxLength = max_vec
            
            #Get all materials
            for i in range(len(msmlObject.material[k])):
                assert isinstance(msmlObject.material[k][i], ObjectElement)

                currentMaterialType = msmlObject.material[k][i].tag

                if currentMaterialType == "linearElasticMaterial":
                    currentYoungs = msmlObject.material[k][i].attributes["youngModulus"]
                    currentPoissons = msmlObject.material[k][i].attributes["poissonRatio"]
                elif currentMaterialType == "mass":
                    currentDensity = msmlObject.material[k][i].attributes["massDensity"]
                else:
                    warn(MSMLSOFAExporterWarning, "Material Type not supported %s" % currentMaterialType)

            materialRegionNode = self.sub("material", materialNode, id=k + 1, name=matregionId,
                                          type="neo-Hookean")
            self.sub("density", materialRegionNode).text = str(currentDensity)
            self.sub("E", materialRegionNode).text = str(currentYoungs)
            self.sub("v", materialRegionNode).text = str(currentPoissons)
        
        self.createMaterialLookupTable(maxLength, msmlObject)
        
    
    def createMaterialLookupTable(self, maxLength, msmlObject):
        self.materialList = [0] * (maxLength + 1)
        for k in range(len(msmlObject.material)):
            material_vec = self.get_value_from_memory(msmlObject.material[k])
            for material in material_vec:
                self.materialList[material]= k+1
        
    def createConstraintRegions(self, msmlObject, meshFilename):
        assert isinstance(msmlObject, SceneObject)
        boundaryNode = self.sub("Boundary", self.node_root)
        count = 0;
        for constraint_set in (msmlObject.constraints[0], ):  #TODO take all constraints
            assert isinstance(constraint_set, ObjectConstraints)
            for constraint in constraint_set.constraints:
                assert isinstance(constraint, ObjectElement)
                currentConstraintType = constraint.tag
                indices_vec = self.get_value_from_memory(constraint, 'indices')
                if currentConstraintType == "fixedConstraint":
                    fixedConstraintNode = self.sub("fix", boundaryNode)
                    bc = "xyz"
                    for index in map(str, indices_vec):
                        self.sub("node", fixedConstraintNode, id=int(index) + 1, bc=bc)
                elif currentConstraintType == "surfacePressure":
                    loadNode = self.sub("Loads", self.node_root)
                    count += 1
                    pressureArg = self.get_value_from_memory(constraint, 'pressure');
                    pressure = - float(pressureArg[0])
                    pressureString = createFeBioPressureOutput(meshFilename, indices_vec, str(count),
                                                                     str(pressure))
                    loadNode.append(etree.fromstring(pressureString))
                    iterations = float(self._msml_file.env.simulation[0].iterations)
                    dt = float(self._msml_file.env.simulation[0].dt)
                    time = dt * iterations
                    loadPointValue1 = "0.00, 0.00"
                    loadPointValue2 = str(time) + ", 1.00"
                    loadDataNode = self.sub("LoadData", self.node_root)
                    loadcurve = self.sub("loadcurve", loadDataNode, id=str(count), type="smooth")
                    loadPoint1 = self.sub("loadpoint", loadcurve)
                    loadPoint1.text = loadPointValue1
                    loadPoint2 = self.sub("loadpoint", loadcurve)
                    loadPoint2.text = loadPointValue2

                else:
                    warn(MSMLSOFAExporterWarning, "Constraint Type not supported %s " % currentConstraintType)


    def createControl(self, currentSofaNode, scobj):
        assert isinstance(scobj, SceneObject)
        type = "solid"
        moduleNode = self.sub("Module", self.node_root, type=type)
        controlNode = self.sub("Control", self.node_root)
        iterations = self._msml_file.env.simulation[0].iterations
        time_steps = self.sub("time_steps", controlNode)
        time_steps.text = str(iterations)
        dt = self._msml_file.env.simulation[0].dt
        step_size = self.sub("step_size", controlNode)
        step_size.text = str(dt)
        # msml doesn't support attributes below
        #=======================================================================
        # max_refs = self.sub("max_refs", controlNode)
        # max_refs.text = "15"
        # max_ups = self.sub("max_ups", controlNode)
        # max_ups.text = "10"
        # dtol = self.sub("dtol", controlNode)
        # dtol.text = "0.001"
        # etol = self.sub("etol", controlNode)
        # etol.text = "0.01"
        # rtol = self.sub("rtol", controlNode)
        # rtol.text = "0"
        # lstol = self.sub("lstol", controlNode)
        # lstol.text = "0.9"
        # time_stepper = self.sub("time_stepper", controlNode)
        # dtmin = self.sub("dtmin", time_stepper)
        # dtmin.text = "0.01"
        # dtmax = self.sub("dtmax", time_stepper)
        # dtmax.text = "0.1"
        # max_retries = self.sub("max_retries", time_stepper)
        # max_retries.text = "5"
        # opt_iter = self.sub("opt_iter", time_stepper)
        # opt_iter.text = "10"
        #=======================================================================
        analysisType = "static"
        analysis = self.sub("analysis", controlNode, type=analysisType)

    def convertToVTK(self, meshFilename):
        iterations = str(self._msml_file.env.simulation[0].iterations)
        dt = self._msml_file.env.simulation[0].dt
        logfile = str(self.file_name + ".txt");
        print(meshFilename)
        for x in range(1, int(self._msml_file.env.simulation[0].iterations)+ 1):
            print("Converting Step (FEBio -> VTK): " + str(x))
            ConvertFEBToVTK(logfile, str(x), meshFilename)

    def createScene(self):
        version = "1.2"
        root = etree.Element("febio_spec", version=version)
        return root

    def createOutput(self):
        type = "febio"
        type2 = "displacement"
        type3 = "stress"
        outputNode = self.sub("Output", self.node_root)
        plotfileNode = self.sub("plotfile", outputNode, type=type)
        self.sub("var", plotfileNode, type=type2)
        self.sub("var", plotfileNode, type=type3)
        logfileName = self.file_name + ".txt"
        logfileNode = self.sub("logfile", outputNode)
        data = "x;y;z"
        self.sub("node_data", logfileNode, data=data, file=logfileName)


    def sub(self, tag, root=None, **kwargs):
        skwargs = {k: str(v) for k, v in kwargs.items()}
        if root is None: root = self.node_root
        return etree.SubElement(root, tag, **skwargs)