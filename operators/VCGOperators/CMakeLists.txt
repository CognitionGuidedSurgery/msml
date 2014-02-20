PROJECT(VCGOperators)
  
SET(VCGOperators_SRCS
   VCGOperators.h
   VCGOperators.cpp
   )

INCLUDE_DIRECTORIES(
  ${VCGOperators_SOURCE_DIR}
  ${VCGOperators_BINARY_DIR}
  ${VCG_INCLUDE_DIR}
  )
  
  
  SET(VCGOperatorsPython_SRCS
       PythonWrappers.cpp
   )
   
#########################
# Sets preprocessor variables
#########################

ADD_LIBRARY(VCGOperators SHARED ${VCGOperators_SRCS})

ADD_LIBRARY(VCGOperatorsPython SHARED ${VCGOperatorsPython_SRCS})
IF(WIN32 AND NOT CYGWIN)
	SET_TARGET_PROPERTIES(VCGOperatorsPython PROPERTIES SUFFIX ".pyd")
ENDIF(WIN32 AND NOT CYGWIN)

set_target_properties(VCGOperatorsPython PROPERTIES PREFIX "")

TARGET_LINK_LIBRARIES(VCGOperators ${VTK_LIBRARIES}
)

TARGET_LINK_LIBRARIES(VCGOperatorsPython ${VTK_LIBRARIES}
${Boost_LIBRARIES}
${PYTHON_LIBRARIES} 
VCGOperators
)