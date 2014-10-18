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

__author__ = 'Alexander Weigl'

from ..model import *
from ..exceptions import *

import msml.sortdef

from .. import log

from .features import get_needed_features
class ExporterOutputVariable(MSMLVariable):
    pass


class Exporter(object):
    def __init__(self, msml_file):
        """
        Args:
          executer (Executer)


        """
        assert isinstance(msml_file, MSMLFile)

        self._datamodel = None
        self._msml_file = msml_file
        self.name = 'base'
        self._output_types_for_tags = {}

        self.id = "__exporter__"

        self.mesh_sort = ['VTK', 'Mesh']
        """The physical and logical sort of the input mesh"""

        self._output = {}
        """Output slots
        :type dict[str, Slot]"""

        self._input = {}
        """Input slots
        :type dict[str, Slot]"""

        self._attributes = {}
        """Attribute values for input slots
        :type dict[str,str]"""

        self.gather_output()
        self.gather_inputs()

        self.arguments = {}
        """stores the References to the input values
        :type dict[str,Reference]
        :see Exporter.link
        """

        self._features = set()
        """Set of supported features from this exporter

        :see :py:meth:`Exporter.match_features`
        :type set[str]
        """

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        self._features = value


    def lookup(self, ref, outarg):
        assert isinstance(ref, Reference)
        obj = ref.task
        slot = ref.slot

        for scene_object in self._msml_file.scene:
            assert isinstance(scene_object, SceneObject)
            for o in scene_object.output:
                assert isinstance(o, ObjectElement)
                if o.id == obj:
                    # TODO define type/Format of this output
                    return self, ExporterOutputVariable(obj, physical=msml.sortdef.VTK)


    def gather_output(self):
        """finds all variables that is provided by the exporter
        :param msmlfile: msml.model.base.MSMLFile
        :return: list of MSMLVariables
        """

        self._output = {}
        for obj in self._msml_file.scene:
            for out in obj.output:
                tag = out.attributes['__tag__']
                id = out.attributes['id']

                fmt = object
                typ = object

                if id in self._output_types_for_tags:
                    typ, fmt = self._output_types_for_tags[id]

                v = ExporterOutputVariable(id, fmt, typ)
                self._output[id] = v

    def gather_inputs(self):
        '''find all references needed by this exporter from workflow
        :param msml_file: msml.model.base.MSMLFile
        :return:
        '''


        def register_object_sets():
            for ig in (scene_obj.sets.nodes + scene_obj.sets.elements + scene_obj.sets.surfaces):
                name = self.get_input_set_name(ig)
                self._input[name] = Slot(name, 'vector.int', 'Indices', parent=self)
                self._attributes[name] = parse_attribute_value(ig.indices)


        def register_material():
            for mr in scene_obj.material:
                ind = mr.indices
                name = self.get_input_material_name(mr)
                self._input[name] = Slot(name, 'vector.int', parent=self)
                self._attributes[name] = parse_attribute_value(ind)

                for material in mr:
                    assert isinstance(material, ObjectElement)
                    for para in material.meta.parameters.values():
                        assert isinstance(para, Slot)
                        name = self.get_input_objectelement_name(material, para)
                        self._input[name] = Slot(name, para.physical_type, parent=self)
                        self._attributes[name] = parse_attribute_value(material.attributes[para.name])
                        log.debug("register %s as input value of material", name)

        def register_constraints():
            for cs in scene_obj.constraints:
                for const in cs.constraints:
                    assert isinstance(const, ObjectElement)
                    for para in const.meta.parameters.values():
                        assert isinstance(para, Slot)

                        try:
                            value = const.attributes[para.name]
                        except KeyError:
                            raise MSMLError(
                                "parameter %s of constraint %s has not proper value" % (para.name, const.id))

                        name = self.get_input_objectelement_name(const, para)
                        self._input[name] = Slot(name, para.physical_type, parent=self)
                        self._attributes[name] = parse_attribute_value(value)
                        log.debug("register %s as input value of material", name)

        for scene_obj in self._msml_file.scene:
            assert isinstance(scene_obj, SceneObject)

            self._input['mesh'] = Slot('mesh', self.mesh_sort[0], self.mesh_sort[1],
                                       required=True, parent=self)

            self._attributes['mesh'] = parse_attribute_value(scene_obj.mesh.mesh)

            register_object_sets()
            register_material()
            register_constraints()


    def get_input_objectelement_name(self, objectelement, parameter):
        """generates the slot name for an objectelement

        :param objectelement: ObjectElement
        :type objectelement: msml.model.base.ObjectElement
        :param parameter: the slot of the given object element
        :type parameter: msml.model.alphabet.Slot
        :return:
        """
        if hasattr(parameter, "name"):
            n = parameter.name
        else:
            n = parameter
        return "%s_%s" % (objectelement.id, n)

    def get_input_mesh_name(self, mesh):
        """ generates the name for an output request within an object declaration
        :param mesh:
        :type msml.model.base.Mesh
        :return:
        :rtype   str
        """
        return "mesh"

    def get_input_set_name(self, setelement):
        """the input slot name for the given setelement
        :param setelement:
        :type setelement: IndexGroup
        :return:
        :type str
        """
        return 'sets_%s' % setelement.id

    def get_input_material_name(self, region):
        """
        :param region:
        :type region: MaterialRegion
        :rtype str
        :return: a name for the indices input slot for the given material region
        """
        return 'mr_%s_indexgroup' % region.id

    def get_input_constraint_name(self, const):
        """generates the input for a given :py:class:`OAConstraint`
        :param const:
        :type msml.model.OAConstraint
        :return:
        """
        return "constraint_%s" % const.id

    def link(self):
        from  msml.model.base import link_algorithm

        slots = dict(self._input)
        self.arguments = link_algorithm(self._msml_file, self._attributes, self, slots)

    def _match_features(self):

        needed = get_needed_features(self._msml_file)
        match = needed <= self.features

        if match:
            log.info("every features is supported by current exporter")
        else:
            log.error("some features are not supported by exporter")
            log.error("-- msml_file: %s", needed)
            log.error("-- supported: %s", self.features)
            log.error("-- not matched: %s", needed - self.features)

        return match

    def init_exec(self, executer):
        """
        initialization by the executer, sets memory and executor member
        :param executer: msml.run.Executer
        :return:
        """
        self._executer = executer
        self._memory = self._executer._memory
        """:type msml.run.memory.Memory"""



    def render(self):
        """
        Builds the File (XML e.g) for the external tool
        """
        pass

    def execute(self):
        "should execute the external tool and set the memory"
        pass

    def evaluate_node(self, expression):
        if ((expression[0:2] == '${') & (expression[-1] == '}') ):
            # in this case, get value from workflow
            data = self._memory._internal
            for seg in expression[2:-1].split("."):
                data = data[seg]

            return data
        else:
            return expression

            # every reference should be full, commented out from weigl
            # if isinstance(resultNode, basestring):
            # resultExpression = resultNode
            # else:
            # resultExpression = resultNode[resultNode.keys()[0]]

    def get_value_from_memory(self, reference, parameter=None):
        """

        :param reference:
        :return:
        """

        if isinstance(reference, str):
            return self.get_value_from_memory(self.arguments[reference])
        elif isinstance(reference, Mesh):
            return self.get_value_from_memory(self.get_input_mesh_name(reference))
        elif isinstance(reference, MaterialRegion):
            return self.get_value_from_memory(self.get_input_material_name(reference))
        elif isinstance(reference, IndexGroup):
            return self.get_value_from_memory(self.get_input_set_name(reference))
        elif isinstance(reference, ObjectElement):
            return self.get_value_from_memory(self.get_input_objectelement_name(reference, parameter))
        elif isinstance(reference, Reference):
            return self._memory.lookup(reference)
        else:
            raise MSMLException("no suitable reference was given (%s)" % reference)

    @property
    def datamodel(self):
        if not self._datamodel:
            self._datamodel = self.generate_data_model()
        return self._datamodel

    def generate_data_model(self):
        def _scene(sceneobject):
            """
            :param scene: an object from the scene
            :type scene: msml.model.base.SceneObject
            :return: a scene object with references solved
            """
            ns = SceneObject(
                sceneobject.id,
                _mesh(sceneobject.mesh),
                _scene_sets(sceneobject.sets),
                map(_region, sceneobject.material),
                map(_constraint, sceneobject.constraints)
            )
            return ns

        def _scene_sets(sets):
            assert isinstance(sets, SceneObjectSets)

            def _resolve(indexgroup):
                assert isinstance(indexgroup, IndexGroup)
                ig = IndexGroup(indexgroup.id, self.get_value_from_memory(indexgroup))
                return ig

            _map_resolve = lambda seq: map(_resolve, seq)

            ns = SceneObjectSets(
                _map_resolve(sets.elements),
                _map_resolve(sets.nodes),
                _map_resolve(sets.surfaces),
            )
            return ns

        def _mesh(mesh):
            assert isinstance(mesh, Mesh)
            return Mesh(mesh.id, mesh.id, self.get_value_from_memory(mesh))

        def _object_element(objectelement):
            assert isinstance(objectelement, ObjectElement)

            attrib = objectelement.attributes
            objectelement.meta
            values = {k: self.get_value_from_memory(objectelement, k) for k in objectelement.meta.parameters}

            return ObjectElement(values, objectelement.meta)


        def _region(materialregion):
            assert isinstance(materialregion, MaterialRegion)

            return MaterialRegion(materialregion.id, self.get_value_from_memory(materialregion),
                                  map(_object_element, materialregion))


        def _constraint(objectconstraints):
            assert isinstance(objectconstraints, ObjectConstraints)
            oc = ObjectConstraints(objectconstraints.name, objectconstraints.for_step)
            oc.constraints = map(_object_element, objectconstraints.constraints)
            return oc

        return map(_scene, self._msml_file.scene)


class XMLExporter(Exporter): pass
