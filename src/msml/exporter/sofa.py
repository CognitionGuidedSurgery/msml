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


__authors__ = 'Stefan Suwelack, Markus Stoll'
__license__ = 'GPLv3'

from warnings import warn
import os
import math
import string

import lxml.etree as etree

#from ..ext import tetgen

from ..model import alphabet
from ..model import base
from ..model.alphabet import PythonOperator
from ..model.base import Task
from .base import XMLExporter, Exporter
from msml.model.exceptions import *
from path import path


class MSMLSOFAExporterWarning(MSMLWarning): pass


class SofaExporter(XMLExporter):
    def __init__(self, msml_file):
        """
      Args:
       executer (Executer)


      """
        self.name = 'SOFAExporter'
        Exporter.__init__(self, msml_file)
        self.export_file = None
        self.working_dir = path()

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

        print("Converting to sofa scn")
        self.export_file = filename[0:-3] + 'scn'
        print self.export_file

        self.working_dir = path(filename).dirname()
        self.write_scn(msmlRootNode, self.export_file)


    def execute(self):
        "should execute the external tool and set the memory"
        print("Executing sofa.")
        os.system("runSofa %s" % self.export_file)


    def write_scn(self, msmlRootNode, filename):
        sofa_scene_node = self.createScene(msmlRootNode)

        sceneNode = msmlRootNode.find("scene")
        for msmlObject in sceneNode.iterchildren():
            if (msmlObject.tag == "object"):
                #create object, the mesh, material regions and constraints
                objectNode = self.createObject(sofa_scene_node, msmlObject, msmlRootNode)
                #physicsElementNode = msmlObject.find("material")
                self.createMeshTopology(objectNode, msmlObject, msmlRootNode)
                materialNode = msmlObject.find("material")
                self.createMaterialRegions(objectNode, materialNode, msmlRootNode)

                #create simulation steps
                constraintsNode = msmlObject.find("constraints")
                self.createConstraintRegions(objectNode, constraintsNode, msmlRootNode)

                #creat post processing request
                self.createPostProcessingRequests(objectNode, msmlObject.find("output"), msmlRootNode)

        #add solver
        solverNode = msmlRootNode.find("environment").find("solver")
        self.createSolvers(objectNode, solverNode, msmlRootNode)

        self.InsertAllTemplateAttributs(sofa_scene_node, solverNode);

        tree = etree.ElementTree(sofa_scene_node)
        tree.write(filename, pretty_print=True)

    def createMeshTopology(self, currentSofaNode, currentMsmlNode, msmlRootNode):

        currentMeshNode = currentMsmlNode.find("mesh")[0]
        currentMeshType = currentMeshNode.tag

        #print (currentMeshType)
        if currentMeshType == "linearTet":
            loaderNode = etree.SubElement(currentSofaNode, "MeshVTKLoader")
            #loaderNode = etree.SubElement(currentSofaNode, "MeshExtendedVTKLoader")
            loaderNode.set("name",
                           "LOADER")  # currentMeshNode.get("name" )) - having a constant name for our the loader simplifies using it as source for nodes generated later.
            #find the filename
            meshValue = currentMeshNode.attrib["mesh"]
            theFilename = self.evaluate_node(meshValue)
            theFilename = self.working_dir / theFilename
            print theFilename

            loaderNode.set("filename", theFilename)
            loaderNode.set("createSubelements",
                           "0")  #does not work as expected. If a single triangle exists in mesh, then for each facet of all tets a triangle is ceated... SOFA bug?
            etree.SubElement(currentSofaNode, "MechanicalObject", name="dofs", template="undef", src="@LOADER")
            etree.SubElement(currentSofaNode, "MeshTopology", name="topo", src="@LOADER")
            #check if child is present

            #if so, check operator compatibility

            #execute operator

            #check if mesh is in MSML folder

            #if not -> copy
        elif currentMeshType == "quadraticTet":
            loaderNode = etree.SubElement(currentSofaNode, "MeshExtendedVTKLoader")
            loaderNode.set("name",
                           "LOADER")  # currentMeshNode.get("name" )) - having a constant name for our the loader simplifies using it as source for nodes generated later.
            #find the filename
            meshValue = currentMeshNode.attrib["mesh"]
            theFilename = self.evaluate_node(meshValue)
            theFilename = self.working_dir / theFilename
            print theFilename

            loaderNode.set("filename", theFilename)
            etree.SubElement(currentSofaNode, "MechanicalObject", name="dofs", template="undef", src="@LOADER")
            etree.SubElement(currentSofaNode, "QuadraticMeshTopology", name="topo", src="@LOADER")

        else:
            print("Mesh type must be mesh.volume.linearTetrahedron.vtk or mesh.volume.quadraticTetrahedron.vtk")


    def createSolvers(self, currentSofaNode, currentMsmlNode, msmlRootNode):
        ODESolverType = currentMsmlNode.get("timeIntegration")

        if (ODESolverType == None):
            print "Error, no ODE solver type specified"
            return
        LinearSolverType = currentMsmlNode.get("linearSolver")
        if (LinearSolverType == None):
            print "Error, no linear solver type specified"
            return

        if (ODESolverType == "dynamicImplicit"):
            etree.SubElement(currentSofaNode, "MyNewmarkImplicitSolver", rayleighStiffness="0.2", rayleighMass="0.02",
                             name="odesolver")
        elif (ODESolverType == "dynamicImplicitEuler"):
            etree.SubElement(currentSofaNode, "EulerImplicitSolver", name="odesolver")
        else:
            print "Error ODE solver ", ODESolverType, " not supported"

        if (LinearSolverType == "direct"):
            etree.SubElement(currentSofaNode, "SparseMKLSolver")
        elif (LinearSolverType == "iterativeCG"):
            etree.SubElement(currentSofaNode, "CGLinearSolver", iterations="100", tolerance="1e-06", threshold="1e-06")
        else:
            print "Error linear solver ", LinearSolverType, " not supported"


    def InsertAllTemplateAttributs(self, sofaRootNode, msmlSolverNode):
        processingUnit = msmlSolverNode.get("processingUnit");
        if (processingUnit == "CPU"):
            value = "Vec3f"
        elif (processingUnit == "GPU"):
            value = "CudaVec3f"
        else:
            print "Invalid processingUnit in solver."
            return;

        for element in sofaRootNode.iter():
            if (element.get("template")):
                if (element.get("template").find("undef") != -1):
                    element.set("template", element.get("template").replace("undef", value));


    def createMaterialRegions(self, currentSofaNode, currentMsmlNode, msmlRootNode):
        youngs = {}
        poissons = {}
        density = {}
        for currentMaterialRegionNode in currentMsmlNode.findall("region"):
            indexGroupNode = currentMaterialRegionNode.find("indexgroup")
            #print "index group", indexGroupNode.get("indices")
            #print indexGroupNode.get("indices")

            indices_key = indexGroupNode.get("indices")
            indices_vec = self.evaluate_node(indices_key)
            indices = '%s' % ', '.join(map(str, indices_vec))

            indices_int = [int(i) for i in indices.split(",")]

            #Get all materials
            for material in currentMaterialRegionNode.iterchildren():
                currentMaterialType = material.tag
                if (currentMaterialType != "indexgroup"):
                    if currentMaterialType == "linearElastic":
                        currentYoungs = material.get("youngModulus")
                        currentPoissons = material.get("poissonRatio")  # not implemented in sofa yet!
                        for i in indices_int:
                            youngs[i] = currentYoungs
                            poissons[i] = currentPoissons
                    elif currentMaterialType == "mass":
                        currentDensity = material.get("density")
                        for i in indices_int:
                            density[i] = currentDensity
                    else:
                        print(currentMaterialType)
                        print("Material Type not supported!!!!!!!!!!!")

        keylist = density.keys()
        keylist.sort();
        density_str = " ".join(str(v) for v in density.values()) 
        youngs_str = " ".join(str(v) for v in youngs.values()) 
        poissons_str = " ".join(str(v) for v in poissons.values()) 

        #merge all different materials to single forcefield/density entries.
        if currentSofaNode.find("MeshTopology") is not None:
            elasticNode = etree.SubElement(currentSofaNode, "TetrahedronFEMForceField", template="undef", name="FEM",
                                           listening="true")
            elasticNode.set("youngModulus", youngs_str)
            elasticNode.set("poissonRatio", poissons[keylist[0]])
            etree.SubElement(currentSofaNode, "TetrahedronSetGeometryAlgorithms",
                             name="aTetrahedronSetGeometryAlgorithm",
                             template="undef");
            massNode = etree.SubElement(currentSofaNode, "DiagonalMass", name="meshMass")
            massNode.set("massDensity", density_str)
        elif (currentSofaNode.find("QuadraticMeshTopology") is not None):
            eelasticNode = etree.SubElement(currentSofaNode, "QuadraticTetrahedralCorotationalFEMForceField",
                                            template="undef", name="FEM", listening="true")
            eelasticNode.set("setYoungModulus", youngs_str)
            eelasticNode.set("setPoissonRatio", poissons[keylist[0]])  # TODO
            emassNode = etree.SubElement(currentSofaNode, "QuadraticMeshMatrixMass", name="meshMass")
            emassNode.set("massDensity", density_str)
        else:
            print "Current mesh topology not supported"


    def createConstraintRegions(self, currentSofaNode, currentMsmlNode, msmlRootNode):
        for a in currentMsmlNode.iterchildren():
            for constraint in a.iterchildren():
                currentConstraintType = constraint.tag

                indices_key = constraint.get("indices")
                indices_vec = self.evaluate_node(indices_key)
                indices = '%s' % ', '.join(map(str, indices_vec))

                if (currentConstraintType == "fixedConstraint"):
                    constraintNode = etree.SubElement(currentSofaNode, "FixedConstraint")
                    constraintNode.set("name", str(constraint.get("name")))
                    constraintNode.set("indices", indices)

                    #elasticNode.set("setPoissonRatio", material.get("poissonRatio"))

                    #check if child is present

                    #if so, check operator compatibility

                    #execute operator

                    #check if mesh is in MSML folder

                    #if not -> copy
                elif (currentConstraintType == "surfacePressure"):
                    constraintNode = etree.SubElement(currentSofaNode, "Node", name="SurfaceLoad")
                    etree.SubElement(constraintNode, "MeshTopology", name="SurfaceTopo",
                                     position="@LOADER.position",
                                     triangles="@LOADER.triangles", quads="@LOADER.quads")
                    etree.SubElement(constraintNode, "MechanicalObject", template="Vec3f", name="surfacePressDOF",
                                     position="@SurfaceTopo.position")
                    surfacePressureForceFieldNode = etree.SubElement(constraintNode, "SurfacePressureForceField",
                                                                     template="Vec3f", name="surfacePressure",
                                                                     pulseMode="1")
                    surfacePressureForceFieldNode.set("pressureSpeed",
                                                      str(float(constraint.get("pressure")) / 10.0))
                    surfacePressureForceFieldNode.set("pressure", constraint.get("pressure"));
                    surfacePressureForceFieldNode.set("triangleIndices", indices)
                    etree.SubElement(constraintNode, "BarycentricMapping", template="undef, Vec3f",
                                     name="barycentricMapSurfacePressure", input="@..", output="@.")

                elif (currentConstraintType == "springMeshToFixed"):
                    constraintNode = etree.SubElement(currentSofaNode, "Node", name="springMeshToFixed")
                    mechObj = etree.SubElement(constraintNode, "MechanicalObject", template="Vec3f",
                                               name="pointsInDeformingMesh")
                    mechObj.set("position", constraint.get("movingPoints"));
                    etree.SubElement(constraintNode, "BarycentricMapping", template="undef, Vec3f",
                                     name="barycentricMapSpringMeshToFixed", input="@..", output="@.")
                    displacedLandLMarks = etree.SubElement(constraintNode, "Node",
                                                           name="fixedPointsForSpringMeshToFixed")
                    mechObj = etree.SubElement(displacedLandLMarks, "MechanicalObject", template="Vec3f",
                                               name="fixedPoints")
                    mechObj.set("position", constraint.get("fixedPoints"));
                    forcefield = etree.SubElement(constraintNode, "RestShapeSpringsForceField", template="Vec3f",
                                                  name="Springs",
                                                  external_rest_shape="fixedPointsForSpringMeshToFixed/fixedPoints",
                                                  drawSpring="true")
                    forcefield.set("stiffness", constraint.get("stiffness"));
                    forcefield.set("rayleighStiffnes", constraint.get("rayleighStiffnes"));

                elif (currentConstraintType == "supportingMesh"):
                    constraintNode = etree.SubElement(currentSofaNode, "Node", name="support")
                    constraintNode.set("name", "support_" + constraint.get("name"))
                    loaderNode = etree.SubElement(constraintNode, "MeshVTKLoader", name="LOADER_supportmesh",
                                                  createSubelements="0")
                    loaderNode.set("filename", constraint.get(
                        "filename"))  #workaround, because node evaluation is only possible for data/operator nodes.
                    etree.SubElement(constraintNode, "MechanicalObject", name="dofs", src="@LOADER_supportmesh",
                                     template="Vec3f", translation="0 0 0")
                    etree.SubElement(constraintNode, "MeshTopology", name="topo", src="@LOADER_supportmesh")
                    forcefield = etree.SubElement(constraintNode, "TetrahedronFEMForceField", listening="true",
                                                  name="FEM", template="Vec3f")
                    forcefield.set("youngModulus", constraint.get("youngModulus"))
                    forcefield.set("poissonRatio", constraint.get("poissonRatio"))
                    etree.SubElement(constraintNode, "TetrahedronSetGeometryAlgorithms",
                                     name="aTetrahedronSetGeometryAlgorithm", template="Vec3f")
                    diagonalMass = etree.SubElement(constraintNode, "DiagonalMass", name="meshMass")
                    diagonalMass.set("massDensity", constraint.get("massDensity"))
                    etree.SubElement(constraintNode, "BarycentricMapping", input="@..", name="barycentricMap",
                                     output="@.", template="undef, Vec3f")

                else:
                    print(currentConstraintType)
                    print("Constraint Type not supported!!!!!!!!!!!")


    def createObject(self, currentSofaNode, currentMsmlNode, msmlRootNode):
        objectNode = etree.SubElement(currentSofaNode, "Node")
        objectNode.set("name", currentMsmlNode.get("id"))

        return objectNode


    def createScene(self, msmlRootNode):
        stepNode = msmlRootNode.find(".//step")
        delta = stepNode.get("dt")  #only one step supported
        root = etree.Element("Node", name="root", dt=delta)
        theGravity = stepNode.get("gravity")
        if theGravity is None:
            theGravity = '0 -9.81 0'
        root.set("gravity", theGravity)
        return root

        #sofa_exporter handles displacementOutputRequest only. Other postProcessing operators need to be adressed in... ?


    def createPostProcessingRequests(self, currentSofaNode, currentMsmlNode, rootMSMLNode):
        for request in currentMsmlNode.iterchildren():
            if (request.tag == "displacement"):
                if (currentSofaNode.find("MeshTopology") is not None):
                    #dispOutputNode = etree.SubElement(currentSofaNode, "ExtendedVTKExporter" )
                    dispOutputNode = etree.SubElement(currentSofaNode, "VTKExporter")
                    filename = self.working_dir / request.get("id")
                    dispOutputNode.set("filename", filename)
                    exportEveryNumberOfSteps = request.get("timestep")
                    dispOutputNode.set("exportEveryNumberOfSteps", exportEveryNumberOfSteps)
                    dispOutputNode.set("XMLformat",
                                       "1")  #using xml=0 still writes a .vtu file but in legacy text format.
                    dispOutputNode.set("edges", "0")
                    #dispOutputNode.set("tetras", "0") #exporting points only
                    #todo export material => allows extraction of surfaces in post processing
                    dispOutputNode.set("tetras", "1")
                    dispOutputNode.set("triangles", "0")
                    dispOutputNode.set("listening", "true")
                    dispOutputNode.set("exportAtEnd", "true")
                    stepNode = rootMSMLNode.find(".//step")
                    timeSteps = int(stepNode.get("iterations"))  #only one stimulation step supported
                    #exportEveryNumberOfSteps = 1 in SOFA means export every second time step.
                    #exportEveryNumberOfSteps = 0 in SOFA means do not export.
                    if (exportEveryNumberOfSteps == 0):
                        lastNumber = 1
                    else:
                        lastNumber = int(math.floor(timeSteps / ( int(exportEveryNumberOfSteps) + 1)))
                    filenameLastOutput = filename + str(lastNumber) + ".vtu"
                    request.set("filename", filenameLastOutput)
                    
                elif (currentSofaNode.find("QuadraticMeshTopology") is not None):
                    dispOutputNode = etree.SubElement(currentSofaNode, "ExtendedVTKExporter")
                    filename = self.working_dir / request.get("id")
                    dispOutputNode.set("filename", filename)
                    dispOutputNode.set("exportEveryNumberOfSteps", request.get("timestep"))
                    dispOutputNode.set("tetras", "0")
                    dispOutputNode.set("quadraticTetras", "1")
                    dispOutputNode.set("listening", "true")
                    dispOutputNode.set("exportAtEnd", "true")
                    #TODO: Fill "filename" of request taking output numbering into account (see VTKExporter)
                else:
                    print "Topolgy type not supported"
