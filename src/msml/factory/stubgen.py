# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
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

"""
from msml.frontend import App
from msml.model.alphabet import Slot
from msml.sorts import conversion


__author__ = 'Alexander Weigl <Alexander.Weigl@student.kit.edu>'
__date__ = "2014-09-27"

import jinja2

TEMPLATE = """
from msml.factory.base import WorkflowBuilderBase, create_object_element,  TaskDummyResult
from msml.factory import *

class WorkflowBuilder(WorkflowBuilderBase):
    {%for operator in alphabet.operators.values() %}
    def {{sanitize(operator.name)}}(self, {{ args( operator ) }}):
        class Result_of_{{sanitize(operator.name)}}(TaskDummyResult):
            {% if operator.output_names() -%}
            {%for o in operator.output_names() %}
            @property
            def {{sanitize(o)}}(self):
                return "${{"{%s."}}{{o}}}" % self.task_id
            {%endfor%}
            {%else%}
            pass
            {%-endif%}

        task = self['{{operator.name}}']( {{ args_name(operator) }} )
        return Result_of_{{sanitize(operator.name)}}(task)
    {%endfor%}

{% for element in alphabet.object_attributes.values() %}
def {{sanitize(element.name)}}({{args(element)}}):
    return create_object_element('{{element.name}}', {{args_name(element)}})
{% endfor %}
"""


def _get_jinja_env():
    def sanitize(string):
        return string.replace('-','_')

    def args(operator):
        positional = []
        optionals = []

        positional = list(operator.input)

        for s in operator.parameters.values():
            assert isinstance(s, Slot)
            if s.required:
                positional.append(s.name)
            else:
                value = conversion(str, s.sort)(s.default) if s.default else None
                optionals.append("%s = %s", s.name, repr(value))

        return ', '.join(positional + optionals)

    def args_name(operator):
        l = list(operator.input) + list(operator.parameters)

        return ', '.join(
            ("%s = %s" % (x,x) for x in l)
        )

    e = jinja2.Environment()

    for f in locals().values():
        if callable(f):
            e.globals[f.func_name] = f
    return e


def generate():
    env = _get_jinja_env()

    template = env.from_string(TEMPLATE)

    app = App(novalidate=True)
    return template.render(alphabet = app.alphabet)



def main():
    content =  generate()
    print content
    with open("examples/BunnyExample/stub.py", 'w') as fp:
        fp.write(content)


__name__ == "__main__" and main()