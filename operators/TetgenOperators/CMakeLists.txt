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

SET(TetgenOperators_SRCS
  TetgenOperators.h
  TetgenOperators.cpp
  )

INCLUDE_DIRECTORIES(
  ${TetgenOperators_SOURCE_DIR}
  ${TetgenOperators_BINARY_DIR}
  ${TETGEN_INCLUDE_DIR}
  ${PYTHON_INCLUDE_DIRS}
  )

SET(TetgenOperatorsPython_SRCS
  PythonWrappers.cpp
  )

SET_SOURCE_FILES_PROPERTIES(tetgen.i PROPERTIES CPLUSPLUS ON)
#SET_SOURCE_FILES_PROPERTIES(tetgen.i PROPERTIES SWIG_FLAGS "-includeall")
SWIG_ADD_MODULE(TetgenOperatorsPython python tetgen.i ${TetgenOperators_SRCS})
SWIG_LINK_LIBRARIES(TetgenOperatorsPython
  ${VTK_LIBRARIES}
  ${TETGEN_LIBRARIES}
  ${Boost_LIBRARIES}
  ${PYTHON_LIBRARIES} 
  )

#########################
# Sets preprocessor variables
#########################

IF(WIN32 AND NOT CYGWIN)
  ADD_LIBRARY(TetgenOperators STATIC ${TetgenOperators_SRCS})
ELSE(WIN32 AND NOT CYGWIN)
  ADD_LIBRARY(TetgenOperators SHARED ${TetgenOperators_SRCS})
ENDIF(WIN32 AND NOT CYGWIN)

TARGET_LINK_LIBRARIES(TetgenOperators ${VTK_LIBRARIES}  ${TETGEN_LIBRARIES})
