  * element_

    * description_
    * parameters_

      * arg_

        * meta_

      * struct_

        * arg_

          * meta_



    * inputs_

      * arg_

        * meta_

      * struct_

        * arg_

          * meta_




  * msml_

    * variables_

      * var_
      * file_

    * scene_

      * group_

        * object_

          * body_
          * material_

            * region_

          * constraints_

            * constraint_

          * mesh_

            * linearTet_
            * quadraticTet_
            * triangularTet_

          * sets_

            * nodes_

              * indexgroup_

            * elements_

              * indexgroup_

            * surfaces_

              * indexgroup_


          * output_

            * arg_

              * meta_

            * struct_

              * arg_

                * meta_





      * object_

        * body_
        * material_

          * region_

        * constraints_

          * constraint_

        * mesh_

          * linearTet_
          * quadraticTet_
          * triangularTet_

        * sets_

          * nodes_

            * indexgroup_

          * elements_

            * indexgroup_

          * surfaces_

            * indexgroup_


        * output_

          * arg_

            * meta_

          * struct_

            * arg_

              * meta_





    * workflow_
    * environment_

      * solver_
      * simulation_

        * step_



  * operator_

    * runtime_

      * python_
      * sh_
      * so_

    * input_

      * arg_

        * meta_

      * struct_

        * arg_

          * meta_



    * output_

      * arg_

        * meta_

      * struct_

        * arg_

          * meta_



    * parameters_

      * arg_

        * meta_

      * struct_

        * arg_

          * meta_



    * annotation_

      * entry_




.. annotation_

annotation
==========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * entry_ {0-0}

:Parents: 
  * operator_ 

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
  * meta_ {0-0}

:Parents: 
  * struct_ 
  * inputs_ 
  * output_ 
  * input_ 
  * parameters_ 

.. body_

body
====


    NO DOCUMENTATION



:Elements: *any element*

:Parents: 
  * object_ 

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

:Parents: 
  * constraints_ 

.. constraints_

constraints
===========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * constraint_ {0-0}

:Parents: 
  * object_ 

.. description_

description
===========


    NO DOCUMENTATION



:Elements: none

:Parents: 
  * element_ 

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

:Parents: None

.. elements_

elements
========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * indexgroup_ {0-0}

:Parents: 
  * sets_ 

.. entry_

entry
=====


    NO DOCUMENTATION


:Attributes:
  * *value* : `string`

    NO DOCUMENTATION

  * **key** : `anySimpleType`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * annotation_ 

.. environment_

environment
===========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * solver_ {1-1}
  * simulation_ {1-1}

:Parents: 
  * msml_ 

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


:Elements: none

:Parents: 
  * variables_ 

.. group_

group
=====


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * group_ {1-1}
  * object_ {1-1}

:Parents: 
  * scene_ 
  * group_ 

.. indexgroup_

indexgroup
==========


    NO DOCUMENTATION


:Attributes:
  * *indices* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * surfaces_ 
  * nodes_ 
  * elements_ 

.. input_

input
=====


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

:Parents: 
  * operator_ 

.. inputs_

inputs
======


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

:Parents: 
  * element_ 

.. linearTet_

linearTet
=========


    NO DOCUMENTATION


:Attributes:
  * *mesh* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * mesh_ 

.. material_

material
========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * region_ {0-0}

:Parents: 
  * object_ 

.. mesh_

mesh
====


    NO DOCUMENTATION



:Elements CHOICE:
  * linearTet_ {1-1}
  * quadraticTet_ {1-1}
  * triangularTet_ {1-1}

:Parents: 
  * object_ 

.. meta_

meta
====


    NO DOCUMENTATION


:Attributes:
  * *value* : `string`

    NO DOCUMENTATION

  * **key** : `anySimpleType`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * arg_ 

.. msml_

msml
====


    NO DOCUMENTATION



:Elements SEQUENCE:
  * variables_ {0-1}
  * scene_ {0-1}
  * workflow_ {0-1}
  * environment_ {0-1}

:Parents: None

.. nodes_

nodes
=====


    NO DOCUMENTATION



:Elements SEQUENCE:
  * indexgroup_ {0-0}

:Parents: 
  * sets_ 

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

:Parents: 
  * scene_ 
  * group_ 

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

:Parents: None

.. output_

output
======


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

:Parents: 
  * operator_ 
  * object_ 

.. parameters_

parameters
==========


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * arg_ {1-1}
  * struct_ {1-1}

:Parents: 
  * operator_ 
  * element_ 

.. python_

python
======


    NO DOCUMENTATION


:Attributes:
  * **module** : `string`

    NO DOCUMENTATION

  * **function** : `string`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * runtime_ 

.. quadraticTet_

quadraticTet
============


    NO DOCUMENTATION


:Attributes:
  * *mesh* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * mesh_ 

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

:Parents: 
  * material_ 

.. runtime_

runtime
=======


    NO DOCUMENTATION



:Elements CHOICE:
  * python_ {1-1}
  * sh_ {1-1}
  * so_ {1-1}

:Parents: 
  * operator_ 

.. scene_

scene
=====


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * group_ {1-1}
  * object_ {1-1}

:Parents: 
  * msml_ 

.. sets_

sets
====


    NO DOCUMENTATION



:Elements SEQUENCE:
  * nodes_ {0-1}
  * elements_ {0-1}
  * surfaces_ {0-1}

:Parents: 
  * object_ 

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


:Elements: none

:Parents: 
  * runtime_ 

.. simulation_

simulation
==========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * step_ {0-0}

:Parents: 
  * environment_ 

.. so_

so
==


    NO DOCUMENTATION


:Attributes:
  * **file** : `string`

    NO DOCUMENTATION

  * **symbol** : `string`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * runtime_ 

.. solver_

solver
======


    NO DOCUMENTATION


:Attributes:
  * *processingUnit* : `string` of [CPU, GPU]    NO DOCUMENTATION

  * *linearSolver* : `string` of [iterativeCG, CG, GMRES]    NO DOCUMENTATION

  * *preconditioner* : `string` of [NOPRECOND, JACOBI, GAUSS_SEIDEL, SGAUSS_SEIDEL, SOR, SSOR, ILU, ILU2, ILU_P]    NO DOCUMENTATION

  * *timeIntegration* : `string` of [dynamicImplicitEuler, Newmark]    NO DOCUMENTATION


:Elements: none

:Parents: 
  * environment_ 

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


:Elements: none

:Parents: 
  * simulation_ 

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
  * arg_ {0-0}

:Parents: 
  * inputs_ 
  * output_ 
  * input_ 
  * parameters_ 

.. surfaces_

surfaces
========


    NO DOCUMENTATION



:Elements SEQUENCE:
  * indexgroup_ {0-0}

:Parents: 
  * sets_ 

.. triangularTet_

triangularTet
=============


    NO DOCUMENTATION


:Attributes:
  * *mesh* : `string`

    NO DOCUMENTATION

  * *id* : `string`

    NO DOCUMENTATION


:Elements: none

:Parents: 
  * mesh_ 

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


:Elements: none

:Parents: 
  * variables_ 

.. variables_

variables
=========


    NO DOCUMENTATION



:Elements SEQUENCE of CHOICE:
  * var_ {1-1}
  * file_ {1-1}

:Parents: 
  * msml_ 

.. workflow_

workflow
========


    NO DOCUMENTATION



:Elements: *any element*

:Parents: 
  * msml_ 

