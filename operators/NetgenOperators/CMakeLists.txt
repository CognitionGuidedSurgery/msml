PROJECT(NetgenOperators)

option(MODULES_NetgenOperators "Should NetgenOperators build?" "ON")

################################################################################
# Dependencies: 

FIND_PACKAGE(NETGEN)

################################################################################
# Guard

SET(NetgenOperators_ACTIVE "OFF")
IF(NOT NETGEN_FOUND)  
  message("NetgenOperators need NETGEN")
  RETURN()
ENDIF()


################################################################################
# NetgenOperators 

SET(NetgenOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("NetgenOperators: ENABLED and ACTIVE")

INCLUDE_DIRECTORIES(${NETGEN_INCLUDE_DIRS})
add_definitions(-DTETLIBRARY)



SET(NetgenOperators_SRCS NetgenOperators.cpp)

INCLUDE_DIRECTORIES(
  ${NetgenOperators_SOURCE_DIR}
  ${NetgenOperators_BINARY_DIR}
  ${NETGEN_INCLUDE_DIR}
  ${WRAPPER_INCLUDES}
  )

SET(NetgenOperators_LIBS
  ${NETGEN_LIBRARIES}
  ${VTK_LIBRARIES}  
  ${Boost_LIBRARIES})

#message("NETGEN libraries are ${NetgenOperators_LIBS}")



MSML_LIBRARY(
  NAME NetgenOperators
  SWIG_FILE netgen.i
  SOURCES ${NetgenOperators_SRCS}
  LIBRARIES ${NetgenOperators_LIBS})
