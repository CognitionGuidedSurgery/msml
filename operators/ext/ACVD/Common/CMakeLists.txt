PROJECT(ACVDCommon)

 # --------------------------------------------------------------------------
 # Library compilation
 ADD_LIBRARY(vtkSurface SHARED 
 RenderWindow.cxx
 vtkDelaunay.cxx
 vtkDualMeshDisplay.cxx
 vtkOFFReader.cxx
 vtkOFFWriter.cxx
 vtkQuadricTools.cxx
 vtkRandomTriangulation.cxx
 vtkSMFReader.cxx
 vtkSurface.cxx
 vtkSurfaceBase.cxx
 vtkVolumeProperties.cxx
 vtkNeighbourhoodComputation.cxx
 vtkCurvatureMeasure.cxx
 vtkMyMinimalStandardRandomSequence.cxx
#  vtkJSWriter.cxx
 )
 

# Set the added libraries
SET(LIB_ADDED 
vtkCommon
vtkFiltering
vtkImaging
vtkIO
vtkRendering
vtkHybrid)

TARGET_LINK_LIBRARIES(vtkSurface  ${LIB_ADDED})

SET(COMMON_EXAMPLES
viewer
viewer2
RandomTriangulation
ExamplevtkSurface
CleanMesh
mesh2vtk
vtk2ply
stl2ply
CheckOrientation
)

 if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" VERSION_GREATER 2.6)
  if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}.${CMAKE_PATCH_VERSION}" VERSION_GREATER 2.8.3)
    cmake_policy(VERSION 2.8.4)
  else()
    cmake_policy(VERSION 2.6)
  endif()
endif()


FOREACH(loop_var ${COMMON_EXAMPLES})
	ADD_EXECUTABLE(${loop_var} ${loop_var}.cxx)
	TARGET_LINK_LIBRARIES(${loop_var} vtkSurface
	vtkCommon vtkFiltering vtkGraphics vtkImaging vtkIO vtkRendering vtkHybrid)
ENDFOREACH(loop_var)

#-----------------------------------------------------------------------------
# Include the file 'InstallLibrary.cmake' which does the clean install job
#SET(LIBRARY_NAME vtkSurface)
#SET(LIBRARY_NAME_BUILD_TREE_CONFIG ${VTKSURFACE_BINARY_DIR})
# Installation
# Headers
#INSTALL_FILES(/include/${LIBRARY_NAME} "\\.h$")
# Binary
#INSTALL_TARGETS(/lib ${LIBRARY_NAME})
#SET(INSTALL_LIBRARY_FILES_DIR ${VTKSURFACE_SOURCE_DIR}/CMake)
#INCLUDE(${VTKSURFACE_SOURCE_DIR}/CMake/InstallLibrary.cmake)
#-----------------------------------------------------------------------------
