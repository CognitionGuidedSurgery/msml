                                _ 
                               | | Medical
     _ __ ___   ___  _ __ ___  | | Simulation
    | '_ ` _ \ / __|| '_ ` _ \ | | Markup 
    | | | | | |\__ \| | | | | || | Language
    |_| |_| |_||___/|_| |_| |_||_| 
                                   

      License: GPLv3
      Authors: Markus Stoll
               Stefan Suwelack
               Alexander Weigl
               Nicolai Schoch
      Version: 0.1alpha
         Date: 2014-02-20
   

Master: [![Circle CI](https://circleci.com/gh/CognitionGuidedSurgery/msml/tree/master.svg?style=svg)](https://circleci.com/gh/CognitionGuidedSurgery/msml/tree/master) 
Experimental:
[![Circle CI](https://circleci.com/gh/CognitionGuidedSurgery/msml/tree/experimental.svg?style=svg)](https://circleci.com/gh/CognitionGuidedSurgery/msml/tree/experimental) 
[![Coverage Status](https://coveralls.io/repos/CognitionGuidedSurgery/msml/badge.png)](https://coveralls.io/r/CognitionGuidedSurgery/msml)

# About

The medical simulation markup language (MSML) is a flexible XML-based description for the biomechanical modeling workflow and finite-element based biomechanical models.

MSML helps you to create biomechanical models from tomographic data, export them to FE solvers and analyze the results. It is very flexible as already existing components (e.g. segmentation algorithms, meshers) can usually be integrated into the framework by providing a single additional XML-file.

The main library is written in Python, but we also provide a large collection of useful C++ operators (e.g. linear tetrahedral and quadratic tetrahedral meshing, mesh size reduction, error analysis etc.).

Additional information can also be found in the paper:
S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel, The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow, Medicine Meets Virtual Reality (MMVR) 2014

If you like MSML and use it in academic work, please cite the paper above.

# Mailing list
Join the mailing list: https://www.lists.kit.edu/wws/info/msml
and post to msml@lists.kit.edu

Please feel free to ask if you have any problems installing, running or extending MSML.

# Getting Started

## Installation:

You need Python, Boost and the visualization toolkit (VTK) in order to run MSML. Additional components need Tetgen, CGAL and VCG. Please refer to our detailed installation guides for [Linux](http://msml.readthedocs.org/en/latest/Installation.html#installation-linux) and [Windows](https://github.com/CognitionGuidedSurgery/msml/wiki/Installation-Windows) in the Github-Wiki.

## First steps

Run the src/msml.py file with the "exec -h" option for help.

MSML contains several simple scenarios to get you started quickly. Here are some examples
1. In order to generate a volume mesh of the Stanford bunny using Tetgen and export the simulation to the SOFA framework type:
   ./msml.py exec -e sofa ../../msml/examples/BunnyExample/bunny.msml.xml 
2. In order to generate a volume mesh of the Stanford bunny using CGAL and export the simulation to the Abaqus FE solver type:
   ./msml.py exec -e abaqus ../../msml/examples/BunnyExample/bunnyCGAL.msml.xml 

Please refer to the Github wiki for further examples.

# Contribute

You have some code/algorithms that might be good fit for the MSML framework? Then we are looking forward to your contribution. Just issue a pull request or contact Stefan Suwelack (suwelack@kit.edu).

# Further questions?
Please contact Stefan Suwelack (suwelack@kit.edu)


