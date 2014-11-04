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

__all__ = ['get_needed_features']

from functools import wraps

PREDICATES = []
def feature_predicate(fn):
    PREDICATES.append(fn)
    return fn

def length_gt_x(x):
    def decorator(pred):
        @wraps(pred)
        def fn(obj):
            return len(pred(obj)) > x
        return fn
    return decorator

length_non_zero = length_gt_x(0)
length_gt_one = length_gt_x(1)


def foreach_sceneobject(pred):
    @wraps(pred)
    def fn(msmlfile):
        for sceneobject in msmlfile.scene:
            r = pred(sceneobject)
            if r:
                return True
        return False
    return fn

def foreach_object_element(pred):
    @wraps(pred)
    def fn(msmlfile):
        seq = list()
        for sceneobject in msmlfile.scene:

            seq += map(pred, sceneobject.output)

            for region in sceneobject.material:
                seq += map(pred, region)

            for cs in sceneobject.constraints:
                seq += map(pred, cs)

        return seq
    return fn

def with_env_solver(pred):
    @wraps(pred)
    def fn(msmlfile):
        return (pred(msmlfile.env.solver), )
    return fn


def get_features():
    def prepare_name(name):
        return name[1:]

    return {prepare_name(p.func_name) : p
            for p in PREDICATES}

@feature_predicate
@length_non_zero
def _scene_objects_supported(msmlfile):
    return msmlfile.scene

@feature_predicate
@length_gt_one
def _multiple_scene_objects(msmlfile):
    return msmlfile.scene

@feature_predicate
@foreach_sceneobject
@length_non_zero
def _sets_nodes_supported(sceneobject):
    return sceneobject.sets.nodes

@feature_predicate
@foreach_sceneobject
@length_non_zero
def _sets_elements_supported(sceneobject):
    return sceneobject.sets.elements

@feature_predicate
@foreach_sceneobject
@length_non_zero
def _sets_surface_supported(sceneobject):
    return sceneobject.sets.surfaces

@feature_predicate
@foreach_sceneobject
@length_non_zero
def _material_region_supported(sceneobject):
    return sceneobject.material

@feature_predicate
@foreach_sceneobject
@length_gt_one
def _amount_material_region_n(sceneobject):
    return  sceneobject.material

@feature_predicate
@foreach_object_element
def _object_atribute_x_supported(objectelement):
    return "object_element_%s_supported" % objectelement.tag


@feature_predicate
@foreach_sceneobject
@length_non_zero
def _constraints_supported(sceneobject):
    return sceneobject.constraints

@feature_predicate
@foreach_sceneobject
@length_gt_one
def _amount_constraints_n(sceneobject):
    return sceneobject.constraints

@feature_predicate
@foreach_sceneobject
@length_non_zero
def _output_supported(sceneobject):
    return sceneobject.output

@feature_predicate
@with_env_solver
def _environment_linearSolver_x_supported(solver):
    return "env_linearsolver_%s_supported" % solver.linearSolver

@feature_predicate
@with_env_solver
def _environment_processingUnit_x_supported(solver):
    return "env_processingunit_%s_supported" % solver.processingUnit

@feature_predicate
@with_env_solver
def _environment_timeIntegration_x_supported(solver):
    return "env_timeintegration_%s_supported" % solver.timeIntegration

@feature_predicate
@with_env_solver
def _environment_preconditioner_x_supported(solver):
    return "env_preconditioner_%s_supported" % solver.preconditioner

@feature_predicate
@length_non_zero
def _environment_simulation_steps_supported(msmlfile):
    return msmlfile.env.simulation

@feature_predicate
@length_gt_one
def _environment_multiple_simulation_steps_supported(msmlfile):
    return msmlfile.env.simulation

from itertools import starmap

def get_needed_features(msml_file):
    def eval_predicate(name, pred):
        r = pred(msml_file)
        if r:
            if r is True: return (name,)
            else: return r
        else:
            return tuple()

    fpred = get_features()
    s = set()
    for features in starmap(eval_predicate, fpred.iteritems()):
        for f in features:
            s.add(f)
    return s