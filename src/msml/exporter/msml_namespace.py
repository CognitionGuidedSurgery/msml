__author__ = 'suwelack'

from rdflib.namespace import ClosedNamespace


MSMLRep= ClosedNamespace(
    uri=URIRef("http://www.msml.org/ontology/msmlRepresentation#"),
    terms=[
        'isRepresentationOf', 'isDataNodeFor']
)