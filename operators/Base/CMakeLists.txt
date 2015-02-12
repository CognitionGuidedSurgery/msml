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

SET(Base_LIBS "")

MSML_LIBRARY(
  NAME Base
  SWIG_FILE base.i
  SOURCES "Converters.h" "Converters.cpp"
  LIBRARIES ${Base_LIBS})
