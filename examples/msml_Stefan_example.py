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

#load scene
for scenario in msmlFiles:
   fileTree = etree.parse(scenario)
   msmlNode = fileTree.getroot()
   scnWriter = SOFAExporter(msmlNode, alphabetNode)
   scnWriter.cachingEnabled = 1      
   head, tail = ntpath.split(scenario)
   #targetFilename = 
   filenameSCN = tail[0:-3]+"scn"
   print filenameSCN
   print ntpath.join(msmlNode.get("directory"),filenameSCN)
   scnWriter.writeSCN(alphabetNode, msmlNode, os.path.join(msmlNode.get("directory"),filenameSCN) )
   
#test generic exporter_old

msmlProcessingFiles = ["../Testdata/LiverExample/postProcessingExample.xml"]

for scenario in msmlProcessingFiles:
   fileTree = etree.parse(scenario)
   msmlNode = fileTree.getroot()
   genericWriter = GenericExporter(msmlNode, alphabetNode)
   genericWriter.cachingEnabled = 1      
   head, tail = ntpath.split(scenario)
   #targetFilename = 
   filenameSCN = tail[0:-3]+"scn"
   print filenameSCN
   print ntpath.join(msmlNode.get("directory"),filenameSCN)
   genericWriter.processMSML(alphabetNode, msmlNode, os.path.join(msmlNode.get("directory"),filenameSCN) )
   
   
abaqusProcessingFiles = ["../Testdata/LiverExample/liverExampleSimple.xml"]

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