# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
# Medicine Meets Virtual Reality (MMVR) 2014
#
# Copyright (C) 2013-2014 see Authors.txt
#
# If you have any questions please feel free to contact us at suwelack@kit.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# endregion

"""Support for User Packages and Repositories.
=============================================


Specification
-------------

Repository Meta Data
^^^^^^^^^^^^^^^^^^^^



Package Meta Data
^^^^^^^^^^^^^^^^^

"""
from msml.log import warn,error

__author__ = 'Alexander Weigl'
__date__ = "2015-01-03"

from lxml import etree
from itertools import chain

from path import path


MSML_REPOSITORY_XSD = path(__file__).dirname() / 'msml-repository.xsd'
MSML_PACKAGES_XSD = path(__file__).dirname() / 'msml-package.xsd'

MSML_REPOSITORY_NS = etree.QName("http://msml.org/repository/1.0/", "e")
MSML_PACKAGES_NS = etree.QName("http://msml.org/package/1.0/", "e")

MSML_PACKAGE_FILENAME = "msml-package.xml"
MSML_REPOSITORY_FILENAME = "msml-repository.xml"

class FileNotFoundError(Exception):
    pass

def xml_load(filename, schema=None):
    parser = etree.XMLParser(
        encoding="utf-8",
        attribute_defaults=True,
        ns_clean=True,
        remove_blank_text=True,
        remove_pis=True,
        remove_comments=True,
        schema=etree.XMLSchema(file=schema)
    )
    if os.path.exists(filename):
        try:
            return etree.parse(filename, parser)
        except etree.XMLSyntaxError:
            error("Syntax error in %s", filename)
            raise FileNotFoundError()

    else:
        raise FileNotFoundError()


def get_attrib(element, attributes):
    if isinstance(attributes, str):
        attributes = map(lambda x: x.strip(), attributes.split(","))
    if element is None:
        return [None] * len(attributes)
    return [element.get(x) for x in attributes]


class Repository(object):
    def __init__(self,
                 base_path,
                 layout_version=1,
                 msml_version=1,
                 active=True):
        self.base_path = base_path

        self._resolve_items = []

        self.msml_version = msml_version
        self.active = active

        self._package_objects = None
        self._import_objects = None

    @staticmethod
    def from_file(filename):
        filename = path(filename)
        if filename.isdir():
            base_path = filename
            filename = base_path / MSML_REPOSITORY_FILENAME
        else:
            base_path = path(filename).dirname()

        root = xml_load(filename, schema=MSML_REPOSITORY_XSD)

        r = Repository(base_path)
        r.msml_version, r.active = get_attrib(root.getroot(), ['msml-version', 'active'])

        r.active = r.active in ('true', 'on', '1')

        for e in root.getroot():
            tag = etree.QName(e.tag).localname
            r._resolve_items.append((tag, e.text.strip()))

        return r

    def add_imports(self, *imports):
        self._resolve_items += map(lambda x: ('import', x), imports)

    @property
    def packages(self):
        return filter(lambda x: x[0] == 'package', self._resolve_items)

    @property
    def imports(self):
        return filter(lambda x: x[0] == 'import', self._resolve_items)

    def get_package_folders(self):
        for p in self.packages:
            yield (self.base_path / p).abspath()

    def get_import_folders(self):
        for i in self._import_objects:
            yield (self.base_path / i).abspath()

    @property
    def packages_(self):
        # TODO better name
        if not self._package_objects:
            self._package_objects = list(map(Package.from_file, self.get_package_folders()))
        return self._package_objects

    @property
    def imports_(self):
        # TODO better name
        if not self._import_objects:
            self._import_objects = list(map(Repository.from_file, self.get_import_folders()))
        return self._import_objects

    def validate(self):
        if self.active:
            p = all(map(lambda x: x.validate(), chain(self.packages_, self.imports_)))
            return p
        else:
            return True

    def resolve_packages(self):
        """recursive resolving packages"""
        packs = []
        for t, p in self._resolve_items:
            p = path(p).expanduser()

            if t == 'package':
                packs.append(Package.create(self.base_path / p))
            else:
                try:
                    r = Repository.from_file(self.base_path / p)
                    if r.active:
                        packs += r.resolve_packages()
                except FileNotFoundError:
                    warn("Could not load imported repository %s at %s", (self.base_path/p).abspath(), self.base_path)
        return packs


class Package(object):
    CACHE = {}  # filename to Package Object

    class Information(object):
        class Maintainer(object):
            def __init__(self, name=None, email=None):
                self.name, self.email = name, email

        class Documentation(object):
            def __init__(self, file=None, url=None, content=None):
                self.file, self.url, self.content = file, url, content

        class Repository(object):
            def __init__(self, url=None, type=None):
                self.url, self.type = url, type

        def __init__(self, maintainer=None, documentation=None, homepage=None, repository=None):
            self.maintainer = maintainer or Package.Information.Maintainer()
            self.documentation = documentation or Package.Information.Documentation()
            self.homepage = homepage
            self.repository = repository or Package.Information.Repository()

    def __init__(self, base_path, name, version,
                 information=None, alphabet_dir=None, python_dir=None, binary_dir=None):
        self.base_path = base_path
        self.name = name
        self.version = version
        self.information = information or Package.Information()
        self.alphabet_dir = alphabet_dir or []
        self.binary_dir = binary_dir or []
        self.python_dir = python_dir or []


    def validate(self):
        r = True
        for a in self.full_alphabet_dir() + self.full_binary_dir() + self.full_python_dir():
            a = path(a)
            if not (a.exists() and a.isdir()):
                r = False
                warn("Directory %s is included by %s in %s, but does not exists." % (a, self.name, self.base_path))
        return r

    @staticmethod
    def create(filename):
        "Creating from file using caching"
        f = filename.abspath()
        if f not in Package.CACHE:
            Package.CACHE[f] = Package.from_file(f)
        return Package.CACHE[f]

    @staticmethod
    def from_file(filename):
        filename = path(filename).abspath()
        if filename.isdir():
            base = filename
            filename = base / MSML_PACKAGE_FILENAME
        else:
            base = path(filename).dirname()

        root = xml_load(filename, MSML_PACKAGES_XSD)

        _find = partial(find, root, MSML_PACKAGES_NS)
        _text = partial(findtext, root, MSML_PACKAGES_NS)
        _textall = partial(findalltext, root, MSML_PACKAGES_NS)
        _attrib = lambda n, a: get_attrib(_find(n), a)


        name, version = get_attrib(root.getroot(), "name, version")

        p = Package(base, name, version)

        p.information.maintainer.name, p.information.maintainer.email = \
            _attrib('maintainer', "name, email")
        p.information.documentation.content = _text("documentation")
        p.information.documentation.url, p.information.documentation.file = \
            _attrib('documentation', 'url, file')

        p.information.homepage = _attrib('homepage', "name, email")

        p.information.repository.url, p.information.repository.type = \
            _attrib('repository', "url, type")

        p.alphabet_dir = _textall("alphabet-dir")
        p.python_dir = _textall("python-dir")
        p.binary_dir = _textall("binary-dir")

        return p

    def __str__(self):
        return "MSMLPackage: %s@%s" % (self.name, self.version)


    def full_alphabet_dir(self):
        return prefix_paths(self.base_path, self.alphabet_dir)

    def full_python_dir(self):
        return prefix_paths(self.base_path, self.python_dir)

    def full_binary_dir(self):
        return prefix_paths(self.base_path, self.binary_dir)

def prefix_paths(prefix, seq):
    p = path(prefix)
    return map(lambda s: p / s, seq)

def get_concrete_paths(seq):
    """calculates the list for alphabet, binary, and python paths

    :param seq: sequence of packages
    :type seq: list[Package]

    :return: a,b,c
    """
    alpha = list()
    bin = list()
    py = list()

    for package in seq:
        alpha += package.full_alphabet_dir()
        bin += package.full_binary_dir()
        py += package.full_python_dir()

    return alpha, bin, py


def clean_paths(seq):
    pred = lambda p: os.path.exists(p) and os.path.isdir(p)

    for e in filter(lambda p: not pred(p), seq):
        warn("Directory %s should be included into the search paths but does not exists or is a directory", e)

    return filter(pred, seq)

from functools import partial
import os.path

def find(element, namespace, name):
    q = ".//" + etree.QName(namespace, name).text
    return element.find(q)


def findall(element, namespace, name):
    q = ".//" + etree.QName(namespace, name).text
    return element.findall(q)


def findtext(element, namespace, name):
    q = ".//" + etree.QName(namespace, name).text
    return element.findtext(q).strip()


def findalltext(element, namespace, name):
    q = ".//" + etree.QName(namespace, name).text
    return list(map(lambda x: x.text, element.findall(q)))