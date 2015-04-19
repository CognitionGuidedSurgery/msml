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
import re

from ...sorts import *
from ...exceptions import *
from msml import sorts

from ..sequence import executeOperatorSequence
from msml.exceptions import MSMLUnknownModuleWarning
from ...log import debug,info, error, warn

from .operator import *

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
        log.critical("No element with name %s found in alphabet, but was requested", obj)
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

    def __repr__(self):
        return "%s(name=%r, quantity=%r,description=%r,parameters=%r, inputs=%r)" % (self.__class__.__name__, self.name, self.quantity, self.description, self.parameters, self.inputs)

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

        #if 'indices' in self.parameters:
        #    return True
        #else:
        #    log.error("OAConstraint: %s does not have an indices attribute defined" % self.name)
        #    return False
        return True


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
                 meta=None, parent=None):
        if physical is None:
            pname = None
            if parent:
                pname = parent.name
            log.critical("Slot %s in parent %s does not have a physical type defined. "
                         "This can cause conversion errors.", name, pname)

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

        self.meta = meta or dict()
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

        self.target = False
        """True iff. this slot holds an output filename.
        :type: bool
        """

        try:
            self.sort = get_sort(self.physical_type, self.logical_type)
        except AssertionError as ae:
            log.error("%s %s has physical_type %s" % (self.parent, self.name, self.physical_type))
            self.sort = None


    def __getattr__(self, item):
        if 'meta' in self.__dict__ and item in self.meta:
            return self.meta[item]
        else:
            return self.__dict__[item]

    def __str__(self):
        return "<Slot %s: %s>" % (self.name, self.sort)



