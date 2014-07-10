__author__ = 'suwelack'

import msml.frontend
import msml.env
from msml.model import *

class Runner(object):
    def __init__(self, file=None, exporter=None, output_dir = None):

        self._file = file
        self._exporter = exporter
        self._output_dir = output_dir

        self._theApp = msml.frontend.App(exporter=exporter, output_dir = output_dir)

        self._mfile = self._theApp._load_msml_file(file)


    def executeMSML(self):

        self._memory = self._theApp.execute_msml(self._mfile)


    def setDisplacements(self, indices, displacements):
        print('Setting displacements...')

       # assert isinstance(mfile, MSMLFile)
       #
       #  sceneobject = mfile.scene[0]
       #  cs = sceneobject.constraints
       #
       #  assert isinstance(cs, ObjectConstraints)
       #
       #  for displacementConstraint in cs.constraints:
       #      assert isinstance(displacementConstraint, ObjectElement)
       #
       #      if displacementConstraint.tag == 'displacementConstraint':
       #          break
       #
       #  displacementConstraint.attributes['attribute'] ...



#    def init_msml_system(self):
#        msml.env.load_user_file()
#        self._load_alphabet()