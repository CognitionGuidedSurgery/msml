PROJECT(TetgenOperators)


FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

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

SET(CMAKE_SWIG_FLAGS "")

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

TARGET_LINK_LIBRARIES(TetgenOperators ${VTK_LIBRARIES}
  ${TETGEN_LIBRARIES}
)

