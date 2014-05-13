.. annotation_

annotation
==========


    NO DOCUMENTATION



:Elements SEQUENCE:

.. arg_

arg
===


    NO DOCUMENTATION


:Attributes:
  * **name** : `string`

    NO DOCUMENTATION

  * **physical** : `string`

    NO DOCUMENTATION

  * *logical* : `string`

    NO DOCUMENTATION

  * *optional* : `boolean`

    NO DOCUMENTATION

  * *default* : `string`

    NO DOCUMENTATION


:Elements SEQUENCE:

.. body_

body
====


    NO DOCUMENTATION



:Elements: *any element*

.. constraint_

constraint
==========


    NO DOCUMENTATION


:Attributes:
  * *name* : `string`

    NO DOCUMENTATION

  * *forStep* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. constraints_

constraints
===========


    NO DOCUMENTATION



:Elements SEQUENCE:

.. description_

description
===========


    NO DOCUMENTATION




.. element_

element
=======


    NO DOCUMENTATION


:Attributes:
  * *name* : `string`

    NO DOCUMENTATION

  * **category** : `string` of [constraint, mesh, basic, indexgroup, material]    NO DOCUMENTATION

  * **quantity** : `string` of [single, multi]    NO DOCUMENTATION


:Elements SEQUENCE:
  * description_ {1-1}
  * parameters_ {0-1}
  * inputs_ {0-1}

.. elements_

elements
========


    NO DOCUMENTATION



:Elements SEQUENCE:

.. entry_

entry
=====


    NO DOCUMENTATION


:Attributes:
  * *value* : `string`

    NO DOCUMENTATION

  * **key** : `anySimpleType`

    NO DOCUMENTATION


:Elements: *any element*

.. environment_

environment
===========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * solver_ {1-1}
  * simulation_ {1-1}

.. file_

file
====


    NO DOCUMENTATION


:Attributes:
  * **name** : `string`

    NO DOCUMENTATION

  * *location* : `string`

    NO DOCUMENTATION

  * *type* : `string`

    NO DOCUMENTATION

  * *format* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. group_

group
=====


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * group_ {1-1}
  * object_ {1-1}

.. indexgroup_

indexgroup
==========


    NO DOCUMENTATION


:Attributes:
  * *indices* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. input_

input
=====


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

.. inputs_

inputs
======


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

.. linearTet_

linearTet
=========


    NO DOCUMENTATION


:Attributes:
  * *mesh* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. material_

material
========


    NO DOCUMENTATION



:Elements SEQUENCE:

.. mesh_

mesh
====


    NO DOCUMENTATION



:Elements CHOICE:
  * linearTet_ {1-1}
  * quadraticTet_ {1-1}
  * triangularTet_ {1-1}

.. meta_

meta
====


    NO DOCUMENTATION


:Attributes:
  * *value* : `string`

    NO DOCUMENTATION

  * **key** : `anySimpleType`

    NO DOCUMENTATION


:Elements: *any element*

.. msml_

msml
====


    NO DOCUMENTATION



:Elements SEQUENCE:
  * variables_ {0-1}
  * scene_ {0-1}
  * workflow_ {0-1}
  * environment_ {0-1}

.. nodes_

nodes
=====


    NO DOCUMENTATION



:Elements SEQUENCE:

.. object_

object
======


    NO DOCUMENTATION


:Attributes:
  * *id* : `string`

    NO DOCUMENTATION


:Elements ALL:
  * body_ {0-1}
  * material_ {0-1}
  * constraints_ {0-1}
  * mesh_ {1-1}
  * sets_ {0-1}
  * output_ {0-1}

.. operator_

operator
========


    NO DOCUMENTATION


:Attributes:
  * **name** : `string`

    NO DOCUMENTATION


:Elements ALL:
  * runtime_ {1-1}
  * input_ {1-1}
  * output_ {1-1}
  * parameters_ {0-1}
  * annotation_ {0-1}

.. output_

output
======


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

.. parameters_

parameters
==========


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

.. python_

python
======


    NO DOCUMENTATION


:Attributes:
  * **module** : `string`

    NO DOCUMENTATION

  * **function** : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. quadraticTet_

quadraticTet
============


    NO DOCUMENTATION


:Attributes:
  * *mesh* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. region_

region
======


    NO DOCUMENTATION


:Attributes:
  * **id** : `string`

    NO DOCUMENTATION

  * **indices** : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. runtime_

runtime
=======


    NO DOCUMENTATION



:Elements CHOICE:
  * python_ {1-1}
  * sh_ {1-1}
  * so_ {1-1}

.. scene_

scene
=====


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * group_ {1-1}
  * object_ {1-1}

.. sets_

sets
====


    NO DOCUMENTATION



:Elements SEQUENCE:
  * nodes_ {0-1}
  * elements_ {0-1}
  * surfaces_ {0-1}

.. sh_

sh
==


    NO DOCUMENTATION


:Attributes:
  * **file** : `string`

    NO DOCUMENTATION

  * **wd** : `string`

    NO DOCUMENTATION

  * *template* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. simulation_

simulation
==========


    NO DOCUMENTATION



:Elements SEQUENCE:

.. so_

so
==


    NO DOCUMENTATION


:Attributes:
  * **file** : `string`

    NO DOCUMENTATION

  * **symbol** : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. solver_

solver
======


    NO DOCUMENTATION


:Attributes:
  * *processingUnit* : `string` of [CPU, GPU]    NO DOCUMENTATION

  * *linearSolver* : `string` of [iterativeCG, CG, GMRES]    NO DOCUMENTATION

  * *preconditioner* : `string` of [NOPRECOND, JACOBI, GAUSS_SEIDEL, SGAUSS_SEIDEL, SOR, SSOR, ILU, ILU2, ILU_P]    NO DOCUMENTATION

  * *timeIntegration* : `string` of [dynamicImplicitEuler, Newmark]    NO DOCUMENTATION


:Elements: *any element*

.. step_

step
====


    NO DOCUMENTATION


:Attributes:
  * *name* : `string`

    NO DOCUMENTATION

  * *dt* : `float`

    NO DOCUMENTATION

  * *iterations* : `int`

    NO DOCUMENTATION


:Elements: *any element*

.. struct_

struct
======


    NO DOCUMENTATION


:Attributes:
  * *name* : `string`

    NO DOCUMENTATION

  * *optional* : `boolean`

    NO DOCUMENTATION


:Elements SEQUENCE:

.. surfaces_

surfaces
========


    NO DOCUMENTATION



:Elements SEQUENCE:

.. triangularTet_

triangularTet
=============


    NO DOCUMENTATION


:Attributes:
  * *mesh* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. var_

var
===


    NO DOCUMENTATION


:Attributes:
  * **name** : `string`

    NO DOCUMENTATION

  * *value* : `string`

    NO DOCUMENTATION

  * *physical* : `string`

    NO DOCUMENTATION

  * *logical* : `string`

    NO DOCUMENTATION


:Elements: *any element*

.. variables_

variables
=========


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * var_ {1-1}
  * file_ {1-1}

.. workflow_

workflow
========


    NO DOCUMENTATION



:Elements: *any element*

