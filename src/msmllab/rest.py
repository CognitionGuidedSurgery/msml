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
__date__ = "2014-07-19"

from flask import Flask, request
from flask_restful import Api, Resource
from flask_restful_swagger import swagger

import msml.sorts
from msml.frontend import App as MSMLApp


msmlapp = MSMLApp()
alphabet = msmlapp.alphabet

app = Flask(__name__)
rapi = Api(app)
api = swagger.docs(rapi, apiVersion='0.1', basePath="i61p154.itec.uka.de:8522")


def error(msg, no=500):
    return {'message': msg, 'number': no}


def slots(slots):
    return [(s.name, s.physical_type, s.logical_type)
            for s in slots.values()]


class OperatorResource(Resource):
    def get(self, operator_name):
        try:
            operator = alphabet.operators[operator_name]

        except KeyError:
            return error("Operator not found")

        print operator.sort.physical.__name__

        return {
            'name': operator.name,
            'input': slots(operator.input),
            'output': slots(operator.output),
            'parameter': slots(operator.parameters),
            'type': operator.sort.physical.__name__,
            'meta': operator.meta
        }

    def post(self, operator_name):
        try:
            operator = alphabet.operators[operator_name]
        except:
            return error("Operator not found")

        try:
            arguments = get_arguments(operator.input, operator.parameters)

            print arguments
        except KeyError as e:
            return error(e.message)

        result = operator(**arguments)
        return result


import msml.model


def create_resource(operator):
    assert isinstance(operator, msml.model.Operator)


    def post(_):
        try:
            arguments = get_arguments(operator.input, operator.parameters)
            print arguments
        except KeyError as e:
            return error(e.message)
        result = operator(**arguments)
        return result

    def get_parameters(operator):
        def param(slot):
            assert isinstance(slot, msml.model.Slot)
            return {
                "name": slot.name,
                "description": slot.meta.get('doc', ""),
                "required": True,
                "allowMultiple": False,
                'type': slot.sort.physical.__name__,
                "paramType": "form"
            }

        return list(map(param, operator.input.values() + operator.parameters.values()))


    meta = swagger.operation(
        nickname=operator.name,
        parameters=get_parameters(operator),
        responseMessages=[
            {
                "code": 201,
                "message": "Created. The URL of the created blueprint should be in the Location header"
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )

    swaggt_post = meta(post)
    resource =  type(operator.name, (Resource,), {'post': swaggt_post})
    api.add_resource(resource, '/'+operator.name)


def get_arguments(*dicts):
    arguments = {}
    for t in dicts:
        for slot in t.values():
            value = request.form.get(slot.name, slot.default)

            if not value:
                print request.form

                raise KeyError("operator slot %s is not given" % slot.name)

            cnv = msml.sorts.conversion(type(value), slot.sort)(value)
            arguments[slot.name] = cnv
    return arguments


class ListOperators(Resource):
    def get(self):
        return [
            (name) for name in alphabet.operators.keys()
        ]

for o in alphabet.operators.values():
    create_resource(o)

api.add_resource(ListOperators, '/operators/')
api.add_resource(OperatorResource, '/operators/<string:operator_name>', endpoint='or')