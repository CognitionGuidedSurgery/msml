PROJECT(VTKSURFACE)



################################################################################
# Guard
SET(ACVDOperators_ACTIVE "OFF")

IF(NOT MODULES_MiscExtOperators)
  MESSAGE(STATUS "ACVDOperator disabled")
  RETURN()
ENDIF()

################################################################################
## CGalOperators

SET(ACVDOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("ACVDOperators: ENABLED and ACTIVE")


#MARK_AS_ADVANCED( FORCE CMAKE_BACKWARDS_COMPATIBILITY )

# for CMake 2.6 corrected behaviour (see "cmake --help-policy CMP0003")
IF(COMMAND cmake_policy AND ${CMAKE_MAJOR_VERSION} EQUAL 2 AND ${CMAKE_MINOR_VERSION} GREATER 4)
  CMAKE_POLICY(SET CMP0003 NEW)
#  CMAKE_POLICY(SET CMP0005 NEW)
ENDIF(COMMAND cmake_policy AND ${CMAKE_MAJOR_VERSION} EQUAL 2 AND ${CMAKE_MINOR_VERSION} GREATER 4)
# --------------------------------------------------------------------------


# --------------------- OPTIONS OF THE PROJECT -----------------------------
# Build static lib by default

OPTION(ACVD_BUILD_SHARED_LIBS "Build vtkSurface with shared libraries." ON)
OPTION(ACVD_BUILD_DOCUMENTATION "Build the html documentation with doxygen." OFF)

OPTION(ACVD_BUILD_DISCRETEREMESHING "Build Discrete Remeshing Tools." ON)
OPTION(ACVD_BUILD_VOLUMEPROCESSING "Build Volume tools" ON)

OPTION(ACVD_USE_MULTITHREADING "Use Multithreaded classes" OFF)

OPTION(ACVD_USE_LLOYDCLUSTERING "Use Lloyd relaxations instead of new algorithm for clustering" OFF)
MARK_AS_ADVANCED(ACVD_USE_LLOYDCLUSTERING)

#
SET (EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin CACHE PATH "Single output directory for building all executables.")
#SET (LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin CACHE PATH "Single output directory for building all libraries.")
#MARK_AS_ADVANCED(LIBRARY_OUTPUT_PATH EXECUTABLE_OUTPUT_PATH)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/ACVD.json
    ${EXECUTABLE_OUTPUT_PATH}/ACVD.json COPYONLY)



SET(VTKSURFACE_PROJECT_DIR ${PROJECT_SOURCE_DIR})
SET(VTKSURFACE_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/Common)
SET(VTKDISCRETEREMESHING_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/DiscreteRemeshing)
SET(VTKVOLUMEPROCESSING_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/VolumeProcessing)
# --------------------------------------------------------------------------
# Find and load Doxygen settings (when required)


IF(ACVD_BUILD_DOCUMENTATION)
    FIND_PACKAGE(Doxygen)
ENDIF(ACVD_BUILD_DOCUMENTATION)

# --------------------------------------------------------------------
# Switch to enable Multithreaded clustering

IF(ACVD_USE_MULTITHREADING)
    ADD_DEFINITIONS (-D DOmultithread)
ENDIF(ACVD_USE_MULTITHREADING)
IF(ACVD_USE_LLOYDCLUSTERING)
    ADD_DEFINITIONS (-D DOLloydClustering)
ENDIF(ACVD_USE_LLOYDCLUSTERING)

# -------------------------- SUBDIRS TO HANDLE -----------------------------

# The main library
ADD_SUBDIRECTORY(Common)

IF(ACVD_BUILD_DISCRETEREMESHING)
    ADD_SUBDIRECTORY(DiscreteRemeshing)
ENDIF(ACVD_BUILD_DISCRETEREMESHING)

IF(ACVD_BUILD_VOLUMEPROCESSING)
    ADD_SUBDIRECTORY(VolumeProcessing)
ENDIF(ACVD_BUILD_VOLUMEPROCESSING)

IF(ACVD_BUILD_DOCUMENTATION)
    ADD_SUBDIRECTORY(doc)
ENDIF(ACVD_BUILD_DOCUMENTATION)

## eof - CMakeLists.txt
