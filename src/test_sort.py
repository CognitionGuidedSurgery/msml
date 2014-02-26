__author__ = 'weigl'

from msml.sorts import *
from msml.model.sortdef import *

S = get_sort(str)
I = get_sort(int)
F = get_sort('filename')
MF = get_sort('meshfile')
LMF = get_sort('linmeshfile')
TMF = get_sort('trimeshfile')
QMF = get_sort('quatmeshfile')

print S, I, F

assert not (S < I)
assert not (I < S)
assert not (S > I)
assert not (S == I)
assert S != I


assert LMF < MF < F
assert TMF < MF < F
assert QMF < MF < F

######
#
#

register_conversion(S, I, int, 100)
register_conversion(S, F, float, 100)

vertcvt = lambda s: Vertice(* map(float, s.split(' ')))

register_conversion(S, Vertice, vertcvt, 75)
register_conversion(S, Vertices,lambda s: map(lambda x: vertcvt(x.strip("; ")),
                                                s.split(";")), 10)


S2I = conversion(S, I)
print S2I("2")
print S2I("22434")
print S2I("2521434")

print conversion(S, F)("52.2")
print conversion(S, Vertice)("1 2 3")
print conversion(S, Vertices)("1 2 3; 4 5 6")