PROJECT(MiscExtOperators)


################################################################################
# Dependencies: 



################################################################################
# Guard

SET(MiscExtOperators_ACTIVE "OFF")  





################################################################################
# MiscExtOperators

SET(MiscExtOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("MiscExtOperators: ENABLED and ACTIVE")


SET(MiscExtOperators_SRCS
  MiscExtOperators.cpp

  )

SET(MiscExtOperators_LIBS
  ${VTK_LIBRARIES}
  vtkSurface
  vtkDiscreteRemeshing
  MiscMeshOperators
)

INCLUDE_DIRECTORIES(
  ${MiscExtOperators_SOURCE_DIR}
  ${MiscExtOperators_BINARY_DIR}
  ${PYTHON_INCLUDE_DIRS}
  #for iohelper:
  ${CMAKE_SOURCE_DIR}/MiscMeshOperators
  ${CMAKE_SOURCE_DIR}/ext/ACVD/Common
  ${CMAKE_SOURCE_DIR}/ext/ACVD/DiscreteRemeshing
  ${CMAKE_SOURCE_DIR}/ext/ACVD/VolumeProcessing
  )

MSML_LIBRARY(
  NAME      MiscExtOperators
  SWIG_FILE miscext.i
  SOURCES   ${MiscExtOperators_SRCS}
  LIBRARIES ${MiscExtOperators_LIBS})



