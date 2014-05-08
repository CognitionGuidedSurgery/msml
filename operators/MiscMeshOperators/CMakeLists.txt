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

INCLUDE_DIRECTORIES(
  ${MiscMeshOperators_SOURCE_DIR}
  ${MiscMeshOperators_BINARY_DIR}
  ${PYTHON_INCLUDE_DIRS}
  )

SET(MiscMeshOperatorsExample_SRCS Example.cpp)
  
  
# Python Wrapper
SET_SOURCE_FILES_PROPERTIES(miscmesh.i PROPERTIES CPLUSPLUS ON)
#SET_SOURCE_FILES_PROPERTIES(tetgen.i PROPERTIES SWIG_FLAGS "-includeall")
SWIG_ADD_MODULE(MiscMeshOperatorsPython python miscmesh.i ${MiscMeshOperators_SRCS})
SWIG_LINK_LIBRARIES(MiscMeshOperatorsPython
  ${VTK_LIBRARIES}
  ${SOLID_LIBRARIES}
  ${TETGEN_LIBRARIES}
  ${Boost_LIBRARIES}
  ${PYTHON_LIBRARIES}
  )

IF(WIN32 AND NOT CYGWIN)
  ADD_LIBRARY(MiscMeshOperators STATIC ${MiscMeshOperators_SRCS})
ELSE()
  ADD_LIBRARY(MiscMeshOperators SHARED ${MiscMeshOperators_SRCS})
ENDIF()

TARGET_LINK_LIBRARIES(MiscMeshOperators ${VTK_LIBRARIES}
  ${TETGEN_LIBRARIES} 
  ${SOLID_LIBRARIES}
  ${Boost_LIBRARIES}
  )

ADD_EXECUTABLE (MiscMeshOperatorsExample ${MiscMeshOperatorsExample_SRCS} )
TARGET_LINK_LIBRARIES(MiscMeshOperatorsExample MiscMeshOperators ${VTK_LIBRARIES}
  ${TETGEN_LIBRARIES}
  ${Boost_LIBRARIES}
  MiscMeshOperators
  )


