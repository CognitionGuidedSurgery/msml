from msml.io.mapper.base_mapping import * 
 
import msml.model.generated.msmlScene as mod
import msml.model.generated.abaqus as ab

class MSML2AbaqusMapping(BaseMapping):




    @complete_map_pre(mod.Constraint)
    def map_Constraint_pre(self, element,parent_source,parent_target, source,target):
        print('map_Constraint_pre not implemented')


    @complete_map_post(mod.Constraint)
    def map_Constraint_post(self, element,parent_source,parent_target,source,target):
        print('map_Constraint_post not implemented')






    @complete_map_pre(mod.ConstraintGroup)
    def map_ConstraintGroup_pre(self, element,parent_source,parent_target, source,target):
        print('map_ConstraintGroup_pre not implemented')


    @complete_map_post(mod.ConstraintGroup)
    def map_ConstraintGroup_post(self, element,parent_source,parent_target,source,target):
        print('map_ConstraintGroup_post not implemented')






    @complete_map_pre(mod.ContainerNode)
    def map_ContainerNode_pre(self, element,parent_source,parent_target, source,target):
        print('map_ContainerNode_pre not implemented')


    @complete_map_post(mod.ContainerNode)
    def map_ContainerNode_post(self, element,parent_source,parent_target,source,target):
        print('map_ContainerNode_post not implemented')






    @complete_map_pre(mod.ContinuumMechanicsProperty)
    def map_ContinuumMechanicsProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_ContinuumMechanicsProperty_pre not implemented')


    @complete_map_post(mod.ContinuumMechanicsProperty)
    def map_ContinuumMechanicsProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_ContinuumMechanicsProperty_post not implemented')






    @complete_map_pre(mod.DataObject)
    def map_DataObject_pre(self, element,parent_source,parent_target, source,target):
        print('map_DataObject_pre not implemented')


    @complete_map_post(mod.DataObject)
    def map_DataObject_post(self, element,parent_source,parent_target,source,target):
        print('map_DataObject_post not implemented')






    @complete_map_pre(mod.ElasticityProperty)
    def map_ElasticityProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_ElasticityProperty_pre not implemented')


    @complete_map_post(mod.ElasticityProperty)
    def map_ElasticityProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_ElasticityProperty_post not implemented')






    @complete_map_pre(mod.Elements)
    def map_Elements_pre(self, element,parent_source,parent_target, source,target):
        print('map_Elements_pre not implemented')


    @complete_map_post(mod.Elements)
    def map_Elements_post(self, element,parent_source,parent_target,source,target):
        print('map_Elements_post not implemented')






    @complete_map_pre(mod.Environment)
    def map_Environment_pre(self, element,parent_source,parent_target, source,target):
        print('map_Environment_pre not implemented')


    @complete_map_post(mod.Environment)
    def map_Environment_post(self, element,parent_source,parent_target,source,target):
        print('map_Environment_post not implemented')






    @complete_map_pre(mod.Faces)
    def map_Faces_pre(self, element,parent_source,parent_target, source,target):
        print('map_Faces_pre not implemented')


    @complete_map_post(mod.Faces)
    def map_Faces_post(self, element,parent_source,parent_target,source,target):
        print('map_Faces_post not implemented')






    @complete_map_pre(mod.FixedConstraint)
    def map_FixedConstraint_pre(self, element,parent_source,parent_target, source,target):
        print('map_FixedConstraint_pre not implemented')


    @complete_map_post(mod.FixedConstraint)
    def map_FixedConstraint_post(self, element,parent_source,parent_target,source,target):
        print('map_FixedConstraint_post not implemented')






    @complete_map_pre(mod.FluidMechanicsProperty)
    def map_FluidMechanicsProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_FluidMechanicsProperty_pre not implemented')


    @complete_map_post(mod.FluidMechanicsProperty)
    def map_FluidMechanicsProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_FluidMechanicsProperty_post not implemented')






    @complete_map_pre(mod.IdContainerNode)
    def map_IdContainerNode_pre(self, element,parent_source,parent_target, source,target):
        print('map_IdContainerNode_pre not implemented')


    @complete_map_post(mod.IdContainerNode)
    def map_IdContainerNode_post(self, element,parent_source,parent_target,source,target):
        print('map_IdContainerNode_post not implemented')






    @complete_map_pre(mod.IdNode)
    def map_IdNode_pre(self, element,parent_source,parent_target, source,target):
        print('map_IdNode_pre not implemented')


    @complete_map_post(mod.IdNode)
    def map_IdNode_post(self, element,parent_source,parent_target,source,target):
        print('map_IdNode_post not implemented')






    @complete_map_pre(mod.IndexSetContainer)
    def map_IndexSetContainer_pre(self, element,parent_source,parent_target, source,target):
        print('map_IndexSetContainer_pre not implemented')


    @complete_map_post(mod.IndexSetContainer)
    def map_IndexSetContainer_post(self, element,parent_source,parent_target,source,target):
        print('map_IndexSetContainer_post not implemented')






    @complete_map_pre(mod.IndexSetDataObject)
    def map_IndexSetDataObject_pre(self, element,parent_source,parent_target, source,target):
        print('map_IndexSetDataObject_pre not implemented')


    @complete_map_post(mod.IndexSetDataObject)
    def map_IndexSetDataObject_post(self, element,parent_source,parent_target,source,target):
        print('map_IndexSetDataObject_post not implemented')






    @complete_map_pre(mod.LinearElasticProperty)
    def map_LinearElasticProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_LinearElasticProperty_pre not implemented')


    @complete_map_post(mod.LinearElasticProperty)
    def map_LinearElasticProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_LinearElasticProperty_post not implemented')






    @complete_map_pre(mod.LinearSolver)
    def map_LinearSolver_pre(self, element,parent_source,parent_target, source,target):
        print('map_LinearSolver_pre not implemented')


    @complete_map_post(mod.LinearSolver)
    def map_LinearSolver_post(self, element,parent_source,parent_target,source,target):
        print('map_LinearSolver_post not implemented')






    @complete_map_pre(mod.MSMLError)
    def map_MSMLError_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLError_pre not implemented')


    @complete_map_post(mod.MSMLError)
    def map_MSMLError_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLError_post not implemented')






    @complete_map_pre(mod.MSMLException)
    def map_MSMLException_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLException_pre not implemented')


    @complete_map_post(mod.MSMLException)
    def map_MSMLException_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLException_post not implemented')






    @complete_map_pre(mod.MSMLOperatorWarning)
    def map_MSMLOperatorWarning_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLOperatorWarning_pre not implemented')


    @complete_map_post(mod.MSMLOperatorWarning)
    def map_MSMLOperatorWarning_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLOperatorWarning_post not implemented')






    @complete_map_pre(mod.MSMLUnknownFunctionWarning)
    def map_MSMLUnknownFunctionWarning_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLUnknownFunctionWarning_pre not implemented')


    @complete_map_post(mod.MSMLUnknownFunctionWarning)
    def map_MSMLUnknownFunctionWarning_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLUnknownFunctionWarning_post not implemented')






    @complete_map_pre(mod.MSMLUnknownModuleWarning)
    def map_MSMLUnknownModuleWarning_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLUnknownModuleWarning_pre not implemented')


    @complete_map_post(mod.MSMLUnknownModuleWarning)
    def map_MSMLUnknownModuleWarning_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLUnknownModuleWarning_post not implemented')






    @complete_map_pre(mod.MSMLWarning)
    def map_MSMLWarning_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLWarning_pre not implemented')


    @complete_map_post(mod.MSMLWarning)
    def map_MSMLWarning_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLWarning_post not implemented')






    @complete_map_pre(mod.MSMLXMLParseError)
    def map_MSMLXMLParseError_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLXMLParseError_pre not implemented')


    @complete_map_post(mod.MSMLXMLParseError)
    def map_MSMLXMLParseError_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLXMLParseError_post not implemented')






    @complete_map_pre(mod.MSMLXMLUnknownTagWarning)
    def map_MSMLXMLUnknownTagWarning_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLXMLUnknownTagWarning_pre not implemented')


    @complete_map_post(mod.MSMLXMLUnknownTagWarning)
    def map_MSMLXMLUnknownTagWarning_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLXMLUnknownTagWarning_post not implemented')






    @complete_map_pre(mod.MSMLXMlWarning)
    def map_MSMLXMlWarning_pre(self, element,parent_source,parent_target, source,target):
        print('map_MSMLXMlWarning_pre not implemented')


    @complete_map_post(mod.MSMLXMlWarning)
    def map_MSMLXMlWarning_post(self, element,parent_source,parent_target,source,target):
        print('map_MSMLXMlWarning_post not implemented')






    @complete_map_pre(mod.MassProperty)
    def map_MassProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_MassProperty_pre not implemented')


    @complete_map_post(mod.MassProperty)
    def map_MassProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_MassProperty_post not implemented')






    @complete_map_pre(mod.MaterialProperty)
    def map_MaterialProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_MaterialProperty_pre not implemented')


    @complete_map_post(mod.MaterialProperty)
    def map_MaterialProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_MaterialProperty_post not implemented')






    @complete_map_pre(mod.MaterialRegion)
    def map_MaterialRegion_pre(self, element,parent_source,parent_target, source,target):
        print('map_MaterialRegion_pre not implemented')


    @complete_map_post(mod.MaterialRegion)
    def map_MaterialRegion_post(self, element,parent_source,parent_target,source,target):
        print('map_MaterialRegion_post not implemented')






    @complete_map_pre(mod.Mesh)
    def map_Mesh_pre(self, element,parent_source,parent_target, source,target):
        print('map_Mesh_pre not implemented')


    @complete_map_post(mod.Mesh)
    def map_Mesh_post(self, element,parent_source,parent_target,source,target):
        print('map_Mesh_post not implemented')






    @complete_map_pre(mod.MeshDataObject)
    def map_MeshDataObject_pre(self, element,parent_source,parent_target, source,target):
        print('map_MeshDataObject_pre not implemented')


    @complete_map_post(mod.MeshDataObject)
    def map_MeshDataObject_post(self, element,parent_source,parent_target,source,target):
        print('map_MeshDataObject_post not implemented')






    @complete_map_pre(mod.Node)
    def map_Node_pre(self, element,parent_source,parent_target, source,target):
        print('map_Node_pre not implemented')


    @complete_map_post(mod.Node)
    def map_Node_post(self, element,parent_source,parent_target,source,target):
        print('map_Node_post not implemented')






    @complete_map_pre(mod.Nodes)
    def map_Nodes_pre(self, element,parent_source,parent_target, source,target):
        print('map_Nodes_pre not implemented')


    @complete_map_post(mod.Nodes)
    def map_Nodes_post(self, element,parent_source,parent_target,source,target):
        print('map_Nodes_post not implemented')






    @complete_map_pre(mod.ODESolver)
    def map_ODESolver_pre(self, element,parent_source,parent_target, source,target):
        print('map_ODESolver_pre not implemented')


    @complete_map_post(mod.ODESolver)
    def map_ODESolver_post(self, element,parent_source,parent_target,source,target):
        print('map_ODESolver_post not implemented')






    @complete_map_pre(mod.ObjectAlreadyInInventoryError)
    def map_ObjectAlreadyInInventoryError_pre(self, element,parent_source,parent_target, source,target):
        print('map_ObjectAlreadyInInventoryError_pre not implemented')


    @complete_map_post(mod.ObjectAlreadyInInventoryError)
    def map_ObjectAlreadyInInventoryError_post(self, element,parent_source,parent_target,source,target):
        print('map_ObjectAlreadyInInventoryError_post not implemented')






    @complete_map_pre(mod.OutputRequest)
    def map_OutputRequest_pre(self, element,parent_source,parent_target, source,target):
        print('map_OutputRequest_pre not implemented')


    @complete_map_post(mod.OutputRequest)
    def map_OutputRequest_post(self, element,parent_source,parent_target,source,target):
        print('map_OutputRequest_post not implemented')






    @complete_map_pre(mod.RayleighDampingProperty)
    def map_RayleighDampingProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_RayleighDampingProperty_pre not implemented')


    @complete_map_post(mod.RayleighDampingProperty)
    def map_RayleighDampingProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_RayleighDampingProperty_post not implemented')






    @complete_map_pre(mod.Scenario)
    def map_Scenario_pre(self, element,parent_source,parent_target, source,target):
        return parent_target, type(mod.Scene())




    @complete_map_post(mod.Scenario)
    def map_Scenario_post(self, element,parent_source,parent_target,source,target):
        pass



    @complete_map_pre(mod.Scene)
    def map_Scene_pre(self, element,parent_source,parent_target, source,target):
        return parent_target, type(mod.SceneObject())


    @complete_map_post(mod.Scene)
    def map_Scene_post(self, element,parent_source,parent_target,source,target):
        pass






    @complete_map_pre(mod.SceneObject)
    def map_SceneObject_pre(self, element,parent_source,parent_target, source,target):
        part = ab.Part()
        part.id = element.id
        parent_target.add_child(part)
        parent_target.addPart(part)

        return part, None






    @complete_map_post(mod.SceneObject)
    def map_SceneObject_post(self, element,parent_source,parent_target,source,target):
        pass






    @complete_map_pre(mod.SimulationEnvironment)
    def map_SimulationEnvironment_pre(self, element,parent_source,parent_target, source,target):
        print('map_SimulationEnvironment_pre not implemented')


    @complete_map_post(mod.SimulationEnvironment)
    def map_SimulationEnvironment_post(self, element,parent_source,parent_target,source,target):
        print('map_SimulationEnvironment_post not implemented')






    @complete_map_pre(mod.SimulationStep)
    def map_SimulationStep_pre(self, element,parent_source,parent_target, source,target):
        print('map_SimulationStep_pre not implemented')


    @complete_map_post(mod.SimulationStep)
    def map_SimulationStep_post(self, element,parent_source,parent_target,source,target):
        print('map_SimulationStep_post not implemented')






    @complete_map_pre(mod.SolidMechanicsProperty)
    def map_SolidMechanicsProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_SolidMechanicsProperty_pre not implemented')


    @complete_map_post(mod.SolidMechanicsProperty)
    def map_SolidMechanicsProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_SolidMechanicsProperty_post not implemented')






    @complete_map_pre(mod.Solver)
    def map_Solver_pre(self, element,parent_source,parent_target, source,target):
        print('map_Solver_pre not implemented')


    @complete_map_post(mod.Solver)
    def map_Solver_post(self, element,parent_source,parent_target,source,target):
        print('map_Solver_post not implemented')






    @complete_map_pre(mod.ViscoelasticProperty)
    def map_ViscoelasticProperty_pre(self, element,parent_source,parent_target, source,target):
        print('map_ViscoelasticProperty_pre not implemented')


    @complete_map_post(mod.ViscoelasticProperty)
    def map_ViscoelasticProperty_post(self, element,parent_source,parent_target,source,target):
        print('map_ViscoelasticProperty_post not implemented')






