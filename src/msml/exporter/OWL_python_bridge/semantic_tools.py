__author__ = 'suwelack'
__license__ = 'GPLv3'

import lxml.etree as etree
from jinja2 import Template

from msml.exceptions import *
import msml.env
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, OWL, RDF, RDFS
from collections import defaultdict
from jinja2 import Template, Environment, PackageLoader
from os import path
import importlib
import inspect
#from msml.model.baseClasses import msmlScene

from msml.model.base import *

#from msml_namespace import MSMLRep

#this class exports an ontology into python classes

class OntoClassRef(URIRef):

    def getClassName(self):
        parts = self.split('#')
        if len(parts) != 2:
            print('Error, URIRef should contain 2 parts!')
        return parts[1]

    def getModuleName(self):
        parts = self.split('#')
        if len(parts) != 2:
            print('Error, URIRef should contain 2 parts!')
        pathParts = parts[0].split('/')

        return pathParts[-1]

    def toStr(self, superclasses=None, attributeDict=None):
        returnStr =''
        #env = Environment(keep_trailing_newline=True, lstrip_blocks=False, trim_blocks=False, loader=PackageLoader('msml.exporter.OWL_python_bridge', 'templates'))
        env = Environment( keep_trailing_newline=False,loader=PackageLoader('msml.exporter.OWL_python_bridge', 'templates'))
        superclass = ''
        if not superclasses:
            superclass = 'object'
        else:
            for theClass in superclasses:
                superclass += theClass.getClassName() + ','
            superclass = superclass[:-1]
        objectAttributes = None
        listAttributes = None

        if(attributeDict):
            objectAttributes = list()
            listAttributes = list()
            for attribute in attributeDict:
                if attributeDict[attribute] == 2:
                    listAttributes.append(attribute)
                else:
                    objectAttributes.append(attribute)


        template = env.get_template('class_template.html')
        returnStr = template.render(name=self.getClassName(), superclass=superclass, listAttributes=listAttributes, objectAttributes=objectAttributes)


        return returnStr


class PropertyInfo(object):
    def __init__(self, type=OWL.DatatypeProperty, exactCardinality=True, cardinality=1, range=None ):
        self.type = type;
        self.exactCardinality = exactCardinality;
        self.cardinality = cardinality;
        self.range = range

class OntologyParser(object):
    def __init__(self, ontologyName):
        self._ontoGraph = Graph()
        self._ontoGraph.parse(ontologyName)
        self._instanceGraph = Graph()

    def createPythonModule(self, directory):

        #for s in self._ontoGraph:
        #    print(s)

        #get a list of all classes (are of type owl#Class)
        classList = self._ontoGraph.subjects(RDF.type, OWL.Class)

        #for all classes
        #check if class has superclass, write signature using jinja template
        modulesDict = defaultdict(list)
        for currentClass in classList:
            classURI = OntoClassRef(currentClass)
            moduleName = classURI.getModuleName()
            modulesDict[moduleName].append(classURI)

        # className = URIRef('http://www.msml.org/ontology/msmlScene#Elements')
        # classList2 = self._ontoGraph.objects(className, RDFS.subClassOf)
        # classList3 = self._ontoGraph.objects(className, URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'))
        # #classList3 = self._ontoGraph.predicate_objects(className)
        #
        # if (className, None, None) in self._ontoGraph:
        #    print "This graph contains triples about Bob!"
        #
        # for aClass in classList2:
        #     print aClass
        #
        # for aClass in classList3:
        #     print aClass
        #
        # print RDFS.subClassOf

        for moduleName in modulesDict:
            establishedClasses = set()
            currentModuleString = str()

            try:
                longModuleName = '..' + moduleName
                currentLoadedModule = importlib.import_module(longModuleName, 'msml.model.baseClasses.subpkg')
                for name, obj in inspect.getmembers(currentLoadedModule):
                    if inspect.isclass(obj):
                        establishedClasses.add( obj.__name__)
                #import statement in generated module
                currentModuleString += 'from msml.model.baseClasses.'+moduleName+' import *\n\n'
            except ImportError:
                pass

            theModule = modulesDict[moduleName]

            for className in theModule:
                #check if class is already there
                currentModuleString  += self.addClassToString(className, establishedClasses)
                #print className.getClassName()

            theFilename = path.abspath(path.join( directory, moduleName+'.py'))
            #print theFilename
            file = open(theFilename, "w")
            file.write(currentModuleString)
            file.close()

    def parseAttributes(self, className):
        #get object properties within class domain
        classURI = URIRef(className)
        propList = self._ontoGraph.subjects(RDFS.domain, classURI )

        returnDict = dict()



        for property in propList:
            ranges = self._ontoGraph.triples( (property, RDFS.range, None) )
            rangeBNode = self._ontoGraph.value( property, RDFS.range, None )

            #distinguish between datatype property and objectproperty
            propertyType = self._ontoGraph.value( property, RDF.type, None)

            if propertyType == OWL.DatatypeProperty:
                print ('datatypeproperty found')
            else:


                cardinality = self._ontoGraph.value( rangeBNode, OWL.qualifiedCardinality, None )

                if cardinality is None:
                    cardinality = self._ontoGraph.value( rangeBNode, OWL.minQualifiedCardinality, None )
                    #little hack here, if cardinality is 1, make it two
                    if cardinality is None:
                        print('Error, cardinality not specified for property '+property)
                    else:
                        cardinality = 2



                propertyURI = OntoClassRef(property)

                if propertyURI.getClassName():
                    returnDict[propertyURI.getClassName()] = cardinality

                restrinctionBNode = self._ontoGraph.value( rangeBNode, OWL.restriction, None )
                cardinality = self._ontoGraph.value( rangeBNode, OWL.qualifiedCardinality, None )
                #for restriction in ranges:
                 #   print restriction

                #print 'test'



        return returnDict

    def addClassToString(self, className, establishedClasses):

        if not className.getClassName() in establishedClasses:
            finalString =''
            #check for superclass
            superClasses = self._ontoGraph.objects(URIRef(className), RDFS.subClassOf)
            classesList = list()
            for superClass in superClasses:
                if superClass:
                    superClassURI = OntoClassRef(superClass)
                    finalString += self.addClassToString( superClassURI, establishedClasses)
                    classesList.append(superClassURI)

            establishedClasses.add(className.getClassName())
            #add in the attributes
            attributes = self.parseAttributes(className)
           
            stringToAdd = className.toStr(superclasses=classesList, attributeDict =attributes )
            finalString=finalString+stringToAdd

            return finalString
        else:
            return ''


    def __recursiveParse(self, currentNodeName, memory):
        print('asdf')