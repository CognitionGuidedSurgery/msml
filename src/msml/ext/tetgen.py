__author__ = 'weigl'

#print(os.environ['LD_LIBRARY_PATH'])

from warnings import warn

from msml.model.exceptions import MSMLUnknownModuleWarning


try:
    import TetgenOperatorsPython as cpp
except ImportError, e:
    warn("Could not load TetgenOperatorsPython. "
         "This is the C++-Modul. Have you successfully compiled and installed it? "
         "Error is %s" % e,
         MSMLUnknownModuleWarning, 0)


def createVolumeMeshTetgen(surfaceMesh, preserveBoundary=True, meshFilename=None):
    '''

    '''
    #preserveBoundary = bool(preserveBoundary)
    return cpp.createVolumeMeshTetgen(surfaceMesh, meshFilename, preserveBoundary)
