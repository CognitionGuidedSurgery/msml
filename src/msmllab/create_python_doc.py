#-*- encoding: utf-8 -*-

__author__ = "Alexander Weigl"

import importlib
from path import path
from codecs import open
from jinja2 import Environment, FileSystemLoader


import inspect

remove_none = lambda seq: filter(lambda x: x is not None, seq)

fldr = path(__file__).parent
env = Environment(loader=FileSystemLoader(fldr))
env.globals['indent'] = lambda string: "   " + string.replace("\n","   \n")

import pydoc

def prepdata(d):
    name, d = d
    return {'name': name, 'doc' : str(d)}

def prepclass(c):
    name, clzz = c
    attrs =    inspect.classify_class_attrs(clzz)
    return {
        'name': name,
        'methods': inspect.getmembers(clzz, predicate=inspect.isfunction),
        'attributes' : attrs
    }

def prepfunc(t):
    name, func = t
    args = inspect.getargspec(func)
    return {
        'name' : name,
        'argspec' : inspect.formatargspec(args.args, args.varargs, args.keywords, args.defaults),
        'doc' : pydoc.getdoc(func) or "\n\n"
    }

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def render(module, filename):
    fullname = module.__name__
    documentation = inspect.getdoc(module)

    exported_names = getattr(module, '__all__', None)

    def create_filter(pred):
        def fn(obj):
            try:
                name = obj.func_name
            except:
                try:
                    name = obj.__name__
                except:
                    return False

            a = exported_names and name in exported_names
            try:
                b = obj.__module__ = module
            except:
                b = False
            return a and b and pred(obj)
        return fn


    functions = map(prepfunc, inspect.getmembers(module, inspect.isfunction))
    classes   = map(prepclass, inspect.getmembers(module, create_filter(inspect.isclass)))
    instances = map(prepdata, inspect.getmembers(module, pydoc.isdata))

    print filename
    content = env.get_template("module.jinja2").render(**locals())
    try:
        with open(filename, 'w','utf-8', 'ignore') as fn:
            fn.write(content)
    except: pass


class base(object):
    def __init__(self):
        self.relname = None
        self.absname = None

    def prepare(self, parent=None):
        if parent:
            self.absname = "%s.%s" % (parent.absname, self.relname)
        else:
            self.absname = self.relname

        print self.absname
        self.module = importlib.import_module(self.absname)
        self.filename = "%s.rst" % self.relname

    def create(self, output_folder):
        pass


class Module(base):
    def __init__(self, name):
        super(Module, self).__init__()
        self.relname = name

    def create(self, output_folder):
        render(self.module, output_folder / self.filename)

class Package(base):
    def __init__(self, name):
        super(Package, self).__init__()
        self.relname = name
        self.sub = []

    def prepare(self, parent=None):
        super(Package, self).prepare(parent)
        self.sub = remove_none(self.sub)
        self.filename = "index.rst"
        for s in self.sub:
            s.prepare(self)

    def create(self, output_folder):
        output_folder = path(output_folder) / self.relname
        print output_folder
        output_folder.makedirs_p()
        render(self.module, output_folder / self.filename)

        for s in self.sub:
            s.create(output_folder)




def scan(start):
    """

    :param start: root folder for scanning
    :type start: path
    :return:
    """

    def package(folder):
        assert isinstance(folder, path)

        if (folder / "__init__.py").exists():

            p = Package(folder.namebase)
            p.sub = list(map(module, folder.files("*.py")))
            p.sub += list(map(package, folder.dirs()))

            return p
        else:
            return None


    def module(file):
        assert isinstance(file, path)
        # name = file.relpath(base).replace('/','.').replace('.py','')
        name = file.namebase
        if name[0] == '_': return None
        m = Module(name)
        return m

    return package(start)


def main():
    d =  scan(path("src/msml"))
    d.prepare()
    d.create("docs/source/test")


    # d = Package("msml",
    #             Package("analytics",
    #                     Module("msml.analytics.alphabet_analytics"),
    #                     Module("msml.analytics.schema_creator"),
    #             ),
    #             Package("msml.api",
    #                     Module("msml.api.msml_optimizer"),
    #                     Module("msml.api.runner"),
    #                     Module("msml.api.simulation_runner"),
    #             ),
    #             Package("msml.exporter",
    #                     Package("msml.exporter.abaqus"),
    #                     Package("msml.exporter.hiflow3"),
    #                     Module("msml.exporter.base"),
    #                     Module("msml.exporter.features"),
    #                     Module("msml.exporter.sofanew"),
    #                     Module("msml.exporter.msml_namespace"),
    #                     Module("msml.exporter.semantic_tools"),
    #                     Module("msml.exporter.sofavisitor"),
    #                     Module("msml.exporter.visitor"),
    #             ),
    #             Module("msml.env"),
    #             Module("msml.envconfig"),
    #             Module("msml.exceptions"),
    #             Module("msml.frontend"),
    #             Module("msml.generators"),
    #             Module("msml.log"),
    #             Module("msml.sortdef"),
    #             Module("msml.sorts"),
    #             Module("msml.xml"),
    # )




main()