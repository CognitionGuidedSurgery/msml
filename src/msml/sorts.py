# -*- encoding: utf-8 -*-
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


"""
Sorts logic.

Factory and Cache for Sorts in MSML.

Currently there are two disjoint sorts hierarchies.

1. format
2. type

`format` describes the kind of storage (e.g. file format)
`type` is the definition of the ground data type (e.g. vector of ints)
sortdef
## example

vector.int + file.vtk

result in: file_vtk__vector_int as subtype of file and vector


sortsdef => name of a sort, characterize by multiple path, seperated with »+«
path     => name/path in the class hierarchy, each class is seperated with ».«
"""

# __all__ = ["__author__", "__date__", "SortsDefinition", "get_sort", "default_sorts_definition"]

from msml.sortdef import *
from . import log
from .exceptions import MSMLException

__author__ = "Alexander Weigl"
__date__ = "2014-01-25, 2014-02-23"


class MSMLMissingConversionException(MSMLException): pass


class SortsDefinition(object):
    def __init__(self, default_sorts=True):
        self.logical_cache = {}
        self.physical_cache = {}
        self.sort_cache = {}

        if default_sorts:
            self._bulk_sorts_load(DEFAULTS_SORTS)

    def get_sort(self, physical, logical=None):
        pythontypes = {str: MSMLString, int: MSMLInt, float: MSMLFloat}
        if physical in pythontypes:
            physical = pythontypes[physical]

        if type(physical) is str:
            physical = self._find_physical(physical)

        if logical and type(logical) is str:
            logical = self._find_logical(logical)

        try:
            return self.sort_cache[physical, logical]
        except:
            s = Sort(physical, logical)
            self.sort_cache[physical, logical] = s
            return s

    def _find_logical(self, typestr):
        try:
            return self.logical_cache[typestr]
        except KeyError as e:
            log.warn("_logical type %s requested, but does not exist" % typestr)
            return None

    def _find_physical(self, fmtstr):
        try:
            return self.physical_cache[fmtstr]
        except KeyError as e:
            s = "physical type %s requested, but does not exist" % fmtstr
            log.error(s)
            raise BaseException(s)


    def register_logical(self, clazz, name=None):
        if not name: name = clazz.__name__
        self.logical_cache[name] = clazz
        return clazz

    def register_physical(self, clazz, name=None):
        if not name: name = clazz.__name__
        self.physical_cache[name] = clazz
        return clazz

    def register_type_with_name(self, name):
        def fn(clazz):
            return self.register_type(clazz, name)

        return fn

    def _bulk_sorts_load(self, defs):
        temp = (('_logical', self.register_logical),
                ('physical', self.register_physical))

        for tp, register in temp:
            for d in defs[tp]:
                if isinstance(d, (tuple, list)):
                    clazz = d[0]
                    names = d[1:]
                else:
                    clazz = d
                    names = tuple()

                if len(names) == 0:
                    names = (clazz.__name__,)

                for n in names:
                    register(clazz, n)


DEFAULTS_SORTS = {
    '_logical': [
        (MSMLLTop, "top", "object", "*"),
        Index,
        IndexSet,
        NodeSet,
        FaceSet,
        ElementSet,
        Mesh,
        VolumeMesh,
        TetrahedralVolume,
        HexahedralVolume,
        QuadraticTetrahedral,
        SurfaceMesh,
        TriangularSurface,
        SquareSurface,
        QuadraticTriangularSurface,
        Image3D,
        Image2D,
        SegmentationImage3D,
        VectorImage3D,
        Scalar,
        Indices,
        VonMisesStress,
        Vector,
        Force,
        Velocity,
        Tensor,
        Stress,
        Displacement,
        Position,
    ],

    'physical': [
        (InFile, 'file'),
        (MSMLString, "str", "string", "s"),
        (MSMLFloat, "float"),
        (MSMLInt, "int"),
        (bool, "bool"),
        (MSMLUInt, "uint"),
        (MSMLListF, "ListF", "vector.float"),
        (MSMLListUI, "ListUI", "vector.uint"),
        (MSMLListI, "ListI", "vector.int"),
        (VTK, "VTK", "vtk", "file.vtk"),
        (VTU, "VTU", "vtu", "file.vtu"),
        (VTI, "VTI", "vti", "file.vti"),
        (VTP, "VTP", "vtp", "file.vtp"), # TODO: add Hiflow3-InputFormat inp (including material IDs).
        DICOM,
        HDF5,
        (STL, "STL", "stl"),
        PNG,
        ctx,
        vdx,
        (TXT, 'TXT', 'txt'),
        (InFile, 'NRRD', 'nrrd'),  # TODO
        (GenericMesh, 'mesh'),
    ],
}

DEFAULT_SORTS_DEFINITION = SortsDefinition()


def default_sorts_definition():
    "return default sorts definition"
    return DEFAULT_SORTS_DEFINITION


def get_sort(t, f=None):
    """
    returns the type object for the given sort definition
    """
    return default_sorts_definition().get_sort(t, f)


def is_sort(x):
    return isinstance(x, type) or isinstance(x, Sort)

# #####################################################################################
# conversion
#
#
#
#
import networkx


def _ptype(o):
    return o if isinstance(o, type) else o.physical


class ConversionNetwork(networkx.DiGraph):
    def register_conversion(self, a, b, fn, precedence):
        assert is_sort(a) or isinstance(a, type)
        assert is_sort(b) or isinstance(b, type)
        assert callable(fn)

        a, b = _ptype(a), _ptype(b)

        self.add_node(a)
        self.add_node(b)

        self.add_edge(a, b, fn=fn, precedence=precedence)

    def converter(self, a, b):
        """returns a function that converts elements of type `a` to element with type `b`.

        """

        def c(n1, n2):
            data = self.get_edge_data(n1, n2)
            return data['fn']


        import inspect, itertools

        from_type = _ptype(a)
        to_type = _ptype(b)

        mro = inspect.getmro(from_type)  # inherited from

        resolve_order = [from_type] + list(mro)
        for start in resolve_order:
            try:
                (length, paths) = networkx.single_source_dijkstra(self, start, to_type, 'precedence')

                if to_type not in length:
                    continue  # not found a valid path, try super class

                path = paths[to_type]

                edges = zip(path[:-1], path[1:])
                converters = list(itertools.starmap(c, edges))

                def fn(val):
                    return reduce(lambda val, convert: convert(val),
                                  converters, val)

                return fn
            except KeyError as e:
                # : Unknown node
                pass

        raise MSMLMissingConversionException("Could not find a conversion for %s -> %s" % (from_type, to_type))


DEFAULT_CONVERSION_NETWORK = ConversionNetwork()


def default_conversion_network():
    return DEFAULT_CONVERSION_NETWORK


register_conversion = DEFAULT_CONVERSION_NETWORK.register_conversion
conversion = DEFAULT_CONVERSION_NETWORK.converter

# #######################################################################################################################
# # Default Conversions!
#

def _bool(s):
    if isinstance(s, bool):
        return s
    if s is None:
        return False
    if isinstance(s, str):
        return s.lower() in ('True', 'TRUE', 'true', 'on', 'yes')
    return bool(s)


def _list_of_type(s, t):
    """Convert an input `s` into a list of `t`
    :param s: string, list or tuple
    :param t: type of elements

    :type s: str
    :type t: type
    :return:
    :rtype: list[t]
    """

    if isinstance(s, str):
        s = map(lambda x: x.strip(), filter(lambda x: x != "", s.split(" ")))

    return map(t, s)


def _list_float(s):
    return _list_of_type(s, MSMLFloat)


def _list_integer(s):
    return _list_of_type(s, lambda x: MSMLInt(float(x)))


def _list_uinteger(s):
    return _list_of_type(s, lambda x: MSMLUInt(float(x)))


def _single_float_list(f):
    return list([f])


def _single_int_list(i):
    return list([i])


register_conversion(float, get_sort('vector.float'), _single_float_list, 100)
register_conversion(float, int, int, 100)
register_conversion(get_sort('float'), get_sort('int'), int, 100)
register_conversion(get_sort('int'), get_sort('str'), str, 100)
register_conversion(get_sort('int'), get_sort('str'), str, 100)
register_conversion(get_sort('vector.float'), get_sort('vector.int'), _list_integer, 100)
register_conversion(get_sort('vector.int'), get_sort('vector.float'), _list_float, 100)
register_conversion(int, get_sort('vector.int'), _single_int_list, 100)
register_conversion(list, get_sort('vector.float'), _list_float, 100)
register_conversion(list, get_sort('vector.int'), _list_float, 100)
register_conversion(str, get_sort("STL"), STL, 100)
register_conversion(str, get_sort("VTP"), VTP, 100)
register_conversion(str, get_sort("VTK"), VTK, 100)
register_conversion(str, get_sort("bool"), _bool, 100)
register_conversion(str, get_sort("ctx"), ctx, 100)
register_conversion(str, get_sort("float"), float, 100)
register_conversion(str, get_sort("int"), int, 100)
register_conversion(str, get_sort("str"), MSMLString, 100)
register_conversion(str, get_sort("vdx"), vdx, 100)
register_conversion(str, get_sort('VTI'), VTI, 100)
register_conversion(str, get_sort('vector.float'), _list_float, 100)
register_conversion(str, get_sort('vector.int'), _list_integer, 100)
register_conversion(tuple, get_sort('vector.float'), _list_float, 100)
register_conversion(tuple, get_sort('vector.int'), _list_float, 100)
register_conversion(unicode, get_sort("STL"), STL, 100)
register_conversion(unicode, get_sort("VTK"), VTK, 100)
register_conversion(unicode, get_sort("bool"), _bool, 100)
register_conversion(unicode, get_sort("float"), float, 100)
register_conversion(unicode, get_sort("int"), int, 100)
register_conversion(unicode, get_sort("str"), MSMLString, 100)
register_conversion(unicode, get_sort('VTI'), VTI, 100)
register_conversion(unicode, get_sort('vector.float'), _list_float, 100)
register_conversion(unicode, get_sort('vector.int'), _list_integer, 100)
register_conversion(type(None), bool, _bool, 100)
register_conversion(str, PNG, PNG, 100)
register_conversion(str, get_sort('NRRD'), InFile, 100)
register_conversion(str, TXT, InFile, 100)

# register_conversion(VTK, MSMLString, lambda x: MSMLString(x.filename + ";" + x.partname), 100)

try:
    from msml.ext.converters_python import vtk_mesh2generic_mesh
    register_conversion(VTK, get_sort('mesh'), vtk_mesh2generic_mesh, 100)


except:
    log.error("No Conversion VTK to GenericMesh avaible. Abaqus may not useable")

try:
    from msml.ext.misc import ConvertVTKToVTU
    import os.path

    def convert_vtk_to_vtu(vtk):
        """Convert VTK to VTU file format.
        :param vtk:
        :type vtk: VTK
        :return:
        :rtype: VTU
        """

        name = "%s_auto_converted.vtu" % vtk
        ConvertVTKToVTU(vtk, name)

        return VTU(name)

    register_conversion(VTK, VTU, convert_vtk_to_vtu, 100)
except:
    log.error("No Conversion VTK to VTU avaaible. Hiflow3 may not useable")
