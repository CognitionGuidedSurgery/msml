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

__author__ = 'Alexander Weigl <uiduw@student.kit.edu>'
__date__ = '2014-05-16'

"""
This modules creates a XSD file for the given :py:class:`msml.model.Alphabet`.

With you can use the generated XSD for validating your MSML files against the current alphabet including operators and worklow.

"""

from collections import namedtuple

from jinja2 import Environment, FileSystemLoader
from path import path

from ..sortdef import *

__all__=['xsd']

directory = path(__file__).dirname()

env = Environment(loader=FileSystemLoader(directory),
                  block_start_string="<!--",
                  block_end_string="-->")
XSD_TEMPLATE = env.get_template("msml_extension.tpl.xsd")

XSD_TYPES = {
    MSMLInt: "xsd:integer",
    MSMLUInt: "xsd:nonNegativeInteger",
    MSMLFloat: "xsd:float",
    bool: "xsd:boolean",
}

from msml.model import *


def xsd(alphabet):
    """
    :param alphabet:
    :type: msml.model.Alphabet
    :return:
    """

    def _xsd_type(x):
        """

        :param x:
         :type x: msml.model.Slot
        :return:
        """
        try:
            return XSD_TYPES[x.sort.physical]
        except:
            return "xsd:string"

    operator_t = namedtuple('operator_t', 'name,attributes,annotation')
    attributes_t = namedtuple('attribute_t', "name,type,required,annotation")

    def _transfer(operator):
        attribs_i = list(map(lambda x: attributes_t(x.name, _xsd_type(x), True, ""),
                             operator.input.values()))
        attribs_p = list(map(lambda x: attributes_t(x.name, _xsd_type(x), x.required, ""),
                             operator.parameters.values()))

        idattrib = [attributes_t("id", "xsd:string", True, "identifier for xml elements")]

        return operator_t(operator.name, idattrib + attribs_i + attribs_p, operator.meta.get('doc', ''))

    def filter_attributes(kind):
        return filter(lambda x: isinstance(x, kind), alphabet._object_attributes.values())

    def _transfer_oa(id_attribute_required=False):
        """
        :param attribute:
        :type attribute: msml.model.alphabet.ObjectAttribute
        :return:
        """

        def _map(attribute):
            attributes = map(lambda x: attributes_t(x.name, _xsd_type(x), True, ""), attribute.parameters.values())
            idattrib = [attributes_t("id", "xsd:string", id_attribute_required, "identifier for xml elements")]
            return operator_t(attribute.name, idattrib + list(attributes), attribute.description)

        return _map


    operators = map(_transfer, alphabet.operators.values())
    materials = map(_transfer_oa(), filter_attributes((OAMaterial)))
    outputs = map(_transfer_oa(True), filter_attributes((OAOutput)))
    constraints = map(_transfer_oa(), filter_attributes((OAConstraint)))

    ptmx = (directory / '..' / 'msml.xsd').abspath()

    return XSD_TEMPLATE.render(operators=operators, materials=materials, outputs=outputs,
                               constraints=constraints, path_to_msml_xsd=ptmx)
