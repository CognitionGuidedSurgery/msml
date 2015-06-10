# -*- encoding: utf-8 -*-
# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
# Medicine Meets Virtual Reality (MMVR) 2014
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

__authors__ = 'Nicolai Schoch, Alexander Weigl <uiduw@student.kit.edu>'
__license__ = 'GPLv3'

import jinja2

from msml.model import *
from msml.exceptions import *
import msml.ext.misc

from msml.log import debug


class MSMLHiFlow3ExporterWarning(MSMLWarning): pass


from ... import log

from path import path
from collections import namedtuple
from ..base import Exporter

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(path(__file__).dirname()))

SCENE_TEMPLATE = jinja_env.get_template("hiflow_scene.tpl.xml")
BCDATA_TEMPLATE = jinja_env.get_template("hiflow_bcdata.tpl.xml")


class BcData(object):
    def __init__(self):
        self.fc = BcDataEntry()  # fixed dirichlet constraint
        self.dc = BcDataEntry()  # displacement dirichlet constraint
        self.fp = BcDataEntry()  # force/pressure neumann constraint


class BcDataEntry(object):
    """Holds the data for a Fixed/Displacement (Dirichlet) constraint or Pressure/Force (Neumann) constraint in the bcdata file.

    """

    def __init__(self):
        self._num = 0
        self._points = []
        self._vectors = []
        self.is_valid()

    def is_valid(self):
        """asserts, that the amount of points and vectors are dividable by 3
           and correct to the given number of points

        :raises: Assertion, if data structure is wrong.
        :return: None
        """
        div3 = lambda x: len(x) % 3 == 0

        assert div3(self._points)
        assert div3(self._vectors)

        assert self._num * 3 == len(self._points)
        assert self._num * 3 == len(self._vectors)


    def append(self, count, points, vectors):
        """Appends the given `points` with `vectors` to the constraint.

        * length of points has to be dividable by 3
        * length of vectors has to be dividable by 3
        * if vectors just holds three components it is repeated
          to the correct amount given by `count`

        * each component of points and vectors is casted to float

        :param count: amount of points
        :param points: a list of points (3*count == len(points)
        :type points: list
        :param vectors: a list of points (3*count == len(points)
        :type list: list

        :return: None
        """
        as_float = lambda seq: map(float, seq)

        points = as_float(points)
        vectors = as_float(vectors)

        if len(vectors) == 3:
            # a single vector is given
            vectors = vectors * count

        self._num += count
        self._points += points
        self._vectors += vectors

        self.is_valid()

    def __repr__(self):
        return "%s.%s(%s, %s, %s)" % (
            self.__module__, type(self).__name__,
            repr(self.num), repr(self._points), repr(self._vectors)
        )

    def __str__(self):
        return "<%s.%s num: %d >" % (self.__module__, type(self).__name__, self._num)

    @property
    def num(self):
        return self._num

    @property
    def points(self):
        return list_to_hf3(self._points)

    @property
    def vectors(self):
        return list_to_hf3(self._vectors)


# namedtuple(...) dynamically creates a class -> class constructor.
Entry = namedtuple("Entry", "mesh bcdata")

# Hiflow3-supported features

HIFLOW_FEATURES = frozenset(
    ['object_element_displacement_supported', 'output_supported', 'object_element_mass_supported',
     'scene_objects_supported', 'constraints_supported', 'env_processingunit_CPU_supported',
     'material_region_supported', 'env_linearsolver_iterativeCG_supported', 'env_preconditioner_None_supported',
     'object_element_linearElasticMaterial_supported', 'sets_elements_supported', 'sets_nodes_supported',
     'sets_surface_supported', 'environment_simulation_steps_supported', 'object_element_fixedConstraint_supported',
     'env_timeintegration_dynamicImplicitEuler_supported', 'interbody_contact_simulation_supported'])
# Note: eventually add new stuff here...

class HiFlow3Exporter(Exporter):
    """Exporter for `hiflow3 <http://hiflow3.org>`_

    .. todo::
        What does this exporter support? - See GitHub issue n73.

    """

    def __init__(self, msml_file):
        """
        :param msml_file:
        :type msml_file: MSMLFile
        """
        self.hf3_parameters = {}
        """a dictionary with parameters for the hf3 exporter with higher priority
        :type: dict
        """

        self.name = 'HiFlow3Exporter'
        self.initialize(
            msml_file=msml_file,
            mesh_sort=('VTU', 'Mesh'), # needed in HiFlow3Exporter!
            #mesh_sort=('INP', 'Mesh'), # needed in MitralExporter!
            features=HIFLOW_FEATURES,
        )


    def render(self):
        """
        Builds the File (XML e.g) for the external tool
        """

        filename = self._msml_file.filename.namebase

        log.info("Converting to HiFlow3 input formats")
        log.info(" -- (hiflow3Scene.xml-file & vtkMesh.vtu-file & hiflow3BCdata.xml-file).")

        self.create_scenes()

        log.info("Hiflow3 Scene Files: %s" % ', '.join(self.scenes))


    def execute(self):
        """Execute `run HiFlow3 Elasticity`

        """
        import msml.envconfig
        import os

        try:
            os.makedirs("SimResults")
        except:
            pass

        for scenefile in self.scenes:
            cmd = "%s %s" % (msml.envconfig.HIFLOW_EXECUTABLE, scenefile)
            log.info("Executing HiFlow3: %s" % cmd)
            os.system(cmd)


    def create_scenes(self):
        """

        :param hf3xmlfile:
        :type hf3xmlfile: file
        :return:
        """
        self.scenes = list()

        for msmlObject in self._msml_file.scene:
            assert isinstance(msmlObject, SceneObject)
            meshFilename = self.get_value_from_memory(msmlObject.mesh)

            hf3_filename = '%s_%s_hf3.xml' % (self._msml_file.filename.namebase, msmlObject.id)

            # only take the first
            bc_filename = self.create_bcdata_files(msmlObject)[0]
            self.scenes.append(hf3_filename)


            class HF3MaterialModel(object):
                def __init__(self):
                    self.id, self.lamelambda, self.lamemu, self.gravity, self.density = [None] * 5

            hiflow_material_models = []
            # get and compute elasticity constants (i.e. material parameters):
            # therefore, iterate over "material" and "material's region"
            # (compare to: NewSofaExporter.createMaterialRegion().)
            for c, matregion in enumerate(msmlObject.material):
                hiflow_model = HF3MaterialModel()
                hiflow_material_models.append(hiflow_model)
                hiflow_model.id = c

                assert isinstance(matregion, MaterialRegion)

                indices = self.get_value_from_memory(matregion)

                # TODO: setup representation of hiflow_model.id for scenarios
                # where bounding boxes cannot bound material regions,
                # but where indices lists can define those material regions.
                # Cp. Mitral Valve example.
                # TODO: setup of better MSML-compatible / generic representation.
                # TODO: build example/test inp-file with correct material region id
                # (i.e.: hiflow_model.id for every point in indices).

                for material in matregion:
                    if 'linearElasticMaterial' == material.attributes['__tag__']:
                        E = float(material.attributes["youngModulus"])
                        NU = float(material.attributes["poissonRatio"])

                        hiflow_model.lamelambda = (E * NU) / ((1 + NU) * (1 - 2 * NU))
                        hiflow_model.lamemu = E / (2 * (1 + NU))
                        hiflow_model.gravity = -9.81

                    if 'mass' == material.attributes['__tag__']:
                        hiflow_model.density = material.attributes['massDensity']
                    
                    # Probably deprecated:
                    #if 'mvGeometry' == material.attributes['__tag__']:
                    #    hiflow_model.mvgeometry = material.attributes['mvGeometry']

            maxtimestep = self._msml_file.env.simulation[0].iterations

            if maxtimestep > 1:
                SolveInstationary = 1
            else:
                SolveInstationary = 0

            # print os.path.abspath(hf3_filename), "!!!!!!"
            
            hf3_MVRpipelineIndicator = self._msml_file.env.solver.hf3_chanceOfContactBoolean
            debug("hiflow3-exporter recognized hf3_MVRpipelineIndicator from _msml_file.env.solver.hf3_chanceOfContactBoolean.")
            
            # In case of MVR pipeline, we have hf3_MVRpipelineIndicator = '1' (i.e. true), 
            # and hence need to include information on the MV geometry in the hf3-scene,
            # elsewise, we do not need to include it.
            if hf3_MVRpipelineIndicator == "1":
                debug("hiflow3-exporter knows: hf3_MVRpipelineIndicator = 1, and thus fills MVR-part of scene-template, too.")
                # TODO: get this out here, and into MitralExporter...
                mvgeometry = self.get_value_from_memory(msmlObject.constraints[0].constraints[0], "mvGeometry")
                with open(hf3_filename, 'w') as fp:
                    #if 1 == self._msml_file.env.solver.hf3_chanceOfContactBoolean:
                    values = dict(hiflow_material_models=hiflow_material_models,
                                  # template arguments
                                  mvgeometryX=mvgeometry[0], # TODO: get this out here, and into MitralExporter
                                  mvgeometryY=mvgeometry[1], # TODO: get this out here, and into MitralExporter
                                  mvgeometryZ=mvgeometry[2], # TODO: get this out here, and into MitralExporter
                                  mvgeometryRadius=mvgeometry[3], # TODO: get this out here, and into MitralExporter
                                  meshfilename=meshFilename,
                                  bcdatafilename=bc_filename,
                                  solverPlatform=self._msml_file.env.solver.processingUnit,
                                  numParaProcCPU=self._msml_file.env.solver.numParallelProcessesOnCPU,
                                  hf3_chanceOfContact=self._msml_file.env.solver.hf3_chanceOfContactBoolean,
                                  SolveInstationary=SolveInstationary,
                                  DeltaT=self._msml_file.env.simulation[0].dt,
                                  maxtimestep=maxtimestep,
                                  linsolver=self._msml_file.env.solver.linearSolver,
                                  precond=self._msml_file.env.solver.preconditioner,
                                  timeIntegrationMethod=self._msml_file.env.solver.timeIntegration,
                                  RayleighRatioMass=self._msml_file.env.solver.dampingRayleighRatioMass,
                                  RayleighRatioStiffness=self._msml_file.env.solver.dampingRayleighRatioStiffness
                                  #
                                  # TODO: include mvGeometryAnalytics-Info (computed in MSML pipeline)  # TODO: get this out here, and into MitralExporter
                                  # at this point of the specific mitral-hiflow3-exporter.
                                  # therefore call mvGeometryAnalyzer-script from HiFlow3-exporter!!!
                                  #
                                  # Note: in future there may be more arguments, such as RefinementLevels, lin/quadElements, ...
                                  # The currently chosen sets of flexible and fixed parameters in HiFlow3Scene.xml-files represent a maximally general optimal setting.
                                  )

                    values.update(self.hf3_parameters)
                    #
                    content = SCENE_TEMPLATE.render(**values)

                    fp.write(content)

            else:
                debug("hiflow3-exporter knows: hf3_MVRpipelineIndicator = 0, and thus does not fill MVR-part of scene-template.")
                with open(hf3_filename, 'w') as fp:
                    values = dict(hiflow_material_models=hiflow_material_models,
                                  # template arguments
                                  meshfilename=meshFilename,
                                  bcdatafilename=bc_filename,
                                  solverPlatform=self._msml_file.env.solver.processingUnit,
                                  numParaProcCPU=self._msml_file.env.solver.numParallelProcessesOnCPU,
                                  hf3_chanceOfContact=self._msml_file.env.solver.hf3_chanceOfContactBoolean,
                                  SolveInstationary=SolveInstationary,
                                  DeltaT=self._msml_file.env.simulation[0].dt,
                                  maxtimestep=maxtimestep,
                                  linsolver=self._msml_file.env.solver.linearSolver,
                                  precond=self._msml_file.env.solver.preconditioner,
                                  timeIntegrationMethod=self._msml_file.env.solver.timeIntegration,
                                  RayleighRatioMass=self._msml_file.env.solver.dampingRayleighRatioMass,
                                  RayleighRatioStiffness=self._msml_file.env.solver.dampingRayleighRatioStiffness
                                  #
                                  # Note: in future there may be more arguments, such as RefinementLevels, lin/quadElements, ...
                                  # The currently chosen sets of flexible and fixed parameters in HiFlow3Scene.xml-files represent a maximally general optimal setting.
                                  )

                    values.update(self.hf3_parameters)
                    #
                    content = SCENE_TEMPLATE.render(**values)

                    fp.write(content)


    def create_bcdata_files(self, obj):
        """creates all bcdata files for all declared steps in `msml/env/simulation`

        :param obj: scene object
        :type obj: msml.model.base.SceneObject
        :return:
        """

        def create():
            for step in self._msml_file.env.simulation:
                filename = '%s_%s_%s.bc.xml' % (self._msml_file.filename.namebase, obj.id, step.name)
                data = self.create_bcdata(obj, step.name)
                # TODO: add priority of mvrBCdataProducer.py at this point in special mitral-hiflow-Exporter.
                # TODO: then call BCdata_for_Hf3Sim_Producer() and BCdata_for_Hf3Sim_Extender().
                content = BCDATA_TEMPLATE.render(data=data)
                with open(filename, 'w') as h:
                    h.write(content)
                yield filename

        return list(create())


    def create_bcdata(self, obj, step):
        """
        :param obj:
        :type obj: msml.model.base.SceneObject
        :type step: msml.model.base.MSMLEnvironment.Simulation.Step

        :return: a object of BcData
        :rtype: BcData
        """
        bcdata = BcData()

        # find the constraints for the given step
        for cs in obj.constraints:
            if cs.for_step == step or cs.for_step == "${%s}" % step:
                break
            else:
                cs = None

            if cs is None:  # nothing to do here
                log.warn("No constraint region found for step %s" % step)
                return bcdata

        mesh_name = self.get_value_from_memory(obj.mesh)

        for constraint in cs.constraints:
            if constraint.tag == "displacedPoints":
                disp_vector = self.get_value_from_memory(constraint, 'displacements')
                points = self.get_value_from_memory(constraint, 'points')
                count = len(points) / 3
                bcdata.dc.append(count, points, disp_vector)
            else:
                indices = self.get_value_from_memory(constraint, "indices")
                points = msml.ext.misc.PositionFromIndices(mesh_name, tuple((map(int, indices))), 'points')
                count = len(points) / 3
                points_str = list_to_hf3(points)
                # TODO: adapt this for non-box-able indices/vertices/facets/cells.
                # Cp. Mitral Valve example.
                if constraint.tag == "fixedConstraint":
                    bcdata.fc.append(count, points, [0, 0, 0])
                elif constraint.tag == "displacementConstraint":
                    disp_vector = constraint.displacement.split(" ")
                    bcdata.dc.append(count, points, disp_vector)
                elif constraint.tag == "surfacePressure":  # TODO! - this will need to be adapted!
                    force_vector = constraint.pressure.split(" ")
                    bcdata.fp.append(count, points, force_vector)

        return bcdata


class HiflowMitral(HiFlow3Exporter):  # inherits from class HiFlow3Exporter, but newly defines create_scenes(), etc.
    """
    This class specifies the standard HiFlow3-Exporter for its use for Mitral Valve simulations.
    It therefore includes specific information on the geometry and simulation setup,
    which is retrieved during the preprocessing workflow/pipeline.
    """
    def __init__(self, msml_file):
        """
        :param msml_file:
        :type msml_file: MSMLFile
        """
        self.hf3_parameters = {}
        """a dictionary with parameters for the hf3 exporter with higher priority
        :type: dict
        """

        self.name = 'HiFlow3Exporter'
        self.initialize(
            msml_file=msml_file,
            #mesh_sort=('VTU', 'Mesh'), # needed in HiFlow3Exporter!
            mesh_sort=('INP', 'Mesh'), # needed in MitralExporter!
            features=HIFLOW_FEATURES,
        )
    
    
    def create_scenes(self):

        # TODO: include information from vtu2hf3inp_inc_MatIDs_Producer-Script (as part of the MSML workflow)
        # into the special MVR exporter, in order to thus compute Index-Sets, etc. here,
        # such that they are available for both the HiFlow3-Exporter and other Exporters, too.

        # list_of_matIDints, list_of_point_matIDints # TODO include this # TODO?!?!?!

        self.hf3_parameters = dict(
            hf3_chanceOfContact=True,
        )

        ## super function
        HiFlow3Exporter.create_scenes(self)

    def create_bcdata_files(self, obj):
        """
        creates all bcdata files for all declared steps in `msml/env/simulation`

        :param obj: scene object
        :type obj: msml.model.base.SceneObject
        :return:
        """

        # TODO: find the constraints for the given step
        # - use BCdataDBC-Producer to find displacement-constraints
        # (representing annuloplasty ring implantation)
        # - use BCdataNBC-Extender to find chordae-pull-force-constraints
        # (representing the pulling chordae during leaflets movement)
        #  #### TODO TODO TODO: include and adapt this here !!!

        def create():
            for step in self._msml_file.env.simulation:
                filename = '%s_%s_%s.bc.xml' % (self._msml_file.filename.namebase, obj.id, step.name)
                data = self.create_bcdata(obj, step.name)
                # TODO: add priority of mvrBCdataProducer.py here. # TODO.
                # call BCdata_for_Hf3Sim_Producer()
                # points, displacements # what?!             ????????????????
                # TODO: call BCdata_for_Hf3Sim_Extender()
                content = BCDATA_TEMPLATE.render(data=data)
                with open(filename, 'w') as h:
                    h.write(content)
                yield filename

        return list(create())


    def create_bcdata(self, obj, step):
        bcdata = BcData()
        
        for constraint in obj.constraints[0]:
            # there are no fixedDirichletBCs in the MVR scenario;
            bcdata.fc.append(0, [], [])
            # displacedPointsConstraint in the MVR scenario;
            if constraint.tag ==  "displacedPointsConstraint":
                points = self.get_value_from_memory(constraint, 'points')
                count = len(points) / 3
                disp_vector = self.get_value_from_memory(constraint, 'displacements')
                bcdata.dc.append(count, points, disp_vector)
            # pointwiseForceConstraint in the MVR scenario;
            if constraint.tag == "pointwiseForceConstraint":
                points = self.get_value_from_memory(constraint, 'points')
                count = len(points) / 3
                force_vector = self.get_value_from_memory(constraint, 'forces')
                bcdata.fp.append(count, points, force_vector)
            # bcdata for MVR scenario done;
        return bcdata


def count_vector(vec, count):
    assert len(vec) == 3
    vec = map(lambda x: "%0.15f" % float(x), vec)
    return ";".join(count * [",".join(vec)])


def list_to_hf3(seq):
    """transfers a seq of values into a string for hiflow3.
    :param seq: a sequence (iterable) of value (int, float, ...)
    :rtype: str
    
    >>> points = map(float, [1,2,3]*3)
    >>> list_to_hf3(points)
    "1.0,2.0,3.0;1.0,2.0,3.0;1.0,2.0,3.0"
    """
    from cStringIO import StringIO

    s = StringIO()

    for i, p in enumerate(seq, 1):
        s.write("%0.15f" % float(p))

        if i % 3 == 0 and i != 1:
            s.write(";")
        else:
            s.write(",")

    s = s.getvalue()[:-1]
    if len(seq) > 0: # in order to have empty BC-lists at least represented in HiFlow3-BCdata-file with numBCtype = 0;
        assert s.count(';') + 1 == len(seq) / 3
    return s

