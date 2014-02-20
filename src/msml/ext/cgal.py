__author__ = 'weigl'

from ..model.exceptions import MSMLUnknownModuleWarning
from warnings import  warn
try:
    import CGALOperatorsPython as cpp

except ImportError, e:
    warn("Could not import CGALOperatorsPython"
         "This is the C++-Modul. Have you successfully compiled and installed it? "
         "Error is %s" % e,
         MSMLUnknownModuleWarning, 0)



def CreateVolumeMeshi2v(*values):
    #converters = [str, str, bool, float, float, float, float, float, bool, bool, bool, bool]
    #from itertools import starmap
    #args = list(starmap(lambda conv, val: conv(val), zip(converters,values)))
    return cpp.CreateVolumeMeshi2v(*values)

def CreateVolumeMeshs2v(*values):
    #converters = [str, str, bool, float, float, float, float, float, bool, bool, bool, bool]
    #from itertools import starmap
    #args = list(starmap(lambda conv, val: conv(val), zip(converters,values)))
    return cpp.CreateVolumeMeshs2v(*values)

