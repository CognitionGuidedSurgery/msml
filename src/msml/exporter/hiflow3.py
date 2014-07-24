#-*- encoding: utf-8 -*-
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

from msml.model.base import *

__authors__ = 'Nicolai Schoch, Alexander Weigl <uiduw@student.kit.edu>'
__license__ = 'GPLv3'

import os
from .base import Exporter
from msml.model import *

import jinja2
from msml.exceptions import *

import msml.ext.misc

class MSMLHiFlow3ExporterWarning(MSMLWarning): pass


from ..log import report

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(path(__file__).dirname()))

SCENE_TEMPLATE = jinja_env.get_template("hiflow_scene.tpl.xml")
BCDATA_TEMPLATE = jinja_env.get_template("hiflow_bcdata.tpl.xml")

FixedConstraint = namedtuple("FixedConstraint", "nFDP fDPointsList fDisplacementsList")
DisplacementConstraint = namedtuple("DisplacementConstraint", "nDDP dDPointsList dDisplacementsList nFoPBCPoints")
ForceOrPressure = namedtuple("ForceOrPressure", "nFoPBCPoints FoPBCPointsList FoPBCVectorsList")
Entry = namedtuple("Entry", "mesh bcdata")


class HiFlow3Exporter(Exporter):
    """Exporter for `hiflow3 <http://hiflow3.org>`_

    .. comment: Information here.

    """

    def __init__(self, msml_file):
        """
        :param msml_file:
        :type msml_file: MSMLFile
        """

        self.name = 'HiFlow3Exporter'
        Exporter.__init__(self, msml_file)
        self.mesh_sort = ('VTU', 'Mesh') # i want a VTU file as input
        self.gather_inputs()

    def render(self):
        """
        Builds the File (XML e.g) for the external tool
        """

        filename = self._msml_file.filename.namebase

        report("Converting to HiFlow3 input formats (hiflow3Scene.xml-file & vtkMesh.vtu-file & BCdata.xml-file).", 'I',
               801)
        self.create_scenes()
        report("Hiflow3 Scene Files: \n\t %s" % '\n\t'.join(self.scenes), 'I', 802)


    def execute(self):
        """Execute `runHiFlow3`

        """
        cmd = "runHiFlow3 %s" % ' '.join(self.scenes)
        report("Executing HiFlow3: %s" % cmd, 'I', 803)
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
            meshFilename = self.evaluate_node(msmlObject.mesh.mesh)

            hf3_filename = '%s_%s_hf3.xml' % (self._msml_file.filename.namebase, msmlObject.id)
            bc_filename = self.create_bcdata(msmlObject)

            self.scenes.append(hf3_filename)


            class HF3MaterialModel(object):
                def __init__(self):
                    self.id, self.lamelambda, self.lamemu, self.gravity, self.density = [None]*5

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

                        E =  float(material.attributes["youngModulus"])
                        NU = float(material.attributes["poissonRatio"])

                        hiflow_model.lamelambda = (E * NU) / ((1 + NU) * (1 - 2 * NU))
                        hiflow_model.lamemu = E / (2 * (1 + NU))
                        hiflow_model.gravity =  -9.81

                    if 'mass' == material.attributes['__tag__']:
                        hiflow_model.density =  material.attributes['massDensity']


            maxtimestep = self._msml_file.env.simulation[0].iterations

            if maxtimestep > 1:
                SolveInstationary = 1
            else:
                SolveInstationary = 0

            #print os.path.abspath(hf3_filename), "!!!!!!"

            with open(hf3_filename, 'w') as fp:
                content = SCENE_TEMPLATE.render(
                    hiflow_material_models = hiflow_material_models,

                    # template arguments
                    meshfilename=meshFilename,
                    bcdatafilename=bc_filename,
                    SolveInstationary=SolveInstationary,
                    DeltaT=self._msml_file.env.simulation[0].dt,
                    maxtimestep=maxtimestep,
                    linsolver=self._msml_file.env.solver.linearSolver,
                    precond=self._msml_file.env.solver.preconditioner
                    # in future, there may be some more...
                    # Note: alternative parsing by means of using *.get("...") possible?!
                )
                fp.write(content)


    # define function to create HiFlow3-compatible BCdata-input-File:
    def create_bcdata(self, obj):
        """
        :param obj:
        :type obj: msml.model.base.SceneObject
        :return:
        """

        fc = None
        fp = None
        dc = None

        mesh_name = self.evaluate_node(obj.mesh.mesh)


        for cs in obj.constraints:
            for constraint in cs.constraints:
                indices = self.evaluate_node(constraint.indices)
                points = msml.ext.misc.positionFromIndices(mesh_name, list(indices), 'points') # positionFromIndices() does not yet work?!
                #points = [1,2,3] # TestOutput
                #     # TODO: list of DPoints
                #     pointsInBoxROIVector=pointsInBoxROIVector,
                #     # TODO: transform MSML-ROIs/Boxes into (lists of) point coordinates:
                #     #TODO: use "getPointsInBoxROI()" (-> compare: abaqusnew.py, lines 129ff) and "extractPointPositions()".

                count = len(indices) / 3
                points_str = list_to_hf3(points)

                assert isinstance(constraint, ObjectElement)
                if constraint.tag == "fixedConstraint":
                    fdis = ';'.join(["0.0, 0.0, 0.0"] * count)
                    fc = FixedConstraint(count, points_str, fdis)
                elif constraint.tag == "displacementConstraint":
                    #get displacment "a b c" = split => ["a", "b", "c"] = expand to amount points => join
                    displacement = ';'.join(count * ','.join(list(constraint.displacement.split(" "))))
                                                             # [1 2 3]
                                                    # '1,2,3'
                                   # 1,2,3;1,2,3;...
                    dc = DisplacementConstraint(count, points_str, displacement)
                elif constraint.tag == "pressureConstraint":
                    force_vector = constraint.pressureValue
                    fp = ForceOrPressure(count, points,
                        ';'.join(','.join(force_vector) * count))

        filename = '%s_%s_bc.xml' % (self._msml_file.filename.namebase, obj.id)
        with open(filename, 'w') as h:
            content = BCDATA_TEMPLATE.render(fp=fp, fc=fc, dc=dc)
            h.write(content)
        return filename

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

    for i,p in enumerate(seq, 1):
        s.write(str(p))
        if i%3 == 0 and i != 1:
            s.write(";")
        else:
            s.write(",")

    s =  s.getvalue()
    return s[:-1]
