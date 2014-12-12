## Modules
# 
PROJECT(ACVDOperators)


option(MODULES_ACVDOperators "Should ACVDOperators be built?" ON)

IF(NOT MODULES_ACVDOperators)
  MESSAGE(STATUS "MiscExtOperators disabled")
  RETURN()
ENDIF()

OPTION(OPTION_ACVD_EXTPROJECT
  "Should ACVDOperators download ACVD and compile it?" ON)

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
# MiscMeshOperators


IF( OPTION_ACVD_EXTPROJECT )
  message("ACVD as external project")

  include(ExternalProject)

  IF( VTK_MAJOR_VERSION GREATER 5 )
    SET(ACVD_BRANCH "vtk6")
  ELSE()
    SET(ACVD_BRANCH "master")
  ENDIF()

  #message("BRANCH: ${ACVD_BRANCH}")

  ExternalProject_Add(ACVD    # Name for custom target
    PREFIX acvd                # Root dir for entire project   
    GIT_REPOSITORY  http://github.com/CognitionGuidedSurgery/ACVD.git       # URL of git repo
    GIT_TAG ${ACVD_BRANCH}       # Git branch name, commit id or tag   
    CMAKE_ARGS 
      -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
      -DVTK_DIR=${VTK_DIR} # pass VTK_DIR 
      -DCMAKE_SKIP_RPATH:BOOL=1 # not needed if make install
      -DBUILD_SHARED_LIBS:bool=FALSE
      -DCMAKE_CXX_FLAGS:STRING=-fPIC

	#LOG_DOWNLOAD 1            # Wrap download in script to log output
	#    LOG_UPDATE 1              # Wrap update in script to log output
	#    LOG_CONFIGURE 1           # Wrap configure in script to log output
	#    LOG_BUILD 1               # Wrap build in script to log output
	#    LOG_TEST 1                # Wrap test in script to log output
	#    LOG_INSTALL 1             # Wrap install in script to log output 
	)

  ExternalProject_Get_Property(ACVD install_dir)
  ExternalProject_Get_Property(ACVD source_dir)
  SET(ACVD_SOURCE_DIR ${source_dir} )
  SET(ACVD_LIB_DIR ${install_dir}/lib)
  SET(ACVD_LIB_SHARED OFF)
ELSE( OPTION_ACVD_EXTPROJECT )

	SET(ACVD_SOURCE_DIR "-notfound" 
		CACHE PATH "root folder of ACVD sources for determining include paths of header")
	
	SET(ACVD_LIB_DIR "-notfound" 
		CACHE PATH "folder of the compiled acvd libraries" )

	SET(ACVD_LIB_SHARED ON
		CACHE BOOLEAN "if ACVD is built as shared object, else -> static")

	message("-- ACVD not using superbuild")

	IF( NOT  ACVD_SOURCE_DIR )
		message("Please provide: ACVD_SOURCE_DIR")
	ENDIF()

	IF( NOT  ACVD_LIB_DIR )
		message("Please provide: ACVD_LIB__DIR")
	ENDIF()

ENDIF( OPTION_ACVD_EXTPROJECT )

SET(ACVDOperators_ACTIVE "ON" PARENT_SCOPE)
MESSAGE("ACVDOperators: ENABLED and ACTIVE")

# not possible, because only known after build time
#FIND_PACKAGE(vtkDiscreteRemeshing)
#FIND_PACKAGE(vtkSrface)
#FIND_PACKAGE(vtkVolumeProcessing)


SET(ACVDOperators_SRCS
	ACVDOperators.cpp)

SET(ACVD_INCLUDE_DIRS
	${ACVD_SOURCE_DIR}/vtkDiscreteRemeshing/
	${ACVD_SOURCE_DIR}/vtkSurface/
	${ACVD_SOURCE_DIR}/vtkVolumeProcessing/
	${ACVD_SOURCE_DIR}/DiscreteRemeshing/
	${ACVD_SOURCE_DIR}/Common/
	${ACVD_SOURCE_DIR}/VolumeProcessing/
	)

IF(WIN32 AND NOT CYGWIN)
	SET(ACVD_LIB_PREFIX ${ACVD_LIB_DIR}/)
	IF( ACVD_LIB_SHARED )
		SET(ACVD_LIB_SUFFIX "dll")
	ELSE()
		SET(ACVD_LIB_SUFFIX "lib")
	ENDIF()
ELSE()
	SET(ACVD_LIB_PREFIX ${ACVD_LIB_DIR}/lib)
	IF( ACVD_LIB_SHARED )
		SET(ACVD_LIB_SUFFIX "so")
	ELSE()
		SET(ACVD_LIB_SUFFIX "a")
	ENDIF()
ENDIF()

SET(ACVD_LIBRARIES
	${ACVD_LIB_PREFIX}vtkVolumeProcessing.${ACVD_LIB_SUFFIX}
	${ACVD_LIB_PREFIX}vtkSurface.${ACVD_LIB_SUFFIX}
	${ACVD_LIB_PREFIX}vtkDiscreteRemeshing.${ACVD_LIB_SUFFIX}
	)

SET(ACVDOperators_LIBS
	${VTK_LIBRARIES}
	${ACVD_LIBRARIES}
	MiscMeshOperators)


INCLUDE_DIRECTORIES(
	${PYTHON_INCLUDE_DIRS}
	#for iohelper:
	${CMAKE_SOURCE_DIR}/MiscMeshOperators
	# external project ACVD
	${ACVD_INCLUDE_DIRS}
	)

message("ACVD include are ${ACVD_INCLUDE_DIRS}")

MSML_LIBRARY(
	NAME      ACVDOperators
	SWIG_FILE acvd.i
	SOURCES   ${ACVDOperators_SRCS}
	LIBRARIES ${ACVDOperators_LIBS})
	
SET(ACVDOperatorsExample_SRCS example.cpp) 	
 	
ADD_EXECUTABLE (ACVDOperatorsExample ${ACVDOperatorsExample_SRCS} ) 	
TARGET_LINK_LIBRARIES(ACVDOperatorsExample 	
 ACVDOperators 	
 ${ACVDOperators_LIBS} 	
) 		


IF( OPTION_ACVD_EXTPROJECT )
	ADD_DEPENDENCIES(ACVDOperators ACVD)
	ADD_DEPENDENCIES(_ACVDOperatorsPython ACVD)
ENDIF()

############################################################################
## Testing

#FILE( GLOB_RECURSE  TEST_FILES test/*)

ADD_DEFINITIONS(-DBOOST_TEST_DYN_LINK)

ADD_EXECUTABLE(ACVDOperatorsTest test/ACVDOperatorsTest.cpp)
TARGET_LINK_LIBRARIES(ACVDOperatorsTest
	ACVDOperators
	${ACVD_LIBS}	
	${Boost_UNIT_TEST_FRAMEWORK_LIBS}
)
ADD_TEST(ACVDOperatorsTest ${CMAKE_OPERATOR_DIRECTORY}/ACVDOperatorsTest)


