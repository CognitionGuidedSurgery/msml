__author__ = 'suwelack'
from msml.io.mapper.base_mapping import *
#from msml.model.generated.msmlScene import *
#from msml.model.base import *
import msml.model.base as base
import msml.model.generated.msmlScene as gen
import msml.model.generated.msmlBase as mbase
from msml.exporter.base import *
import uuid

class Msml2MsmlMapping(BaseMapping):

    def __init__(self, exporter):
        self._exporter = exporter
        BaseMapping.__init__(self)

    @complete_map_pre(base.SceneObject)
    def map_SceneObject_pre(self, element,parent_source,parent_target, source,target):
        #add scene object to scenario
        sc = gen.Scene()
        sc.id =  element.id + '_scene'
        parent_target.add_child(sc)
        parent_target.scene = sc
        #add environment
        en = gen.Environment()
        en.id = element.id + '_env'
        parent_target.add_child(en)
        parent_target.environment = en
        #add scene object
        so = gen.SceneObject()
        so.id = element.id
        sc.add_child(so)
        sc.addObject(so)

        self.init_sets(element, so, source, target)
        return so


    @complete_map_post(base.SceneObject)
    def map_SceneObject_post(self, element,parent_source,parent_target,source,target):
        pass

    @complete_map_pre(base.ObjectConstraints)
    def map_object_constraints_pre(self, element,parent_source,parent_target,source,target):
        cg = gen.ConstraintGroup()
        cg.id = parent_source.id+'_constraint_group'
        parent_target.add_child(cg)
        parent_target.addConstraintGroup(cg)
        return cg



    @complete_map_post(base.ObjectConstraints)
    def map_object_constraints_post(self, element,parent_source,parent_target,source,target):
        pass

    @complete_map_pre(base.ContactGeometry)
    def map_contact_geometry_pre(self, element,parent_source,parent_target,source,target):
        pass



    @complete_map_post(base.ContactGeometry)
    def map_contact_geometry_post(self, element,parent_source,parent_target,source,target):
        pass

    @complete_map_pre(base.MaterialRegion)
    def map_MaterialRegion_pre(self, element,parent_source,parent_target,source,target):
        mr = gen.MaterialRegion()
        mr.id = element.id
        #indices_vec = self._exporter.get_value_from_memory(element, 'indices')
        mr.indexset = self.get_index_set( element, mbase.ElementSet(), parent_target)

        parent_target.add_child(mr)
        parent_target.addMaterialRegion(mr)

        return mr



    @complete_map_post(base.MaterialRegion)
    def map_MaterialRegion_post(self, element,parent_source,parent_target,source,target):
        pass

    @complete_map_pre(base.Mesh)
    def map_Mesh_pre(self, element,parent_source,parent_target,source,target):
        mesh = gen.Mesh()
        mesh.id = element.id + "_mesh"
        meshData = gen.MeshDataObject()
        meshData.id = element.id + "_mesh_data"

        if element.type == 'linearTet':
            meshData.logicaltype = mbase.LinearTetrahedralMesh()
        else:
            raise MSMLError("Mesh logical type %s for mesh %s not supported by msml2msml mapping" % (element.type, element.id))
        meshData.value = self._exporter.get_value_from_memory(mesh.id.strip("_mesh"))
        meshData.physicaltype = type(meshData.value)
        parent_target.add_child(mesh)
        parent_target.mesh = mesh
        mesh.add_child(meshData)
        mesh.dataobject = meshData
        return mesh




    @complete_map_post(base.Mesh)
    def map_Mesh_post(self, element,parent_source,parent_target,source,target):
        pass

    @complete_map_pre(base.ObjectElement)
    def map_ObjectElement_pre(self, element,parent_source,parent_target,source,target):
        if element.tag == 'linearElasticMaterial':
            lem = gen.LinearElasticProperty()
            lem.poissonratio = element.attributes['poissonRatio']
            lem.youngmodulus = element.attributes['youngModulus']
            lem.id = element.attributes['id']
            parent_target.add_child(lem)
            parent_target.addMaterialProperty(lem)
            return lem


        elif element.tag == 'mass':
            m = gen.MassProperty()
            m.density = element.attributes['massDensity']
            m.id = element.attributes['id']
            parent_target.add_child(m)
            parent_target.addMaterialProperty(m)
            return m

        elif element.__tag__ == 'fixedConstraint':
            co = gen.FixedConstraint()
            co.id = self.get_id(element.attributes['id'])
            co.indices = self.get_index_set( element, mbase.ElementSet(), parent_target.parent)

            parent_target.add_child(co)
            parent_target.addConstraint(co)
            return co





    @complete_map_post(base.ObjectElement)
    def map_ObjectElement_post(self, element,parent_source,parent_target,source,target):
        pass

    @complete_map_pre(base.SceneObjectSets)
    def map_SceneObjectSets_pre(self, element,parent_source,parent_target, source,target):
        pass

    @complete_map_post(base.SceneObjectSets)
    def map_SceneObjectSets_post(self, element,parent_source,parent_target,source,target):
        pass

    def get_id(self, inputId):
        if inputId is None:
            return uuid.uuid4()
        else:
            return inputId
        
    def get_step(self, name):
        if name is not None:
            return name
        else:
            return self._exporter._msml_file.env.simulation[0].name

    def get_index_set(self, indexgroup, indexType, target_so):

        id = indexgroup.indices
        id = id.strip('${}')



        for set in target_so.indexsetcontainer.getIndexSetDatas():
            if set.id == id:
                return set

        indexData = gen.IndexSetDataObject()
        indexData.id = id
        indexData.physicaltype = mbase.MSMLListUI()
        if isinstance(indexType, mbase.NodeSet):
            indexData.logicaltype = mbase.NodeSet()
        elif isinstance(indexType, mbase.ElementSet):
            indexData.logicaltype = mbase.ElementSet()
        elif isinstance(indexType, mbase.FaceSet):
            indexData.logicaltype = mbase.FaceSet()
        else:
            raise MSMLError("Index type %s is not supported by MSML2MSMLMapping" % (indexType))

        indexData.value = self._exporter.get_value_from_memory(indexgroup, 'indices')
        target_so.indexsetcontainer.add_child(indexData)
        target_so.indexsetcontainer.addIndexSetData(indexData)


        return indexData

    def init_sets(self,source_so, target_so, source,target):
        ic = gen.IndexSetContainer()
        target_so.add_child(ic)
        target_so.indexsetcontainer = ic

        #element sets
        for set in source_so.sets.elements:
            indexData = gen.IndexSetDataObject()
            indexData.id = set.id
            indexData.physicaltype = mbase.MSMLListUI()
            indexData.logicaltype = mbase.ElementSet()
            indexData.value = self._exporter.get_value_from_memory(set, 'indices')
            ic.add_child(indexData)
            ic.addIndexSetData(indexData)

        #enode sets
        for set in source_so.sets.nodes:
            indexData = gen.IndexSetDataObject()
            indexData.id = set.id
            indexData.physicaltype = mbase.MSMLListUI()
            indexData.logicaltype = mbase.NodeSet()
            indexData.value = self._exporter.get_value_from_memory(set, 'indices')
            ic.add_child(indexData)
            ic.addIndexSetData(indexData)

        #face sets
        for set in source_so.sets.surfaces:
            indexData = gen.IndexSetDataObject()
            indexData.id = set.id
            indexData.physicaltype = mbase.MSMLListUI()
            indexData.logicaltype = mbase.FaceSet()
            indexData.value = self._exporter.get_value_from_memory(set, 'indices')
            ic.add_child(indexData)
            ic.addIndexSetData(indexData)



