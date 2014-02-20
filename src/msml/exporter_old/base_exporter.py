#TODO LICENSE

from lxml import etree
import os
import imp, sys
import os.path
import shutil
import ntpath
import os.path

from msml import lib_prefix

__author__= ""  #TODO
__date__  = ""  #TODO
__version__= "" #TODO




class BaseExporter:
  
   rootNodeMSML = 0
   rootNodeMSMLAlphabet = 0
   cachingEnabled = 1
   inputDirectory = ""
   outputDirectory = ""
      
   def __init__(self, _rootNodesMSML, _rootNodeMSMLAlphabet, _inputDirectory, _outputDirectory):

      
      self.rootNodeMSML = _rootNodesMSML
      self.rootNodeMSMLAlphabet = _rootNodeMSMLAlphabet
      

      #store input/output directory
      self.inputDirectory = _inputDirectory
      self.outputDirectory = _outputDirectory
      if(not os.path.exists(_outputDirectory)):
          os.makedirs(_outputDirectory)

      
   
   def findNodeNyName(self,name):
      #print name 
      nodeList = []
      for node in self.rootNodeMSML.iter():
         if(node.get("name") == name):
            nodeList.append(node)
      if(len(nodeList) == 0):
         print "Error, node ",name," not found"
      elif(len(nodeList) == 1):
         returnNode = nodeList[0]
      else:
         print "Error, several nodes named",name
      return returnNode
      
   def findNodeTypeInAlphabet(self, nodeType):
      nodeList = []
      for node in  self.rootNodeMSMLAlphabet.iter():
         if((node.tag == nodeType) and len(node)):
            nodeList.append(node)
      if(len(nodeList) == 0):
         print "Error, node ",nodeType," not found"
      elif(len(nodeList) == 1):
         returnNode = nodeList[0]
      else:
         print "Error, several nodes of type ",nodeType
      return returnNode
      
   def executeOperator(self, targetNodeAlphabet, targetNode, inputValue):
      #find operator directory
      #print "Executing operator ", targetNodeAlphabet
      
      directoriesList = self.rootNodeMSMLAlphabet.iter("operatorDirectories")
      print "Directories ", directoriesList
      validDirectory = []
      
      for directories in directoriesList:
        for directory in directories:
            print directory.get("path")     
            #check here if path is the right one
            moduleName = "lib" + targetNodeAlphabet.get("moduleName")
            wholeFilenameLib = os.path.join( directory.get("path") , moduleName )
            print wholeFilenameLib
            #print wholeFilenameLib + ".so"
            #if any throws python error.
            if(os.path.isfile(wholeFilenameLib + ".so") or os.path.isfile(wholeFilenameLib + ".a") or os.path.isfile(wholeFilenameLib + ".lib") or os.path.isfile(wholeFilenameLib + ".dll") or os.path.isfile(wholeFilenameLib + ".pyd")):
                    

               validDirectory = directory.get("path")
               if(validDirectory[-1] != os.path.sep):
                   validDirectory = validDirectory + os.path.sep
                
      if(not(len(validDirectory))):
         print "Operator ",targetNodeAlphabet.get("moduleName") ,"could not be found, please check operator directories settings in MSML_Alphabet/msml_operators/"
         return
   
      validDirectoryList = []
      validDirectoryList.append(validDirectory)

      f, filename, description = imp.find_module(lib_prefix() + targetNodeAlphabet.get("moduleName"), validDirectoryList)
      currentOperatorModule =  imp.load_module(targetNodeAlphabet.get("moduleName"), f, filename, description)      
      #print("Current module name is"+targetNodeAlphabet.get("moduleName"))
      
      #print "Attributes are.."
      #dir(currentOperatorModule)
      #print "finished"

      moduleName = "currentOperatorModule"
      methodName = targetNodeAlphabet.get("methodName")
      
      parameterNames = []
      parameterTypes = []
      parameterList = []
      #For each parameter of the operators xml defintion: find value in msml node => ordered parameterList => c++ 
      if (targetNodeAlphabet.find("parameters") is not None) :     
          for parameter in targetNodeAlphabet.find("parameters"):
             parameterNames.append(parameter.tag)
             parameterTypes.append(parameter.get("type"))
             paraTypes = parameter.get("type").split(".")
             print paraTypes
             
             #TODO: load default values from config file
             
             if( (len(paraTypes) == 2) and (paraTypes[-2] == "vector") ):            
                currentParameter = []
                if(paraTypes[-1] == "float"):
                   exec("currentParameter = "+moduleName+"."+"VecDouble()")
                if(paraTypes[-1] == "int"):
                   exec("currentParameter = "+moduleName+"."+"VecUInt()")
                   
                #evalString = "currentParameter = "+moduleName+"."+ parameter.get("type")+"()"
                #exec(evalString)
                valueList = targetNode.get(parameter.tag).split() 
                for value in valueList:
                   if(paraTypes[-1] == "float"):
                      currentParameter.append(float(value))
                   if(paraTypes[-1] == "int"):
                      currentParameter.append(int(value))
                  # print value
                parameterList.append(currentParameter)
             elif (paraTypes[-1] == "int"):
                parameterList.append(int(targetNode.get(parameter.tag)))
             elif (paraTypes[-1] == "float"):
                parameterList.append(float(targetNode.get(parameter.tag)))
             elif (paraTypes[-1] == "double"):
                parameterList.append(float(targetNode.get(parameter.tag)))
             elif (paraTypes[-1] == "bool"):
                 #bool(str aStr) returns true if aStr is not "".
                parameterList.append(targetNode.get(parameter.tag) in ['true', 'True', 'TRUE', '1', 'yes'])
             elif (paraTypes[0] == "file"): #hack: Accept linked nodes as parameters to allow multiple inputs
                filePath = targetNode.get(parameter.tag)                    
                if(filePath[0] == "@"):
                    currentLinkedNodeName = filePath[1:]
                    #recursive call
                    filePath = self.evaluateNode(targetNode, currentLinkedNodeName)
                    parameterList.append(filePath)
                    #else: just copy if file exists
                else:
                    if(~ os.path.isabs(filePath)):
                    #follow relative path from MSML file to data file and generate absolute path.       
                        filePath = str(os.path.abspath(os.path.join(self.inputDirectory, filePath)))
                        parameterList.append(filePath)
                   
             else:
                parameterList.append(targetNode.get(parameter.tag))
          
            
            
         
      output = []
      outputFilename = []
      finalMethodCall = "output = currentOperatorModule"+"."+methodName+"("+"inputValue"
      #check if output filename is defined, if so: add to function 
      outputParameterValue = targetNode.get(targetNodeAlphabet.find("outputName").getchildren()[0].tag )
               
      if(outputParameterValue != None ):
         outputParameterFormat = targetNodeAlphabet.find("outputFormats").getchildren()[0].tag 
         if(outputParameterFormat.split(".")[0] == "file"):
            #convert to absolute path of result directory           
            head, tail = ntpath.split(outputParameterValue)      
            if(len(head) == 0):
               outputParameterValue = os.path.join(self.outputDirectory, outputParameterValue)
            outputFilename = outputParameterValue
            finalMethodCall += ", " + "outputFilename"
             
      if(inputValue != None ):
         inputValueFormat = targetNodeAlphabet.find("inputFormats").getchildren()[0].tag 
         if(inputValueFormat.split(".")[0] == "file"):
            if(~ os.path.isabs(inputValue)):
               #follow relative path from MSML file to data file and generate absolute path.       
               inputValue = str(os.path.abspath(os.path.join(self.inputDirectory, inputValue)))
               
      i=0
      for parameter in parameterList:
         finalMethodCall = finalMethodCall + "," + "parameterList[" + str(i) + "]"
         i+=1
      
      finalMethodCall+= ")"
      #targetNode.get(targetNodeAlphabet.get("outputName"))
     # print finalMethodCall
      
      #output = currentOperatorModule.computeIndicesFromBoxROI(inputValue,parameterList[0],parameterList[1])
      print inputValue
      print finalMethodCall
      exec(finalMethodCall)
      
     # print '[%s]' % ', '.join(map(str, output))
     
      #if( (targetNodeAlphabet.get("type")[1:4]  != file) and (targetNodeAlphabet.get("type") != "string") ):
      #   outputPythonList = []
      #   for value in output:
      #      outputPythonList.append(value)
      #   output = outputPythonList
      
      #convert to string, markus: do we really need string here? We have to convert back to int in some cases. E.g. using several getIndices Operators + lookup_table to assemble the stiffness array.  
      print output
      outputFormat = targetNodeAlphabet.find("outputFormats").getchildren()[0].tag.split(".")
      if((len(outputFormat) ==2) and (outputFormat[-2] == "vector")):
         output = '%s' % ', '.join(map(str, output))
      #else:
      #   output = '%s' % ', '.join(map(str, output))   
     # print output 
      print "operator output is: ", output  
      return output
         
      
      
      
#parameterName = "\" working!!\""
#finalCommand = moduleName+"."+functionName+"("+parameterName+")"
#print finalCommand
#myString = eval(finalCommand)
      
      
   def evaluateNode(self, outputNode, targetNodeName):
      targetNode = self.findNodeNyName(targetNodeName)  
      
      #check if data type or operator type
      #find node types in MSMLAlphabet
      outputNodeAlphabet = self.findNodeTypeInAlphabet(outputNode.tag)
      targetNodeAlphabet = self.findNodeTypeInAlphabet(targetNode.tag)
      
     # print outputNodeAlphabet
     # print targetNodeAlphabet
      
      outputTypes=0
      outputFormats=0
      outputNames=0
      targetTypes=0
      targetFormats=0
      targetNames=0
                 
      #print targetNodeAlphabet.tag
      if(targetNodeAlphabet.get("type") == "data"):
         targetNames = targetNodeAlphabet.find("dataName").getchildren()[0].tag
         targetFormats = targetNodeAlphabet.find("dataFormats").getchildren()[0].tag
         targetTypes = [ targetNodeAlphabet.tag ]
         #targetType = targetNodeAlphabet.find("dataType").getchildren()[0].tag
             
      elif(targetNodeAlphabet.get("type") == "operator"):
         targetNames = targetNodeAlphabet.find("outputName").getchildren()[0].tag
         targetFormats = targetNodeAlphabet.find("outputFormats").getchildren()[0].tag
         targetTypes = [ targetNodeAlphabet.find("outputTypes").getchildren()[0].tag ]
          
      else:
         print "targetNode", targetNodeAlphabet.tag, " is neither data nor operator type, no evaluation possible!"
         return
         
      if(outputNodeAlphabet.get("type") == "data"):
          outputNames = outputNodeAlphabet.find("dataName").getchildren()[0].tag
          outputFormats = outputNodeAlphabet.find("dataFormats").getchildren()[0].tag
          outputTypes = [ outputNodeAlphabet.tag ]
          #outputType = outputNodeAlphabet.find("dataType").getchildren()[0].tag
             
      elif(outputNodeAlphabet.get("type") == "operator"):
          outputNames = outputNodeAlphabet.find("outputName").getchildren()[0].tag
          outputFormats = outputNodeAlphabet.find("inputFormats").getchildren()[0].tag
          outputTypes = map(lambda x:x.tag, outputNodeAlphabet.find("inputTypes").getchildren())
             
      else:
         print "outputNode", outputNodeAlphabet.tag, " is neither data nor operator type, no evaluation possible!"
         return
      
      outputFormat = outputFormats
      outputName =  outputNames
      print outputTypes
      print targetTypes
      outputType = set(outputTypes).intersection(targetTypes).pop()
      targetType= set(outputTypes).intersection(targetTypes).pop()
      targetFormat = targetFormats
      targetName = targetNames
        
      #compare format and types
      if((not len(set(outputTypes).intersection(targetTypes))) or (targetFormat != outputFormat)):
          print "Types or formats do not match output format is",outputFormat, " target Format is", targetFormat
          print len(set(outputTypes).intersection(targetTypes))
          return         
       
      
      #check link exists (always the case for data, maybe the case for oeprator)
      output = []
      
      if(targetNodeAlphabet.get("type") == "data"):
         if(targetNode.get(targetName)):
            #check if name is linked, if so then recursively call evlauate node
            #print "target node is ",targetNode," with targetName ",targetName
            output = targetNode.get(targetName)
            if(output[0] == "@"):
               currentLinkedNodeName = output[1:]
               #recursive call
               output = self.evaluateNode(targetNode, currentLinkedNodeName)
            #else: just copy if file exists
            else:
               if(targetFormat.split(".")[0] == "file"):
                  head, tail = ntpath.split(output)  
                  copyFilename = os.path.join(self.outputDirectory, tail)
                  try: #a simple if condition output != copyFilename does not work with \ / mixtures (win)
                     shutil.copy(output, copyFilename )
                     output = tail
                  except:
                      print "Error during copy operation." 
                                                        
               
      if(targetNodeAlphabet.get("type") == "operator"):
         inputName = targetNodeAlphabet.find("inputName").getchildren()[0].tag
         inputValue = targetNode.get(inputName)      
         #print inputName, inputValue
         if(inputValue[0] == "@"):
            currentLinkedNodeName = inputValue[1:]
            #recursive call
            inputValue = self.evaluateNode(targetNode, currentLinkedNodeName)       
               
         #print inputValue, targetNode, targetName
         #if operator: execute and 
         if(targetNodeAlphabet.get("type") == "operator"):
            print targetNodeAlphabet
           # print targetNode
           # print inputValue
            output = self.executeOperator(targetNodeAlphabet, targetNode, inputValue)
          
     # print output
      #print targetFormat
      #return output value
      if(self.cachingEnabled):
         #if output is file -> convert to absolute path
         if(targetFormat.split(".")[0] == "file"):
            #print output
            head, tail = ntpath.split(output)      
            if(len(head) == 0):
               output = os.path.join(self.outputDirectory ,output)
           # else:
           #    output = self.rootNodeMSML.get("directory") + platform_path_slash() + tail
         targetNode.set(targetName, output)
         
      print "Output from target node name " + targetNodeName + " is "+output

      return output
      
   def startDataNodeEvaluation(self, targetNode):
      #get alphabet node
      targetNodeAlphabet = self.findNodeTypeInAlphabet(targetNode.tag)
      if(targetNodeAlphabet == None):
         print "Error, can not find node type ", targetNode.tag, " in alphabet"
      if(targetNodeAlphabet.get("type") != "data"):
         print "Error, startDataNodeEvlaution can only be called from data nodes"
      targetName = targetNodeAlphabet.find("dataName").getchildren()[0].tag
      targetFormat = targetNodeAlphabet.find("dataFormats").getchildren()[0].tag
      
      output = []
      if(targetNode.get(targetName)):
            #check if name is linked, if so then recursively call evlauate node
            #print "target node is ",targetNode," with targetName ",targetName
            output = targetNode.get(targetName)
            if(output[0] == "@"):
               currentLinkedNodeName = output[1:]
               #recursive call
               output = self.evaluateNode(targetNode, currentLinkedNodeName)
            else:
               if(targetFormat.split(".")[0] == "file"):
                  head, tail = ntpath.split(output)  
                  copyFilename = os.path.join(self.outputDirectory ,tail)
                  #if output is file -> convert to absolute path
                  if(targetFormat.split(".")[0] == "file"):
#<<<<<<< HEAD:MSML_Python/base_exporter.py
#                    head, tail = ntpath.split(output)        
#                    head2, tail2 = ntpath.split(self.rootNodeMSML.base) 
#                   output = os.path.abspath(os.path.join(head2, output))
#=======
                    head, tail = ntpath.split(output)
                    output = os.path.abspath(os.path.join(self.inputDirectory, output))
#>>>>>>> f6af1dca971576c13ce4d94343de0fe27460c626:src/msml/exporter/base_exporter.py
                    if(output != copyFilename):
                     shutil.copy(output, copyFilename )
                     output = tail      
      
      if(self.cachingEnabled):
         #if output is file -> convert to absolute path
         if(targetFormat.split(".")[0] == "file"):
            head, tail = ntpath.split(output)
            print head
            if(len(head) == 0):
               output = os.path.join( self.outputDirectory , output)
         targetNode.set(targetName, output)
         
      return output
   
   def evaluateIndexGroup(self,indexGroupNode):
      #check if index group node is a link
      indices = []
      if(indexGroupNode.get("indices")[0] == "@"):
         #in this case check the link         
         currentLinkedIndexGroupName = indexGroupNode.get("indices")[1:]
         currentLinkedIndexGroup = indexGroupNode.find(currentLinkedIndexGroupName)
         print  currentLinkedIndexGroupName
         print  currentLinkedIndexGroup
         print  currentLinkedIndexGroup.get("indices")
         if not len(currentLinkedIndexGroup):
            print "Error: index group ", currentLinkedIndexGroupName, " not found"
         else:
            print currentLinkedIndexGroup
            #indices = self.evaluateIndexGroup(currentLinkedIndexGroup)      
      else:
         indices = constraintRegionNode.get("indices")
         
      return indices
      

