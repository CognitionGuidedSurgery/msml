
CMAKE_MINIMUM_REQUIRED(VERSION 2.6.2)

SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMake")


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
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
ENDIF(MSVC)

MESSAGE(" #############################")    
MESSAGE(" # CMAKE BUILD TYPE = ${CMAKE_BUILD_TYPE}")    
MESSAGE(" #############################")

#SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x") 

#message("CMAKE does not set RPATH, please adapt your LD_LIBRARY_PATH")
#set(CMAKE_SKIP_RPATH true)


# Find VTK
FIND_PACKAGE(VTK REQUIRED)
INCLUDE(${VTK_USE_FILE})

# SWIG
FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})
SET(CMAKE_SWIG_FLAGS "")

# Find Python
FIND_PACKAGE(PythonLibs REQUIRED)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_DIRS})

#MESSAGE("Include dirs of Python: " ${PYTHON_INCLUDE_DIRS} )
#message("Libs of Python: " ${PYTHON_LIBRARIES} )


# Find Boost
FIND_PACKAGE(Boost COMPONENTS program_options filesystem iostreams REQUIRED)
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})

#message("Include dirs of Boost : " ${Boost_INCLUDE_DIR} )
#message("cmake module path: " ${CMAKE_MODULE_PATH} )
#message("Booth2 python library: " ${Boost_PYTHON_LIBRARY} )
#MESSAGE("Boost Libraries = " ${Boost_LIBRARIES})  
  
#########################
# Misc Options
#########################

SET(PYTHON_SITE_PACKAGE ""
    CACHE PATH "Path to python site-package directory")

SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin) 
SET(LIBRARY_OUTPUT_PATH  ${CMAKE_BINARY_DIR}/bin) 
#SET(BUILD_SHARED_LIBS ON)
SET(CMAKE_INCLUDE_CURRENT_DIR ON)


INCLUDE_DIRECTORIES(${CMAKE_CURRENT_BINARY_DIR}/CMake/)

SET(CMAKE_OPERATOR_DIRECTORY ${CMAKE_BINARY_DIR}/bin
    CACHE PATH "Choose the operator path.")
    
SET(CMAKE_TESTDATA_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../Testdata
    CACHE PATH "Choose the test data path.")
add_definitions( -DTEST_DATA_PATH="${TESTDATA_PATH}" )



#SET(CMAKE_PYTHON_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../MSML_Python
#    CACHE PATH "Choose the test data path.")

set(SOFA_BIN_DIRECTORY "SOFA_BIN_DIRECTORY_NOT_FOUND" CACHE FILEPATH "description")
    
CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/Config.xml.in ${CMAKE_CURRENT_SOURCE_DIR}/../share/Config.xml)
CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/envconfig.py ${CMAKE_CURRENT_SOURCE_DIR}/../src/msml/envconfig.py)

SET(CMAKE_ECLIPSE_MAKE_ARGUMENTS "-j${x}" CACHE STRING "" FORCE ) 
    
################################################################################
## Modules
# 

ADD_SUBDIRECTORY(TetgenOperators)
ADD_SUBDIRECTORY(VCGOperators)  
ADD_SUBDIRECTORY(MiscMeshOperators)
ADD_SUBDIRECTORY(CGALOperators)
ADD_SUBDIRECTORY(CLI)           


