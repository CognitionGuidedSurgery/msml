# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
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
__date__ = "2014-03-13"

import math
import os
import subprocess

from path import path

from .. import log

import lxml.etree as etree
from ..model import *
from .base import XMLExporter, Exporter
from msml.exceptions import *
from ..sortdef import VTK

from ..log import error, warn, info, fatal, critical, debug


class MSMLSOFAExporterWarning(MSMLWarning): pass


class SofaExporter(XMLExporter):
    def __init__(self, msml_file):
        """
      Args:
       executer (Executer)


      """
        self.name = 'SOFAExporter'
        self.id = 'SOFAExporter'
        Exporter.__init__(self, msml_file)
        self.export_file = None
        self.working_dir = path()  #path.dirname(msml_file.filename)
        self._memory_update = {}  #cache for changes to _memory, updated after execution.

    def init_exec(self, executer):
        """initialization by the executer, sets memory and executor member
        :param executer: msml.run.Executer
        :return:
        """
     
        self._executer = executer
        self._memory = self._executer._memory

    def render(self):
        """
        Builds the File (XML e.g) for the external tool
        """

        self.export_file = path(self._msml_file.filename).namebase + ".scn"
        info("Converting to sofa scn: %s", self.export_file)

        import codecs

        with codecs.open(self.export_file, 'w', 'utf-8') as scnfile:  #should be open with codecs.open
            rootelement = self.write_scn()
            rootelement.write(scnfile, pretty_print=True)
            #s = etree.tostring(rootelement, encoding="utf-8")
            #scnfile.write(s)


    def execute(self):
        "should execute the external tool and set the memory"
        import msml.envconfig

        filenameSofaBatch = "%s_SOFA_batch.txt" % self.export_file

        with open(filenameSofaBatch, 'w') as f:
            timeSteps = self._msml_file.env.simulation[0].iterations  #only one step supported
            f.write(os.path.join(os.getcwd(), self.export_file) + ' ' + str(
                timeSteps) + ' ' + self.export_file + '.simu \n')


        cmd = "%s -l SOFACuda %s" % (msml.envconfig.SOFA_EXECUTABLE, filenameSofaBatch)

        if(msml.envconfig.SOFA_EXECUTABLE.find('runSofaExtended') > -1):
            timeSteps = self._msml_file.env.simulation[0].iterations  #only one step supported
            callCom = '-l SofaCUDA -l MediAssist -g batch -n ' + str(timeSteps) + ' ' + os.path.join(os.getcwd(),
                                                                                                     self.export_file) + '\n'
            cmd = "%s  %s" % (msml.envconfig.SOFA_EXECUTABLE, callCom )

        log.info("Executing %s" % cmd)
        log.info("Working directory: %s" % os.getcwd())

        os.system(cmd)

        self._memory._internal.update(self._memory_update)  #update output

        #subprocess.call(cmd)


    def write_scn(self):
        processingUnit = self._msml_file.env.solver.processingUnit

        self._processing_unit = "Vec3f" if processingUnit == "CPU" else "CudaVec3f"

        self.node_root = self.createScene()

        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)

            #create object, the mesh, material regions and constraints
            objectNode = self.createObject(self.node_root, msmlObject)

            #physicsElementNode = msmlObject.find("material")
            self.createMeshTopology(objectNode, msmlObject)
            self.createMaterialRegions(objectNode, msmlObject)

            #create simulation steps
            self.createConstraintRegions(objectNode, msmlObject)

            #creat post processing request
            self.createPostProcessingRequests(objectNode, msmlObject)

            #add solver
        self.createSolvers()

        return etree.ElementTree(self.node_root)

    def createMeshTopology(self, objectNode, msmlObject):
        assert isinstance(msmlObject, SceneObject)
        mesh_value = msmlObject.mesh.mesh
        mesh_type = msmlObject.mesh.type

        theFilename = self.working_dir / self.get_value_from_memory(msmlObject.mesh)

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
            warn(MSMLSOFAExporterWarning,
                 "Mesh type must be mesh.volume.linearTetrahedron.vtk or mesh.volume.quadraticTetrahedron.vtk")
            return None
        return loaderNode


    def createSolvers(self):
        if self._msml_file.env.solver.timeIntegration == "Newmark":
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

        youngs = {}
        poissons = {}
        density = {}


        for matregion in msmlObject.material:
            assert isinstance(matregion, MaterialRegion)
            indices_key = matregion.indices
            indices_vec = self.get_value_from_memory(matregion)
            indices = '%s' % ', '.join(map(str, indices_vec))


            indices_int = [int(i) for i in indices.split(",")]
            indices_int.sort()

            #Get all materials
            for material in matregion:
                assert isinstance(material, ObjectElement)
                currentMaterialType = material.tag

                if currentMaterialType == "linearElasticMaterial":
                    currentYoungs = self.get_value_from_memory(material, "youngModulus")
                    currentPoissons = self.get_value_from_memory(material,
                                                                 "poissonRatio")  # not implemented in sofa yet!
                    for i in indices_int:  #TODO Performance (maybe generator should be make more sense)
                        youngs[i] = currentYoungs
                        poissons[i] = currentPoissons
                elif currentMaterialType == "mass":
                    currentDensity = self.get_value_from_memory(material, "massDensity")
                    for i in indices_int:
                        density[i] = currentDensity
                else:
                    warn("Material Type not supported %s" % currentMaterialType, MSMLSOFAExporterWarning)


        def _to_str(mapping):
            keys = list(mapping.keys())
            keys.sort()
            sorted_values = (mapping[k] for k in keys)
            return ' '.join(map(str, sorted_values))

        density_str = _to_str(density)
        youngs_str = _to_str(youngs)
        poissons_str = _to_str(poissons)


        #merge all different materials to single forcefield/density entries.
        if objectNode.find("MeshTopology") is not None:
            elasticNode = self.sub("TetrahedronFEMForceField", objectNode,
                                   template=self._processing_unit, name="FEM",
                                   listening="true", youngModulus=youngs_str,
                                   poissonRatio=poissons[indices_int[0]])
            self.sub("TetrahedronSetGeometryAlgorithms", objectNode,
                     name="aTetrahedronSetGeometryAlgorithm",
                     template=self._processing_unit)
            massNode = self.sub("DiagonalMass", objectNode, name="meshMass")
            massNode.set("massDensity", density_str)

        elif objectNode.find("QuadraticMeshTopology") is not None:
            eelasticNode = self.sub("QuadraticTetrahedralCorotationalFEMForceField", objectNode,
                                    template=self._processing_unit, name="FEM", listening="true",
                                    youngModulus=youngs[0],
                                    poissonRatio=poissons[indices_int[0]])  # TODO
            emassNode = self.sub("QuadraticMeshMatrixMass", objectNode,
                                 name="meshMass", massDensity=density[0])
        else:
            warn(MSMLSOFAExporterWarning, "Current mesh topology not supported")


    def createConstraintRegions(self, objectNode, msmlObject):
        assert isinstance(msmlObject, SceneObject)

        for constraint_set in (msmlObject.constraints[0], ):  #TODO take all constraints
            assert isinstance(constraint_set, ObjectConstraints)

            for constraint in constraint_set.constraints:
                assert isinstance(constraint, ObjectElement)
                currentConstraintType = constraint.tag
                indices_vec = self.get_value_from_memory(constraint, 'indices')
                if (indices_vec is not None):
                    indices = '%s' % ', '.join(map(str, indices_vec))

                if currentConstraintType == "fixedConstraint":
                    constraintNode = self.sub("FixedConstraint", objectNode,
                                              name=constraint.id or constraint_set.name,
                                              indices=indices)

                    #elasticNode.set("setPoissonRatio", material.get("poissonRatio"))

                    #check if child is present

                    #if so, check operator compatibility

                    #execute operator

                    #check if mesh is in MSML folder

                    #if not -> copy
                elif currentConstraintType == "surfacePressure":
                    constraintNode = self.sub("Node", objectNode, name="SurfaceLoad")

                    self.sub("MeshTopology", constraintNode,
                             name="SurfaceTopo",
                             position="@LOADER.position",
                             triangles="@LOADER.triangles", quads="@LOADER.quads")

                    self.sub("MechanicalObject", constraintNode, template="Vec3f", name="surfacePressDOF",
                             position="@SurfaceTopo.position")
                    p = self.get_value_from_memory(constraint, 'pressure') / 10


                    surfacePressureForceFieldNode = self.sub("SurfacePressureForceField", constraintNode,
                                                             template="Vec3f",
                                                             name="surfacePressure",
                                                             pulseMode="1",
                                                             pressureSpeed=p,
                                                             # TODO this is broken
                                                             pressure=constraint.pressure,
                                                             triangleIndices=indices)

                    self.sub("BarycentricMapping", constraintNode,
                             template=self._processing_unit + ", Vec3f",
                             name="barycentricMapSurfacePressure",
                             input="@..", output="@.")

                elif currentConstraintType == "springMeshToFixed":

                    constraintNode = self.sub("Node", objectNode, name="springMeshToFixed")
                    mechObj = self.sub("MechanicalObject", constraintNode, template="Vec3f",
                                       name="pointsInDeformingMesh",
                                       position=constraint.get("movingPoints"))

                    self.sub("BarycentricMapping", constraintNode,
                             template=self._processing_unit + ", Vec3f",
                             name="barycentricMapSpringMeshToFixed",
                             input="@..",
                             output="@.")

                    displacedLandLMarks = self.sub("Node", constraintNode,
                                                   name="fixedPointsForSpringMeshToFixed")
                    
                    mechObj = self.sub("MechanicalObject", displacedLandLMarks,
                                       template="Vec3f",
                                       name="fixedPoints")

                    mechObj.set("position", constraint.get("fixedPoints"))

                    forcefield = self.sub("RestShapeSpringsForceField", constraintNode,
                                          template="Vec3f",
                                          name="Springs",
                                          external_rest_shape="fixedPointsForSpringMeshToFixed/fixedPoints",
                                          drawSpring="true",
                                          stiffness=constraint.get("stiffness"),
                                          rayleighStiffnes=constraint.get("rayleighStiffnes"))

                elif currentConstraintType == "supportingMesh":

                    constraintNode = self.sub("Node", objectNode, name="support_" + constraint.get("name"))
                    loaderNode = self.sub("MeshVTKLoader", constraintNode,
                                          name="LOADER_supportmesh",
                                          createSubelements="0",
                                          filename=constraint.get("filename"))

                    self.sub("MechanicalObject", constraintNode,
                             name="dofs",
                             src="@LOADER_supportmesh",
                             template="Vec3f",
                             translation="0 0 0")

                    self.sub("MeshTopology", constraintNode,
                             name="topo",
                             src="@LOADER_supportmesh")

                    forcefield = self.sub("TetrahedronFEMForceField", constraintNode, listening="true",
                                          name="FEM", template="Vec3f",
                                          youngModulus=constraint.get("youngModulus"),
                                          poissonRatio=constraint.get("poissonRatio"))

                    self.sub("TetrahedronSetGeometryAlgorithms", constraintNode,
                             name="aTetrahedronSetGeometryAlgorithm",
                             template="Vec3f")

                    diagonalMass = self.sub("DiagonalMass", constraintNode,
                                            name="meshMass",
                                            massDensity=constraint.get("massDensity"))

                    self.sub("BarycentricMapping", constraintNode,
                             input="@..",
                             name="barycentricMap",
                             output="@.",
                             template=self._processing_unit + ", Vec3f")

                elif currentConstraintType == "displacementConstraint":

                    #compute length of time stepo
                    timeSteps = self._msml_file.env.simulation[0].iterations
                    dt  = self._msml_file.env.simulation[0].dt
                    timestep = float(timeSteps) *dt
                    keytimes = '0 '+str(timestep)+ ' ' +str( 100000) # this is a bad hack! -> if simulation runs further, it stays stable

                    #TODO: How do we get the disp values from memory?
                    disp_vec = {0,0,0.01}
                    tempMovement = '%s' % ' '.join(map(str, disp_vec))
                    theMovement = "0 0 0 "+tempMovement+" 0 0 0"
                    constraintNode = self.sub('LinearMovementConstraint', objectNode,
                                              name=constraint.id or constraint_set.name,
                                              indices=indices, movements=theMovement, keyTimes = keytimes)
                    #constraintNode = self.sub("DirichletBoundaryConstraint", objectNode,
                    #                      name=constraint.id or constraint_set.name,
                    #                      dispIndices=indices, displacements=constraint.displacement)
                else:
                    warn(MSMLSOFAExporterWarning, "Constraint Type not supported %s " % currentConstraintType)


    def createObject(self, currentSofaNode, scobj):
        assert isinstance(scobj, SceneObject)
        objectNode = self.sub("Node", name=scobj.id)
        return objectNode


    def createScene(self):
        dt = str(self._msml_file.env.simulation[0].dt)
        root = etree.Element("Node", name="root", dt=dt)
        theGravityVec =  self._msml_file.env.simulation[0].gravity
        theGravity = str(theGravityVec)
        #timeSteps = self._msml_file.env.simulation[0].iterations  #only one step supported
        if theGravity is None:
            theGravity = '0 -9.81 0'
        root.set("gravity", theGravity)
        return root

        #sofa_exporter handles displacementOutputRequest only. Other postProcessing operators need to be adressed in... ?


    def createPostProcessingRequests(self, objectNode, msmlObject):
        for request in msmlObject.output:
            assert isinstance(request, ObjectElement)
            filename = self.working_dir / request.id

            if request.tag == "displacement":
                if objectNode.find("MeshTopology") is not None:
                    #dispOutputNode = self.sub(currentSofaNode, "ExtendedVTKExporter" )
                    exportEveryNumberOfSteps = request.get("timestep")

                    dispOutputNode = self.sub("VTKExporter", objectNode,
                                              filename=filename,
                                              exportEveryNumberOfSteps=exportEveryNumberOfSteps,
                                              XMLformat=1,
                                              edges=0,
                                              #todo export material => allows extraction of surfaces in post processing
                                              tetras=1,
                                              triangles=0,
                                              listening="true",
                                              exportAtEnd="true")

                    timeSteps = self._msml_file.env.simulation[0].iterations

                    #exportEveryNumberOfSteps = 1 in SOFA means export every second time step.
                    #exportEveryNumberOfSteps = 0 in SOFA means do not export.
                    if exportEveryNumberOfSteps == 0:
                        lastNumber = 1
                    else:
                        lastNumber = int(math.floor(int(timeSteps) / ( int(exportEveryNumberOfSteps) + 1)))
                    
                    if (request.useAsterisk): 
                        self._memory_update[self.id] = {request.id: VTK(str(filename + '*' + ".vtu"))} 
                    else:
                        self._memory_update[self.id] = {request.id: VTK(str(filename + str(lastNumber) + ".vtu"))} 


                elif objectNode.find("QuadraticMeshTopology") is not None:
                    exportEveryNumberOfSteps = request.get("timestep")

                    dispOutputNode = self.sub("ExtendedVTKExporter", objectNode,
                                              filename=filename,
                                              exportEveryNumberOfSteps=exportEveryNumberOfSteps,
                                              #todo export material => allows extraction of surfaces in post processing
                                              tetras=0,
                                              quadraticTetras=1,
                                              listening="true",
                                              exportAtEnd="true")

                    # untested block:
                    
                    # timeSteps = self._msml_file.env.simulation[0].iterations
                    #
                    # #exportEveryNumberOfSteps = 1 in SOFA means export every second time step.
                    # #exportEveryNumberOfSteps = 0 in SOFA means do not export.
                    # if exportEveryNumberOfSteps == 0:
                    #     lastNumber = 1
                    # else:
                    #     lastNumber = int(math.floor(int(timeSteps) / ( int(exportEveryNumberOfSteps) + 1)))
                    #
                    #if (request.useAsterisk): 
                    #    self._memory_update[self.id] = {request.id: VTK(str(filename + '*' + ".vtu"))} 
                    #else:
                    #    self._memory_update[self.id] = {request.id: VTK(str(filename + str(lastNumber) + ".vtu"))} 



                    #TODO: Fill "filename" of request taking output numbering into account (see VTKExporter)
                else:
                    warn(MSMLSOFAExporterWarning, "Topolgy type not supported")

    def sub(self, tag, root=None, **kwargs):
        skwargs = {k: str(v) for k, v in kwargs.items()}
        if root is None: root = self.node_root
        return etree.SubElement(root, tag, **skwargs)