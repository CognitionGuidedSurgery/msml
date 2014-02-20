
from lxml import etree
import os
import imp, sys
import os.path
import shutil
import ntpath
import os.path

from .base import Exporter


__author__= "Alexander Weigl"
__date__  = "2014-01-27"  #TODO
__version__= "0.1"

class SimpleExporter(Exporter):
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
     # print outputTypes
     # print targetTypes
      outputType = set(outputTypes).intersection(targetTypes).pop()
      targetType= set(outputTypes).intersection(targetTypes).pop()
      targetFormat = targetFormats
      targetName = targetNames
        
      #compare format and types
      if((not len(set(outputTypes).intersection(targetTypes))) or (targetFormat != outputFormat)):
          print "Types or formats do not match" 
          #print outputFormat
         # print targetFormat
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
                    head, tail = ntpath.split(output)
                    output = os.path.abspath(os.path.join(self.inputDirectory, output))
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
      

