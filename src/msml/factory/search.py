# region <gplv3>
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
# endregion <gplv3>

__author__ = 'Alexander Weigl'
__date__ = "2014-05-10"

import functools

import msml.env
import msml.sorts
import msml.sortdef
from msml.sorts import *
from msml.sortdef import *


class OperatorQuery(object):
    def __init__(self, alphabet=None):
        if alphabet is None:
            alphabet = msml.env.current_alphabet
        self.results = alphabet.operators.values()


    def __and__(self, other):
        next = OperatorQuery()
        next.results = other(self.results)
        return next

    def get(self):
        return self.results


def as_filter(predicate):
    def fn(*args, **kwargs):
        pred = predicate(*args, **kwargs)
        return functools.partial(filter, pred)

    functools.update_wrapper(fn, predicate)
    return fn


def slot_type(tp, slottype):
    if isinstance(tp, tuple):
        sort = get_sort(*tp)

    if isinstance(tp, str):
        sort = get_sort(tp)

    if isinstance(tp, type):
        sort = get_sort(tp)

    def _predicate(operator):
        if slottype == 'I':
            slots = operator.input.values()
        if slottype == 'O':
            slots = operator.output.values()
        if slottype == 'P':
            slots = operator.parameters.values()

        return any(map(lambda slot: slot.sort <= sort, slots))

    return _predicate


def applyall(*fn):
    def _inner(*args, **kwargs):
        return map(lambda f: f(*args, **kwargs), fn)

    return _inner


def every(*fn):
    a = applyall(*fn)

    def _inner(*args, **kwargs):
        return all(a(*args, **kwargs))

    return _inner


def some(*fn):
    a = applyall(*fn)

    def _inner(*args, **kwargs):
        return any(a(*args, **kwargs))

    return _inner


hasInputOfType = functools.partial(slot_type, slottype='I')
hasOutputOfType = functools.partial(slot_type, slottype='O')
hasParameterOfType = functools.partial(slot_type, slottype='P')

import operator


def names(operators):
    fn = operator.attrgetter('name')
    return map(fn, operators)


import msml.frontend

msml.frontend.App()
op = msml.env.current_alphabet.operators.values()
print names(filter(hasInputOfType(msml.sortdef.VTK), op))

print names(filter(
    every(
        hasParameterOfType(MSMLString),
        hasParameterOfType(bool)), op))

