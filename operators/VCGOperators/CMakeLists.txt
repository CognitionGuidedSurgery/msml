  ## Modules
#
PROJECT(VCGOperators)


option(MODULES_VCGOperators "Should VCGOperators be built?" "ON")

IF(NOT MODULES_VCGOperators)
  MESSAGE(STATUS "VCGOperators disabled")
  RETURN()
ENDIF()

################################################################################
# Dependencies:

SET(VCGOperators_ACTIVE "OFF" PARENT_SCOPE)

IF(NOT MODULES_MiscMeshOperators)
  MESSAGE("MiscMeshOperators needed by VCGOperators")
ENDIF()

################################################################################
# Guard

IF(NOT MODULES_VCGOperators)
  MESSAGE("VCGOperators disabled by user!")
  RETURN()
ENDIF()

################################################################################
# External Dependencies:
include(ExternalProject)

ExternalProject_Add(VCG    # Name for custom target
  #[DEPENDS projects...]       # Targets on which the project depends
  PREFIX vcg                # Root dir for entire project
  #GIT_REPOSITORY  http://github.com/CognitionGuidedSurgery/ACVD.git       # URL of git repo
  #GIT_TAG master              # Git branch name, commit id or tag
  SVN_REPOSITORY    http://svn.code.sf.net/p/vcg/code/trunk
  SVN_REVISION -r 5516
  CONFIGURE_COMMAND ${CMAKE_COMMAND} -E echo etest
  BUILD_COMMAND ${CMAKE_COMMAND} -E echo No build necessary
  INSTALL_COMMAND ${CMAKE_COMMAND} -E echo No install necessary

  #[SOURCE_DIR dir]            # Source dir to be used for build
  #[CONFIGURE_COMMAND cmd...]  # Build tree configuration command
  #[CMAKE_COMMAND /.../cmake]  # Specify alternative cmake executable
  #[CMAKE_GENERATOR gen]       # Specify generator for native build
  #[CMAKE_GENERATOR_TOOLSET t] # Generator-specific toolset name
  #[CMAKE_ARGS args...]        # Arguments to CMake command line
  #CMAKE_ARGS -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
  #           -DCMAKE_SKIP_RPATH:BOOL=1
  #[CMAKE_CACHE_ARGS args...]  # Initial cache arguments, of the form -Dvar:string=on
 #--Build step-----------------
  #[BINARY_DIR dir]            # Specify build dir location
  #[BUILD_COMMAND cmd...]      # Command to drive the native build
  #[BUILD_IN_SOURCE 1]         # Use source dir for build dir
 #--Install step---------------
 #INSTALL_DIR dir           # Installation prefix
  #[INSTALL_COMMAND cmd...]    # Command to drive install after build
 #--Test step------------------
  #[TEST_BEFORE_INSTALL 1]     # Add test step executed before install step
  #[TEST_AFTER_INSTALL 1]      # Add test step executed after install step
  #[TEST_COMMAND cmd...]       # Command to drive test
 #--Output logging-------------
  LOG_DOWNLOAD 1            # Wrap download in script to log output
  LOG_UPDATE 1              # Wrap update in script to log output
  LOG_CONFIGURE 1           # Wrap configure in script to log output
  LOG_BUILD 1               # Wrap build in script to log output
  LOG_TEST 1                # Wrap test in script to log output
  LOG_INSTALL 1             # Wrap install in script to log output
  )



################################################################################
# MiscMeshOperators
SET(VCGOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("VCGOperators: ENABLED and ACTIVE")

ExternalProject_Get_Property(VCG install_dir)
#SET(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH} ${install_dir}/lib/CMake/VCG/" )

MESSAGE("VCG install dir is ${install_dir}")
SET(VCGOperators_SRCS
  VCGOperators.cpp
  )

SET(VCGOperators_LIBS
  ${VTK_LIBRARIES}
  MiscMeshOperators
  )

INCLUDE_DIRECTORIES(
  ${VCGOperators_SOURCE_DIR}
  ${VCGOperators_BINARY_DIR}
  ${PYTHON_INCLUDE_DIRS}

  #for iohelper:
  ${CMAKE_SOURCE_DIR}/MiscMeshOperators

  # external project VCG
  ${install_dir}/src/VCG/vcglib
  )





MSML_LIBRARY(
  NAME      VCGOperators
  SWIG_FILE vcg.i
  SOURCES   ${VCGOperators_SRCS}
  LIBRARIES ${VCGOperators_LIBS})

ADD_DEPENDENCIES(VCGOperators VCG)
ADD_DEPENDENCIES(_VCGOperatorsPython VCG)
