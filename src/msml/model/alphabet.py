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

from collections import namedtuple, OrderedDict
import pickle
from warnings import warn

from .exceptions import *
from ..titen import titen
from .base import MSMLVariable


__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

XSD_ALPHABET = """
<?xml version="1.0" encoding="UTF-8"?>
<xsd:schema targetNamespace="http://sfb125.de/msml"
    elementFormDefault="unqualified" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns="http://sfb125.de/msml">

    <xsd:redefine schemaLocation="msml.xsd">
        <xsd:complexType name="workflow_t">
            <xsd:complexContent>
                <xsd:extension base="workflow_t">
                    <xsd:sequence>
                        <xsd:choice>
             {for o in operators}
                            <xsd:element name="{$ o.name}">
                                <xsd:complexType>
                                    <xsd:attribute name="id" type="xsd:string" use="required" />
                                {for a in o.attributes}
                                    <xsd:attribute name="{$ a.name}" type="xsd:string" use="{$ a.use}" />
                                {end}
                                </xsd:complexType>
                            </xsd:element>
             {end}
                        </xsd:choice>
                    </xsd:sequence>
                </xsd:extension>
            </xsd:complexContent>
        </xsd:complexType>
    </xsd:redefine>
</xsd:schema>
"""
XSD_TEMPLATE = titen(text=XSD_ALPHABET)


class Alphabet(object):
    def __init__(self, elements=[]):
        self._operators = OrderedDict()
        self._object_attributes = OrderedDict()

        self.append(elements)

    @property
    def operators(self): return self._operators

    @property
    def object_attributes(self): return self._object_attributes

    def append(self, elements):
        for e in elements:
            if isinstance(e, Operator):
                self._operators[e.name] = e
            elif isinstance(e, ObjectAttribute):
                self._object_attributes[e.name] = e

    def __contains__(self, obj):
        return bool(self.type(obj))

    def __getitem__(self, obj):
        return self.get(obj)

    def type(self, obj):
        if obj in self._operators:
            return "operator"
        elif obj in self._object_attributes:
            return "element"
        return None

    def get(self, obj):
        if obj in self._operators:
            return self._operators[obj]
        elif obj in self._object_attributes:
            return self._object_attributes[obj]
        return None

    def validate(self):
        for o in self._operators.values():
            o.validate()
            #r = map(lambda x: x.validate(), self._operators.values())
            #return r

    def _xsd(self):
        """
        
        """
        operator_t = namedtuple('operator_t', 'name,attributes')
        attributes_t = namedtuple('attribute_t', "name,use")

        def _transfer(operator):
            attribs_i = list(map(lambda x: attributes_t(x.name, 'required'), operator.input))
            attribs_p = list(map(lambda x: attributes_t(x.name, 'optional'), operator.parameters))

            return operator_t(operator.name,
                              attribs_i + attribs_p)

        operators = map(_transfer, self._operators.values())
        return XSD_TEMPLATE(operators=operators)

    def __str__(self):
        o = ",".join(self._operators.keys())
        e = ",".join(self._object_attributes.keys())

        return "Alphabet: (Operators: %s) (Elements: %s) " % (o, e)


    def save(self, filename):
        with open(filename, 'w') as file:
            pickle.dump(self, file)

            #import jsonpickle
            #print(jsonpickle.encode(self))


    @staticmethod
    def load(filename):
        with open(filename, 'r') as file:
            return pickle.load(file)


class ObjectAttribute(object):
    def __init__(self, name, quantity='single', description="documentation N/A",
                 parameters=None, inputs=None):
        self.name = name
        self.quantity = quantity
        self.description = description
        self.parameters = parameters
        self.inputs = inputs

    @staticmethod
    def find_class(category):
        global _object_attribute_categories
        return _object_attribute_categories[category]


class OAConstraint(ObjectAttribute):
    pass


class OAMaterial(ObjectAttribute):
    pass


class OAMesh(ObjectAttribute):
    pass


class OAIndexGroup(ObjectAttribute):
    pass


class OABody(ObjectAttribute):
    pass


_object_attribute_categories = {'basic': ObjectAttribute, 'material': OAMaterial, 'constraint': OAConstraint,
                                'mesh': OAMesh, 'indexgroup': OAIndexGroup, 'data': OABody}


class Argument(MSMLVariable):
    def __init__(self, name, typ=None, format=None, required=True):
        MSMLVariable.__init__(self, name, format, typ)
        self.required = required
        self.default = None


StructArgument = namedtuple('StructArgument', 'name,args')


def _list_to_dict(lis, attrib='name'):
    if not lis:
        return OrderedDict()

    d = OrderedDict()
    for e in lis:
        d[getattr(e, attrib)] = e
    return d


class Operator(object):
    """Operator"""

    def __init__(self,
                 name,
                 input=None,
                 output=None,
                 parameters=None,
                 runtime=None,
                 meta=None):
        """
        
        """
        self.name = name
        self.input = _list_to_dict(input)
        self.output = _list_to_dict(output)
        self.parameters = _list_to_dict(parameters)

        self.meta = meta
        self.runtime = runtime

        self._filename = None

    def __str__(self): return "{Operator %s}" % self.name

    def output_names(self):
        return self.output.keys()

    def input_names(self):
        return self.input.keys()

    def parameter_names(self):
        return self.parameters.keys()

    def acceptable_names(self):
        return self.input_names() + self.parameter_names()

    def __contains__(self, attrib):
        return attrib in self.input or attrib in self.parameters

    def __call__(self, *args, **env):
        pass


    def validate(self):
        return True


#     def check_types(self, args, kwargs):
#         sig = signature(self.func)
#         type_bind = sig.bind(*self.args)
#         val_bind = sig.bind(*args)
#
#         T = type_bind.args
#         V = val_bind.args
#
#         return issubtype(V, T)
#
#     def _execute(self, *args, **kwargs):
#         sig = signature(self.func)
#         fargs = sig.bind_partial(*args)  # , **kwargs)
#
#         if self.check_types(args, kwargs):
#             a = self.func(*fargs.args)
#             if not issubtype(a, self.out):
#                 raise BaseException("return types mismatch")
#             return a
#         else:
#             raise BaseException("argument type does not match defined types")


class PythonOperator(Operator):
    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta)
        self.function_name = runtime['function']
        self.modul_name = runtime['module']
        self.function = None

    def _check_function(self):
        pass


    def __str__(self):
        return "<PythonOperator: %s.%s>" % (self.modul_name, self.function_name)

    def __call__(self, **kwargs):
        if not self.__function:
            self.bind_function()

        # bad for c++ modules, because of loss of signature
        # r = self.__function(**kwargs)

        args = [kwargs.get(x, None) for x in self.acceptable_names()]
        r = self.__function(*args)

        if not isinstance(r, tuple):
            r = (r,)

        results = dict(zip(self.output_names(), r))
        return results

    def bind_function(self):
        import importlib

        try:
            #print("LOADING: %s.%s" % (self.modul_name, self.function_name))
            mod = importlib.import_module(self.modul_name)
            self.__function = getattr(mod, self.function_name)

            return self.__function
        except ImportError, e:
            warn("%s.%s is not available (module not found)" % (self.modul_name, self.function_name),
                 MSMLUnknownModuleWarning, 0)
        except AttributeError, e:
            warn("%s.%s is not available (function/attribute not found)" % (self.modul_name, self.function_name),
                 MSMLUnknownFunctionWarning, 0)

    def validate(self):
        self.bind_function()


class ShellOperator(Operator):
    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta)

        self.command_tpl = runtime['template']

    def __call__(self, **kwargs):
        import os

        command = self.command_tpl.format(**kwargs)
        os.system(command)


class SharedObjectOperator(PythonOperator):
    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta)

        self.symbol_name = runtime['symbol']
        self.filename = runtime['file']


    def bind_function(self):
        import ctypes

        object = ctypes.CDLL(self.filename)

        self.__function = getattr(object, self.symbol_name)
        return self.__function

