__author__ = 'Alexander Weigl'

import warnings

import lxml.etree as ET

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
        self.name = 'exporter'
        self._output_types_for_tags = {}

        self._output = {}
        self._input = {}

        self.gather_output()
        self.gather_inputs()


    def lookup(self, ref, outarg):
        pass


    def gather_output(self):
        """
        finds all variables that is provided by the exporter
        :param msmlfile: msml.model.base.MSMLFile
        :return: list of MSMLVariables
        """

        self._output = {}
        for obj in self._msml_file.scene:
            for out in obj.output:
                tag = out.attributes['__tag__']
                id = out.attributes['id']

                fmt = None
                typ = "*"

                if id in self._output_types_for_tags:
                    typ, fmt = self._output_types_for_tags[id]

                v = ExporterOutputVariable(id, fmt, typ)
                self._output[id] = v

    def gather_inputs(self):
        '''
        find all references needed by this exporter from workflow
        :param msml_file: msml.model.base.MSMLFile
        :return:
        '''

        indexgroups_arg = Argument("indices", 'indices')

        for scene_obj in self._msml_file.scene:
            assert isinstance(scene_obj, SceneObject)

            self._input['mesh'] = (parse_attribute_value(scene_obj.mesh.mesh), Argument('mesh', 'mesh'))

            for i, ig in enumerate(scene_obj.sets.nodes +
                    scene_obj.sets.elements +
                    scene_obj.sets.surfaces):
                self._input['sets_%d' % i] = (parse_attribute_value(ig.indices), indexgroups_arg)

            for mr in scene_obj.material:
                ind = mr.get_indices().attributes['indices']
                self._input['mr_%s_indexgroup' % mr.id] = (parse_attribute_value(ind), indexgroups_arg)


    def link(self):
        self.arguments = {}
        for key, (value, arginfo) in self._input.iteritems():
            if isinstance(value, Reference):
                a = self._msml_file.lookup(value)
                if a:
                    outtask, outarg = a
                    value.link_from_task(outtask, outarg)
                    try:
                        value.link_to_task(self, arginfo)
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
                    ref.link_to_task(self, self._input[key])
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
                raise MSMLError("no case %s : %s " % (value, str(type(value))))


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

    def evaluate_node(self,expression):
        if((expression[0:2]=='${')&(expression[-1]=='}') ):
            #in this case, get value from workflow
            resultNode = self._memory._internal[expression[2:-1]]
            if isinstance(resultNode, basestring):
                resultExpression = resultNode
            else:
                resultExpression = resultNode[resultNode.keys()[0]]
        else:
            resultExpression = expression

        return resultExpression


class XMLExporter(Exporter):
    def render(self):
        scene = self._mfile.scene

def dict_to_xml(d, parent_node=None, tag_name="__tag__"):
    if isinstance(d, dict):
        tag = d[tag_name]
        del d[tag_name]

        if parent_node is not None:
            element = ET.SubElement(parent_node, tag)
        else:
            element = ET.Element(tag)

        for k, v in d.items():
            if isinstance(v, list) and isinstance(v[0], dict):
                for a in v:
                    element.append(dict_to_xml(a, element))
            else:
                element.attrib[k] = unicode(v)

        return element
    return None

def dictxml(**kwargs):
    return dict_to_xml(kwargs)

if __name__ == '__main__':
    print dictxml(__tag__ = 'root', a = 1, b = 'abc', c = 3.2)