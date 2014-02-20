"""
MSML -- Meta model.

defines classes for:

* operators 
* environments
* scene elements
* msml-files    

"""

__author__ = "Alexander Weigl"
__date__ = "2014-01-25"

from .exceptions import *

from .alphabet import Alphabet, Operator, PythonOperator, SharedObjectOperator, ShellOperator, \
    Argument, StructArgument, ObjectAttribute

from .base import MSMLFile, MSMLVariable, struct, \
    MSMLFileVariable, Workflow, Task, ObjectElement, SceneObject, \
    ObjectConstraints, SceneSets, IndexGroup, Mesh, MaterialRegion, \
    Reference, parse_attribute_value, random_var_name, Constant



