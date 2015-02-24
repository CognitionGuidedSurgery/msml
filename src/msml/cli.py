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

from __future__ import print_function, absolute_import
from collections import namedtuple
from msml.model.base import MSMLVariable
from msml.sortdef import *

from .xml import load_msml_file
import jinja2


"""Support for the CLI (command line interface) format of MITK/Slicer


"""
__author__ = 'Alexander Weigl <Alexander.Weigl@student.kit.edu>'

__all__ = ['get_cli_xml']

jenv = jinja2.Environment(loader=jinja2.PackageLoader("msml", ""))

CLI_TEMPLATE = jenv.get_template('cli.jinja2')


def get_cli_xml(filename=None, msml_file=None,
                **kwargs):
    """

    :param filename:
    :param msml_file:
    :param kwargs:

                 category=None,
                title=None,
                description=None,
                version=None,
                docurl=None,
                license=None,
                contributor=None,
                acknowledgements=None,
    :return:
    """
    if filename:
        msml_file = load_msml_file(filename)

    assert msml_file

    ns = kwargs

    inputs = []
    outputs = []
    parameters = []

    for var in msml_file.variables.values():
        assert isinstance(var, MSMLVariable)

        a = var_to_cli(var)
        if issubclass(var.sort.physical, InFile):
            inputs.append(a)
        else:
            parameters.append(a)


    ns['inputs'] = inputs
    ns['outputs'] = outputs
    ns['parameters'] = parameters

    return CLI_TEMPLATE.render(**ns)


class CliParameter(object):
    def __init__(self, type = None, name= None, label = None, longflag = None, channel= None, index = None, description= None):
        self.__dict__.update(locals())

TYPE_MAP ={
    int : "integer",
    float: "float",
    MSMLFloat: 'float',
    MSMLString: 'string',
    MSMLInt: 'integer',
    MSMLUInt: 'integer',
}


def var_to_cli(variable):
    para = CliParameter()

    try:
        para.type = TYPE_MAP[variable.sort.physical]
    except:
        para.type = "string" # fallback
    para.name = variable.name
    para.label = "no idea what this is"
    para.longflag = variable.name

    if issubclass(variable.sort.physical, InFile):
        para.channel = "input"

    return para