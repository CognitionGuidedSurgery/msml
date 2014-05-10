.. role:: red
.. raw:: html

    <style> .red {color: #ff6b59;} </style>

Version: 2014-05-05 15:21:01.096766

**Operatoren:**  mesherTetgen_  mesherCGALi2v_  mesherCGALs2v_  colormesh_  apply-dvf_  materialId-to-index_  boxROIToIndexOperator_  stl2vtk_  generateDVF_  ExtractAllSurfacesByMaterial_  surfaceExtract_  vtk-mesh-to-abaqus-mesh-str_  voxelize_  paraview_

**Elemente:**  displacementContraint_  surfacePressure_  springMeshToFixed_  fixedConstraint_  supportingMesh_  mass_  linearElasticMaterial_  illumination_


Operatoren
---------------------------------------



mesherTetgen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.tetgen``
:function: ``createVolumeMeshTetgen``

*Inputs:*

=========== ============= ============== ======================================= ======== ======= ==============
name        physical_type logical_type   sort                                    required default doc
=========== ============= ============== ======================================= ======== ======= ==============
surfaceMesh vtk           triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
=========== ============= ============== ======================================= ======== ======= ==============


*Output:*

==== ============= ============= ======================================= ======== ======= ==============
name physical_type logical_type  sort                                    required default doc
==== ============= ============= ======================================= ======== ======= ==============
mesh vtk           linearTetMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
==== ============= ============= ======================================= ======== ======= ==============


*Parameters:*

================ ============= ============ ============================================ ======== ======= =======================================
name             physical_type logical_type sort                                         required default doc
================ ============= ============ ============================================ ======== ======= =======================================
preserveBoundary bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None> True     None    :red:`MISSING`
meshFilename     filename      None         None                                         True     None    Optional input filename for the output.
================ ============= ============ ============================================ ======== ======= =======================================



*Annotations:*






mesherCGALi2v
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.cgal``
:function: ``CreateVolumeMeshi2v``

*Inputs:*

===== ============= ================= ======================================= ======== ======= ==============
name  physical_type logical_type      sort                                    required default doc
===== ============= ================= ======================================= ======== ======= ==============
image VTI           segmentationImage <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
===== ============= ================= ======================================= ======== ======= ==============


*Output:*

==== ============= ============= ======================================= ======== ======= ==============
name physical_type logical_type  sort                                    required default doc
==== ============= ============= ======================================= ======== ======= ==============
mesh VTK           linearTetMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
==== ============= ============= ======================================= ======== ======= ==============


*Parameters:*

====================== ============= ============ ============================================== ======== ======= =======================================
name                   physical_type logical_type sort                                           required default doc
====================== ============= ============ ============================================== ======== ======= =======================================
meshFilename           str           None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    Optional input filename for the output.
facet_angle            float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    :red:`MISSING`
facet_size             float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    :red:`MISSING`
facet_distance         float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    :red:`MISSING`
cell_radius_edge_ratio float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    :red:`MISSING`
cell_size              float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    :red:`MISSING`
odt                    bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>   True     None    :red:`MISSING`
lloyd                  bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>   True     None    :red:`MISSING`
pertube                bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>   True     None    :red:`MISSING`
exude                  bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>   True     None    :red:`MISSING`
====================== ============= ============ ============================================== ======== ======= =======================================



*Annotations:*






mesherCGALs2v
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.cgal``
:function: ``CreateVolumeMeshs2v``

*Inputs:*

=========== ============= ============== ======================================= ======== ======= ==============
name        physical_type logical_type   sort                                    required default doc
=========== ============= ============== ======================================= ======== ======= ==============
surfaceMesh file.vtk      triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
=========== ============= ============== ======================================= ======== ======= ==============


*Output:*

==== ============= ============= ======================================= ======== ======= ==============
name physical_type logical_type  sort                                    required default doc
==== ============= ============= ======================================= ======== ======= ==============
mesh file.vtk      linearTetMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
==== ============= ============= ======================================= ======== ======= ==============


*Parameters:*

====================== ============= ============ ============================================= ======== ======= =======================================
name                   physical_type logical_type sort                                          required default doc
====================== ============= ============ ============================================= ======== ======= =======================================
meshFilename           filename      None         None                                          True     None    Optional input filename for the output.
preserveFeatures       bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>  True     None    :red:`MISSING`
facet_angle            float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    :red:`MISSING`
facet_size             float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    :red:`MISSING`
facet_distance         float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    :red:`MISSING`
cell_radius_edge_ratio float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    :red:`MISSING`
cell_size              float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    :red:`MISSING`
odt                    bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>  True     None    :red:`MISSING`
lloyd                  bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>  True     None    :red:`MISSING`
pertube                bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>  True     None    :red:`MISSING`
exude                  bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None>  True     None    :red:`MISSING`
====================== ============= ============ ============================================= ======== ======= =======================================



*Annotations:*






colormesh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``colorMeshOperator``

*Inputs:*

==== ============= ============ ============================================================== ======== ======= ==============
name physical_type logical_type sort                                                           required default doc
==== ============= ============ ============================================================== ======== ======= ==============
mesh vtk           Mesh         <Sort: <class 'msml.sortdef.VTK'> <class 'msml.sortdef.Mesh'>> True     None    :red:`MISSING`
==== ============= ============ ============================================================== ======== ======= ==============


*Output:*

=========== ============= ============== ======================================= ======== ======= ==============
name        physical_type logical_type   sort                                    required default doc
=========== ============= ============== ======================================= ======== ======= ==============
coloredMesh vtk           triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
=========== ============= ============== ======================================= ======== ======= ==============


*Parameters:*

=========== ============= ============ ============================================== ======== ======= ==============
name        physical_type logical_type sort                                           required default doc
=========== ============= ============ ============================================== ======== ======= ==============
coloredMesh str           None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    :red:`MISSING`
=========== ============= ============ ============================================== ======== ======= ==============



*Annotations:*






apply-dvf
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``ApplyDVF``

*Inputs:*

======== ============= ============ ================================================================= ======== ======= ==============
name     physical_type logical_type sort                                                              required default doc
======== ============= ============ ================================================================= ======== ======= ==============
ApplyDVF VTK           Image3D      <Sort: <class 'msml.sortdef.VTK'> <class 'msml.sortdef.Image3D'>> True     None    :red:`MISSING`
======== ============= ============ ================================================================= ======== ======= ==============


*Output:*

============== ============= ============ ================================================================= ======== ======= ==============
name           physical_type logical_type sort                                                              required default doc
============== ============= ============ ================================================================= ======== ======= ==============
outputDefImage VTI           Image3D      <Sort: <class 'msml.sortdef.VTK'> <class 'msml.sortdef.Image3D'>> True     None    :red:`MISSING`
============== ============= ============ ================================================================= ======== ======= ==============


*Parameters:*

================ ============= ============ ============================================ ======== ======= ==============
name             physical_type logical_type sort                                         required default doc
================ ============= ============ ============================================ ======== ======= ==============
dvf              VTK           None         <Sort: <class 'msml.sortdef.VTK'> None>      True     None    :red:`MISSING`
multipleDVF      bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None> True     None    :red:`MISSING`
reverseDirection bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None> True     None    :red:`MISSING`
================ ============= ============ ============================================ ======== ======= ==============



*Annotations:*






materialId-to-index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``computeIndicesFromMaterialId``

*Inputs:*

==== ============= ============= ======================================= ======== ======= ==============
name physical_type logical_type  sort                                    required default doc
==== ============= ============= ======================================= ======== ======= ==============
mesh vtk           linearTetMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
==== ============= ============= ======================================= ======== ======= ==============


*Output:*

======= ============= ============ ============================================= ======== ======= ==============
name    physical_type logical_type sort                                          required default doc
======= ============= ============ ============================================= ======== ======= ==============
indices vector.int    indexGroup   <Sort: <class 'msml.sortdef.MSMLListI'> None> True     None    :red:`MISSING`
======= ============= ============ ============================================= ======== ======= ==============


*Parameters:*

==== ============= ============ ============================================== ======== ======= ==============
name physical_type logical_type sort                                           required default doc
==== ============= ============ ============================================== ======== ======= ==============
num  int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None>    True     None    :red:`MISSING`
type string        None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    :red:`MISSING`
==== ============= ============ ============================================== ======== ======= ==============



*Annotations:*






boxROIToIndexOperator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``computeIndicesFromBoxROI``

*Inputs:*

==== ============= =============================== ======================================= ======== ======= ==============
name physical_type logical_type                    sort                                    required default doc
==== ============= =============================== ======================================= ======== ======= ==============
mesh file.vtk      linearTetMesh, quadraticTetMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
==== ============= =============================== ======================================= ======== ======= ==============


*Output:*

======= ============= ============ ============================================= ======== ======= ==============
name    physical_type logical_type sort                                          required default doc
======= ============= ============ ============================================= ======== ======= ==============
indices vector.int    indexgroup   <Sort: <class 'msml.sortdef.MSMLListI'> None> True     None    :red:`MISSING`
======= ============= ============ ============================================= ======== ======= ==============


*Parameters:*

====== ============= ============ ============================================== ======== ======= ==============
name   physical_type logical_type sort                                           required default doc
====== ============= ============ ============================================== ======== ======= ==============
box    vector.float  None         <Sort: <class 'msml.sortdef.MSMLListFI'> None> True     None    :red:`MISSING`
select string        None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    :red:`MISSING`
====== ============= ============ ============================================== ======== ======= ==============



*Annotations:*






stl2vtk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``convertSTLToVTK``

*Inputs:*

======= ============= ============== ======================================= ======== ======= ==============
name    physical_type logical_type   sort                                    required default doc
======= ============= ============== ======================================= ======== ======= ==============
STLMesh stl           triangularMesh <Sort: <class 'msml.sortdef.STL'> None> True     None    :red:`MISSING`
======= ============= ============== ======================================= ======== ======= ==============


*Output:*

======= ============= ============== ======================================= ======== ======= ==============
name    physical_type logical_type   sort                                    required default doc
======= ============= ============== ======================================= ======== ======= ==============
VTKMesh vtk           triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
======= ============= ============== ======================================= ======== ======= ==============


*Parameters:*

=========== ============= ============ ============================================== ======== ======= =======================================
name        physical_type logical_type sort                                           required default doc
=========== ============= ============ ============================================== ======== ======= =======================================
vtkFilename str           None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    Optional input filename for the output.
=========== ============= ============ ============================================== ======== ======= =======================================



*Annotations:*






generateDVF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``GenerateDVF``

*Inputs:*

======= ================= ======================================= ==== ======== ======= ==============
name    physical_type     logical_type                            sort required default doc
======= ================= ======================================= ==== ======== ======= ==============
RefMesh file.vtk+file.vtu linearTetMesh+displacementOutputRequest None True     None    :red:`MISSING`
======= ================= ======================================= ==== ======== ======= ==============


*Output:*

==== ============= ============ ======================================= ======== ======= ==============
name physical_type logical_type sort                                    required default doc
==== ============= ============ ======================================= ======== ======= ==============
DVF  file.vtk      image        <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
==== ============= ============ ======================================= ======== ======= ==============


*Parameters:*

====================== ============= ============ ============================================ ======== ======= =======================================
name                   physical_type logical_type sort                                         required default doc
====================== ============= ============ ============================================ ======== ======= =======================================
DVFFilename            filename      None         None                                         True     None    Optional input filename for the output.
DeformedMesh           file.vtu      None         None                                         True     None    :red:`MISSING`
multipleReferenceGrids bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None> True     None    :red:`MISSING`
====================== ============= ============ ============================================ ======== ======= =======================================



*Annotations:*






ExtractAllSurfacesByMaterial
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``ExtractAllSurfacesByMaterial``

*Inputs:*

====== ============= ============================ ======================================= ======== ======= ==============
name   physical_type logical_type                 sort                                    required default doc
====== ============= ============================ ======================================= ======== ======= ==============
meshIn file.vtk      linearTetMesh+triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
====== ============= ============================ ======================================= ======== ======= ==============


*Output:*

======= ============= ============================ ======================================= ======== ======= ==============
name    physical_type logical_type                 sort                                    required default doc
======= ============= ============================ ======================================= ======== ======= ==============
meshOut file.vtk      linearTetMesh+triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
======= ============= ============================ ======================================= ======== ======= ==============


*Parameters:*

=============== ============= ============ ==== ======== ======= =======================================
name            physical_type logical_type sort required default doc
=============== ============= ============ ==== ======== ======= =======================================
meshOutFilename None          filename     None True     None    Optional input filename for the output.
cut             None          bool         None True     None    :red:`MISSING`
=============== ============= ============ ==== ======== ======= =======================================



*Annotations:*






surfaceExtract
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``ExtractAllSurfacesByMaterial``

*Inputs:*

====== ============= ============ ============================================================== ======== ======= ==============
name   physical_type logical_type sort                                                           required default doc
====== ============= ============ ============================================================== ======== ======= ==============
meshIn vtk           Mesh         <Sort: <class 'msml.sortdef.VTK'> <class 'msml.sortdef.Mesh'>> True     None    :red:`MISSING`
====== ============= ============ ============================================================== ======== ======= ==============


*Output:*

======= ============= ============ ============================================================== ======== ======= ==============
name    physical_type logical_type sort                                                           required default doc
======= ============= ============ ============================================================== ======== ======= ==============
meshOut vtk           Mesh         <Sort: <class 'msml.sortdef.VTK'> <class 'msml.sortdef.Mesh'>> True     None    :red:`MISSING`
======= ============= ============ ============================================================== ======== ======= ==============


*Parameters:*

==== ============= ============ ============================================ ======== ======= ==============
name physical_type logical_type sort                                         required default doc
==== ============= ============ ============================================ ======== ======= ==============
cud  bool          None         <Sort: <class 'msml.sortdef.MSMLBool'> None> True     None    :red:`MISSING`
==== ============= ============ ============================================ ======== ======= ==============



*Annotations:*






vtk-mesh-to-abaqus-mesh-str
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``convertVTKMeshToAbaqusMeshString``

*Inputs:*

========= ============= ============================== ======================================= ======== ======= ==============
name      physical_type logical_type                   sort                                    required default doc
========= ============= ============================== ======================================= ======== ======= ==============
inputMesh file.vtk      linearTetMesh+quadraticTetMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
========= ============= ============================== ======================================= ======== ======= ==============


*Output:*

==== ============= ============================== ============================================== ======== ======= ==============
name physical_type logical_type                   sort                                           required default doc
==== ============= ============================== ============================================== ======== ======= ==============
mesh string        linearTetMesh+quadraticTetMesh <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    :red:`MISSING`
==== ============= ============================== ============================================== ======== ======= ==============


*Parameters:*

============ ============= ============ ============================================== ======== ======= ==============
name         physical_type logical_type sort                                           required default doc
============ ============= ============ ============================================== ======== ======= ==============
partName     string        None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    :red:`MISSING`
materialName string        None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    :red:`MISSING`
============ ============= ============ ============================================== ======== ======= ==============



*Annotations:*






voxelize
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


:red:`DOCUMENTATION MISSING`



:type: PythonOperator
:modul: ``msml.ext.misc``
:function: ``voxelizeSurfaceMesh``

*Inputs:*

=========== ============= ============== ======================================= ======== ======= ==============
name        physical_type logical_type   sort                                    required default doc
=========== ============= ============== ======================================= ======== ======= ==============
surfaceMesh vtk           triangularMesh <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
=========== ============= ============== ======================================= ======== ======= ==============


*Output:*

===== ============= ================= ======================================= ======== ======= ==============
name  physical_type logical_type      sort                                    required default doc
===== ============= ================= ======================================= ======== ======= ==============
image vti           segmentationImage <Sort: <class 'msml.sortdef.VTK'> None> True     None    :red:`MISSING`
===== ============= ================= ======================================= ======== ======= ==============


*Parameters:*

============= ============= ============ ============================================== ======== ======= =======================================
name          physical_type logical_type sort                                           required default doc
============= ============= ============ ============================================== ======== ======= =======================================
imageFilename string        None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    Optional input filename for the output.
resolution    int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None>    True     None    :red:`MISSING`
============= ============= ============ ============================================== ======== ======= =======================================



*Annotations:*






paraview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    - calls paraview with the given ``mesh``
    - user have to click apply to display within paraview
    - blocks the execution



:type: **ShellOperator**
:template: ``paraview --data={data}``

*Inputs:*

==== ============= ============ ============================================================== ======== ======= ==============
name physical_type logical_type sort                                                           required default doc
==== ============= ============ ============================================================== ======== ======= ==============
data VTK           Mesh         <Sort: <class 'msml.sortdef.VTK'> <class 'msml.sortdef.Mesh'>> True     None    :red:`MISSING`
==== ============= ============ ============================================================== ======== ======= ==============


*Output:*

none


*Parameters:*

none



*Annotations:*


doc
    - calls paraview with the given ``mesh``
    - user have to click apply to display within paraview
    - blocks the execution






Attributes
---------------------------------------



.. _displacementContraint:

displacementContraint ``OAConstraint``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Set fixed points


============ ============= ============ ============================================= ======== ======= ================================================
name         physical_type logical_type sort                                          required default doc
============ ============= ============ ============================================= ======== ======= ================================================
time         float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    Set time.
indices      vector.int    None         <Sort: <class 'msml.sortdef.MSMLListI'> None> True     None    Set indices of fixed points separated by spaces.
displacement vector.int    None         <Sort: <class 'msml.sortdef.MSMLListI'> None> True     None    State the displacement of the point.
============ ============= ============ ============================================= ======== ======= ================================================




.. _surfacePressure:

surfacePressure ``OAConstraint``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Add pressure load to surface


======== ============= ============ =========================================== ======== ======= ================================================
name     physical_type logical_type sort                                        required default doc
======== ============= ============ =========================================== ======== ======= ================================================
time     int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None> True     None    Set time
indices  int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None> True     None    Set indices of fixed points separated by spaces.
pressure int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None> True     None    State the pressure of the triangle.
======== ============= ============ =========================================== ======== ======= ================================================




.. _springMeshToFixed:

springMeshToFixed ``OAConstraint``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Add a spring from point in mesh to fixed point in space.


================ ============= ============ ============================================== ======== ======= =====================================================
name             physical_type logical_type sort                                           required default doc
================ ============= ============ ============================================== ======== ======= =====================================================
stiffness        int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None>    True     None    Stiffness between fixed and moving points
rayleighStiffnes int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None>    True     None    rayleighStiffnes between fixed and moving points
fixedPoints      int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None>    True     None    Coordinates of the fixed points: x1 y1 z1 x2 y2 z2...
movingPoints     vector.float  None         <Sort: <class 'msml.sortdef.MSMLListFI'> None> True     None    Coordinates of the fixed points: x1 y1 z1 x2 y2 z2...
================ ============= ============ ============================================== ======== ======= =====================================================




.. _fixedConstraint:

fixedConstraint ``OAConstraint``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Set fixed points


======= ============= ============ ============================================= ======== ======= ================================================
name    physical_type logical_type sort                                          required default doc
======= ============= ============ ============================================= ======== ======= ================================================
time    float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    Set time.
indices vector.int    None         <Sort: <class 'msml.sortdef.MSMLListI'> None> True     None    Set indices of fixed points separated by spaces.
======= ============= ============ ============================================= ======== ======= ================================================




.. _supportingMesh:

supportingMesh ``OAConstraint``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Add a secondary mesh to support to main mesh. Usable for vessels or bones.


============ ============= ============ ============================================== ======== ======= ========================================================
name         physical_type logical_type sort                                           required default doc
============ ============= ============ ============================================== ======== ======= ========================================================
youngModulus float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    homogenous youngModulus
poissonRatio float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    homogenous poissonRatio
filename     string        None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    filename (TODO: allow @ operator with use data objects).
============ ============= ============ ============================================== ======== ======= ========================================================




.. _mass:

mass ``ObjectAttribute``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Set properties of the mass


=========== ============= ============ ============================================== ======== ======= =====================
name        physical_type logical_type sort                                           required default doc
=========== ============= ============ ============================================== ======== ======= =====================
name        str           None         <Sort: <class 'msml.sortdef.MSMLString'> None> True     None    Name the mass element
massDensity float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None>  True     None    Set the mass density
=========== ============= ============ ============================================== ======== ======= =====================




.. _linearElasticMaterial:

linearElasticMaterial ``OAMaterial``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Choose a linear elastic model


============ ============= ============ ============================================= ======== ======= ==================================
name         physical_type logical_type sort                                          required default doc
============ ============= ============ ============================================= ======== ======= ==================================
poissonRatio float         None         <Sort: <class 'msml.sortdef.MSMLFloat'> None> True     None    Set the poisson ratio of the model
youngModulus int           None         <Sort: <class 'msml.sortdef.MSMLInt'> None>   True     None    Set the young modulus of the model
============ ============= ============ ============================================= ======== ======= ==================================




.. _illumination:

illumination ``ObjectAttribute``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Set the illumination model


===== ============= ============ ============================================= ======== ======= =============
name  physical_type logical_type sort                                          required default doc
===== ============= ============ ============================================= ======== ======= =============
color vector.int    None         <Sort: <class 'msml.sortdef.MSMLListI'> None> True     None    Set the color
===== ============= ============ ============================================= ======== ======= =============


