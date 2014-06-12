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

import msml.sortdef

import warnings

from ..model import *


class ExporterOutputVariable(MSMLVariable):
    pass


class Exporter(object):
    def __init__(self, msml_file):
        """
        Args:
          executer (Executer)


        """
        assert isinstance(msml_file, MSMLFile)
        self._msml_file = msml_file
        self.name = 'base'
        self._output_types_for_tags = {}

        self.mesh_sort = ['VTK', 'Mesh']
        """The physical and logical sort of the input mesh"""

        self._output = {}
        """Output slots
        :type dict[str, Slot]"""

        self._input  = {}
        """Input slots
        :type dict[str, Slot]"""

        self.gather_output()
        self.gather_inputs()

        self.arguments = {}
        """stores the References to the input values
        :type dict[str,Reference]
        :see Exporter.link
        """


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

        for scene_obj in self._msml_file.scene:
            assert isinstance(scene_obj, SceneObject)

            self._input['mesh'] = Slot('mesh', self.mesh_sort[0], self.mesh_sort[1], required=True,
                                       default=parse_attribute_value(scene_obj.mesh.mesh), parent=self)

            for ig in (scene_obj.sets.nodes + scene_obj.sets.elements + scene_obj.sets.surfaces):
                name = self.get_input_set_name(ig)
                self._input[name] = Slot(name, 'vector.int', 'Indices',
                        default=parse_attribute_value(ig.indices), parent=self)

            for mr in scene_obj.material:
                ind = mr.indices
                name = self.get_input_material_name(mr)
                self._input[name] = Slot('mr_%s_indexgroup' % mr.id, 'vector.int',
                                                               default=parse_attribute_value(ind), parent=self)

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

    def link(self):
        self.arguments = {}
        for key, slot in self._input.iteritems():
            value = slot.default
            if isinstance(value, Reference):
                opposite = self._msml_file.lookup(value)
                if opposite:
                    outtask, outarg = opposite
                    value.link_from_task(outtask, outarg)
                    try:
                        value.link_to_task(self, slot)
                    except KeyError, e:
                        f = str(var)
                        t = str(self.name)
                        i = key
                        op = str(self.operator)
                        inputs = ",".join(map(str, self.operator.acceptable_names()))

                        raise BindError(
                            "you try to connect {start} to Task '{target}' but slot {inputname} is unknown for {operator} (Inputs {inputs})".format(
                                start=f, target=t, inputname=i, operator=op, inputs=inputs
                            ))
                    self.arguments[key] = value
                else:
                    warnings.warn("Lookup after %s does not succeeded" % value)
            elif isinstance(value, Constant):
                var = MSMLVariable(random_var_name(), value=value.value);
                self._msml_file.add_variable(var)
                ref = Reference(var.name, None)
                outtask, outarg = self._msml_file.lookup(ref)
                ref.link_from_task(outtask, outarg)

                try:
                    ref.link_to_task(self, self._input[key][1])
                except ImportError, e:
                    f = str(var)
                    t = str(self.name)
                    i = key
                    op = str(self.operator)
                    inputs = ",".join(map(str, self.operator.acceptable_names()))

                    raise BindError(
                        "you try to connect {start} to Task '{target}' but slot {inputname} is unknown for {operator} (Inputs {inputs})".format(
                            start=f, target=t, inputname=i, operator=op, inputs=inputs
                        ))

                self.arguments[key] = ref
            else:
                raise MSMLError("no case %s : %s " % (key, str(type(value))))


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
        pass


    def execute(self):
        "should execute the external tool and set the memory"
        pass

    def evaluate_node(self, expression):
        if ((expression[0:2] == '${') & (expression[-1] == '}') ):
            # in this case, get value from workflow
            resultNode = self._memory._internal[expression[2:-1]]
            if isinstance(resultNode, basestring):
                resultExpression = resultNode
            else:
                resultExpression = resultNode[resultNode.keys()[0]]
        else:
            resultExpression = expression

        return resultExpression


class XMLExporter(Exporter): pass
