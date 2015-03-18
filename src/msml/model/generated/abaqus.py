from msml.model.generated.msmlScene import *

class Part(IdNode):


   def __init__(self):
      self._sections = list()
      IdNode.__init__(self)


   @property
   def indexsetcontainer(self):
      return self._indexsetcontainer

   @indexsetcontainer.setter
   def indexsetcontainer(self, value):
      self._indexsetcontainer = value

   @property
   def meshdataobject(self):
      return self._meshdataobject

   @meshdataobject.setter
   def meshdataobject(self, value):
      self._meshdataobject = value


   def addSection(self,section):
      self._sections.append(section)
   def getSections(self):
      return self._sections




class BoundaryCondition(IdNode):



   @property
   def indexset(self):
      return self._indexset

   @indexset.setter
   def indexset(self, value):
      self._indexset = value





class FixedDisplacementBoundaryCondition(BoundaryCondition):
    pass






class Material(IdNode):
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




class MaterialTemplate(IdNode):
    pass






class Instance(IdNode):
    pass






class Step(IdNode):
    pass






class BoundaryConditionContainer(IdNode):
    pass






class PartContainer(IdNode):
    pass






class HistoryOutput(IdNode):
    pass






class InputDeck(ScenarioRoot):


   def __init__(self):
      self._fieldoutputs = list()
      self._outputrequests = list()
      self._materialtemplates = list()
      self._historyoutputs = list()
      self._boundaryconditioncontainers = list()
      self._parts = list()
      ScenarioRoot.__init__(self)


   @property
   def assembly(self):
      return self._assembly

   @assembly.setter
   def assembly(self, value):
      self._assembly = value


   def addFieldOutput(self,fieldoutput):
      self._fieldoutputs.append(fieldoutput)
   def getFieldOutputs(self):
      return self._fieldoutputs

   def addOutputRequest(self,outputrequest):
      self._outputrequests.append(outputrequest)
   def getOutputRequests(self):
      return self._outputrequests

   def addMaterialTemplate(self,materialtemplate):
      self._materialtemplates.append(materialtemplate)
   def getMaterialTemplates(self):
      return self._materialtemplates

   def addHistoryOutput(self,historyoutput):
      self._historyoutputs.append(historyoutput)
   def getHistoryOutputs(self):
      return self._historyoutputs

   def addBoundaryConditionContainer(self,boundaryconditioncontainer):
      self._boundaryconditioncontainers.append(boundaryconditioncontainer)
   def getBoundaryConditionContainers(self):
      return self._boundaryconditioncontainers

   def addPart(self,part):
      self._parts.append(part)
   def getParts(self):
      return self._parts




class Section(IdNode):



   @property
   def elementsetid(self):
      return self._elementsetid

   @elementsetid.setter
   def elementsetid(self, value):
      self._elementsetid = value

   @property
   def materialid(self):
      return self._materialid

   @materialid.setter
   def materialid(self, value):
      self._materialid = value





class DisplacementRotationBoundaryCondition(BoundaryCondition):
    pass






class FieldOutput(IdNode):
    pass






