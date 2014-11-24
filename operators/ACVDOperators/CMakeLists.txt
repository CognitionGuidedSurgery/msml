## Modules
# 
PROJECT(ACVDOperators)


option(MODULES_ACVDOperators "Should ACVDOperators be built?" "ON")

IF(NOT MODULES_ACVDOperators)
  MESSAGE(STATUS "MiscExtOperators disabled")
  RETURN()
ENDIF()

################################################################################
# Dependencies: 

SET(ACVDOperators_ACTIVE "OFF" PARENT_SCOPE)

IF(NOT MODULES_MiscMeshOperators)
  MESSAGE("MiscMeshOperators needed by ACVDOperators")  
ENDIF()

################################################################################
# Guard

IF(NOT MODULES_ACVDOperators)
  MESSAGE("ACDOperators disabled by user!")
  RETURN()
ENDIF()

################################################################################
# External Dependencies: 
include(ExternalProject)

IF( VTK_MAJOR_VERSION GREATER 5 )
  SET(ACVD_BRANCH "vtk6")
ELSE ()
  SET(ACVD_BRANCH "master")
ENDIF ()

ExternalProject_Add(ACVD    # Name for custom target
  #[DEPENDS projects...]       # Targets on which the project depends
  PREFIX acvd                # Root dir for entire project   
  GIT_REPOSITORY  http://github.com/CognitionGuidedSurgery/ACVD.git       # URL of git repo
  GIT_TAG ${ACVD_BRANCH}       # Git branch name, commit id or tag   
  #[SOURCE_DIR dir]            # Source dir to be used for build
  #[CONFIGURE_COMMAND cmd...]  # Build tree configuration command
  #[CMAKE_COMMAND /.../cmake]  # Specify alternative cmake executable
  #[CMAKE_GENERATOR gen]       # Specify generator for native build
  #[CMAKE_GENERATOR_TOOLSET t] # Generator-specific toolset name
  #[CMAKE_ARGS args...]        # Arguments to CMake command line
  CMAKE_ARGS -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
             -DVTK_DIR=${VTK_DIR} # pass VTK_DIR 
             -DCMAKE_SKIP_RPATH:BOOL=1 # not needed if make install
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
SET(ACVDOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("ACVDOperators: ENABLED and ACTIVE")

ExternalProject_Get_Property(ACVD install_dir)
SET(CMAKE_MODULE_PATH "${CMAKE_MODULE_PATH} ${install_dir}/lib/CMake/acvd/" )


# not possible, because only known after build time
#FIND_PACKAGE(vtkDiscreteRemeshing)
#FIND_PACKAGE(vtkSrface)
#FIND_PACKAGE(vtkVolumeProcessing)


SET(ACVDOperators_SRCS
  ACVDOperators.cpp
  )

SET(ACVDOperators_LIBS
  ${VTK_LIBRARIES}
  ${install_dir}/lib/libvtkVolumeProcessing.so
  ${install_dir}/lib/libvtkSurface.so
  ${install_dir}/lib/libvtkDiscreteRemeshing.so    
  MiscMeshOperators
  )

INCLUDE_DIRECTORIES(
  ${ACVDOperators_SOURCE_DIR}
  ${ACVDOperators_BINARY_DIR}
  ${PYTHON_INCLUDE_DIRS}
  
  #for iohelper:
  ${CMAKE_SOURCE_DIR}/MiscMeshOperators

  # external project ACVD
  ${install_dir}/include/vtkVolumeProcessing/ 
  ${install_dir}/include/vtkDiscreteRemeshing/
  ${install_dir}/include/vtkSurface/
  )

MSML_LIBRARY(
  NAME      ACVDOperators
  SWIG_FILE acvd.i
  SOURCES   ${ACVDOperators_SRCS}
  LIBRARIES ${ACVDOperators_LIBS})












