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

import os

import jinja2

from msml.model import *
from msml.exceptions import *
import msml.ext.misc


class MSMLHiFlow3ExporterWarning(MSMLWarning): pass

from .. import log

from path import path
from collections import namedtuple
from .base import Exporter

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(path(__file__).dirname()))

SCENE_TEMPLATE = jinja_env.get_template("hiflow_scene.tpl.xml")
BCDATA_TEMPLATE = jinja_env.get_template("hiflow_bcdata.tpl.xml")


class BcData(object):
    def __init__(self):
        self.fc = BcDataEntry()
        self.dc = BcDataEntry()
        self.fp = BcDataEntry()


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

        self.name = 'HiFlow3Exporter'
        Exporter.__init__(self, msml_file)
        self.mesh_sort = ('VTU', 'Mesh')  # i want a VTU file as input
        self.gather_inputs()

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
        """Execute `runHiFlow3`

        """
        cmd = "runHiFlow3 %s" % ' '.join(self.scenes)
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

                # TODO: (Nico, 2014-07-11)
                # build inp-file with correct material region id
                # (i.e.: hiflow_model.id for every point in indices)

                for material in matregion:
                    if 'linearElasticMaterial' == material.attributes['__tag__']:
                        E = float(material.attributes["youngModulus"])
                        NU = float(material.attributes["poissonRatio"])

                        hiflow_model.lamelambda = (E * NU) / ((1 + NU) * (1 - 2 * NU))
                        hiflow_model.lamemu = E / (2 * (1 + NU))
                        hiflow_model.gravity = -9.81

                    if 'mass' == material.attributes['__tag__']:
                        hiflow_model.density = material.attributes['massDensity']

            maxtimestep = self._msml_file.env.simulation[0].iterations

            if maxtimestep > 1:
                SolveInstationary = 1
            else:
                SolveInstationary = 0

            #print os.path.abspath(hf3_filename), "!!!!!!"

            with open(hf3_filename, 'w') as fp:
                content = SCENE_TEMPLATE.render(
                    hiflow_material_models=hiflow_material_models,
                    # template arguments
                    meshfilename=meshFilename,
                    bcdatafilename=bc_filename,
                    numParaProcCPU=self._msml_file.env.solver.numParallelProcessesOnCPU,
                    SolveInstationary=SolveInstationary,
                    DeltaT=self._msml_file.env.simulation[0].dt,
                    maxtimestep=maxtimestep,
                    linsolver=self._msml_file.env.solver.linearSolver,
                    precond=self._msml_file.env.solver.preconditioner,
                    timeIntegrationMethod=self._msml_file.env.solver.timeIntegration,
                    RayleighRatioMass=self._msml_file.env.solver.dampingRayleighRatioMass,
                    RayleighRatioStiffness=self._msml_file.env.solver.dampingRayleighRatioStiffness
                    # Note: in future, there may be some more, such as CPU/GPU, RefinementLevels, lin/quadElements, ...
                    # So far, the remaining parameters in HiFlow3Scene.xml-files are chosen to represent a general optimal setting.
                )
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
                content = BCDATA_TEMPLATE.render(data = data)
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

        if cs is None: # nothing to do here
            log.warn("No constraint region found for step %s" % step)
            return bcdata

        mesh_name = self.get_value_from_memory(obj.mesh)

        for constraint in cs.constraints:
            indices = self.get_value_from_memory(constraint, "indices")
            points = msml.ext.misc.positionFromIndices(mesh_name, indices, 'points')
            count = len(points) / 3
            points_str = list_to_hf3(points)

            if constraint.tag == "fixedConstraint":
                bcdata.fc.append(count, points, [0, 0, 0])
            elif constraint.tag == "displacementConstraint":
                disp_vector = constraint.displacement.split(" ")
                bcdata.dc.append(count, points, disp_vector)
            elif constraint.tag == "pressureConstraint":
                force_vector = constraint.pressure.split(" ")
                bcdata.fp.append(count, points, force_vector)

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
    assert s.count(';') + 1 == len(seq) / 3
    return s
