__author__ = 'suwelack'

from path import path

from msml.io.OWL_python_bridge.semantic_tools import OntologyParser


modulepath = path(__file__).dirname()


parser = OntologyParser(modulepath / 'MSMLBaseOntology.owl')
modulesDirectory = modulepath / '..' / '..' / 'model' / 'generated'
parser.createPythonModule(modulesDirectory)

parser2 = OntologyParser(modulepath / 'AbaqusOntology.owl')

impMod = list()
impMod.append('msmlScene')
parser2.createPythonModule(modulesDirectory, impMod)