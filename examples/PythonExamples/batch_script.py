#TODO: Better handling of path to msml python src

import sys
sys.path.append('../../src/')
import msml
import run_msml
import copy
from lxml import etree     
import os
import ntpath

#load msml file
msmlFilePath = os.path.abspath("postProcessingExample.xml")
head, msmlFileName =  ntpath.split(msmlFilePath)

 
#load alphabet
os.chdir('../../src/')
msml.createAlphabet()
alphabetNode = msml.loadAlphabet()

directoryIn = os.path.abspath("../examples/PythonExamples/ToColor")
directoryOut = os.path.abspath("../examples/PythonExamples/Colored")

os.chdir(directoryIn)
for files in os.listdir("."):
   fileTree = etree.parse(msmlFilePath)
   msmlRoot = fileTree.getroot()    
   msmlNode = msmlRoot.find(".//colorMeshOperator")
   msmlNode.set("coloredMesh",directoryOut+ "/" + files)
   msmlNode.set("mesh",directoryIn+ "/" + files)
   run_msml.run_msml(msmlRoot, alphabetNode, directoryIn, directoryOut, files + "_processedBy_" + msmlFileName, 'generic', True, True, True)

