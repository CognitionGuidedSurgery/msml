Extend MSML
========================

How to write an Exporter
------------------------

You have to consider following parts for implementing of an Exporter:

1. Writing your Exporter
2. Register your Exporter
3. Get your Exporter into the *MSML core*

**Attention** This is a draft until `issues 5 <https://github.com/CognitionGuidedSurgery/msml/issues/5>`_
and `7 <https://github.com/CognitionGuidedSurgery/msml/issues/7>`_ are solved.

Writing your Exporter
+++++++++++++++++++++

You should start by deriving from `Exporter` class. It provides the default functionality for the variable resoltuion (`Exporter.lookup`) and slot linking (`Exporter.link`, `Exporter.gather_inputs`).
The function `Exporter.evaluate_node` provides an easy access for variables in the `Memory`.

Normally you only need to override:

.. code-block:: python

    def render(self):
        """Builds the File (XML e.g) for the external tool"""
        pass

    def execute(self):
        "should execute the external tool and set the memory"
        pass


* In `self.render()` you should create the export file (e.g. Abaqus: *.inp, Sofa: *.scn).  The function can access the current executor (`self._executor`), the memory (`self._memory`) and the MSML file object (`self._msml_file`).
* In `self.execute` you should call the external program and set the requested result into Memory (`self._memory`)

Register your Exporter
++++++++++++++++++++++

There are to choices for providing Exporters for the command line interface (`--exporter, -e` option).
The module `msml.exporter` provides the global register `__REGISTER`.

Choice 1: Exporter in MSML Core
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Exporter that are deliviered with *MSML core* can be inserted in the `__REGISTER` directly:

1. Import module/class in `src/msml/exporter/__init__.py`
2. Add entry to dictionary `__REGISTER` (L51) with name and constructor.

Please see the notes below for adding an Exporter to the *MSML core*

Choise 2: Exporter not in MSML
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your exporter is not available in *MSML* you can embbedd him with your *user file* (normally `~/.config/msmlrc.py`, can be changed on command line).

In the rc file you can import your exporter and register it:

.. code-block:: python

    # msml rc file: ~/.config/msmlrc.py
    from yourpackage import yourexporter
    from msml.exporter import register_exporter

    register_exporter("yourexporter",  yourexporter)


Get your Exporter into the *MSML core*
++++++++++++++++++++++++++++++++++++++

Following requirements are needed for inclusion of your Exporter:

1. source code under gplv3 with preamble from *MSML*
2. Variables with `__author__ = "Name <email>"`, `__version__` and `__date__`

The Exporter should only use plain python with minimal use of libraries.

You can submit your code per E-Mail, Issues or Pull Request.
A grant of write access is possible.


How to create an Operator
-------------------------

An operator in MSML is a function that perform a bunch of operation.
This is similiar to a python function definition.

An Operator consists of:

* runtime information
  * python operator (module, function)
  * shell operator (command template)
  * shared object operator (file, symbol name)
* list input slots (name, type, format)
* list of output slots (name, type, format)
* list of paramters (name, type)
* arbitary meta data in annotations element

Example
+++++++

.. highlight:: xml
   :linenothreshold: 5

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <msml:operator xmlns:msml="http://sfb125.de/msml"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://sfb125.de/msml"
                   name="colormesh">
        <runtime>
            <python module="msml.ext.misc"
                    function="colorMeshOperator"/>
        </runtime>

        <input>
            <arg name="mesh"
                 type="linearTetMesh, quadraticTetMesh"
                 format="file.vtk"/>

            <arg name="coloredMesh"
                 type="triangularMesh"
                 format="file.vtk"/>
        </input>

        <output>
            <arg name="coloredMesh"
                 type="triangularMesh"
                 format="file.vtk"/>
        </output>

    </msml:operator>


How to create a new Element
---------------------------

Elements are very special. They describe information in the scene graph and are handled by the exporters. Normally any definition of a new element leads to a change in an exporter.

Example
+++++++



.. code-block:: xml

   <msml:element xmlns:msml="http://sfb125.de/msml"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://sfb125.de/msml" name="linearElasticMaterial"
                 category="material" quantity="single">

       <description>
           Choose a linear elastic model
       </description>

       <parameters>
           <arg name="poissonRatio" default="0.3">
               <meta key="doc" value="Set the poisson ratio of the model"/>
           </arg>
           <arg name="youngModulus" default="3000">
               <meta key="doc" value="Set the young modulus of the model"/>
           </arg>
       </parameters>
   </msml:element>
