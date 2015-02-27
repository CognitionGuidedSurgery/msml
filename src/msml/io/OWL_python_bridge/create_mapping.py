__author__ = 'suwelack'

from msml.io.OWL_python_bridge.Mapping_Creator import MappingCreator
from path import path

modulepath = path(__file__).dirname()



filename = modulepath / '..' / 'mapper' / 'msml2abaqus_mapping.py'

creator = MappingCreator()
creator.create_mapping('msmlScene', filename)
