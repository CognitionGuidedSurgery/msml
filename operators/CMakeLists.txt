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
 

#MESSAGE("Include dirs of Python: " ${PYTHON_INCLUDE_DIRS} )
#message("Libs of Python: " ${PYTHON_LIBRARIES} )


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
    
SET(CMAKE_TESTDATA_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../Testdata
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

CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/envconfig.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../src/msml/envconfig.py)

SET(CMAKE_ECLIPSE_MAKE_ARGUMENTS "-j${x}" CACHE STRING "" FORCE ) 

SET(SWIG_LANG "python")
#SET(SWIG_LANG "java")


IF( "${SWIG_LANG}" STREQUAL "python")
  # Find Python
  FIND_PACKAGE(PythonLibs REQUIRED)
  SET(WRAPPER_LIBRARIES ${PYTHON_LIBRARIES})
  SET(WRAPPER_INCLUDES  ${PYTHON_INCLUDE_DIRS})
#ELSEIF( "${SWIG_LANG}" EQUAL "java")
ELSE()
  FIND_PACKAGE(JNI)
  SET(WRAPPER_LIBRARIES ${JNI_LIBRARIES})
  SET(WRAPPER_INCLUDES  ${JNI_INCLUDE_DIRS})
  
  # this does not work
  #message(${JNI_FOUND})
  #IF(NOT ${JNI_FOUND})
  #  message("Java Wrapper selected but no JNI found. JAVA_HOME set?")
  #  RETURN()
  #ENDIF()
ENDIF()


#message(${SWIG_LANG})
#message(${JNI_LIBRARIES})


INCLUDE_DIRECTORIES(${WRAPPER_INCLUDES})

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
  
  #message("AAAAAA ${ML_UNPARSED_ARGUMENTS}")

  SET_SOURCE_FILES_PROPERTIES(${ML_SWIG_FILE} PROPERTIES CPLUSPLUS ON)
  #SET_SOURCE_FILES_PROPERTIES(tetgen.i PROPERTIES SWIG_FLAGS "-includeall")

  SWIG_ADD_MODULE(${ML_NAME}Python ${SWIG_LANG} ${ML_SWIG_FILE}
    ${ML_SOURCES} "${CMAKE_SOURCE_DIR}/common/log.cpp")
  
  SWIG_LINK_LIBRARIES(
    ${ML_NAME}Python
    ${ML_LIBRARIES}
    ${WRAPPER_LIBRARIES}
    )

  
  IF(WIN32 AND NOT CYGWIN)
    ADD_LIBRARY(${ML_NAME} STATIC ${ML_SOURCES} "${CMAKE_SOURCE_DIR}/common/log.cpp")
  ELSE()
    set_target_properties (_${ML_NAME}Python PROPERTIES COMPILE_DEFINITIONS "PYTHONLOGGING")
	ADD_LIBRARY(${ML_NAME} SHARED ${ML_SOURCES} "${CMAKE_SOURCE_DIR}/common/log.cpp")
  ENDIF()
 
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
ADD_SUBDIRECTORY(CGALOperators/CGALOperatorsExamples)      
ADD_SUBDIRECTORY(ACVDOperators) 


