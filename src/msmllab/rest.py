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
import json
from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource, fields, marshal
from msml.frontend import App as MSMLApp


msmlapp = MSMLApp()
alphabet = msmlapp.alphabet

app = Flask(__name__)
api = Api(app)


def error(msg, no=500):
    return {'message': msg, 'number': no}


def slots(slots):
    return [ (s.name, s.physical_type, s.logical_type)
                for s in slots.values()]


class OperatorResource(Resource):
    def get(self, operator_name):
        try:
            operator = alphabet.operators[operator_name]

        except KeyError:
            return error("Operator not found")

        return {
                'name': operator.name,
                'input': slots(operator.input),
                'output': slots(operator.output),
                'parameter': slots(operator.parameters),
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



import msml.sorts


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


api.add_resource(ListOperators, '/operators/')
api.add_resource(OperatorResource, '/operators/<string:operator_name>', endpoint = 'or')