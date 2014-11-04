Getting Started
---------------

After the :doc:`Installation` you can start with the examples. Simply use the :file:`run_examples.py`
and select an example to run.

If this works, we write and execute our first msml file.


.. glossary::

    Exporter
        Is the part of the program that translate the ``<scene>`` into the corresponding input
        for the simulation step. Currently available are: Sofa, Hiflow, Abaqus, For writing one on your own refer to :ref:`How to write an Exporter`

    Operator
        is like a function or a procedure in programing languages. An operator has input, parameter and output slots.
        The input and parameter slots takes values directly or variables or other output slots.

    Task
        consists of a corresponding operator and values of input and parameters slots. You can a Task as
        an instance of an Operator.

    Logical Type
    Physical Type
    Sort
        A sort consists of an logical and physical type. More informations: :ref:`Sort Logic and Type Safety`





Writing MSML-Files
------------------

A MSML-File is an XML-File following the :file:`msml.xsd` schema.
The MSML transfer a given MSML-File into into a corresponding instance of :py:class:`msml.model.base.MSMLFile`.

We start with an empty XML-File:


.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <p:msml xmlns:p="http://sfb125.de/msml">

    </p:msml>

We refer to the namespace ``http://sfb125.de/msml``. The corresponding xsd schema lies in :file:`src/msml/msml.xsd`.
You should bind the namespace to this file over the xml catalog in your ide.

An MSML-File consists of four parts:

:variables:
    describes a set of variables, that have a value, logical and physical type.
    The value of variables can load from an external file.

:workflow:
    a set of task, calls for of an operator


:scene:
    a set of object nodes.

:environment:
    fix and defined settings for exporter


We start with the ``<variables>`` for the input variables.

.. code-block:: xml

    <p:msml xmlns:p="http://sfb125.de/msml">
         <variables>
            <var name="input_vol_mesh"
                value="bunnyVolumeMesh.vtk"
                logical="Mesh"
                physical="file.vtk"/>

            <var name="input_surf_mesh"
                 value="Bunny6000Surface.vtk"
                 logical="Mesh"
                 physical="str"/>

        </variables>


In the next step we describe the operators we want to *call*.
The tag name is the operator name. Every operator should have an ``id`` attribute, that is needed to refer
to his output slots. We use the tetgen to create a volume mesh from a surface mesh. The second step is getting
the vertex indices within the region of interests.

.. todo::

    refer to api documenation oprators, refer to howto of write an operator


.. code-block:: xml

    <workflow>

        <mesherTetgen id="bunnyVolumeMesher"
                      meshFilename="${input_vol_mesh}"
                      surfaceMesh="${input_surf_mesh}"
                      preserveBoundary="0"/>

        <boxROIToIndexOperator id="bodyToIndexGroup"
                               box="-0.1 -0.03  -0.07 0.06 0.19 0.06"
                               mesh="${bunnyVolumeMesher}"
                               select="elements"/>

        <boxROIToIndexOperator id="bottomToIndexGroup"
                               box="-0.1 0.03 -0.07 0.07 0.035 0.06"
                               mesh="${bunnyVolumeMesher}"
                               select="points"/>

    </workflow>


The scene consists of one object. It has a mesh, output, materials and constraints.
The mesh is simple the generated volume mesh from tetgen. The material is built up with multiple regions.
Each region describes the material of multiple vertices.
The constraints are splitted in multiple steps. In each step different constraints can be activated.
The steps are correspond to the steps in the ``<environment>``. Additionaly you can request outputs for a specific object.

.. todo::

    refer to documeantion of elements


.. code-block:: xml

    <scene>
        <object id="bunny">
            <mesh>
                <linearTet id="bunnyMesh" mesh="${bunnyVolumeMesher}"/>
            </mesh>

            <material>
                <region id="bunnyMaterial" indices="${bodyToIndexGroup}">
                    <linearElasticMaterial youngModulus="80000" poissonRatio="0.49"/>
                    <mass name="abc" massDensity="1000"/>
                </region>
            </material>

            <constraints>
                <constraint name="test" forStep="${initial}">
                    <fixedConstraint time="0" indices="${bottomToIndexGroup}"/>
                </constraint>
            </constraints>

            <output>
                <displacement id="liver" timestep="1"/>
            </output>
        </object>
    </scene>


.. todo::

    explain environment


.. code-block:: xml

    <environment>
        <solver linearSolver="iterativeCG" processingUnit="CPU"
                timeIntegration="dynamicImplicitEuler"/>
        <simulation>
            <step name="initial" dt="0.05" iterations="100"/>
        </simulation>
    </environment>
