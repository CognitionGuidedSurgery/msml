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

__author__ = 'Alexander Weigl'
__date__ = "2014-07-19"

from jinja2 import Template

from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from msml.frontend import App as MSMLApp


msmlapp = MSMLApp()
alphabet = msmlapp.alphabet

OPERATOR_GET = Template("""Hi, I am {o.name}

My Input are as follow:

{for i in o.input}
    i
{end}
""")

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))



def error(msg, no=500):
    return {'message': msg, 'number': no}


class OperatorResource(Resource):
    def get(self, operator_name):
        try:
            operator = alphabet.operators[operator_name]
            return {
                'name': operator.name,
                'input': operator.input_names(),
                'output': operator.output_names(),
                'parameter': operator.parameter_names(),
                'meta': operator.meta
            }
        except:
            return error("Operator not found")

    def post(self, operator_name):
        try:
            operator = alphabet.operators[operator_name]

            for inp in operator.input_names():
                request.get['']


            return {
                'name': operator.name,
                'input': operator.input_names(),
                'output': operator.output_names(),
                'parameter': operator.parameter_names(),
                'meta': operator.meta
            }
        except:
            return error("Operator not found")








class ListOperators(Resource):
    def get(self):
        return alphabet.operators.keys()


api.add_resource(ListOperators, '/operators/')
api.add_resource(OperatorResource, '/operators/<string:operator_name>')

