__author__ = 'suwelack'


from msml.io.mapper.base_mapping import *

import msml.model.generated.msmlScene as mod
import msml.model.generated.abaqus as ab
import msml.model.generated.msmlBase as mbase
from jinja2 import Template, Environment, PackageLoader

class Abaqus2StringMapping(BaseMapping):

    def __init__(self):
        self._env = Environment( keep_trailing_newline=False,loader=PackageLoader('msml.io.mapper', 'templates'))

    @complete_map_pre(ab.InputDeck)
    def map_InputDeck_pre(self, element,parent_source,parent_target, source,target):

        template = self._env.get_template('InputDeck_template.html')
        returnStr = template.render()
        target.append(returnStr)

        return target, ab.PartContainer


    @complete_map_post(ab.InputDeck)
    def map_InputDeck_post(self, element,parent_source,parent_target,source,target):

        return None,None


    @complete_map_pre(ab.PartContainer)
    def map_PartContainer_pre(self, element,parent_source,parent_target, source,target):

        template = self._env.get_template('PartContainer_template.html')
        returnStr = template.render()
        target.append(returnStr)

        return target, ab.Part



    @complete_map_post(ab.PartContainer)
    def map_PartContainer_post(self, element,parent_source,parent_target,source,target):


        return None,None


    @complete_map_pre(ab.Part)
    def map_Part_pre(self, element,parent_source,parent_target, source,target):
        template = self._env.get_template('Part_template.html')
        returnStr = template.render(id=element.id)
        target.append(returnStr)

        return target, mod.MeshDataObject


    @complete_map_post(ab.Part)
    def map_Part_post(self, element,parent_source,parent_target,source,target):

        return None,None

    @complete_map_pre(mod.MeshDataObject)
    def map_MeshDataObject_pre(self, element,parent_source,parent_target, source,target):

        template = self._env.get_template('MeshDataObject_template.html')
        vertNumber = len(element.value.vertices)/3
        returnStr = template.render(sizes=element.value.cell_sizes, connectivity=element.value.connectivity, vertices=element.value.vertices, vertNumber = vertNumber)
        target.append(returnStr)

        return target, None


    @complete_map_post(mod.MeshDataObject)
    def map_MeshDataObject_post(self, element,parent_source,parent_target,source,target):

        return None,None


    @complete_map_pre(ab.Instance)
    def map_Instance_pre(self, element,parent_source,parent_target, source,target):
        template = self._env.get_template('Instance_template.html')
        returnStr = template.render(id = element.id, partId = element.partid)
        target.append(returnStr)
        return None,None


    @complete_map_post(ab.Instance)
    def map_Instance_post(self, element,parent_source,parent_target,source,target):

        return None,None


    @complete_map_pre(ab.Assembly)
    def map_Assembly_pre(self, element,parent_source,parent_target, source,target):
        template = self._env.get_template('Assembly_template.html')
        returnStr = template.render(id = element.id)
        target.append(returnStr)
        return None,None


    @complete_map_post(ab.Assembly)
    def map_Assembly_post(self, element,parent_source,parent_target,source,target):

        return None,None
