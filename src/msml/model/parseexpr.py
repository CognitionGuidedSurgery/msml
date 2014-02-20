#-*- encoding: utf-8 -*-

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
