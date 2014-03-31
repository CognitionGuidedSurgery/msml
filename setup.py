#!/usr/bin/env python
from __future__ import  print_function

import sys
sys.path.insert(0, "src/")

from distutils.core import setup, Command
from pip.req import parse_requirements


install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

from glob import glob
import msml
import os

import shutil

__author__ = "Alexander Weigl"


class cmake_compile(Command):
    """

    """

    description = "compile the msml operators through cmake"
    user_options = [
        ('operators=', 'O', 'select operators to build'),
        ('build-dir=', None, 'cmake-build directory'),
        ('operator-dir=', None, 'directory with the CMakeLists.txt' )
    ]

    modules = ['TetgenOperatorsPython', 'MiscMeshOperatorsPython', 'CGALOperatorsPython']
    
    #["MiscMeshOperators", "TetgenOperators", "CGALOperators",
    #           "TetgenOperatorsPython", "MiscMeshOperatorsPython",
    #           "VCGOperators", "CGALOperatorsPython"]

    def initialize_options(self):
        self.operators = None
        self.opdir = "MSML_Operators"
        self.build_dir = "cbuild/"

    def finalize_options(self):
        self.ensure_string_list("operators")
        if self.operators:
            for s in self.operators:
                if s not in cmake_compile.modules:
                    print("Operator %s is unknown" % s)
        else:
            print("Build all known operators")
            self.operators = cmake_compile.modules

        print("Operators are in %s" % self.opdir)
        print("Build directory: %s " % self.build_dir)

    def run(self):
        current = os.getcwd()

        def spawn(command):
            if self._dry_run:
                return 0
            return os.system(command)

        self.mkpath(self.build_dir)
        os.chdir(self.build_dir)

        spawn('cmake ../%s' % self.opdir )

        available_mods = {mod : spawn('make %s' % mod)
                          for mod in cmake_compile.modules}

        for k,v in available_mods.items():
            print("%30s: %s" % (k, "YES" if v else "NO"))

        os.chdir(current)
        target = "%s/src/msml/ext" % current
        for so in glob('%s/bin/*.so' % self.build_dir):
            #print("Copy %s into %s" % (so, target))
            self.copy_file(so, target)


setup(
    name='msml',
    version=msml.__version__,
    description='', #TODO
    author=msml.__author__,
    contact_email='', #TODO MAILINGLISTE
    url=' http://awesomewhere.internet/msml', #TODO

    maintainer="Alexander Weigl",
    maintainer_email="Alexander.Weigl@student.kit.edu",


    packages = ['msml', 'msml.ext', 'msml.exporter', 'msml.run', 'msml.model'],
    package_dir={'': 'src'},

    scripts=["src/msml.py"],
    #		ext_modules     = [ tetgen_ext ]

    platforms="linux",
    long_description=msml.__doc__,

    keywords=['msml', 'biomechanical'], #TODO
    license='GPL3',

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        #          'Operating System :: MacOS :: MacOS X',
        #          'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],

    requires = reqs,
    provides= ["msml"],
    cmdclass={'cmake': cmake_compile}
)


