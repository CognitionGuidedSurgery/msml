__author__ = 'suwelack'
import inspect
import importlib
from jinja2 import Template, Environment, PackageLoader


class MappingCreator(object):

    def create_mapping(self,mod, filename):

            finalStr ='from msml.io.mapper.base_mapping import * \n \n'

            finalStr += 'import msml.model.generated.'+mod+' as mod\n\n'

            finalStr +="class "+mod+'2xMapping(BaseMapping):\n\n'


            try:
                currentLoadedModule = importlib.import_module('..'+ mod, 'msml.model.generated.subpkg')
                for name, obj in inspect.getmembers(currentLoadedModule):
                    if inspect.isclass(obj):
                        finalStr  = finalStr + self.create_class_mapping( obj.__name__)

            except ImportError:
                pass

            file = open(filename, "w")
            file.write(finalStr)
            file.close()



    def create_class_mapping(self, class_name):
        env = Environment( keep_trailing_newline=False,loader=PackageLoader('msml.io.OWL_python_bridge', 'templates'))
        template = env.get_template('mapping_class_template.html')
        returnStr = template.render(class_name = class_name)
        return returnStr
