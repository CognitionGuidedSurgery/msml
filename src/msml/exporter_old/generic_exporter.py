from lxml import etree     
import os
from .base_exporter import BaseExporter


class GenericExporter(BaseExporter):  
      
   def processMSML(self, alphabetNode, msmlRootNode, filename):
      for msmlNode in msmlRootNode.iterchildren():
         print "Processing node " + msmlNode.tag
         targetNodeAlphabet = self.findNodeTypeInAlphabet(msmlNode.tag)
         if(targetNodeAlphabet == None):
            print "Error, can not find node type ", targetNode.tag, " in alphabet"
         elif(targetNodeAlphabet.get("type") == "data"):
            self.startDataNodeEvaluation( msmlNode)

      treeMSML = etree.ElementTree( msmlRootNode)
      processedFilename = os.path.splitext(filename)[0]+"GenericProcessed.xml"
      treeMSML.write(processedFilename, pretty_print=True)
      