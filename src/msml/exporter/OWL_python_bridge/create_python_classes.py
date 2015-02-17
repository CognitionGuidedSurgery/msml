__author__ = 'suwelack'

from semantic_tools import OntologyParser
from path import path

modulepath = path(__file__).dirname()


parser = OntologyParser(modulepath / 'MSMLBaseOntology.owl')
modulesDirectory = modulepath / '..' / '..' / 'model' / 'generated'
parser.createPythonModule(modulesDirectory)