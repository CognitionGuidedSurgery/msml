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
SET(VCGOperators_SRCS ${VTK_LIBRARIES} ${VCG_LIBRARIES})

INCLUDE_DIRECTORIES(
  ${VCGOperators_SOURCE_DIR}
  ${VCGOperators_BINARY_DIR}
  ${VCG_INCLUDE_DIR}
)


    
MSML_LIBRARY(
  NAME      VCGOperators
  SWIG_FILE vcg.i
  SOURCES   ${VCGOperators_SRCS}
  LIBRARIES ${VCGOperators_LIBS})