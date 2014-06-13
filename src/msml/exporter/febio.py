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
from docutils.nodes import Element
from xml.etree import ElementPath


__authors__ = 'Stefan Suwelack, Alexander Weigl, Markus Stoll, Sarah Grimm'
__license__ = 'GPLv3'
__date__ = "2014-05-26"

from warnings import warn
import os
import math

from ..model import *
from .base import XMLExporter, Exporter
from path import path
import subprocess

import lxml.etree as etree
from xml.etree.ElementTree import Element
from msml.model.exceptions import *


class MSMLSOFAExporterWarning(MSMLWarning): pass


class FeBioExporter(XMLExporter):
    def __init__(self, msml_file):
        """
      Args:
       executer (Executer)


      """
        self.name = 'FeBioExporter'
        self.id = 'FeBioExporter'
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
        print("Converting to febio feb")
        self.export_file = path(self._msml_file.filename).namebase + ".feb"
        print self.export_file

        #with open(self.export_file, "w") as febfile:
            #self.write_feb(febfile)
        import codecs

        with codecs.open(self.export_file, 'w', 'utf-8') as febfile:  #should be open with codecs.open
           rootelement = self.write_feb()
           rootelement.write(febfile, pretty_print=True, encoding='iso-8859-1', xml_declaration=True)
            #s = etree.tostring(rootelement, encoding="utf-8")
            #scnfile.write(s)

    def execute(self):
        "should execute the external tool and set the memory"
        print("Executing FeBio.")
        pass


    def write_feb(self):
       # assert isinstance(febfile, file)

        self.node_root = self.createScene()
        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)

            meshObj = msmlObject.mesh
            meshValue = meshObj.mesh
            meshFilename = self.evaluate_node(meshValue)

            self.createControl(self.node_root, msmlObject)
            # TODO this should be obselete with automical converters
            self.createMaterialRegions(self.node_root, msmlObject)
            import msml.ext.misc
            theInpString = msml.ext.misc.convertVTKMeshToFeBioMeshString(meshFilename, msmlObject.id, 'Neo-Hooke')
            #meshTree = etree.fromstring(theInpString);
            self.node_root.append(etree.fromstring(theInpString))
            
            self.createConstraintRegions(msmlObject)
            self.createOutput()
            #febfile.write(theInpString)
            
            #create object, the mesh, material regions and constraints
            #objectNode = self.createObject(self.node_root, msmlObject)

            #physicsElementNode = msmlObject.find("material")
            #self.createMeshTopology(objectNode, msmlObject)
            #self.createMaterialRegions(objectNode, msmlObject)

            #create simulation steps

            #creat post processing request
            #self.createPostProcessingRequests(objectNode, msmlObject)

            #add solver
        #self.createSolvers()

        return etree.ElementTree(self.node_root)

    def createMeshTopology(self, objectNode, msmlObject):
        assert isinstance(msmlObject, SceneObject)
        mesh_value = msmlObject.mesh.mesh
        mesh_type = msmlObject.mesh.type

        theFilename = self.working_dir / self.evaluate_node(mesh_value)

        # TODO currentMeshNode.get("name" )) - having a constant name for our the loader simplifies using it as source for nodes generated later.
        # TODO does not work as expected. If a single triangle exists in mesh, then for each facet of all tets a triangle is ceated... SOFA bug?

        #check if child is present
        #if so, check operator compatibility
        #execute operator
        #check if mesh is in MSML folder

        #if not -> copy

        if mesh_type == "linearTet":
            loaderNode = self.sub("MeshVTKLoader", objectNode,
                                  name="LOADER", filename=theFilename,
                                  createSubelements=0)
            #  createSubelements does not work as expected. If a single triangle exists in mesh, then for each facet of all tets a triangle is ceated... SOFA bug?
            self.sub("MechanicalObject", objectNode,
                     name="dofs", template=self._processing_unit, src="@LOADER")
            self.sub("MeshTopology", objectNode,
                     name="topo", src="@LOADER")
        elif mesh_type == "quadraticTet":
            loaderNode = self.sub("MeshExtendedVTKLoader", objectNode,
                                  name="LOADER", filename=theFilename)
            self.sub("MechanicalObject", objectNode,
                     name="dofs", template=self._processing_unit, src="@LOADER")
            self.sub("QuadraticMeshTopology", objectNode,
                     name="topo", src="@LOADER")
        else:
            warn(MSMLSOFAExporterWarning, "Mesh type must be mesh.volume.linearTetrahedron.vtk or mesh.volume.quadraticTetrahedron.vtk")
            return None
        return loaderNode


    def createSolvers(self):
        if self._msml_file.env.solver.timeIntegration == "dynamicImplicit":
            self.sub("MyNewmarkImplicitSolver",
                     rayleighStiffness="0.2",
                     rayleighMass="0.02",
                     name="odesolver")

        elif self._msml_file.env.solver.timeIntegration == "dynamicImplicitEuler":
            self.sub("EulerImplicitSolver",
                     name="odesolver")
        else:
            warn(MSMLSOFAExporterWarning, "Error ODE solver %s not supported" %
                                          self._msml_file.env.solver.timeIntegration)

        if self._msml_file.env.solver.linearSolver == "direct":
            self.sub("SparseMKLSolver")
        elif self._msml_file.env.solver.linearSolver == "iterativeCG":
            self.sub("CGLinearSolver",
                     iterations="100", tolerance="1e-06", threshold="1e-06")
        else:
            warn(MSMLSOFAExporterWarning, "Error linear solver %s not supported" %
                                          self._msml_file.env.solver.linearSolver)


    def createMaterialRegions(self, objectNode, msmlObject):
        assert isinstance(msmlObject, SceneObject)

        materialNode = self.sub("Material", self.node_root)
        
        for k in range(len(msmlObject.material)):
            assert isinstance(msmlObject.material[k], MaterialRegion)
            indexGroupNode = msmlObject.material[k].get_indices()
            matregionId = msmlObject.material[k].id
            assert isinstance(indexGroupNode, ObjectElement)

            indices_key = indexGroupNode.attributes["indices"]
            indices_vec = self.evaluate_node(indices_key)
            indices = '%s' % ', '.join(map(str, indices_vec))

            indices_int = [int(i) for i in indices.split(",")]
            #Get all materials
            for i in range(len(msmlObject.material[k])):
                assert isinstance(msmlObject.material[k][i], ObjectElement)

                currentMaterialType = msmlObject.material[k][i].attributes['__tag__']
                if currentMaterialType == "indexgroup":
                    continue

                if currentMaterialType == "linearElastic":
                    currentYoungs = msmlObject.material[k][i].attributes["youngModulus"]
                    currentPoissons = msmlObject.material[k][i].attributes["poissonRatio"]
                elif currentMaterialType == "mass":
                    currentDensity = msmlObject.material[k][i].attributes["density"]
                else:
                    warn(MSMLSOFAExporterWarning, "Material Type not supported %s" % currentMaterialType)

            
            materialRegionNode = self.sub("material", materialNode, id=k+1, name = matregionId, type="neo-Hookean" )
            self.sub("density", materialRegionNode).text = str(currentDensity)
            self.sub("E", materialRegionNode).text = str(currentYoungs)
            self.sub("v", materialRegionNode).text = str(currentPoissons)


#===============================================================================
#         keylist = density.keys()
#         keylist.sort()
# 
#         _select = lambda x: (x[k] for k in keylist)
#         _to_str = lambda x: ' '.join(_select(x))
# 
#         density_str = _to_str(density)
#         youngs_str = _to_str(youngs)
#         poissons_str = _to_str(poissons)
#===============================================================================


        #merge all different materials to single forcefield/density entries.
        #=======================================================================
        # if objectNode.find("MeshTopology") is not None:
        #     elasticNode = self.sub("TetrahedronFEMForceField", objectNode,
        #                            template=self._processing_unit, name="FEM",
        #                            listening="true", youngModulus=youngs_str,
        #                            poissonRatio=poissons[keylist[0]])
        #     self.sub("TetrahedronSetGeometryAlgorithms", objectNode,
        #              name="aTetrahedronSetGeometryAlgorithm",
        #              template=self._processing_unit)
        #     massNode = self.sub("DiagonalMass", name="meshMass")
        #     massNode.set("massDensity", density_str)
        # elif objectNode.find("QuadraticMeshTopology") is not None:
        #     eelasticNode = self.sub("QuadraticTetrahedralCorotationalFEMForceField", objectNode,
        #                             template=self._processing_unit, name="FEM", listening="true",
        #                             setYoungModulus=youngs_str,
        #                             setPoissonRatio=poissons[keylist[0]])  # TODO
        #     emassNode = self.sub("QuadraticMeshMatrixMass", objectNode,
        #                          name="meshMass", massDensity=density_str)
        # else:
        #     warn(MSMLSOFAExporterWarning, "Current mesh topology not supported")
        #=======================================================================


    def createConstraintRegions(self, msmlObject):
        assert isinstance(msmlObject, SceneObject)
        boundaryNode = self.sub("Boundary", self.node_root)
        for constraint_set in (msmlObject.constraints[0], ):  #TODO take all constraints
            assert isinstance(constraint_set, ObjectConstraints)
            for constraint in constraint_set.constraints:
                assert isinstance(constraint, ObjectElement)
                currentConstraintType = constraint.tag
                indices_vec = self.evaluate_node(constraint.indices)
                print(map(str, indices_vec))
                if currentConstraintType == "fixedConstraint":
                    fixedConstraintNode = self.sub("fix", boundaryNode)
                    bc = "xyz"
                    for index in map(str, indices_vec):
                        self.sub("node", fixedConstraintNode, id=int(index)+1, bc=bc)
                elif currentConstraintType == "surfacePressure":
                    print("Pressure")
                else:
                    warn(MSMLSOFAExporterWarning, "Constraint Type not supported %s " % currentConstraintType)


    def createControl(self, currentSofaNode, scobj):
        assert isinstance(scobj, SceneObject)
        type ="solid"
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
        analysis = self.sub("analysis", controlNode, type = analysisType)

    def createScene(self):
        version = "1.2"  
        root = etree.Element("febio_spec", version=version)
        return root
    
    def createOutput(self):
        type = "febio"
        type2 = "displacement"
        type3 = "stress"  
        outputNode = self.sub("Output", self.node_root)
        plotfileNode = self.sub("plotfile", outputNode, type = type)
        self.sub("var", plotfileNode, type = type2)
        self.sub("var", plotfileNode, type = type3)

    def sub(self, tag, root=None, **kwargs):
        skwargs = {k: str(v) for k, v in kwargs.items()}
        if root is None: root = self.node_root
        return etree.SubElement(root, tag, **skwargs)