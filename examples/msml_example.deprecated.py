import msml_controller
import copy
from lxml import etree     
import os
from sofa_exporter import SOFAExporter
import ntpath

###
import os
os.system("printMSMLAlphabet.py")
###


#list of msml filenames
testDataDir = "E:\\GIT\\msml\\Testdata\\"
#msmlFiles = ["CGALi2vLungs/LungsSuperHighValues.xml"]
#msmlFiles = ["CGALi2vLungs/LungsContact_new.xml"]
#msmlFiles = ["CGALi2vExample/CGALExample.xml"]
#msmlFiles = ["CGALi2vExample/CGALExampleAndSurface.xml"]

msmlFiles = ["BunnyExample\\bunnyExample.xml"]
#msmlFiles.append()

#load alphabet
alphabetTree = etree.parse("alphabet.xml")
alphabetNode = alphabetTree.getroot()

#load scene
for scenario_file in msmlFiles:
   scenario = testDataDir + scenario_file
   fileTree = etree.parse(scenario)
   msmlNode = fileTree.getroot()
   scnWriter = SOFAExporter(msmlNode, alphabetNode)
   scnWriter.cachingEnabled = 1      
   head, tail = ntpath.split(scenario)
   #targetFilename = 
   filenameSCN = tail[0:-3]+"scn"
   print filenameSCN
   print ntpath.join(msmlNode.get("directory"),filenameSCN)
   scnWriter.writeSCN(alphabetNode, msmlNode, os.path.join(msmlNode.get("directory"), filenameSCN))