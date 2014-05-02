__author__ = 'weigl'

from msml.sorts import *
from pprint import  pprint
pprint(default_sorts_definition().physical_cache)
pprint(default_sorts_definition().logical_cache)


S = get_sort("str")
I = get_sort(int)
F = get_sort(float)

print S, "    ", I


# MF = get_sort('mesh_file')
# LMF = get_sort('lin_mesh_file')
# TMF = get_sort('tri_mesh_file')
# QMF = get_sort('quat_mesh_file')
#
# print S, I, F
#
assert not (S < I)
assert not (I < S)
assert not (S > I)
assert not (S == I)
assert S != I



S2I = conversion(S, I)
print S2I("2")
print S2I("22434")
print S2I("2521434")

print conversion(S, F)("52.2")
