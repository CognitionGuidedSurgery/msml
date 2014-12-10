__author__ = 'suwelack'
__license__ = 'GPLv3'

import lxml.etree as etree
from jinja2 import Template

from .base import XMLExporter, Exporter
from msml.exceptions import *
import msml.env
import rdflib.plugins.sparql as sparql
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF, OWL, RDF, RDFS
from collections import defaultdict
from jinja2 import Template, Environment
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
        env = Environment(keep_trailing_newline=True, lstrip_blocks=False, trim_blocks=False)
        superclass = ''
        if not superclasses:
            superclass = 'object'
        else:
            for theClass in superclasses:
                superclass += theClass.getClassName() + ','
            superclass = superclass[:-1]

        template = env.from_string('\nclass {{name}}({{superclass}}):\n   pass\n ')
        returnStr = template.render(name=self.getClassName(), superclass=superclass)


        return




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
                print className.getClassName()

            theFilename = path.abspath(path.join( directory, moduleName+'.py'))
            print theFilename
            file = open(theFilename, "w")
            file.write(currentModuleString)
            file.close()

    def parseAttributes(self, className):
        #get object properties within class domain
        classList = self._ontoGraph.subjects(RDF.type, OWL.Class)


        classList = self._ontoGraph.subjects(RDF.type, OWL.Class)
        for currentClass in classList:
            print currentClass

        print('Now with sparql')
        #self._ontoGraph.bind("owl", OWL)

        # typeURI = URIRef(RDF.type)
        # classURI = OWL.Class
        #
        # queryString = "SELECT ?name  WHERE { ?name <"+RDF.type.lower()+"> <"+OWL.Class.lower()+">}"
        # print(queryString)
        #
        # testStr = 'SELECT ?name  WHERE { ?name <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#class>}'
        # q=sparql.prepareQuery('SELECT ?name  WHERE { ?name <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?c}')
        # qres = self._ontoGraph.query(q)
        #
        # for row in qres:
        #     print(row)
        #
        #
        # print('complete')
        #
        # msml.sorts.conversion(typea, typeb,)

    def addClassToString(self, className, establishedClasses):

        if not className.getClassName() in establishedClasses:
            finalString =' '
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
            finalString += className.toStr(superclasses=classesList, attributeDict =attributes )
            return finalString
        else:
            return ''


    def __recursiveParse(self, currentNodeName, memory):
        print('asdf')