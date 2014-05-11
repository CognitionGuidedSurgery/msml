PROJECT(MiscMeshOperators)

OPTION(MODULES_MiscMeshOperators "Should MiscMeshOperators be built?" "ON")

################################################################################
# Dependencies: 

FIND_PACKAGE(TETGEN)

################################################################################
# Guard

SET(MiscMeshOperators_ACTIVE "OFF")  

IF(NOT MODULES_MiscMeshOperators)
  MESSAGE("MiscMeshOperators disabled by user!")
ENDIF()

IF(NOT TETGEN_FOUND) 
  message("MiscMeshOperators need Tetgen, but not found!")
  RETURN()
ENDIF()


################################################################################
# MiscMeshOperators

SET(MiscMeshOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("MiscMeshOperators: ENABLED and ACTIVE")


SET(MiscMeshOperators_SRCS
  IOHelper.cpp
  MiscMeshOperators.cpp
  PostProcessingOperators.cpp
  IndexRegionOperators.cpp   
  MappingOperators.cpp
  )

SET(MiscMeshOperators_LIBS
  ${VTK_LIBRARIES}
  ${SOLID_LIBRARIES}
  ${TETGEN_LIBRARIES}
  ${Boost_LIBRARIES})

INCLUDE_DIRECTORIES(
  ${MiscMeshOperators_SOURCE_DIR}
  ${MiscMeshOperators_BINARY_DIR}
  ${PYTHON_INCLUDE_DIRS}
  )

MSML_LIBRARY(
  NAME      MiscMeshOperators
  SWIG_FILE miscmesh.i
  SOURCES   ${MiscMeshOperators_SRCS}
  LIBRARIES ${MiscMeshOperators_LIBS})


SET(MiscMeshOperatorsExample_SRCS Example.cpp)
  
ADD_EXECUTABLE (MiscMeshOperatorsExample ${MiscMeshOperatorsExample_SRCS} )
TARGET_LINK_LIBRARIES(MiscMeshOperatorsExample 
  MiscMeshOperators 
  ${MiscMeshOperators_LIBS}
)

