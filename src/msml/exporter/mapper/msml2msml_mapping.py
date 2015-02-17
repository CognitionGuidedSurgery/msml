__author__ = 'suwelack'
from msml.exporter.mapper.base_mapping import *
from msml.model.generated.msmlScene import *
from msml.model.base import *

class Msml2MsmlMapping(BaseMapping):
    @complete_map_pre('msml.model.base.SceneObject')
    def map_SceneObject_pre(self, element,source,target):
        print "hello"

    @complete_map_post('msml.model.base.SceneObject')
    def map_SceneObject_post(self, element,source,target):
        print "hello"
