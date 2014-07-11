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

            # # get and compute elasticity constants (i.e. material parameters):
            # # therefore, iterate over "material" and "material's region"
            # # (compare to: NewSofaExporter.createMaterialRegion().)
            # youngs = {}
            # poissons = {}
            # density = {}
            #
            # for matregion in msmlObject.material:
            # assert isinstance(matregion, MaterialRegion)
            #
            # indexGroupNode = matregion.get_indices()  # needed for two or more materialregions only?!
            #
            # assert isinstance(indexGroupNode, ObjectElement)  # needed for two or more materialregions only?!
            #
            # indices_key = indexGroupNode.attributes["indices"]  # needed for two or more materialregions only?!
            #     indices_vec = self.evaluate_node(indices_key)  # needed for two or more materialregions only?!
            #     indices = '%s' % ', '.join(map(str, indices_vec))  # needed for two or more materialregions only?!
            #
            #     indices_int = [int(i) for i in indices.split(",")]  # needed for two or more materialregions only?!
            #
            #     # Get all materials
            #     for material in matregion:
            #         assert isinstance(material, ObjectElement)
            #
            #         currentMaterialType = material.attributes['__tag__']  # what?!
            #         if currentMaterialType == "indexgroup":  # what?!
            #             continue
            #
            #         if currentMaterialType == "linearElastic":
            #             currentYoungs = material.attributes["youngModulus"]
            #             currentPoissons = material.attributes["poissonRatio"]
            #             for i in indices_int:  # needed for two or more materialregions only?! #TODO Performance (maybe generator should be make more sense)
            #                 youngs[i] = currentYoungs  # needed for two or more materialregions only?!
            #                 poissons[i] = currentPoissons  # needed for two or more materialregions only?!
            #         elif currentMaterialType == "mass":
            #             currentDensity = material.attributes["density"]
            #             for i in indices_int:  # needed for two or more materialregions only?!
            #                 density[i] = currentDensity  # needed for two or more materialregions only?!
            #         else:
            #             warn(MSMLHiFlow3ExporterWarning, "Material Type not supported %s" % currentMaterialType)
            #
            #             # now we have: youngs[], poissons[], density[].
            #             # since HiFlow3 is currently dealing with one material only, the for-loop is to be ended here.

            # the thus obtained linearElasticityConstants for the (imposed) one given material are:
            #NU = poissons[0]  # by definition: set NU = poissons[0], so HiFlow3 can handle without weak material boundaries.
            #E = youngs[0]  # by definition: set E = youngs[0], so HiFlow3 can handle without weak material boundaries.
            # and hence


            class HF3MaterialModel(object):
                def __init__(self):
                    self.id, self.l, self.mu, self.g, self.d = [None]*5

            hiflow_material_models = []
            for c, matregion in enumerate(msmlObject.material):
                hiflow_model = HF3MaterialModel()
                hiflow_material_models.append(hiflow_model)
                hiflow_model.id = c

                assert isinstance(matregion, MaterialRegion)

                indices = self.get_value_from_memory(matregion)

                # built inp file with right material region id (hiflow_model.id for every point in indices) NICO!

                for material in matregion:
                    if 'linearElasticMaterial' == material.attributes['__tag__']:

                        E =  float(material.attributes["youngModulus"])
                        NU = float(material.attributes["poissonRatio"])

                        hiflow_model.l = (E * NU) / ((1 + NU) * (1 - 2 * NU))
                        hiflow_model.mu = E / (2 * (1 + NU))
                        hiflow_model.g =   9.81 #gravity

                    if 'mass' == material.attributes['__tag__']:
                        hiflow_model.d =  material.attributes['massDensity'] # density


            maxtimestep = self._msml_file.env.simulation[0].iterations

            if maxtimestep > 1:
                SolveInstationary = 1
            else:
                SolveInstationary = 0

            #debug
            #density = [0]
            #lamemu = 42
            #lamelambda = 42

            print os.path.abspath(hf3_filename), "!!!!!!"

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
                    # in future, there may be some more?! # alternatively parsing by means of using *.get("...") possible?!
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
                points = msml.ext.misc.positionFromIndices(mesh_name, list(indices), 'points')
                #points = [1,2,3]


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
                    force_vector = constraint.pressureValue # assume [5 3 3] kg / m * s^2
                    fp = ForceOrPressure(count, points,
                        ';'.join(','.join(force_vector) * count))

        filename = '%s_%s_bc.xml' % (self._msml_file.filename.namebase, obj.id)
        with open(filename, 'w') as h:
            content = BCDATA_TEMPLATE.render(fp=fp, fc=fc, dc=dc)
            h.write(content)
        return filename


def list_to_hf3(seq):
    from cStringIO import StringIO

    s = StringIO()

    for i,p in seq:
        s.write(p)
        if i%3 == 0 and i != 0:
            s.write(";")
        else:
            s.write(",")

    s = str(s)
    return s[:-1]





        #
        # for roiBoxes in msmlObject.workflow:  # TODO: stimmt das so?
        # assert isinstance(roiBoxes, boxROI)
        #
        # indicesVector = computeIndicesFromBoxROI(string
        # meshFilename, vector < double > roiBoxes, string
        # type)  # hier müssen die type-definitions wieder raus...
        #     # in "IndexRegionOperators.cpp"
        #     # TODO: what is type "tetrahedron"?
        #     pointsInBoxROIVector = extractPointPositions(std::vector < int > indicesVector, const
        #     char * meshFilename)
        #     # in "MiscMeshOperators.cpp"
        #     numfDpoints = len(pointsInBoxROIVector) / 3
        #     zeroDisplacementVectors = ''
        #     for it in range(1, numfDpoints):
        #         zeroDisplacementVectors.append('0,0,0;')
        #     zeroDisplacementVectors = zeroDisplacementVectors[0:-1]
        #
        # # writing boundary conditions
        # bcxmlfile.write(tpl.render(
        #     # template arguments
        #     # ---
        #     # TODO: Number of fDpoints
        #     numfDpoints=numfDpoints,
        #
        #     # TODO: list of DPoints
        #     pointsInBoxROIVector=pointsInBoxROIVector,
        #     # TODO: transform MSML-ROIs/Boxes into (lists of) point coordinates:
        #     #TODO: use "getPointsInBoxROI()" (-> compare: abaqusnew.py, lines 129ff) and "extractPointPositions()".
        #
        #     #TODO: list of zeroDisplacementVectors
        #     zeroDisplacementVectors=zeroDisplacementVectors,
        #
        #     #---
        #     #TODO: Number of dDpoints
        #
        #     #TODO: list of dDPoints getPointsInBoxROI()
        #
        #     #TODO: list of displacementVectors getVectorsInBoxROI()
        #
        #     #---
        #     #TODO: Number of ForceOrPressureBCPoints
        #
        #     #TODO: list of ForceOrPressureBCPoints getPointsInBoxROI()
        #
        #     #TODO: list of ForceOrPressureVectors
        #
        #     #---
        # ))
        #
