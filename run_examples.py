#region gplv3
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
#   S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
#   The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#   Medicine Meets Virtual Reality (MMVR) 2014
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
#endregion

from __future__ import print_function

__author__ = "Alexander Weigl"
__date__ = "2014-03-10"

import sys

sys.path.insert(0, "src/")

from msml import frontend

from path import path

root = path("examples")

bunny = root / "BunnyExample"

EXAMPLES = [
    ("Bunny", bunny / "bunny.msml.xml", "Prepare the standard bunny for simulation"),
    ("Bunny CGAL", bunny / "bunnyCGAL.msml.xml", "Prepare the standard bunny for simulation"),
    ("Bunny CGAL High", bunny / "bunnyCGALHigh.msml.xml", "Prepare the standard bunny for simulation"),
    ("Bunny Cuda", bunny / "bunnyExampleCuda.xml", "Prepare the standard bunny for simulation"),
    ("Bunny VoxMesh", bunny / "bunnyVoxelMeshing.msml.xml", "Prepare the standard bunny for simulation"),
    ("Lungs", root / "CGALi2vLungs/Lungs_new.xml", ""),
    ("CGal", root / "CGALi2vExample/CGALExample.xml", ""),
    ("Liver", root / "LiverExample/liverLinear.msml.xml", "Prepare a liver mesh simulation"),
    ("Color", root / "PythonExamples/color-example.xml", "Workflow only example. Colorize   a Mesh")
]


def main():
    print("""
                                    _
                               | | Medical
     _ __ ___   ___  _ __ ___  | | Simulation
    | '_ ` _ \ / __|| '_ ` _ \ | | Markup
    | | | | | |\__ \| | | | | || | Language
    |_| |_| |_||___/|_| |_| |_||_|


\x1b[32mAvailable Examples\x1b[0m
""")

    for i, (name, file, desc) in enumerate(EXAMPLES):
        print("\t \x1b[1m%d\x1b[0m \x1b[34;1m%20s\x1b[0m : %s\n\t\t\t%s\n" % (i, name, file, desc))

    print("Select Examples [0]:", end=" ")
    try:
        number = int(raw_input()) or 0
    except:
        number = 0

    try:
        name, file, desc = EXAMPLES[number]
        print("Executing: %s" % name)

        options = {'--alphabet': 'alphabet.cache',
                   '--exporter': 'nsofa',
                   '--output': None,
                   '--start-script': '~/.config/msmlrc.py',
                   '--verbose': False,
                   '--xsd-file': None,
                   '-S': True,
                   '-w': False,
                   '<file>': [file],
                   '<paths>': [],
                   'alphabet': False,
                   'exec': True,
                   'show': False}

        import msml.exporter

        print(msml.exporter.get_exporter(options['--exporter']))

        frontend.main(options)
    except Exception as e:
        raise


if "__main__" == __name__:
    main()
