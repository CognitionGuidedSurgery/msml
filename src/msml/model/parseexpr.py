#-*- encoding: utf-8 -*-

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


__author__ = 'Alexander Weigl'
__date__ = "2014-02-02"

from pyparsing import *
import pyparsing as pp

def test(expr, string):
    print "T: %s" % string,
    try:
        r = expr.parseString(string)
        print " ... ok"
        print "\t %s" % r
    except pp.ParseException, e:
        print " ... error"
        print "%s^" % (' ' *(e.col +2 )), "   ", e

from collections import namedtuple

FNC = namedtuple("FNC", 'toks')
VAL = namedtuple("VAL", 'toks')

def create_reference(string, loc, toks):
    if isinstance(toks[-1] , bool):
        return FNC(toks[:-1])
    else:
        return VAL(toks)

T_START = Literal("${").suppress()
T_IDENTIFIER =  Word(alphanums+"'_-$+")
T_SEP = Literal(".").suppress()
T_CALL = Literal('()').setParseAction(lambda *args: True)
T_PIPE = Literal("|")
T_END = Literal("}").suppress()
T_ANY = Word(alphanums+"!§%&/()=?ß-~_-,.;:<>'")

pointedids = T_IDENTIFIER + ZeroOrMore(T_SEP + T_IDENTIFIER)
refexpr = T_START +  pointedids + Optional( T_CALL | ( T_PIPE + pointedids))+ T_END

refexpr.setParseAction(create_reference)

TESTS = [
    "${abc}",
    "${abc()}",
    "${abc.def()}",
    "${abc.ef}",
    "${os.getcwd}/test.html",
    "${os.getcwd}/test.${os.getext}",
    "${os.getcwd()}/test.${os.getext}",
    "${'yyyy-mm-dd'|datetime.date}"
]

complete = OneOrMore( (NotAny(T_START) +  T_ANY) | refexpr)
map(lambda t: test(complete, t), TESTS)
