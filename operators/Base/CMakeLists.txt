PROJECT(Base)

option(MODULES_Base "Should Base Module build?, Yes you want!" "ON")

################################################################################
# Dependencies: 


################################################################################
# Guard


################################################################################
# TetgenOperators 

SET(Base_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("Base: ENABLED and ACTIVE")

FILE(GLOB BASE_SRC *.cpp)

INCLUDE_DIRECTORIES(
  ${Base_SOURCE_DIR}
  ${Base_BINARY_DIR}
  )

SET_SOURCE_FILES_PROPERTIES(base.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(BasePython ${SWIG_LANG}  base.i ${BASE_SRC})
SWIG_LINK_LIBRARIES(BasePython
  ${VTK_LIBRARIES}
  ${Boost_LIBRARIES}
  ${PYTHON_LIBRARIES} 
  )

