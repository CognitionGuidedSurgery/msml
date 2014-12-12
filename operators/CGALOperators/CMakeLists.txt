PROJECT(CGALOperators)

option(MODULES_CGALOperators "Should CGALOperators build?" "ON")

################################################################################
# Dependencies: 

FIND_PACKAGE(CGAL QUIET COMPONENTS Core ImageIO)
FIND_PACKAGE(Boost)

################################################################################
# Guard
SET(CGALOperators_ACTIVE "OFF")

IF(NOT MODULES_CGALOperators)
  MESSAGE(STATUS "CGALOperator disabled by user")
  RETURN()
ENDIF()

IF( NOT CGAL_FOUND) 
  MESSAGE("CGALOperators need the CGal Library. Not adding to build")
  RETURN()
ENDIF()

IF( NOT Boost_FOUND )
  MESSAGE("CGALOperators need the Boost Library. Not adding to build")
  RETURN()
ENDIF()

IF( NOT Boost_VERSION GREATER 103400 )
  MESSAGE(STATUS "CGALOperators need Boost in new version FOUND: ${Boost_VERSION}")
  message(STATUS "NOTICE: This program requires Boost >= 1.34.1, and will not be compiled.")
  RETURN()
ENDIF()
      
IF(NOT MiscMeshOperators_ACTIVE)
  message(STATUS "CGALOperators need MiscMeshOperators")
  RETURN()
ENDIF()


################################################################################
## CGalOperators

SET(CGALOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("CGALOperators: ENABLED and ACTIVE")

SET(CGALOperators_SRCS
  CGALOperators.cpp
  CGALOperators.h
  cgal_tet_to_vtk.h
  )

SET(CGALOperators_LIBS
  ${VTK_LIBRARIES} MiscMeshOperators)

INCLUDE( ${CGAL_USE_FILE} )
INCLUDE_DIRECTORIES(
  ${CMAKE_SOURCE_DIR}/MiscMeshOperators
  ${WRAPPER_INCLUDES})
# weigl: hä?

include(CGAL_CreateSingleSourceCGALProgram)
include_directories(BEFORE "../../include")


if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" VERSION_GREATER 2.6)
  if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}.${CMAKE_PATCH_VERSION}" VERSION_GREATER 2.8.3)
    cmake_policy(VERSION 2.8.4)
  else()
    cmake_policy(VERSION 2.6)
  endif()
endif()

MSML_LIBRARY(
  NAME      CGALOperators
  SWIG_FILE cgal.i 
  SOURCES   ${CGALOperators_SRCS}
  LIBRARIES ${CGALOperators_LIBS})

if(MSVC)
  # /bigobj is required for CGAL builds for windows
  SET( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /bigobj" )
  SET( CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /bigobj" )
endif()


############################################################################
## Testing

ADD_DEFINITIONS(-DBOOST_TEST_DYN_LINK)

ADD_EXECUTABLE(CGALOperatorsTest test/CGALOperatorsTest.cpp)
TARGET_LINK_LIBRARIES(CGALOperatorsTest
	CGALOperators
	${Boost_UNIT_TEST_FRAMEWORK_LIBS}
)
ADD_TEST(CGALOperatorsTest ${CMAKE_OPERATOR_DIRECTORY}/CGALOperatorsTest)