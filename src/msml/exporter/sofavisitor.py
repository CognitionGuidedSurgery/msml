__author__ = 'weigl'

from __future__ import print_function

from lxml import etree
from warnings import warn

from .visitor import *
import math


class MSMLSOFAExporterWarning(Warning):
    pass

def SubElement(root, tag, **kwargs):
    skwargs = {k: str(v) for k, v in kwargs.items()}
    return etree.SubElement(root, tag, **skwargs)


constraint_dispatcher = Dispatcher(attrib_getter(4, 'tag'),
                                   "Constraint Type not supported %s ")

mesh_dispatcher = Dispatcher(attrib_getter(4, 'type'),
                             "Mesh type must be mesh.volume.linearTetrahedron.vtk or "
                             "mesh.volume.quadraticTetrahedron.vtk\n"
                             "mesh type not supported %s")

material_dispatcher = Dispatcher(attrib_getter(4, 'tag'),
                                 "Constraint Type not supported %s ")


@constraint_dispatcher.register("fixedConstraint")
def _fixedConstraint(visitor, _object, _material, _region, constraint):
    indices_vec = visitor.evaluate_node(constraint.indices)
    indices = '%s' % ', '.join(map(str, indices_vec))

    constraintNode = SubElement(_object, "FixedConstraint",
                                name=constraint.id,
                                indices=indices)


@constraint_dispatcher.register("surfacePressure")
def _surfacePressure(visitor, _object, _material, _region, constraint):
    indices_vec = visitor.evaluate_node(constraint.indices)
    indices = '%s' % ', '.join(map(str, indices_vec))

    _node = SubElement(_object, "Node", name="SurfaceLoad")

    SubElement(_node, "MeshTopology",
               name="SurfaceTopo",
               position="@LOADER.position",
               triangles="@LOADER.triangles", quads="@LOADER.quads")

    SubElement(_node, "MechanicalObject", template="Vec3f", name="surfacePressDOF",
               position="@SurfaceTopo.position")

    SubElement(_node, "SurfacePressureForceField",
               template="Vec3f",
               name="surfacePressure",
               pulseMode="1",
               pressureSpeed=str(float(
                   constraint.pressure) / 10.0),
               pressure=constraint.get("pressure"),
               triangleIndices=indices)

    SubElement(_node, "BarycentricMapping", _node,
               template="undef, Vec3f",
               name="barycentricMapSurfacePressure",
               input="@..", output="@.")


@constraint_dispatcher.register("springMeshToFixed")
def _springMeshToFixed(visitor, _object, _material, _region, constraint):
    indices_vec = visitor.evaluate_node(constraint.indices)
    indices = '%s' % ', '.join(map(str, indices_vec))

    _node = SubElement(_object, "Node", name="springMeshToFixed")

    SubElement(_node, "MechanicalObject", template="Vec3f",
               name="pointsInDeformingMesh",
               position=constraint.get("movingPoints"))

    SubElement(_node, "BarycentricMapping",
               template="undef, Vec3f",
               name="barycentricMapSpringMeshToFixed",
               input="@..",
               output="@.")

    displacedLandLMarks = SubElement(_node, "Node",
                                     name="fixedPointsForSpringMeshToFixed")

    SubElement(displacedLandLMarks, "MechanicalObject",
               template="Vec3f",
               name="fixedPoints",
               position=constraint.get("fixedPoints"))

    SubElement(_node, "RestShapeSpringsForceField",
               template="Vec3f",
               name="Springs",
               external_rest_shape="fixedPointsForSpringMeshToFixed/fixedPoints",
               drawSpring="true",
               stiffness=constraint.get("stiffness"),
               rayleighStiffnes=constraint.get("rayleighStiffnes"))


@constraint_dispatcher.register("supportingMesh")
def _supportingMesh(visitor, _object, _material, _region, constraint):
    indices_vec = visitor.evaluate_node(constraint.indices)
    indices = '%s' % ', '.join(map(str, indices_vec))

    _node = SubElement("Node", name="support_%s" % constraint.get("name"))
    SubElement(_node, "MeshVTKLoader",
               name="LOADER_supportmesh",
               createSubelements="0",
               filename=constraint.get("filename"))

    SubElement(_node, "MechanicalObject",
               name="dofs",
               src="@LOADER_supportmesh",
               template="Vec3f",
               translation="0 0 0")

    SubElement("MeshTopology", _node,
               name="topo",
               src="@LOADER_supportmesh")

    SubElement("TetrahedronFEMForceField", _node, listening="true",
               name="FEM", template="Vec3f",
               youngModulus=constraint.get("youngModulus"),
               poissonRatio=constraint.get("poissonRatio"))

    SubElement(_node, "TetrahedronSetGeometryAlgorithms",
               name="aTetrahedronSetGeometryAlgorithm",
               template="Vec3f")

    SubElement(_node, "DiagonalMass",
               name="meshMass",
               massDensity=constraint.get("massDensity"))

    SubElement(_node, "BarycentricMapping",
               input="@..",
               name="barycentricMap",
               output="@.",
               template="undef, Vec3f")


@mesh_dispatcher.register('linearTet')
def _linearTet(exporter, _msml, _scene, _object, mesh):
    mesh_value = mesh.mesh
    theFilename = exporter.working_dir / exporter.evaluate_node(mesh_value)

    SubElement(_object, "MeshVTKLoader",
               name="LOADER", filename=theFilename,
               createSubelements=0)
    SubElement(_object, "MechanicalObject",
               name="dofs", template=_msml._processing_unit, src="@LOADER")
    SubElement(_object, "MeshTopology",
               name="topo", src="@LOADER")


@mesh_dispatcher.register('quadraticTet')
def _quadraticTet(exporter, _msml, _scene, _object, mesh):
    mesh_value = mesh.mesh
    theFilename = exporter.working_dir / exporter.evaluate_node(mesh_value)

    SubElement(_object, "MeshExtendedVTKLoader",
               name="LOADER", filename=theFilename)
    SubElement(_object, "MechanicalObject",
               name="dofs",
               template=_msml._processing_unit,
               src="@LOADER")

    SubElement(_object, "QuadraticMeshTopology",
               name="topo", src="@LOADER")


class SofaVisitor(Visitor):
    def __init__(self, exporter):
        self.exporter = exporter

    def msml_begin(self, msml_file):
        dt = "0.05"  # TODO find dt from msmlfile > env > simulation
        root = etree.Element("Node", name="root", dt=dt)
        theGravity = "0 0 -9.81"  # TODO find gravity in msmlfile > env > simulation stepNode.get("gravity")
        if theGravity is None:
            theGravity = '0 -9.81 0'
        root.set("gravity", theGravity)
        self._msml_file = msml_file
        return root

    def environment_solver(self, _msml, _environment, solver):
        if solver.timeIntegration == "dynamicImplicit":
            SubElement(_msml, "MyNewmarkImplicitSolver",
                       rayleighStiffness="0.2",
                       rayleighMass="0.02",
                       name="odesolver")

        elif solver.timeIntegration == "dynamicImplicitEuler":
            SubElement("EulerImplicitSolver",
                       name="odesolver")
        else:
            warn(MSMLSOFAExporterWarning, "Error ODE solver %s not supported" % solver.timeIntegration)

        if solver.linearSolver == "direct":

            SubElement(_msml, "SparseMKLSolver")

        elif solver.linearSolver == "iterativeCG":

            SubElement(_msml, "CGLinearSolver",
                       iterations="100",
                       tolerance="1e-06",
                       threshold="1e-06")
        else:
            warn(MSMLSOFAExporterWarning, "Error linear solver %s not supported" % solver.linearSolver)

        processingUnit = solver.processingUnit
        _msml._processing_unit = "Vec3f" if processingUnit == "CPU" else "CudaVec3f"


    def object_begin(self, _msml, _scene, object):
        return SubElement("Node", name=object.id)

    def object_mesh(self, _msml, _scene, _object, mesh):
        return mesh_dispatcher(self.exporter, _msml, _scene, _object, mesh)

    def object_constraint_element(self, _msml, _scene, _object, _constraints, _constraint, element):
        constraint_dispatcher(self.exporter, _msml, _scene, _object, _constraints, _constraint, element)


    def object_material_begin(self, _msml, _scene, _object, regions):
        youngs = {}
        poissons = {}
        density = {}

        for matregion in regions:
            indexGroupNode = matregion.get_indices()

            assert isinstance(indexGroupNode, ObjectElement)

            indices_key = indexGroupNode.attributes["indices"]
            indices_vec = self.exporter.evaluate_node(indices_key)
            indices = '%s' % ', '.join(map(str, indices_vec))

            indices_int = [int(i) for i in indices.split(",")]

            #Get all materials
            for material in matregion:
                assert isinstance(material, ObjectElement)

                currentMaterialType = material.attributes['__tag__']
                if currentMaterialType == "indexgroup":
                    continue

                if currentMaterialType == "linearElastic":
                    currentYoungs = material.attributes["youngModulus"]
                    currentPoissons = material.attributes["poissonRatio"]  # not implemented in sofa yet!
                    for i in indices_int:  #TODO Performance (maybe generator should be make more sense)
                        youngs[i] = currentYoungs
                        poissons[i] = currentPoissons
                elif currentMaterialType == "mass":
                    currentDensity = material.attributes["density"]
                    for i in indices_int:
                        density[i] = currentDensity
                else:
                    warn(MSMLSOFAExporterWarning, "Material Type not supported %s" % currentMaterialType)

        keylist = density.keys()
        keylist.sort()

        _select = lambda x: (x[k] for k in keylist)
        _to_str = lambda x: ' '.join(_select(x))

        density_str = _to_str(density)
        youngs_str = _to_str(youngs)
        poissons_str = _to_str(poissons)


        #merge all different materials to single forcefield/density entries.
        if _object.find("MeshTopology") is not None:

            SubElement(_object, "TetrahedronFEMForceField",
                       template=_msml._processing_unit, name="FEM",
                       listening="true", youngModulus=youngs_str,
                       poissonRatio=poissons[keylist[0]])

            SubElement(_object, "TetrahedronSetGeometryAlgorithms",
                       name="aTetrahedronSetGeometryAlgorithm",
                       template=_msml._processing_unit)

            SubElement(_object, "DiagonalMass",
                       name="meshMass",
                       massDensity=density_str)

        elif _object.find("QuadraticMeshTopology") is not None:

            SubElement(_object, "QuadraticTetrahedralCorotationalFEMForceField",
                       template=self._processing_unit,
                       name="FEM",
                       listening="true",
                       setYoungModulus=youngs_str,
                       setPoissonRatio=poissons[keylist[0]])  # TODO

            SubElement(_object, "QuadraticMeshMatrixMass",
                       name="meshMass", massDensity=density_str)
        else:
            warn(MSMLSOFAExporterWarning, "Current mesh topology not supported")

    def object_end(self, _msml, _scene, _object, sceneobject):
        for request in sceneobject.output:
            assert isinstance(request, ObjectElement)
            filename = self.working_dir / request.id
            if request.tag == "displacementOutputRequest":
                if _object.find("MeshTopology") is not None:
                    #dispOutputNode = self.sub(currentSofaNode, "ExtendedVTKExporter" )
                    exportEveryNumberOfSteps = request.get("timestep")

                    dispOutputNode = SubElement(_object, "VTKExporter",
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

                    filenameLastOutput = filename + str(lastNumber) + ".vtu"
                    dispOutputNode.set("filename", filenameLastOutput)

                elif _object.find("QuadraticMeshTopology") is not None:
                    SubElement(_object, "ExtendedVTKExporter",
                               filename=filename,
                               exportEveryNumberOfSteps=exportEveryNumberOfSteps,
                               #todo export material => allows extraction of surfaces in post processing
                               tetras=0,
                               quadraticTetras=1,
                               listening="true",
                               exportAtEnd="true")

                    #TODO: Fill "filename" of request taking output numbering into account (see VTKExporter)
                else:
                    warn(MSMLSOFAExporterWarning, "Topolgy type not supported")


class SofaVisitorExporter(VisitorExporterFramework):
    def __init__(self, msml_file):
        super(VisitorExporterFramework, self).__init__(msml_file, SofaVisitor)

