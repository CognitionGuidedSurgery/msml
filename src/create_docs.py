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


__author__ = 'Alexander Weigl <uiduw@student.kit.edu>'
__date__ = '2014-05-14'

from msml.frontend import App


import jinja2
from path import path
from msml.model import *
from StringIO import StringIO


def table(parameter):
    justify = 30
    p = (parameter.name, parameter.type, parameter.format, None, parameter.default)
    ljust = lambda x: str(x)[:14].ljust(justify)
    return ' '.join(map(ljust, p))

def rsttable(seq, fields = "name,physical_type,logical_type,sort,required,default,doc"):
    def get(obj, key):
        try:
            return getattr(obj, key)
        except:
            if key in ("doc", "type"):
                return ":red:`MISSING`"
            else:
                return None

    def sep(char = "="):
        for sz in colsizes:
            string.write(char * sz )
            string.write(" ")
        string.write("\n")

    def out(seq):
        for s, sz in zip(seq, colsizes):
            string.write(s.ljust(sz))
            string.write(" ")
        string.write("\n")

    fields = fields.split(",")


    tbl = [fields] + \
          [list(map(lambda x: str(get(s, x)), fields))
           for s in seq]

    colsizes = [0] * len(fields)

    for line in tbl:
        for col, val in enumerate(line):
            if colsizes[col] < len(val):
                colsizes[col] = len(val)

    string = StringIO()
    if tbl[1:]:
        sep("=")
        out(tbl[0])
        sep('=')
        for l in tbl[1:]: out(l)
        sep("=")
    else:
        string.write("none\n")
        #string.write("none".center(sum(colsizes)))
        #string.write("\n")

    return string.getvalue()

def indent(string, spaces = 4):
    i =  " " * spaces
    return i + string.replace("\n", "\n" + i)

def oerator_runtime(op):
    import msml.model

    if isinstance(op, PythonOperator):
        return """
:type: PythonOperator
:modul: ``%s``
:function: ``%s``""" %( op.modul_name, op.function_name)

    elif isinstance(op, ShellOperator):
        return """
:type: **ShellOperator**
:template: ``%s``""" % op.command_tpl
    elif isinstance(op, SharedObjectOperator):
        return """
:type: **SharedObject**
:file: ``%s``
:symbol: ``%s``""" %(op.filename, op.symbol_name)

    return ""

def typename(obj):
    t = type(obj)
    return t.__name__

env = jinja2.Environment(loader=jinja2.FileSystemLoader(
    path(__file__).dirname()
))

def format_sort(sort):
    """
    :type sort: msml.sortdef.Sort
    :return:
    """
    def name(t):
        """ :type t: type """
        if t:
            if t.__module__.startswith('__'):
                return t.__name__
            else:
                return "%s.%s" % (t.__module__ , t.__name__)
        else: return "*"

    return "(:py:class:`%s`, :py:class:`%s`)" %(name(sort.physical), name(sort.logical))


env.filters['rsttable'] = rsttable
env.filters['type'] = typename
env.filters['indent'] = indent
env.filters['runtime'] = oerator_runtime
env.filters['title'] = lambda x,t="=": t*len(x)
env.filters['format_sort'] = format_sort


app = App()
operator_template = env.get_template("operator_doc.tpl")
output_dir = path("docs/source/operators")
output_dir.mkdir_p()

operators = list()

for o in app.alphabet.operators.values():
    s = operator_template.render(operator =o)
    filnm = output_dir/o.name+".rst"
    operators.append(o.name)
    with open(filnm, 'w') as fp:
        fp.write(s)


##### ###########################################################################

import re
find_msml_comments = re.compile(r'/\*MSMLDOC(?P<meta>.*?)\*/',
                                re.DOTALL | re.MULTILINE)

def extract_cpp_documenation(filename):
    print "FOUND: %s" % filename
    with open(filename) as handle:
        content = handle.read()
    return find_msml_comments.findall(content)

cpp_docs = path("docs/source/extension")

def clean_comment(c):
    lines = c.strip().replace("\t", "    ").split("\n")

    def spaces(s):
        for i,c in enumerate(s):
            if c == ' ': continue
            return i

    sp = min(map(spaces, lines))
    return map(lambda s: s[sp:], lines)

def build_cpp_documentation(folder):
    cpp_files = path(folder).walkfiles("*.h")
    comments = {fn : extract_cpp_documenation(fn) for fn in cpp_files}

    output_dir = cpp_docs #/ folder.namebase
    #output_dir.mkdir_p()

    counter = 0
    print "WRITE: %s" % (output_dir/folder.name+".rst")
    with open(output_dir/folder.name+".rst",'w') as fp:
        for cts in comments.values():
                for c in cts:
                    for line in clean_comment(c):
                        fp.write(line)
                        fp.write("\n")
                    fp.write("\n\n")



for folder in path("operators/").listdir():
    if folder.isdir() and folder.endswith("Operators"):
        build_cpp_documentation(folder)


