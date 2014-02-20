#!/usr/bin/env python

"""
this is the startup script for msml

run "msml.py --help" to show all parameters
"""

import optparse
import os
import sys
import os.path
import ntpath
import subprocess
from lxml import etree

import msml


def get_option_parser():
    parser = optparse.OptionParser()

    #text parameter
    parser.add_option("-f", "--file", dest="filename", help="MSML file", metavar="FILE")
    parser.add_option("-e", "--exporter_old", dest="exportEngine", help="Specify exporter_old engine; sofa, abaqus or generic",
                      default='generic')
    parser.add_option("-d", "--directory", dest="outputDirectory", help="output directory (must be an absolute path)",
                      metavar="DIRECTORY")

    #boolean (flag) options
    parser.add_option('-r', '--rebuildAlphabet', help='rebuild alphabet', dest='rebuildAlphabetFlag', default=False,
                      action='store_true')
    parser.add_option('-n', '--nocaching', help='enable/disable caching', dest='cachingFlag', default=True,
                      action='store_false')
    parser.add_option("-s", "--start", dest="runsimulation", help="Start the simulation (only SOFA exporter_old)",
                      default=False, action='store_true')
    parser.add_option("-p", "--postProcessing", dest="postProcessing",
                      help="Process postProcessing section after simulation (requires --start flag)", default=False,
                      action='store_true')

    return parser


#default entry point with arguments from console
def main():
    (opts, args) = get_option_parser().parse_args()
    #create alphabet if necessary
    if opts.rebuildAlphabetFlag:
        print "Rebuilding alphabet"
        msml.createAlphabet()

    #load alphabet
    alphabetNode = msml.loadAlphabet()

    #load msml file to msmlNode
    if opts.filename:
        fileTree = etree.parse(opts.filename)
    else:
        print("You have to give a msml-xml file! See %s --help for more information" % sys.argv[0])
        sys.exit(1)
    msmlNode = fileTree.getroot()
    head, tail = ntpath.split(opts.filename)
    filename = str(tail[0:-4])

    inputDirectory = os.path.dirname(os.path.abspath(opts.filename))

    #If parameter -d is not set, generate output directory based on input file name and location.
    outputDirectory = opts.outputDirectory
    if (outputDirectory is None):
        outputDirectory = os.path.join(inputDirectory, filename + "Results")

    print fileTree
    print msmlNode
    print ("Processing file " + opts.filename)
    print ("Exporting to " + opts.exportEngine + " simulation engine")
    print ("Output directory " + outputDirectory )
    print opts.exportEngine
    run_msml(msmlNode, alphabetNode, inputDirectory, outputDirectory, filename, opts.exportEngine, opts.runsimulation, opts.runsimulation, opts.cachingFlag)
    
#second entry point for batch scripts which may change the MSML Node before running the simulation.
def run_msml(msmlNode, alphabetNode, inputDirectory, outputDirectory, filename, exportEngine, runsimulation, postProcessing, cachingFlag):
    if (exportEngine.lower() == 'sofa'):
        print "Exporting to SOFA..."

        filenameSCN = filename + ".scn"

        scnWriter = msml.exporter.SOFAExporter(msmlNode, alphabetNode, inputDirectory, outputDirectory)
        scnWriter.cachingEnabled = cachingFlag
        scnWriter.writeSCN(alphabetNode, msmlNode, os.path.join(outputDirectory, filenameSCN))
        #TODO: move to Sofa_Runner.py
        if runsimulation is True:
            filenameSofaBatch = "%s_SOFA_batch.txt" % filename
            pathSofaJob = os.path.join(outputDirectory, filenameSofaBatch)
            f = open(pathSofaJob, 'w')
            timeSteps = (int)(msmlNode.find(".//step").get("timesteps")) #only one step is supported
            f.write(os.path.join(outputDirectory, filenameSCN) + ' ' + str(timeSteps) + ' ' + filename + '.simu \n')
            f.close()
            sofaBatchExecutable = alphabetNode.find("cmakeGeneratedConfig").find("runSofaExecutable")[0].get("path")
            subprocess.call(sofaBatchExecutable + " -l SOFACuda " + pathSofaJob)
            if postProcessing is True:
                for msmlObject in msmlNode.iterchildren():
                    if msmlObject.tag == "postProcessing":
                        genWriter = msml.exporter.GenericExporter(msmlNode, alphabetNode, inputDirectory,
                                                                  outputDirectory)
                        genWriter.cachingEnabled = cachingFlag
                        genWriter.processMSML(alphabetNode, msmlObject, os.path.join(outputDirectory, filename))

    elif exportEngine.lower() == "abaqus":
        filenameInp = filename + ".inp"
        #print ntpath.join(outputDirectory,filenameSCN)
        inpWriter = msml.exporter.AbaqusExporter(msmlNode, alphabetNode, inputDirectory, outputDirectory)
        inpWriter.cachingEnabled = cachingFlag
        inpWriter.writeINP(alphabetNode, msmlNode, os.path.join(outputDirectory, filenameInp))

    elif exportEngine.lower() == "generic":
        filenameMSML = filename + ".xml"
        #print ntpath.join(outputDirectory,filenameSCN)
        genWriter = msml.exporter.GenericExporter(msmlNode, alphabetNode, inputDirectory, outputDirectory)
        genWriter.cachingEnabled = cachingFlag
        genWriter.processMSML(alphabetNode, msmlNode, os.path.join(outputDirectory, filenameMSML))


if __name__ == "__main__":
    main()