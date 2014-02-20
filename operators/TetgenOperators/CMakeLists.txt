PROJECT(TetgenOperators)

SET(TetgenOperators_SRCS
   TetgenOperators.h
   TetgenOperators.cpp
   )

INCLUDE_DIRECTORIES(
  ${TetgenOperators_SOURCE_DIR}
  ${TetgenOperators_BINARY_DIR}
  ${TETGEN_INCLUDE_DIR}
   ${PYTHON_INCLUDE_DIRS}
  #${VCG_INCLUDE_DIR}
  )
  
SET(TetgenOperatorsPython_SRCS
       PythonWrappers.cpp
   )
#########################
# Sets preprocessor variables
#########################

IF(WIN32 AND NOT CYGWIN)
    ADD_LIBRARY(TetgenOperators STATIC ${TetgenOperators_SRCS})
ELSE(WIN32 AND NOT CYGWIN)
    ADD_LIBRARY(TetgenOperators SHARED ${TetgenOperators_SRCS})
ENDIF(WIN32 AND NOT CYGWIN)

ADD_LIBRARY(TetgenOperatorsPython SHARED ${TetgenOperatorsPython_SRCS})
IF(WIN32 AND NOT CYGWIN)
	SET_TARGET_PROPERTIES(TetgenOperatorsPython PROPERTIES SUFFIX ".pyd")
ENDIF(WIN32 AND NOT CYGWIN)

set_target_properties(TetgenOperatorsPython PROPERTIES PREFIX "")

TARGET_LINK_LIBRARIES(TetgenOperators ${VTK_LIBRARIES}
${TETGEN_LIBRARIES}
)

TARGET_LINK_LIBRARIES(TetgenOperatorsPython ${VTK_LIBRARIES}
${TETGEN_LIBRARIES}
${Boost_LIBRARIES}
${PYTHON_LIBRARIES} 
TetgenOperators
)

