import msml_controller
import copy
from lxml import etree     
import os
from sofa_exporter import SOFAExporter
from generic_exporter import GenericExporter
from abaqus_exporter import AbaqusExporter
import ntpath


__author__= ""  #TODO
__date__  = ""  #TODO
__version__= "" #TODO


###
import os
os.system("python printMSMLAlphabet.py")
###


#list of msml filenames
#msmlFiles = ["../Testdata/BunnyExample/bunnyExample.xml"]
msmlFiles = []#["../Testdata/LiverExample/liverExampleSimple.xml"]

#load alphabet
alphabetTree = etree.parse("alphabet.xml")
alphabetNode = alphabetTree.getroot()

  
   
abaqusProcessingFiles = ["../Testdata/RectumExample/rectumExample.xml"]

for scenario in abaqusProcessingFiles:
   fileTree = etree.parse(scenario)
   msmlNode = fileTree.getroot()
   inpWriter = AbaqusExporter(msmlNode, alphabetNode)
   inpWriter.cachingEnabled = 1      
   head, tail = ntpath.split(scenario)
   #targetFilename = 
   filenameSCN = tail[0:-3]+"inp"
   print filenameSCN
   print ntpath.join(msmlNode.get("directory"),filenameSCN)
   inpWriter.writeINP(alphabetNode, msmlNode, os.path.join(msmlNode.get("directory"),filenameSCN) )