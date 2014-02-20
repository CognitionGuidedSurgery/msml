__author__ = 'Alexander Weigl'
__date__ = '2014-02-01'

from warnings import warn

import lxml.etree as etree

from .base import XMLExporter
from msml.model.exceptions import *


class MSMLSofaExporterWarning(MSMLWarning): pass


class SofaExporter(XMLExporter):
    def do_object_mesh(self, mesh, parent_node):
        '''


        '''

        mkind = mesh.type
        mid = mesh.id
        mattr = mesh.mesh

        meshfile = self._memory.lookup(mattr)

        if mkind == 'linearTet':
            etag = "MeshVTKLoader"
        elif mkind == 'quadraticTet':
            etag = 'MeshExtendedVTKLoader'
        else:
            warn("Mesh type must be mesh.volume.linearTetrahedron.vtk or mesh.volume.quadraticTetrahedron.vtk",
                 MSMLSofaExporterWarning)

        loaderNode = etree.SubElement(parent_node, etag, {
            'name': mid,
            'filename': meshfile,
            'createSubelements': 0,
        })

        etree.SubElement(parent_node, "MechanicalObject", {
            'name': "dofs",
            'template': "undef",
            'src': "@%s" % mid
        })

        etree.SubElement(parent_node, "MeshTopology", {
            'name': "topo",
            'src': "@%s" % mid
        })


    def render(self):
        dt = self._mfile.env.simulation[0].dt
        #TODO gravity missing

        self._root = etree.Element('Node', {
            'name': 'root',
            'dt': dt,
            'gravity': '0 0 10',
            'showBehaviour': '1',
            'showCollisionModel': '1'
        })

    def do_object(self, scobj):
        pass


    def do_env_solver(self, solver):
        try:
            linearSolver = solver['linearSolver']
            processingUnit = solver['processingUnit']
            timeIntegration = solver['timeIntegration']
        except KeyError, e:
            raise MSMLError('solver information are insufficient', e)

        if timeIntegration == "dynamicImplicit":
            etree.SubElement(self._root, "MyNewmarkImplicitSolver",
                             rayleighStiffness="0.2", rayleighMass="0.02",
                             name="odesolver")

        elif timeIntegration == "dynamicImplicitEuler":
            etree.SubElement(self._root, "EulerImplicitSolver", name="odesolver")

        else:
            warn("ODE solver %s not supported" % linearSolver, MSMLSofaExporterWarning)

        if linearSolver == 'direct':
            etree.SubElement(self._root, "SparseMKLSolver")
        elif linearSolver == "iterativeCG":
            etree.SubElement(self._root, "CGLinearSolver",
                             iterations="100", tolerance="1e-06", threshold="1e-06")
        else:
            warn("Error linear solver %s not supported" % linearSolver)

        # post processing
        value = "Vec3f" if processingUnit == "CPU" else "CudaVec3f"
        for element in sofaRootNode.iter():
            if (element.get("template")):
                if (element.get("template").find("undef") != -1):
                    element.set("template", element.get("template").replace("undef", value));


    def createMaterialRegions(self, materials):
        youngs = {}
        poissons = {}
        density = {}

        for region in materials:
            indices_entry = region.get_indices()
            indices = self._memory.lookup(indices_entry.indices)

            indices_int = [int(i) for i in indices.split(",")]

            #  Get all materials
            for material_element in region:
                mat_type = material_element['type']

                if mat_type != "indexgroup":
                    if mat_type == "linearElastic":
                        currentYoungs = material_element["youngModulus"]
                        currentPoissons = material_element["poissonRatio"]  # not implemented in sofa yet!
                        for i in indices_int:
                            youngs[i] = currentYoungs
                            poissons[i] = currentPoissons
                    elif mat_type == "mass":
                        currentDensity = material_element["density"]
                        for i in indices_int:
                            density[i] = currentDensity
                    else:
                        warn("Material Type not supported! Found type: %s" % mat_type, MSMLSofaExporterWarning)

        keylist = density.keys()
        keylist.sort()

        _gen_str_list = lambda map: " ".join((map[i] for i in keylist ))

        density_str = _gen_str_list(density)
        youngs_str = _gen_str_list(youngs)
        poissons_str = _gen_str_list(poissons)

        #merge all different materials to single forcefield/density entries.
        if currentSofaNode.find("MeshTopology") is not None:
            elasticNode = etree.SubElement(self._root, "TetrahedronFEMForceField",
                                           template="undef", name="FEM", listening="true",
                                           youngModulus=youngs_str,
                                           poissonRatio=poissons[keylist[0]])

            etree.SubElement(self._root, "TetrahedronSetGeometryAlgorithms",
                             name="aTetrahedronSetGeometryAlgorithm",
                             template="undef")

            etree.SubElement(self._root, "DiagonalMass", name="meshMass",
                             massDensity=density_str)

        elif currentSofaNode.find("QuadraticMeshTopology") is not None:
            etree.SubElement(self._root, "QuadraticTetrahedralCorotationalFEMForceField",
                             template="undef", name="FEM", listening="true",
                             setYoungModulus=youngs_str,
                             setPoissonRatio=poissons[keylist[0]])
            etree.SubElement(self._root, "QuadraticMeshMatrixMass",
                             name="meshMass", massDensity=density_str)
        else:
            warn("Current mesh topology not supported", MSMLSofaExporterWarning)


    def createConstraintRegions(self, constraints):
        constraints = constraints[0]  #first step

        indices_var = constraints.get_indices()
        indices = self._memory.lookup(indices_var)

        for constraint in constraints.elements:
            ctag = constraint['name']
            if ctag != 'indexgroup':
                try:
                    factory = CONSTRAINTS_FACTORIES[ctag]
                    factory(self._root, ctag, indices, **constraint)
                except KeyError, e:
                    warn("Constraint Type not supported %s" % ctag, MSMLSofaExporterWarning)


def createObject(self, currentSofaNode, currentMsmlNode, msmlRootNode):
    objectNode = etree.SubElement(currentSofaNode, "Node")
    objectNode.set("name", currentMsmlNode.get("name"))
    return objectNode


def createPostProcessingRequests(self, currentSofaNode, currentMsmlNode):
    for request in currentMsmlNode.iterchildren():
        if (request.tag == "displacementOutputRequest"):
            if (currentSofaNode.find("MeshTopology") is not None):
                #dispOutputNode = etree.SubElement(currentSofaNode, "ExtendedVTKExporter" )
                dispOutputNode = etree.SubElement(currentSofaNode, "VTKExporter")
                filename = os.path.join(self.outputDirectory, request.get("name"))
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
                timeSteps = int(
                    (self.rootNodeMSML.find(".//step").get("timesteps")))  #only one stimulation step supported
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
                filename = os.path.join(self.outputDirectory, request.get("name"))
                dispOutputNode.set("filename", filename)
                dispOutputNode.set("exportEveryNumberOfSteps", request.get("timestep"))
                dispOutputNode.set("tetras", "0")
                dispOutputNode.set("quadraticTetras", "1")
                dispOutputNode.set("listening", "true")
                dispOutputNode.set("exportAtEnd", "true")
                #TODO: Fill "filename" of request taking output numbering into account (see VTKExporter)
            else:
                print "Topolgy type not supported"


def _write(self, filename):
    self._root.write(filename, pretty_print=True)


def register(registry, name):
    def decorator(fn):
        CONSTRAINTS_FACTORIES[name] = fn

    return decorator


CONSTRAINTS_FACTORIES = {}
import functools

register_constraint = functools.partial(register, CONSTRAINTS_FACTORIES)


@register_constraint("fixedConstraints")
def _fixed_constraint(parent_node, name, indices):
    constraintNode = etree.SubElement(currentSofaNode, "FixedConstraint", {
        "name": name,

        "indices": indices
    })


@register_constraint("surfacePressure")
def _surface_pressure(parent_node, name, indices):
    constraintNode = etree.SubElement(parent_node, "Node", name="SurfaceLoad")
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


@register_constraint("springMeshToFixed")
def _spring_mesh_to_fixed(parent_node, name, indices, movingPoints=None, fixedPoints=None, stiffness=None,
                          rayleighStiffnes=None):
    constraintNode = etree.SubElement(parent_node, "Node", name="springMeshToFixed")
    mechObj = etree.SubElement(constraintNode, "MechanicalObject", template="Vec3f",
                               name="pointsInDeformingMesh")
    mechObj.set("position", movingPoints);
    etree.SubElement(constraintNode, "BarycentricMapping", template="undef, Vec3f",
                     name="barycentricMapSpringMeshToFixed", input="@..", output="@.")
    displacedLandLMarks = etree.SubElement(constraintNode, "Node",
                                           name="fixedPointsForSpringMeshToFixed")
    mechObj = etree.SubElement(displacedLandLMarks, "MechanicalObject", template="Vec3f",
                               name="fixedPoints")
    mechObj.set("position", fixedPoints);
    forcefield = etree.SubElement(constraintNode, "RestShapeSpringsForceField", template="Vec3f",
                                  name="Springs",
                                  external_rest_shape="fixedPointsForSpringMeshToFixed/fixedPoints",
                                  drawSpring="true")
    forcefield.set("stiffness", stiffness);
    forcefield.set("rayleighStiffnes", rayleighStiffnes);


@register_constraint("supportingMesh")
def _support_mesh(parent_node, name, indices, filename, youngModulus, poissonRatio, massDensity):
    constraintNode = etree.SubElement(parent_node, "Node", name="support")
    constraintNode.set("name", "support_%s" % name)
    loaderNode = etree.SubElement(constraintNode, "MeshVTKLoader", name="LOADER_supportmesh",
                                  createSubelements="0")
    loaderNode.set("filename", filename)  #workaround, because node evaluation is only possible for data/operator nodes.
    etree.SubElement(constraintNode, "MechanicalObject", name="dofs", src="@LOADER_supportmesh",
                     template="Vec3f", translation="0 0 0")
    etree.SubElement(constraintNode, "MeshTopology", name="topo", src="@LOADER_supportmesh")
    forcefield = etree.SubElement(constraintNode, "TetrahedronFEMForceField", listening="true",
                                  name="FEM", template="Vec3f")
    forcefield.set("youngModulus", youngModulus)
    forcefield.set("poissonRatio", poissonRatio)
    etree.SubElement(constraintNode, "TetrahedronSetGeometryAlgorithms",
                     name="aTetrahedronSetGeometryAlgorithm", template="Vec3f")
    diagonalMass = etree.SubElement(constraintNode, "DiagonalMass", name="meshMass")
    diagonalMass.set("massDensity", massDensity)
    etree.SubElement(constraintNode, "BarycentricMapping", input="@..", name="barycentricMap",
                     output="@.", template="undef, Vec3f")