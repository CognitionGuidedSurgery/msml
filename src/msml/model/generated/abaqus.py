from msml.model.generated.msmlScene import *

class PartContainer(IdNode):


   def __init__(self):
      self._parts = list()
      IdNode.__init__(self)



   def addPart(self,part):
      self._parts.append(part)
   def getParts(self):
      return self._parts




class Material(IdNode):



   @property
   def materialproperty(self):
      return self._materialproperty

   @materialproperty.setter
   def materialproperty(self, value):
      self._materialproperty = value





class InputDeck(ScenarioRoot):


   def __init__(self):
      self._fieldoutputs = list()
      self._loads = list()
      self._outputrequests = list()
      self._historyoutputs = list()
      self._materials = list()
      self._steps = list()
      ScenarioRoot.__init__(self)


   @property
   def assembly(self):
      return self._assembly

   @assembly.setter
   def assembly(self, value):
      self._assembly = value

   @property
   def boundaryconditioncontainer(self):
      return self._boundaryconditioncontainer

   @boundaryconditioncontainer.setter
   def boundaryconditioncontainer(self, value):
      self._boundaryconditioncontainer = value

   @property
   def partcontainer(self):
      return self._partcontainer

   @partcontainer.setter
   def partcontainer(self, value):
      self._partcontainer = value


   def addFieldOutput(self,fieldoutput):
      self._fieldoutputs.append(fieldoutput)
   def getFieldOutputs(self):
      return self._fieldoutputs

   def addLoad(self,load):
      self._loads.append(load)
   def getLoads(self):
      return self._loads

   def addOutputRequest(self,outputrequest):
      self._outputrequests.append(outputrequest)
   def getOutputRequests(self):
      return self._outputrequests

   def addHistoryOutput(self,historyoutput):
      self._historyoutputs.append(historyoutput)
   def getHistoryOutputs(self):
      return self._historyoutputs

   def addMaterial(self,material):
      self._materials.append(material)
   def getMaterials(self):
      return self._materials

   def addStep(self,step):
      self._steps.append(step)
   def getSteps(self):
      return self._steps




class FieldOutput(IdNode):
    pass






class Part(IdNode):


   def __init__(self):
      self._sections = list()
      IdNode.__init__(self)


   @property
   def meshdataobject(self):
      return self._meshdataobject

   @meshdataobject.setter
   def meshdataobject(self, value):
      self._meshdataobject = value

   @property
   def indexsetcontainer(self):
      return self._indexsetcontainer

   @indexsetcontainer.setter
   def indexsetcontainer(self, value):
      self._indexsetcontainer = value


   def addSection(self,section):
      self._sections.append(section)
   def getSections(self):
      return self._sections




class Instance(IdNode):



   @property
   def partid(self):
      return self._partid

   @partid.setter
   def partid(self, value):
      self._partid = value





class BoundaryConditionContainer(IdNode):


   def __init__(self):
      self._boundaryconditions = list()
      IdNode.__init__(self)



   def addBoundaryCondition(self,boundarycondition):
      self._boundaryconditions.append(boundarycondition)
   def getBoundaryConditions(self):
      return self._boundaryconditions




class BoundaryCondition(IdNode):



   @property
   def indexset(self):
      return self._indexset

   @indexset.setter
   def indexset(self, value):
      self._indexset = value





class FixedDisplacementBoundaryCondition(BoundaryCondition):
    pass






class Load(IdNode):
    pass






class DisplacementRotationBoundaryCondition(BoundaryCondition):
    pass






class Section(IdNode):



   @property
   def indexset(self):
      return self._indexset

   @indexset.setter
   def indexset(self, value):
      self._indexset = value





class Step(IdNode):
    pass






class Assembly(IdNode):


   def __init__(self):
      self._instances = list()
      IdNode.__init__(self)


   @property
   def indexsetcontainer(self):
      return self._indexsetcontainer

   @indexsetcontainer.setter
   def indexsetcontainer(self, value):
      self._indexsetcontainer = value


   def addInstance(self,instance):
      self._instances.append(instance)
   def getInstances(self):
      return self._instances




class HistoryOutput(IdNode):
    pass






