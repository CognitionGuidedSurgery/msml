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
from msml.model.alphabet import PythonOperator, ShellOperator, SharedObjectOperator

__author__ = 'Alexander Weigl'
__date__ = "2014-03-19"

import jinja2
import os.path
import msml.env
import msml.frontend
from StringIO import StringIO

# deprecated by create_docs.py
# def export_alphabet_overview_rst(alphabet=None):
#     if not alphabet:
#         alphabet = msml.env.current_alphabet
#
#     def table(parameter):
#         justify = 30
#         p = (parameter.name, parameter.type, parameter.format, None, parameter.default)
#         ljust = lambda x: str(x)[:14].ljust(justify)
#         return ' '.join(map(ljust, p))
#
#     def rsttable(seq, fields = "name,physical_type,logical_type,sort,required,default,doc"):
#         def get(obj, key):
#             try:
#                 return getattr(obj, key)
#             except:
#                 if key in ("doc", "type"):
#                     return ":red:`MISSING`"
#                 else:
#                     return None
#
#         def sep(char = "="):
#             for sz in colsizes:
#                 string.write(char * sz )
#                 string.write(" ")
#             string.write("\n")
#
#         def out(seq):
#             for s, sz in zip(seq, colsizes):
#                 string.write(s.ljust(sz))
#                 string.write(" ")
#             string.write("\n")
#
#         fields = fields.split(",")
#
#
#         tbl = [fields] + \
#               [list(map(lambda x: str(get(s, x)), fields))
#                for s in seq]
#
#         colsizes = [0] * len(fields)
#
#         for line in tbl:
#             for col, val in enumerate(line):
#                 if colsizes[col] < len(val):
#                     colsizes[col] = len(val)
#
#         string = StringIO()
#         if tbl[1:]:
#             sep("=")
#             out(tbl[0])
#             sep('=')
#             for l in tbl[1:]: out(l)
#             sep("=")
#         else:
#             string.write("none\n")
#             #string.write("none".center(sum(colsizes)))
#             #string.write("\n")
#
#         return string.getvalue()
#
#     def indent(string, spaces = 4):
#         i =  " " * spaces
#         return i + string.replace("\n", "\n" + i)
#
#     def oerator_runtime(op):
#         import msml.model
#
#         if isinstance(op, PythonOperator):
#             return """
# :type: PythonOperator
# :modul: ``%s``
# :function: ``%s``""" %( op.modul_name, op.function_name)
#
#         elif isinstance(op, ShellOperator):
#             return """
# :type: **ShellOperator**
# :template: ``%s``""" % op.command_tpl
#         elif isinstance(op, SharedObjectOperator):
#             return """
# :type: **SharedObject**
# :file: ``%s``
# :symbol: ``%s``""" %(op.filename, op.symbol_name)
#
#         return ""
#
#     def typename(obj):
#         t = type(obj)
#         return t.__name__
#
#     jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
#     #jenv.filters['table'] = table
#     jenv.filters['rsttable'] = rsttable
#     jenv.filters['type'] = typename
#     jenv.filters['indent'] = indent
#     jenv.filters['runtime'] = oerator_runtime
#     template = jenv.get_template("alphabet_doc.tpl")
#
#     import datetime
#
#     return template.render(alphabet=alphabet, time = datetime.datetime.now())

########################################################################################################################
##
ELEMENT_DEFAULT_VALIDATORS = []

import abc


class ReportEntry(object):
    def __init__(self, format_tpl = None, level = "ERROR", identifier = 0, element = "", argument = "", **kwargs):
        self._params = kwargs
        self._params["level"] = level
        self._params["identifier"] = identifier
        self._params["element"] = element
        self._params["argument"] = argument
        if format_tpl:
            self._format_tpl = format_tpl
        else:
            self._format_tpl = "\x1b[31;3m{level}\x1b[0m-\x1b[32;2m{id}\x1b[0m: \x1b[33;3m{element} {argument}\x1b[0m \x1b[37;1;2;3m{msg}\x1b[0m"

    def __str__(self):
        return self._format_tpl.format(**self._params)

class Validator(object):
    """This class defines the Validator protocol.
    A validator is a function that returns a list of errors.
    An error should be evaluated to a ``str``
    """
    @abc.abstractmethod
    def __call__(self, to_validate):
        return []




class ElementDescriptionValidator(Validator):
    """Validation if the description in an element is set."""
    def __call__(self, element):
        if element.description is None \
        or element.description.strip() == "":
            return ReportEntry(
                    element=element.name,
                    identifier=1,
                    msg="Element has no description/documentation")
        return []

class ArgumentValidator(Validator):
    """Base class for all Validators that runs on input/parameters/output arguments."""
    def __init__(self, attribute):
        self._attrib = attribute
        self.identifier = 0
        self.level = "ERROR"

    def __call__(self, element_or_operator):
        val = getattr(element_or_operator, self._attrib)

        if isinstance(val, dict):
            seq = val.values()
        else:
            seq = val

        self.element = element_or_operator

        res = []
        for s in seq:
            self._check_argument(res, s)

        self.element = None
        return res


    def _check_argument(self, result, arg):
        pass

class TypeValidator(ArgumentValidator):
    def __init__(self, attribute = "parameters"):
        ArgumentValidator.__init__(self, attribute)
        self.level = "ERROR"
        self.identifier = 1

    def _check_argument(self, l,  arg):
        if arg.physical_type is None or arg.physical_type == "":
            l.append(ReportEntry(
                level = self.level, element = self.element.name, id=self.identifier,
                attr=self._attrib, argument= arg.name, msg = "type is None or an empty string"))

        if arg.doc is None or arg.doc == "":
            l.append(ReportEntry(
                level = "WARN", element = self.element.name, id=2,
                attr=self._attrib, argument= arg.name, msg = "no documentation"))

        if not arg.required and (arg.default is None or arg.default == ""):
            l.append(ReportEntry(
                level = "WARN", element = self.element.name, id=3,
                attr=self._attrib, argument= arg.name, msg = "argument is optional and it seems there is no default value"))


ELEMENT_DEFAULT_VALIDATORS+= (TypeValidator("parameters"), ElementDescriptionValidator())

def check_element_completeness(alphabet = None, validators = None):
    if alphabet is None:
        alphabet = msml.env.CURRENT_ALPHABET

    if validators is None:
        validators = ELEMENT_DEFAULT_VALIDATORS

    report = list()
    for element in alphabet.object_attributes.values():
        for validator in validators:
            report += validator(element)
    return report
