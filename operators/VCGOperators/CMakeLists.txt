PROJECT(VCGOperators)

OPTION(MODULES_VCGOperators "Should VCGOperators be built?" "ON")

################################################################################
# Dependencies:   

FIND_PACKAGE(VCG)

################################################################################
# Guard
SET(VCGOperators_ACTIVE "OFF")  

IF(NOT MODULES_VCGOperators) 
  MESSAGE(STATUS "VCGOperators disabled by user!")
  RETURN()
ENDIF()

IF(NOT VCG_FOUND)
  MESSAGE(STATUS "VCGOperators need VCG, but this library was not found")
  RETURN()
ENDIF(NOT VCG_FOUND)

################################################################################
# MiscMeshOperators
SET(VCGOperators_ACTIVE "ON" PARENT_SCOPE)  
MESSAGE("VCGOperators: ENABLED and ACTIVE")

SET(VCGOperators_SRCS VCGOperators.cpp)

INCLUDE_DIRECTORIES(
  ${VCGOperators_SOURCE_DIR}
  ${VCGOperators_BINARY_DIR}
  ${VCG_INCLUDE_DIR}
)
  
SET_SOURCE_FILES_PROPERTIES(vcg.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(VCGOperatorsPython python vcg.i ${VCGOperators_SRCS})
SWIG_LINK_LIBRARIES(VCGOperatorsPython ${VTK_LIBRARIES} ${PYTHON_LIBRARIES})
ADD_LIBRARY(VCGOperators SHARED ${VCGOperators_SRCS})
TARGET_LINK_LIBRARIES(VCGOperators ${VTK_LIBRARIES}
)
