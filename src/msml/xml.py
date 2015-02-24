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


""" msml.msml_xml provides functionality to read and process MSML XML-Files to the msml Python models.

"""
from __future__ import print_function

from lxml import etree

from path import path

from msml.model import *
from msml.model.base import SceneObject
import msml.log
from .exceptions import MSMLError


__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

__all__ = ['load_alphabet', 'load_msml_file', 'xmldom']


def load_alphabet(folder=None, file_list=None):
    """
    Load and build the Alphabet

    :param folder: a name of a folder
    :type folder: str or path.path

    :param list file_list: list of file names

    :return: an alphabet object, not validated
    :rtype: Alphabet
    """
    if not file_list:
        file_list = []

    if folder:
        folder = path(folder)
        file_list += folder.walkfiles("*.xml")

    d = lambda x: xmldom(x.abspath(), "a.xsd")  # Enable xsd
    docs = map(d, file_list)
    results = map(parse_file, docs)
    return Alphabet(results)


def load_msml_file(fil):
    """ Process the given XML-File to and MSMLFile object.

    Args:
      fil (str): filename of an existing XML file

    Returns:
      MSMLFile
    """
    msml_node = xmldom(fil)
    obj = msml_file_factory(msml_node)
    obj.filename = path(fil)
    return obj


def parse_file(R):
    tag = _tag_name(R.tag)

    if tag in _parse_hooks:
        hook = _parse_hooks[tag]
        return hook(R)
    else:
        msml.log.fatal("for element %s is no parse hook registered" % tag)


def get_default_scheme():
    return path(__file__).dirname() / "msml.xsd"


def xmldom(files, schema=None):
    if not schema:
        schema = get_default_scheme()

    try:
        with open(schema, 'r') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)
    except BaseException as e:
        # raise e
        schema = None
    xmlparser = etree.XMLParser(schema=schema, remove_comments=True, remove_pis=True, remove_blank_text=True)

    def xmlopen(xmlfilename):
        try:
            with open(xmlfilename, 'r') as f:
                return etree.fromstring(f.read(), xmlparser)
        except BaseException, e:
            raise MSMLError("could not read %s" % xmlfilename, e)

    if isinstance(files, (str, path, file)):
        return xmlopen(files)
    else:
        return map(xmlopen, files)


def etree_to_dict(t):
    d = {t.tag: map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d


def keyval_factory(meta_node):
    if meta_node is not None:
        return _parse_entry_list(meta_node.iterchildren())
    else:
        return {}


def _except_none(dic, key):
    try:
        return dic[key]
    except:
        return None


def _tag_name(tag):
    p = tag.rfind('}')
    if p:
        return tag[p + 1:]
    return tag


def _attributes(node, attribs, **defaults):
    """

    """

    def _get(key):
        try:
            return node.attrib[key]
        except KeyError:
            try:
                return defaults[key]
            except KeyError:
                return None

    if isinstance(attribs, str):
        attribs = attribs.split(', ')

    if len(attribs) == 1:
        return _get(attribs[0])
    else:
        return (_get(x) for x in attribs)

import itertools


def _parse_task(task_node):
    if task_node is None:
        return []
    else:
        attrib = dict(task_node.attrib)
        task = Task(name=_tag_name(task_node.tag), attrib=attrib)
        sub = list(itertools.chain(*map(_parse_task, task_node.iterchildren())))
        task.sub_tasks = sub
        return [task] + sub


def msml_file_factory(msml_node):
    def _parse_variables(var_node):
        vars = []

        if var_node is None:
            return vars

        for n_var in var_node.iterchildren():
            get = lambda x: _except_none(n_var.attrib, x)
            name = get('name')
            physical = get('physical')
            logical = get('logical')

            if _tag_name(n_var.tag) == 'var':
                v = MSMLVariable(name, physical, logical, get('value'))

            if _tag_name(n_var.tag) == 'file':
                v = MSMLFileVariable(name, physical, logical, get('location'))

            vars.append(v)
        return vars

    def _parse_workflow(wf_node):
        wf = Workflow()
        tasks = map(_parse_task, wf_node.iterchildren())
        for t in tasks:
            for s in t:
                wf.add_task(s)
        return wf

    def _parse_elements(parent_node):
        def _parse_element(element_node):
            params = dict(element_node.attrib)
            params['__tag__'] = _tag_name(element_node.tag)
            o = ObjectElement(params)
            return o

        if parent_node is not None:
            return list(map(_parse_element, parent_node.iterchildren()))
        else:
            return list()

    def _parse_object(object_node):
        '''example:
        <object id="bunny">
			<mesh>
				<linearTet id="bunnyMesh" mesh="${bunnyVolumeMesher}" />
			</mesh>

			<sets>
				<nodes>
					<indexgroup id="constraintRegion" indices="@{bottomToIndexGroup}" />
				</nodes>
				<elements>
					<indexgroup id="bodyRegion" indices="@{bodyToIndexGroup}" />
				</elements>
				<surfaces>
					<indexgroup id="constraintRegion" indices="@{bottomToIndexGroup}" />
				</surfaces>
			</sets>

			<material>
				<region id="bunnyMaterial">
					<!--<materialRegion name=""> -->
					<indexGroup indices="@bodyRegion" />
					<linearElastic youngModulus="80000" poissonRatio="0.49" />
					<mass density="1000" />
				</region>
			</material>

			<constraints>
				<constraint name="bodyConstraint" forStep="${initial}">
				</constraint>
			</constraints>

			<output>
				<displacement name="Liver" timestep="1" />
			</output>
		</object>
        '''
        if _tag_name(object_node.tag) != 'object':
            msml.log.warn("only 'object' is supported, group or "
                 "other elements are not allowed, found: %s'" % object_node.tag)

        def _parse_mesh(mesh_node):
            'example: 	<linearTet id="bunnyMesh" mesh="${bunnyVolumeMesher}" />'
            t = _tag_name(mesh_node.tag)
            m = mesh_node.attrib['mesh']
            i = mesh_node.attrib['id']
            return Mesh(t, i, m)
        
        def _parse_contactGeometry(contactGeometry_node):
            'example:     <contactsurface id="contactSurface" surface="${MovingSurface}"/>'
            t = _tag_name(contactGeometry_node.tag)
            m = contactGeometry_node.attrib['surface']
            i = contactGeometry_node.attrib['id']
            return ContactGeometry(t, i, m)

        def _parse_constraints(constraints_node):
            '''example:
            <constraints>
				<constraint name="bodyConstraint" forStep="${initial}">
				</constraint>
			</constraints>'''

            def _parse_constraint(constraint_node):
                name, fs = _attributes(constraint_node, 'name, forStep')
                oc = ObjectConstraints(name, fs)

                oc.constraints = _parse_elements(constraint_node)
                return oc

            return map(_parse_constraint, constraints_node.iterchildren())

        def _parse_material(mat_node):
            '''
            <material>
				<region id="bunnyMaterial">
					<indexGroup indices="@bodyRegion" />
					<linearElastic youngModulus="80000" poissonRatio="0.49" />
					<mass density="1000" />
				</region>
			</material>
            '''
            if mat_node is None:
                return list()

            def _parse_region(reg_node):
                ident, ind = _attributes(reg_node, ['id', 'indices'])
                elements = list(_parse_elements(reg_node))
                return MaterialRegion(ident, ind, elements)

            return map(_parse_region, mat_node.iterchildren())


        oid = object_node.attrib['id']
        scene_object = SceneObject(oid)

        mesh_node = object_node.find('mesh')[0]
        mesh = _parse_mesh(mesh_node)

        sets_node = object_node.find('sets')
        sets = SceneObjectSets()
        if (sets_node is not None):
            element_sets = sets_node.find('elements')
            nodes_sets = sets_node.find('nodes')
            surfaces_sets = sets_node.find('surfaces')

            sets.nodes = _parse_indexgroup_list(nodes_sets)
            sets.surfaces = _parse_indexgroup_list(surfaces_sets)
            sets.elements = _parse_indexgroup_list(element_sets)

        constraints = ObjectConstraints(name="empty")      
        constraints_node = object_node.find('constraints')
        if(constraints_node is not None):
            constraints = _parse_constraints(constraints_node)

        material_node = object_node.find('material')
        material = _parse_material(material_node)

        output_node = object_node.find('output')
        output = _parse_elements(output_node)

        scene_object.mesh = mesh
        scene_object.output = output
        scene_object.sets = sets
        scene_object.material = material
        scene_object.constraints = constraints
        
        #collision detection stuff
        #get contact surface
        contactGeometryNode = object_node.find("contactsurface")
        if(contactGeometryNode is not None):
            scene_object.contactGeometry = _parse_contactGeometry(contactGeometryNode)       

        return scene_object

    def _parse_scene(scene_node):
        return map(_parse_object, scene_node.iterchildren())

    def _parse_indexgroup_list(node):
        if node is not None:
            return map(lambda n: IndexGroup(*_attributes(n, 'id, indices')),
                       node.iterchildren())
        else:
            return list()

    def _parse_environment(env_node):
        env = MSMLEnvironment()

        solver_node = env_node.find('solver')
        env.solver.processingUnit = solver_node.get('processingUnit')
        env.solver.numParallelProcessesOnCPU = solver_node.get('numParallelProcessesOnCPU')
        env.solver.linearSolver = solver_node.get('linearSolver')
        env.solver.preconditioner = solver_node.get('preconditioner')
        env.solver.timeIntegration = solver_node.get('timeIntegration')
        env.solver.dampingRayleighRatioMass = solver_node.get('dampingRayleighRatioMass')
        env.solver.dampingRayleighRatioStiffness = solver_node.get('dampingRayleighRatioStiffness')
        env.solver.mass = solver_node.get('mass')

        simulation_node = env_node.find('simulation')
        for s in simulation_node.iterchildren():
            #parse gravity attribute, if given            
            gravityAttrib = s.get('gravity')         
            gravity = None  
            if(gravityAttrib is not None):
                gravity = map(float, gravityAttrib.split())
            env.simulation.add_step(name=s.get('name'),
                                    dt=s.get('dt'),
                                    iterations=s.get('iterations'),
                                    gravity=gravity)

        return env

    n_variables = msml_node.find('variables')
    n_workflow = msml_node.find('workflow')
    n_scene = msml_node.find('scene')
    n_environment = msml_node.find('environment')

    if n_scene is not None:
        scene = _parse_scene(n_scene)
    else:
        scene = None

    if n_environment is not None:
        env = _parse_environment(n_environment)
    else:
        env = None

    return MSMLFile(variables=_parse_variables(n_variables),
                    env=env,
                    scene=scene,
                    workflow=_parse_workflow(n_workflow))


from collections import OrderedDict


def _parse_entry_list(nodelist):
    d = OrderedDict()

    for node in nodelist:
        key = node.attrib['key']
        if 'value' in node.attrib:
            value = node.attrib['value']
        else:
            value = node.text

        if value:
            d[key] = value.strip()

    return d


def _argument_sets(node, parent=None, as_ordered_dict=False):
    def _parse_arg(node):
        n, p, l, r, d, t = _attributes(node, 'name, physical, logical, required, default, target', required=True)
        meta = _parse_entry_list(node.iterchildren())
        arg = Slot(n, p, l, bool(int(r)), d, meta, parent)
        arg.target = msml.sorts._bool(t)
        return arg

    # def _parse_struct(node):
    # get = lambda k: _except_none(node.attrib, k)
    # return StructArgument(get('name'), _argument_sets(node))

    def _parse_subelements(node):
        if node.tag == 'arg':
            return _parse_arg(node)
        #        elif node.tag == 'struct':
        #            return _parse_struct(node)
        else:
            raise BaseException("unexpecting element")


    if node is not None and len(node) > 0:
        result = map(_parse_subelements, node.iterchildren())
    else:
        result = []

    if as_ordered_dict:
        o = OrderedDict()
        for r in result:
            o[r.name] = r
        return o
    else:
        return result


def operator_factory(operator_node):
    """

    """

    def runtime_factory(node):
        TAGS = {'python': ('function', 'method'), 'sh': ('file', 'wd'), 'so': ('file', 'symbol')}

        for k, v in TAGS.items():
            n = node.find(k)
            if n is not None:
                d = dict(n.attrib)
                d['exec'] = k
                return d

        raise BaseException('unexpected runtime type!')


    name = operator_node.attrib['name']

    n_runtime = operator_node.find('runtime')
    n_input = operator_node.find('input')
    n_output = operator_node.find('output')
    n_parameters = operator_node.find('parameters')
    n_annotation = operator_node.find('annotation')

    runtime = runtime_factory(n_runtime)
    op_classes = {'python': PythonOperator,
                  'sh': ShellOperator,
                  'so': SharedObjectOperator, }
    factory = op_classes[runtime['exec']]

    op = factory(name=name, runtime=runtime)

    input = _argument_sets(n_input, op, True)
    output = _argument_sets(n_output, op, True)
    parameters = _argument_sets(n_parameters, op, True)
    meta = keyval_factory(n_annotation)

    op.input = input
    op.output = output
    op.parameters = parameters
    op.meta = meta

    return op


def element_factory(element_node):
    name = element_node.attrib['name']
    quantity = element_node.attrib['quantity']
    category = element_node.attrib['category']
    clazz = ObjectAttribute.find_class(category)

    obj = clazz(name=name, quantity=quantity)

    description = element_node.find('description').text

    if description is not None:
        description = description.strip()

    input_node = element_node.find('input')
    parameter_node = element_node.find('parameters')

    input = _argument_sets(input_node, obj, True)
    parameters = _argument_sets(parameter_node, obj, True)

    obj.input = input
    obj.parameters = parameters
    obj.description = description

    return obj


_parse_hooks = {'operator': operator_factory, 'element': element_factory}
