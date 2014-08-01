MSML Internals
======================================


Data flow
---------


* Parsing
* validation
* graph building
  * variables

* executer
  * operator
* exporter


Sort Logic and Type Safety
--------------------------

MSML use sorts logic as the backbone of type safety. Sorts are mapped to Python classes and types.
The base package of msml comes with a predefined sorts for the defined operators. If you have any wishes feel free to open an [issue](https://github.com/CognitionGuidedSurgery/msml/issues).

We use two sorts trees! One tree is the **logical type** the other one is for **physical type**. The **logical** hierarchy describes the data type (mesh, index set, image etc.). The **physical** expresses how the data is represented in memory or on hdd.


Sort Hierarchy
^^^^^^^^^^^^^^

Logical
~~~~~~~

* IndexSet

  * NodeSet
  * FaceSet
  * ElementSet
  * MultiPurposeIndexSet

* Mesh

  * Volume

    * Tetrahdral
    * Hexahedral
    * QuadraticTetrahedral

  * Surface

    * Triangular

* Image
    * Image2D
    * Image3D

* PhysicalQuantities

  * Scalar

    * VonMises Stress

  * Vector

    * Displacement
    * Force
    * Velocity

  * Tensor

    * Stress

Physical
~~~~~~~~

* InMemory

  * float
  * int
  * uint
  * str
  * ListUI
  * ListI
  * ListF

* AsFilename ( :py:class::`str`)

  * JPG
  * PNG
  * ContainerFile

    * VTK
    * VTU
    * VTI
    * DICOM
    * HDF5
  * STL


Sorten Verträglichkeit
^^^^^^^^^^^^^^^^^^^^^^


Conversion
^^^^^^^^^^

A conversion between two representations can be done automatically if there is a knwon transfer function.
The `msml.sorts` module provides the nessecary interface:

.. code-block:: python

   msml.sorts.register_transfer( given = Sort(Mesh, VTK)),
                                 to = (Mesh.Surface:triangular, AsFilename.STL),
                                 fn = lambda x: int(x),
                                 precedence = 100)


The automatic conversion can only take place between Sorts that have
the same data types, but different representations. Only operators can
change one data type to another. This mapping is usually not
unique. With these definition we are able to build an network of
conversions from one type to another. Another point is the check of
user input in the XML file, especially if a format given.

The function `register_check` handle this:

.. code-block:: python

   msml.sorts.register_check(sort = Sort(filename, vtk),
      lambda xml_user_input: xml_user_input.endswith(".vtk"))


## Define a sort by your own



Exporter Interface
------------------


Build Graph
-----------


Executioner
-----------
