from msml.model.baseClasses.msmlScene import *

class IdNode(Node):



   @property
   def id(self):
      return self._id

   @id.setter
   def id(self, value):
      self._id = value





class DataObject(IdNode):



   @property
   def logicaltype(self):
      return self._logicaltype

   @logicaltype.setter
   def logicaltype(self, value):
      self._logicaltype = value

   @property
   def physicaltype(self):
      return self._physicaltype

   @physicaltype.setter
   def physicaltype(self, value):
      self._physicaltype = value

   @property
   def value(self):
      return self._value

   @value.setter
   def value(self, value):
      self._value = value





class IndexSetDataObject(DataObject):
    pass






class MeshDataObject(DataObject):
    pass






class MaterialProperty(IdNode):
    pass






class ContinuumMechanicsProperty(MaterialProperty):
    pass






class ViscoelasticProperty(ContinuumMechanicsProperty):
    pass






class RayleighDampingProperty(ViscoelasticProperty):



   @property
   def alpha(self):
      return self._alpha

   @alpha.setter
   def alpha(self, value):
      self._alpha = value

   @property
   def beta(self):
      return self._beta

   @beta.setter
   def beta(self, value):
      self._beta = value





class SimulationEnvironment(Node):
    pass






class ContainerNode(Node):


   def __init__(self):
      self._childs = list()
      Node.__init__(self)



   def addChild(self,child):
      self._childs.append(child)
   def getChilds(self):
      return self._childs




class Nodes(ContainerNode):
    pass






class Scene(Node):


   def __init__(self):
      self._objects = list()
      Node.__init__(self)



   def addObject(self,object):
      self._objects.append(object)
   def getObjects(self):
      return self._objects




class IdContainerNode(ContainerNode):



   @property
   def id(self):
      return self._id

   @id.setter
   def id(self, value):
      self._id = value





class FluidMechanicsProperty(ContinuumMechanicsProperty):
    pass






class Elements(ContainerNode):
    pass






class Solver(IdNode):



   @property
   def dt(self):
      return self._dt

   @dt.setter
   def dt(self, value):
      self._dt = value

   @property
   def solvertype(self):
      return self._solvertype

   @solvertype.setter
   def solvertype(self, value):
      self._solvertype = value

   @property
   def processingunit(self):
      return self._processingunit

   @processingunit.setter
   def processingunit(self, value):
      self._processingunit = value

   @property
   def iterations(self):
      return self._iterations

   @iterations.setter
   def iterations(self, value):
      self._iterations = value





class LinearSolver(Solver):
    pass






class IndexSetContainer(IdNode):


   def __init__(self):
      self._indexsetdatas = list()
      IdNode.__init__(self)



   def addIndexSetData(self,indexsetdata):
      self._indexsetdatas.append(indexsetdata)
   def getIndexSetDatas(self):
      return self._indexsetdatas




class SimulationStep(IdNode):


   def __init__(self):
      self._solvers = list()
      IdNode.__init__(self)



   def addSolver(self,solver):
      self._solvers.append(solver)
   def getSolvers(self):
      return self._solvers




class SolidMechanicsProperty(ContinuumMechanicsProperty):
    pass






class ElasticityProperty(SolidMechanicsProperty):
    pass






class LinearElasticProperty(ElasticityProperty):



   @property
   def poissonratio(self):
      return self._poissonratio

   @poissonratio.setter
   def poissonratio(self, value):
      self._poissonratio = value

   @property
   def youngmodulus(self):
      return self._youngmodulus

   @youngmodulus.setter
   def youngmodulus(self, value):
      self._youngmodulus = value





class Mesh(IdNode):



   @property
   def dataobject(self):
      return self._dataobject

   @dataobject.setter
   def dataobject(self, value):
      self._dataobject = value





class MaterialRegion(IdNode):


   def __init__(self):
      self._materialpropertys = list()
      IdNode.__init__(self)


   @property
   def indexset(self):
      return self._indexset

   @indexset.setter
   def indexset(self, value):
      self._indexset = value


   def addMaterialProperty(self,materialproperty):
      self._materialpropertys.append(materialproperty)
   def getMaterialPropertys(self):
      return self._materialpropertys




class ODESolver(Solver):
    pass






class ConstraintGroup(IdNode):


   def __init__(self):
      self._constraints = list()
      IdNode.__init__(self)



   def addConstraint(self,constraint):
      self._constraints.append(constraint)
   def getConstraints(self):
      return self._constraints




class Constraint(IdNode):



   @property
   def step(self):
      return self._step

   @step.setter
   def step(self, value):
      self._step = value

   @property
   def indexset(self):
      return self._indexset

   @indexset.setter
   def indexset(self, value):
      self._indexset = value





class Scenario(ScenarioRoot):



   @property
   def environment(self):
      return self._environment

   @environment.setter
   def environment(self, value):
      self._environment = value

   @property
   def scene(self):
      return self._scene

   @scene.setter
   def scene(self, value):
      self._scene = value





class MassProperty(ContinuumMechanicsProperty):



   @property
   def density(self):
      return self._density

   @density.setter
   def density(self, value):
      self._density = value





class Faces(ContainerNode):
    pass






class OutputRequest(IdNode):
    pass






class FixedConstraint(Constraint):
    pass






class SceneObject(IdNode):


   def __init__(self):
      self._constraintgroups = list()
      self._materialregions = list()
      self._outputs = list()
      IdNode.__init__(self)


   @property
   def mesh(self):
      return self._mesh

   @mesh.setter
   def mesh(self, value):
      self._mesh = value

   @property
   def sets(self):
      return self._sets

   @sets.setter
   def sets(self, value):
      self._sets = value

   @property
   def indexsetcontainer(self):
      return self._indexsetcontainer

   @indexsetcontainer.setter
   def indexsetcontainer(self, value):
      self._indexsetcontainer = value


   def addConstraintGroup(self,constraintgroup):
      self._constraintgroups.append(constraintgroup)
   def getConstraintGroups(self):
      return self._constraintgroups

   def addMaterialRegion(self,materialregion):
      self._materialregions.append(materialregion)
   def getMaterialRegions(self):
      return self._materialregions

   def addOutput(self,output):
      self._outputs.append(output)
   def getOutputs(self):
      return self._outputs




class Environment(Node):
    pass






