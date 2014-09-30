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

from collections import OrderedDict
import pickle

from ..sorts import *
from msml.log import report
from ..exceptions import *
from msml import sorts

from sequence import executeOperatorSequence
from msml.exceptions import MSMLUnknownModuleWarning

__author__ = "Alexander Weigl"
__date__ = "2014-01-25"


__all__ = ['Alphabet',
           'ObjectAttribute',
           'OAOutput',
           'OAConstraint',
           'OAMaterial',
           'Slot',
           'Operator',
           'SharedObjectOperator',
           'PythonOperator',
           'ShellOperator']


class Alphabet(object):
    """`Alphabet`holds the information about defined :py:class:`Operator`s and :py:class:`ObjectAttribute`s

    Normally it will created from a bunch of xml files.

    """

    def __init__(self, elements=[]):
        self._operators = OrderedDict()
        self._object_attributes = OrderedDict()
        self.append(elements)

    @property
    def operators(self):
        """dictionary of defined operators
        :type: OrderedDict
        """
        return self._operators

    @property
    def object_attributes(self):
        """a dictionary of all available object attributes
        :type: OrderedDict
        """
        return self._object_attributes

    def append(self, elements):
        """add a new element (operator or attribute) to the alphabet

        :type elements: list[Operator] or list[ObjectAttribute]

        .. seealso:

           :py:class:`Operator`
           :py:class:`ObjectAttribute`

        """
        for e in elements:
            if isinstance(e, Operator):
                self._operators[e.name] = e
            elif isinstance(e, ObjectAttribute):
                self._object_attributes[e.name] = e

    def __contains__(self, obj):
        """Test if the given `obj` is in the alphabet.

        :type obj: Operator or ObjectAttribute
        :rtype: bool
        :returns:
        """
        return bool(self.type(obj))

    def __getitem__(self, obj):
        return self.get(obj)

    def type(self, obj):
        """
        :returns: the type of the given `obj`
        :type obj: Operator or ObjectAttribute
        """
        if obj in self._operators:
            return "operator"
        elif obj in self._object_attributes:
            return "element"
        return None

    def get(self, obj):
        """
        :param obj: an identifier for an :py:class:`Operator` or an :py:class:`ObjectAttribute`
        :type obj: str
        """
        if obj in self._operators:
            return self._operators[obj]
        elif obj in self._object_attributes:
            return self._object_attributes[obj]
        return None

    def validate(self):
        """Validates the alphabet.
        Calls `.validate()` on each contained element.
        """
        r = map(lambda x: x.validate(), self._operators.values())
        s = map(lambda x: x.validate(), self._object_attributes.values())
        return all(r) and all(s)

    def __str__(self):
        o = ",".join(self._operators.keys())
        e = ",".join(self._object_attributes.keys())
        return "Alphabet: (Operators: %s) (Elements: %s) " % (o, e)

    def save(self, filename):
        """pickles the alphabet into a binary dump to the given `filename`
        :type filename: str """
        with open(filename, 'w') as file:
            pickle.dump(self, file)

            # import jsonpickle
            # print(jsonpickle.encode(self))

    @staticmethod
    def load(filename):
        """loads a  pickled alphabet from the given `filename`
         :param filename:
         :type filename: str
        """
        with open(filename, 'r') as file:
            return pickle.load(file)



class ObjectAttribute(object):
    """Class of all user-defineable constraints, outputs, materials.
    """

    def __init__(self, name, quantity='single',
                 description="documentation N/A",
                 parameters=None, inputs=None):
        self.name = name
        """The attribute name. This name is used by the user as xml tag name"""

        self.quantity = quantity
        """Unused. Should say how often the element can be used in an object definition"""

        self.description = description
        """Description by the user for this attribute"""

        self.parameters = parameters
        """Parameters of this ObjectAttribute.
        :type: dict[str,Slot]
        """

        self.inputs = inputs
        """Unused and deprecated

        """

    @staticmethod
    def find_class(category):
        """Finds the correct class for an given category.
        :returns: the suitable constructor
        :type category: str
        :rtype: type
        """
        global _object_attribute_categories
        return _object_attribute_categories[category]

    def validate(self):
        """Validation of this attribute"""
        return True


class OAOutput(ObjectAttribute):
    pass


class OAConstraint(ObjectAttribute):
    def validate(self):
        """validates a Object Constraints.

        :constraints: * indices attribute have to present
        :rtype: bool
        """

        if 'indices' in self.parameters:
            return True
        else:
            report("OAConstraint: %s does not have an indices attribute defined" % self.name, 'E', 182)
            return False


class OAMaterial(ObjectAttribute):
    pass


_object_attribute_categories = {'basic': ObjectAttribute, 'material': OAMaterial, 'constraint': OAConstraint,
                                "output": OAOutput}
"""Register for attribute category and suitable class"""


class Slot(object):
    """An input, parameter or output slot of an operator or an element
    Consists of name, physical and logical type.

    Proxy for meta data.

    """
    # : slot type is not set
    SLOT_TYPE_UNKNOWN = -1

    #: slot is an input
    SLOT_TYPE_INPUT = 0

    #: slot is an output
    SLOT_TYPE_OUTPUT = 1

    #: slot is a parameter
    SLOT_TYPE_PARAMETER = 2

    def __init__(self, name, physical, logical=None,
                 required=True, default=None,
                 meta=dict(), parent=None):
        if (physical is None):
            warn("Slot %s does not have a physical type defined. This can cause conversion errros.)" % (name), MSMLUnknownModuleWarning, 0)
        self.name = name
        """slot name
        :type: str
        """
        self.logical_type = logical
        """the logical type given by the user as str
        :type: str
        """
        self.physical_type = physical
        """the physical type given by the user as str
        :type: str
        """
        self.required = required
        """True iff. this slot has to be set in the xml tags
        :type: bool
        """
        self.default = default
        """default value of this slot. has to be if :py:var:`required` is True"""
        self.meta = meta
        """various and arbitrary meta data
        :type: dict"""

        self.parent = parent
        """the parent of this slot. Can be an :py:class:`Operator` or :py:class:`ObjectAttribute` or an :py:class:`Exporter`
        :type: Operator or msml.exporter.Exporter or ObjectAttribute
        """

        self.slot_type = Slot.SLOT_TYPE_UNKNOWN
        """slot type. see class SLOT\_TYPE\_\* variables.
        :type: int
        """

        self.sort = None
        """the sort of this slot. derived from `physical_type` and `logical_type`
        :type: Sort
        """
        try:
            self.sort = get_sort(self.physical_type, self.logical_type)
        except AssertionError as ae:
            report("%s %s has physical_type %s" % (self.parent, self.name, self.physical_type),
                   kind="E", number=156)
            self.sort = None


    #def __getattr__(self, item):
        #assert (self.meta is not None)
        #return self.meta[item]

    def __str__(self):
        return "<Slot %s: %s>" % (self.name, self.sort)


def _list_to_dict(lis, attrib='name'):
    if not lis:
        return OrderedDict()

    d = OrderedDict()
    for e in lis:
        d[getattr(e, attrib)] = e
    return d


class Operator(object):
    """Operator hold all slots, runtime information and meta data"""

    def __init__(self,
                 name,
                 input=None,
                 output=None,
                 parameters=None,
                 runtime=None,
                 meta=None):
        """Constructs an operator from the given arguments.
        :type name: str
        :type input: list
        :type output: list
        :type:parameters: list
        :type runtime: dict
        :type meta: dict
        """
        self.name = name

        self.input = _list_to_dict(input)
        """:type: dict"""

        self.output = _list_to_dict(output)
        """:type: dict"""

        self.parameters = _list_to_dict(parameters)
        """:type: dict"""

        self.meta = meta
        """:type: dict"""

        self.runtime = runtime
        """:type: dict"""

        self._filename = None
        """filename of the xml file, which defined this operator
        :type: str"""

    def __str__(self): return "{Operator %s}" % self.name

    def output_names(self):
        """:returns all names of the output slots
        :rtype: list[str]
        """
        return self.output.keys()

    def input_names(self):
        """:returns all names of the input slots
        :rtype: list[str]
        """
        return self.input.keys()

    def parameter_names(self):
        """:returns all names of the parameter slots
        :rtype: list[str]
        """
        return self.parameters.keys()

    def acceptable_names(self):
        """all names of input or parameter slots
        :rtype: list[str]
        """
        return self.input_names() + self.parameter_names()

    def __contains__(self, attrib):
        """checks if attrib is a valid input or parameter name"""
        return attrib in self.input or attrib in self.parameters

    def __call__(self, *args, **env):
        """execution of this operator, with the given arguments"""
        pass


    def validate(self):
        """validation of this operator
        :returns: True iff. this operator is well-defined
        :rtype: bool"""
        return True


# def check_types(self, args, kwargs):
# sig = signature(self.func)
# type_bind = sig.bind(*self.args)
# val_bind = sig.bind(*args)
#
# T = type_bind.args
# V = val_bind.args
#
# return issubtype(V, T)
#
# def _execute(self, *args, **kwargs):
# sig = signature(self.func)
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
    """Operator for Python functions.

    """

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        """
        :param runtime: should include the key: "function" and "module"
        .. seealso: :py:meth:`Operator.__init__`
        """
        Operator.__init__(self, name, input, output, parameters, runtime, meta)
        self.function_name = runtime['function']
        """name of the pyhton function"""
        self.modul_name = runtime['module']
        """the name of the python module"""
        self._function = None
        """the found and bind python function"""

    def _check_function(self):
        pass

    def __str__(self):
        return "<PythonOperator: %s.%s>" % (self.modul_name, self.function_name)
    
    
    def __call__(self, **kwargs):
        if not self._function:
            self.bind_function()

        # bad for c++ modules, because of loss of signature
        # r = self.__function(**kwargs)
        
        #replace empty values with defaults from operators xml description (by getting all defaults and overwrite with given user values)
        defaults = dict()
        for x in self.parameters.values():
            if x.default is not None:
                defaults[x.name] = sorts.conversion(str, x.sort)(x.default)
        kwargsUpdated = defaults
        kwargsUpdated.update(kwargs)
                   
        args = [kwargsUpdated.get(x, None) for x in self.acceptable_names()]
        
        
        if sum('*' in str(arg) for arg in args):        
                r = executeOperatorSequence(self, args) 
        else:
            print(args)
            r = self._function(*args)

        if len(self.output) == 0:
            results = None
        elif len(self.output) == 1:
            results = {self.output_names()[0]: r}
        else:
            results = dict(zip(self.output_names(), r))

        return results
        
    def bind_function(self):
        """Search and bind the python function. Have to be called before `__call__`"""
        import importlib

        try:
            #print("LOADING: %s.%s" % (self.modul_name, self.function_name))
            mod = importlib.import_module(self.modul_name)
            self._function = getattr(mod, self.function_name)

            return self._function
        except ImportError, e:
            warn("%s.%s is not available (module not found)" % (self.modul_name, self.function_name),
                 MSMLUnknownModuleWarning, 0)
        except AttributeError, e:
            print(dir(mod))
            warn("%s.%s is not available (function/attribute not found)" % (self.modul_name, self.function_name),
                 MSMLUnknownFunctionWarning, 0)

    def validate(self):
        return self.bind_function() is not None


class ShellOperator(Operator):
    """ShellOperator

    """

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta)

        self.command_tpl = runtime['template']

    def __call__(self, **kwargs):
        import os
        
        #replace empty values with defaults from operators xml description (by getting all defaults and overwrite with given user values)
        defaults = dict()
        for x in self.parameters.values():
            if x.default is not None:
                defaults[x.name] = sorts.conversion(str, x.sort)(x.default)
        kwargsUpdated = defaults
        kwargsUpdated.update(kwargs)
                   
        args = [kwargsUpdated.get(x, None) for x in self.acceptable_names()]
        
        if sum('*' in str(arg) for arg in args):        
            r = executeOperatorSequence(self, args) 
        else:
            self._function(args)
        
        results = None
        if len(self.output) == 1 and 'out_filename' in kwargs:
            results = {self.output_names()[0]: kwargs.get('out_filename')}
        return results
    
    def _function(self, *args):
        if (len(args)==1):
            args = args[0]
        kwargs =  dict(zip(self.acceptable_names(), args))
        command = self.command_tpl.format(**kwargs)
        os.system(command)


class SharedObjectOperator(PythonOperator):
    """Shared Object Call via ctype"""

    def __init__(self, name, input=None, output=None, parameters=None, runtime=None, meta=None):
        Operator.__init__(self, name, input, output, parameters, runtime, meta)

        self.symbol_name = runtime['symbol']
        self.filename = runtime['file']


    def bind_function(self):
        import ctypes

        object = ctypes.CDLL(self.filename)

        self.__function = getattr(object, self.symbol_name)
        return self.__function

