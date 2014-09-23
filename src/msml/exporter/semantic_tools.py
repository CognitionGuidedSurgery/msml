__author__ = 'suwelack'
__license__ = 'GPLv3'

import lxml.etree as etree
from jinja2 import Template

from .base import XMLExporter, Exporter
from msml.exceptions import *
import msml.env
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from msml.model import *

from msml_namespace import MSMLRep


class OntologyParser(object):
    def __init__(self, ontologyName):
        self._ontoGraph = Graph()
        self._ontoGraph.parse(ontologyName)
        self._instanceGraph = Graph()

    def parse_ontology_from_python_memory(self, representationNodeName, memory):

        repNamespace = Namespace('http://www.msml.org/ontology/msmlRepresentation')

        typeURI =

        #get type of data node
        dataNodeType = value(representationNodeName,MSMLRep.isRepresentationOf, NONE)

        print(dataNodeType)

        #print(testTuples)

       # for s,p,o in self._ontoGraph:
       #    print s,p,o

        print('finish')

        #dataNodeName = self._ontoGraph.triples(representationNodeName,NONE, NONE)
        #self._ontoGraph.
        #create node in instance graph


        #get all properties of data node


        #for all properties: get value from memory

        #add properties to instance node

        #for all children of representationNode: call recursiveParse



    def __recursiveParse(self, currentNodeName, memory):
        print('asdf')