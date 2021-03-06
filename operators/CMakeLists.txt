PROJECT(MSML)

CMAKE_MINIMUM_REQUIRED(VERSION 2.6.2)

SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
	"${CMAKE_SOURCE_DIR}/CMake")


#########################
# Set default Build Type to Debug
#########################

IF (NOT CMAKE_BUILD_TYPE)
	SET(CMAKE_BUILD_TYPE Release CACHE STRING
		"Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel."
		FORCE)
ENDIF (NOT CMAKE_BUILD_TYPE)

if(MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP")
ELSE()
  # set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
ENDIF(MSVC)

MESSAGE(" #############################")    
MESSAGE(" # CMAKE BUILD TYPE = ${CMAKE_BUILD_TYPE}")    
MESSAGE(" #############################")


## Activating c++0x for gcc 
## currently supported by VTK6.X (bug)
#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x") 

# for deactivating the rpath within shared object (runtime path defines places
# for loading libraries as abspaths)
#message("CMAKE does not set RPATH, please adapt your LD_LIBRARY_PATH")
#set(CMAKE_SKIP_RPATH true)


# Find VTK
FIND_PACKAGE(VTK REQUIRED)
INCLUDE(${VTK_USE_FILE})

# SWIG
FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})
IF(WIN32 AND NOT CYGWIN)
  IF(CMAKE_BUILD_TYPE MATCHES Release)
    SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/bin/release)
  ELSE()
      SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/bin/debug)
  ENDIF()
ELSE()
  SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/bin)
ENDIF()
#SWIG options
SET(SWIG_LANG "python")
# Find Python
FIND_PACKAGE(PythonLibs REQUIRED)
if(NOT PYTHON_DEBUG_LIBRARIES)
	# linux workaround:
	set(PYTHON_DEBUG_LIBRARIES ${PYTHON_LIBRARIES})
endif(NOT PYTHON_DEBUG_LIBRARIES)
SET(WRAPPER_LIBRARIES_RELEASE ${PYTHON_LIBRARIES})
SET(WRAPPER_LIBRARIES_DEBUG ${PYTHON_DEBUG_LIBRARIES})
SET(WRAPPER_INCLUDES  ${PYTHON_INCLUDE_DIRS})
INCLUDE_DIRECTORIES(${WRAPPER_INCLUDES})

# Find Boost
FIND_PACKAGE(Boost COMPONENTS 
	program_options 
	unit_test_framework 
	filesystem iostreams
	regex
    system
	iostreams
	REQUIRED)

INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
set(Boost_USE_STATIC_LIBS OFF)
add_definitions( -DBOOST_ALL_DYN_LINK )
LINK_DIRECTORIES(${Boost_LIBRARY_DIR})

#message("Include dirs of Boost : " ${Boost_INCLUDE_DIR} )
#message("cmake module path: " ${CMAKE_MODULE_PATH} )
#message("Booth2 python library: " ${Boost_PYTHON_LIBRARY} )
#MESSAGE("Boost Libraries = " ${Boost_LIBRARIES})  

#########################
# Testing 
#########################
INCLUDE(CTest)
ENABLE_TESTING()

#########################
# Misc Options
#########################

SET(PYTHON_SITE_PACKAGE ""
    CACHE PATH "Path to python site-package directory")

#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
# deprecated
SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin) 
SET(LIBRARY_OUTPUT_PATH  ${CMAKE_BINARY_DIR}/bin) 
#SET(BUILD_SHARED_LIBS ON)
SET(CMAKE_INCLUDE_CURRENT_DIR ON)

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_BINARY_DIR}/CMake/)

SET(CMAKE_OPERATOR_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    CACHE PATH "Choose the operator path.")
    
SET(CMAKE_TESTDATA_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../share/testdata
    CACHE PATH "Choose the test data path.")
add_definitions( -DTESTDATA_PATH="${CMAKE_TESTDATA_PATH}" )


#SET(CMAKE_PYTHON_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../MSML_Python
#    CACHE PATH "Choose the test data path.")

FIND_FILE(SOFA_EXECUTABLE "sofaBatch" NAMES "sofaBatch.exe" "sofaBatchExtended"
    DOC "")

FIND_FILE(HIFLOW_EXECUTABLE "hiflow3" NAMES "hiflow3"
    DOC "")

FIND_FILE(ABAQUS_EXECUTABLE "abaqus" NAMES "abaqus" "abaqus"
    DOC "")


CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/Config.xml.in
  ${CMAKE_CURRENT_SOURCE_DIR}/../share/Config.xml)

CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/msml-package.xml.in
  ${CMAKE_CURRENT_SOURCE_DIR}/../share/msml-package.xml)

CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/envconfig.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../src/msml/envconfig.py)

SET(CMAKE_ECLIPSE_MAKE_ARGUMENTS "-j${x}" CACHE STRING "" FORCE ) 

################################################################################
## Macro
#
MACRO(MSML_LIBRARY)
  CMAKE_PARSE_ARGUMENTS(ML 
    ""   # options
    "NAME;SWIG_FILE" # single arg
    "SOURCES;LIBRARIES" # multi arg
    ${ARGN}
    )
  

  SET_SOURCE_FILES_PROPERTIES(${ML_SWIG_FILE} PROPERTIES CPLUSPLUS ON)

  SWIG_ADD_MODULE(${ML_NAME}Python ${SWIG_LANG} ${ML_SWIG_FILE}
     "${CMAKE_SOURCE_DIR}/common/log.cpp")
  
  SWIG_LINK_LIBRARIES(${ML_NAME}Python
    optimized ${ML_NAME} ${ML_LIBRARIES} ${WRAPPER_LIBRARIES_RELEASE}
	debug ${ML_NAME} ${ML_LIBRARIES} ${WRAPPER_LIBRARIES_DEBUG}
    )

  set_target_properties (_${ML_NAME}Python PROPERTIES COMPILE_DEFINITIONS "PYTHONLOGGING")
  ADD_LIBRARY(${ML_NAME} SHARED ${ML_SOURCES} "${CMAKE_SOURCE_DIR}/common/log.cpp")
  TARGET_LINK_LIBRARIES(${ML_NAME} ${ML_LIBRARIES})
  
ENDMACRO()

    
################################################################################
## Modules
# 
ADD_SUBDIRECTORY(Base)
ADD_SUBDIRECTORY(TetgenOperators)
ADD_SUBDIRECTORY(VCGOperators)
ADD_SUBDIRECTORY(MiscMeshOperators)
ADD_SUBDIRECTORY(CGALOperators)
ADD_SUBDIRECTORY(CLI)
ADD_SUBDIRECTORY(ACVDOperators) 

