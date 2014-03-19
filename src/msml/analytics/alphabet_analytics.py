# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
#   S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
#   The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#   Medicine Meets Virtual Reality (MMVR) 2014
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

"""
This module provides functionality of validating the current loadable alphabet.


"""

__author__ = 'Alexander Weigl'
__date__ = "2014-03-19"


import jinja2


RST_TEMPLATE = """
Alphabet
=======================================


Operatoren
---------------------------------------


Attributes
----------------------------------------

{% for name, attrib in alphabet.object_attributes.items() %}

## {{ name }}

> {{ attrib.description }}


===============  =============== =============== =============== ===============
name             type            format          optional        default
---------------  --------------- --------------- --------------- ---------------{% for param in attrib.parameters.values() %}
{{ param|table }}{% endfor %}
===============  =============== =============== =============== ===============

{% endfor %}



"""

import msml.env
import msml.frontend


def export_alphabet_overview_markdown(alphabet=None):
    if not alphabet:
        alphabet = msml.env.current_alphabet

    def table(parameter):
        justify = 30
        p = (parameter.name, parameter.type, parameter.format, None, parameter.default)
        ljust = lambda x: str(x)[:14].ljust(justify)
        return ' '.join(map(ljust, p))



    jenv = jinja2.Environment()
    jenv.filters['table'] = table
    template = jenv.from_string(RST_TEMPLATE)

    return template.render(alphabet=alphabet)

