MSML User Extension
===================


**Current Status** *draft*

This document describes the notation and functionalities from MSML User Packages and Repositories.

# Introduction

We want an easy way to extend MSML. Obvisouly these extension provide functionalities for MSML Workflows.
These extensions need to be shared easily as Workflows.
This extension mechanism will be important, if we provide MSML as a webservice instance. Webservice users can specify which packages are necessary to execute the workflow.
Within these document we propose the concept of **User Repository** and **User Package**.


# Ontology

We define multiple terms:

**User Package:** A user package is anthology of operators. It provides the necessary alphabet files, the code for operators (python) or executables.

**User Repository** Multiple packages can be packed together.


User Package
------------


Configuration

.. code-block:: yaml

   format-version: 1
   name:           mup-cli
   maintainer:     "Alexander Weigl <alexander.weigl@student.kit.edu>"
   version:        "2015.01.03"
   git:            "https://github.com/CognitionGuidedSurgery/mup-cli.git"
   alphabet-path:
     - alphabet/
   binary-search-path:
     - bin/
   python-path:
     - py/


## Support from MSML


# User Repository


## Folder Structure


## Support from MSML

## Functionalities


# Package directories
