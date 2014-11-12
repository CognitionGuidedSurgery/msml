PROJECT(TetgenOperators)

option(MODULES_TetgenOperators "Should TetgenOperators build?" "ON")

################################################################################
# Dependencies: 

FIND_PACKAGE(TETGEN)

################################################################################
# Guard

SET(TetgenOperators_ACTIVE "OFF")
IF(NOT TETGEN_FOUND)  
  message("TetgenOperators need TETGEN")
  RETURN()
ENDIF()


################################################################################
# TetgenOperators 

SET(TetgenOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("TetgenOperators: ENABLED and ACTIVE")

INCLUDE_DIRECTORIES(${TETGEN_INCLUDE_DIRS})
add_definitions(-DTETLIBRARY)

SET(TetgenOperators_SRCS TetgenOperators.cpp)

INCLUDE_DIRECTORIES(
  ${TetgenOperators_SOURCE_DIR}
  ${TetgenOperators_BINARY_DIR}
  ${TETGEN_INCLUDE_DIR}
  ${WRAPPER_INCLUDES}
  )

SET(TetgenOperators_LIBS
  ${VTK_LIBRARIES}
  ${TETGEN_LIBRARIES}
  ${Boost_LIBRARIES})
  
  message("TETGEN libraries are ${TetgenOperators_LIBS}")

MSML_LIBRARY(
  NAME TetgenOperators
  SWIG_FILE tetgen.i 
  SOURCES ${TetgenOperators_SRCS}
  LIBRARIES ${TetgenOperators_LIBS})
