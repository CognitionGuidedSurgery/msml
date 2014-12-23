PROJECT(MSML)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6.2)

SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH}
	"${CMAKE_SOURCE_DIR}/CMake")


########################################################################################################################
# Prepare Installation
########################################################################################################################

INCLUDE(InstallRequiredSystemLibraries)

SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Medical Simulation Markup Language")
SET(CPACK_PACKAGE_VENDOR "http://CognitionGuidedSurgery.de see Authors.txt for details")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/../README.md")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/../LICENSE")

SET(CPACK_PACKAGE_VERSION_MAJOR "0")
SET(CPACK_PACKAGE_VERSION_MINOR "8")
SET(CPACK_PACKAGE_VERSION_PATCH "2")

SET(CPACK_PACKAGE_INSTALL_DIRECTORY "msml-${CMake_VERSION_MAJOR}.${CMake_VERSION_MINOR}")

IF(WIN32 AND NOT UNIX)
  # There is a bug in NSI that does not handle full unix paths properly. Make
  # sure there is at least one set of four (4) backlasshes.
  SET(CPACK_PACKAGE_ICON "${CMake_SOURCE_DIR}/Utilities/Release\\\\InstallIcon.bmp")
  SET(CPACK_NSIS_INSTALLED_ICON_NAME "bin\\\\MyExecutable.exe")
  SET(CPACK_NSIS_DISPLAY_NAME "${CPACK_PACKAGE_INSTALL_DIRECTORY} My Famous Project")
  SET(CPACK_NSIS_HELP_LINK "http:\\\\\\\\www.my-project-home-page.org")
  SET(CPACK_NSIS_URL_INFO_ABOUT "http:\\\\\\\\www.my-personal-home-page.com")
  SET(CPACK_NSIS_CONTACT "me@my-personal-home-page.com")
  SET(CPACK_NSIS_MODIFY_PATH ON)
ELSE(WIN32 AND NOT UNIX)

  #SET(CPACK_STRIP_FILES "bin/MyExecutable")
  #SET(CPACK_SOURCE_STRIP_FILES "")

ENDIF(WIN32 AND NOT UNIX)
#SET(CPACK_PACKAGE_EXECUTABLES "MyExecutable" "My Executable")



## DEBIAN
SET(CPACK_DEBIAN_PACKAGE_DEPENDS "libc6 (>= 2.3.1-6), libgcc1 (>= 1:3.4.2-12)")
SET(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "amd64")
SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "Alexander Weigl <Alexander.Weigl@student.kit.edu>")
INCLUDE(CPack)

########################################################################################################################
# Set default Build Type to Debug
########################################################################################################################

SET(CMAKE_BUILD_TYPE Debug CACHE STRING
   "Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel.")

########################################################################################################################
# Compiler Flags (CMAKE_CXX_FLAGS)
########################################################################################################################

IF(MSVC)
  SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /MP" CACHE STRING "Build with Multiple Processes")
ELSE()
  ## Activating c++0x for gcc
  ## currently supported by VTK6.X (bug)
  # set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x" CACHE STRING)
ENDIF(MSVC)

MESSAGE(STATUS "BUILD TYPE = ${CMAKE_BUILD_TYPE}")

# for deactivating the rpath within shared object (runtime path defines places for loading libraries as abspaths)
#message("CMAKE does not set RPATH, please adapt your LD_LIBRARY_PATH")
#set(CMAKE_SKIP_RPATH true)


########################################################################################################################
# Global Dependencies
########################################################################################################################


########################################################################################################################
# VTK

FIND_PACKAGE(VTK REQUIRED)
INCLUDE(${VTK_USE_FILE})

IF(NOT VTK_FOUND)
  message("VTK is required to build MSML")
  message("for ubuntu14.10: sudo apt-get install python-vtk6 libvtk6 libvtk6-dev")
  message("for ubuntu14.04: sudo apt-get install libvtk5.8 libvtk5-dev")
  message("for fedora: yum install vtk-devel.x86_64 vtk-python.x86_64")
  message("if you have a own-compiled version please set VTK_DIR")
ENDIF()

########################################################################################################################
# SWIG
FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

IF(NOT SWIG_FOUND)
  message("SWIG is required to build MSML")
  message("for ubuntu: sudo apt-get install swig")
  message("for fedora: yum install swig")
  message("if you have a own-compiled version please set the environment PATH variable")
ENDIF()

SET(SWIG_LANG "python")
FIND_PACKAGE(PythonLibs REQUIRED)

IF(NOT PYTHON_DEBUG_LIBRARIES)
 # linux workaround:
 SET(PYTHON_DEBUG_LIBRARIES ${PYTHON_LIBRARIES})
ENDIF(NOT PYTHON_DEBUG_LIBRARIES)

SET(WRAPPER_LIBRARIES_RELEASE ${PYTHON_LIBRARIES})
SET(WRAPPER_LIBRARIES_DEBUG ${PYTHON_DEBUG_LIBRARIES})
SET(WRAPPER_INCLUDES  ${PYTHON_INCLUDE_DIRS})

INCLUDE_DIRECTORIES(${WRAPPER_INCLUDES})



IF(WIN32 AND NOT CYGWIN)
  IF(CMAKE_BUILD_TYPE MATCHES Release)
    SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/bin/release)
  ELSE()
      SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/bin/debug)
  ENDIF()
ELSE()
  SET(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_BINARY_DIR}/bin)
ENDIF()
 
########################################################################################################################
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
SET(Boost_USE_STATIC_LIBS OFF)
ADD_DEFINITIONS(-DBOOST_ALL_DYN_LINK)
LINK_DIRECTORIES(${Boost_LIBRARY_DIR})

IF(NOT SWIG_FOUND)
  message("Boost>=1.48 is required to build MSML")
  message("Please make following components available: program_options unit_test_framework filesystem iostreams	regex system iostreams")
  message("for ubuntu: sudo apt-get install libboost …")
  message("for fedora: yum install libboost …")
ENDIF()


#message("Include dirs of Boost : " ${Boost_INCLUDE_DIR} )
#message("cmake module path: " ${CMAKE_MODULE_PATH} )
#message("Booth2 python library: " ${Boost_PYTHON_LIBRARY} )
#MESSAGE("Boost Libraries = " ${Boost_LIBRARIES})  

########################################################################################################################
# Testing 
########################################################################################################################
INCLUDE(CTest)
ENABLE_TESTING()

########################################################################################################################
# Misc Options
########################################################################################################################

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
ADD_DEFINITIONS( -DTESTDATA_PATH="${CMAKE_TESTDATA_PATH}" )


#SET(CMAKE_PYTHON_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../MSML_Python
#    CACHE PATH "Choose the test data path.")

FIND_FILE(SOFA_EXECUTABLE "sofaBatch" NAMES "runSofa" "runSofa.exe" "sofaBatch.exe" "sofaBatchExtended"
    DOC "")

FIND_FILE(HIFLOW_EXECUTABLE "hiflow3" NAMES "elasticity"  DOC "PATH to elasticity executable")

FIND_FILE(ABAQUS_EXECUTABLE "abaqus" NAMES "abaqus" "abaqus" DOC "Path to abaqus executable")

IF(NOT SOFA_EXECUTABLE)
  message(WARNING "Sofa not find on your system, looked for sofaBatch or runSofa executable. Sofa simulation will not work")
ENDIF()


IF(NOT ABAQUS_EXECUTABLE)
  message(WARNING "Abaqus not find on your system, looked for abaqus executable. Abaqus simulation will not work")
ENDIF()


IF(NOT HIFLOW_EXECUTABLE)
  message(WARNING "Hiflow not find on your system, looked for elasticity. Hiflow simulation will not work")
ENDIF()

SET(CMAKE_ECLIPSE_MAKE_ARGUMENTS "-j${x}" CACHE STRING "" FORCE )

## FIND site-package dir from the default Python instance
IF(NOT PYTHON_SITE_PACKAGES)
  EXECUTE_PROCESS( COMMAND python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(True)" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES OUTPUT_STRIP_TRAILING_WHITESPACE)
ENDIF()

SET(PYTHON_INSTALL_PACKAGES "${CMAKE_INSTALL_PREFIX}${PYTHON_SITE_PACKAGES}"
    CACHE STRING "Python site-package folder")

message(STATUS "Python Install dir: " ${PYTHON_INSTALL_PACKAGES})
########################################################################################################################
# Configure Files
########################################################################################################################

CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/Config.xml.in
  ${CMAKE_CURRENT_SOURCE_DIR}/../share/Config.xml)

CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/CMake/envconfig.py
  ${CMAKE_CURRENT_SOURCE_DIR}/../src/msml/envconfig.py)


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
     "${CMAKE_SOURCE_DIR}/common/log.cpp")
  
  SWIG_LINK_LIBRARIES(${ML_NAME}Python
    optimized ${ML_NAME} ${ML_LIBRARIES} ${WRAPPER_LIBRARIES_RELEASE}
	debug ${ML_NAME} ${ML_LIBRARIES} ${WRAPPER_LIBRARIES_DEBUG}
    )

  
  IF(WIN32 AND NOT CYGWIN)
    ADD_LIBRARY(${ML_NAME} SHARED ${ML_SOURCES} "${CMAKE_SOURCE_DIR}/common/log.cpp")
	set_target_properties (_${ML_NAME}Python PROPERTIES COMPILE_DEFINITIONS "PYTHONLOGGING") #experimental
  ELSE()
    set_target_properties (_${ML_NAME}Python PROPERTIES COMPILE_DEFINITIONS "PYTHONLOGGING")
	ADD_LIBRARY(${ML_NAME} SHARED ${ML_SOURCES} "${CMAKE_SOURCE_DIR}/common/log.cpp")
  ENDIF()
 
  TARGET_LINK_LIBRARIES(${ML_NAME} ${ML_LIBRARIES})

  ## install of shared object into library
  INSTALL(TARGETS ${ML_NAME} LIBRARY DESTINATION lib)

  ## install python extension into site-package folder
  INSTALL(TARGETS _${ML_NAME}Python LIBRARY DESTINATION "${PYTHON_INSTALL_PACKAGES}/")
  INSTALL(FILES ${CMAKE_SWIG_OUTDIR}/${ML_NAME}Python.py DESTINATION "${PYTHON_INSTALL_PACKAGES}/")

ENDMACRO()

################################################################################
INSTALL(DIRECTORY "${CMAKE_SOURCE_DIR}/../src/msml"
        DESTINATION "${PYTHON_INSTALL_PACKAGES}"
        FILES_MATCHING
          PATTERN "*.py"
          PATTERN "*.xsd"
          PATTERN "*.xml"
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
                    GROUP_EXECUTE GROUP_READ)
    
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
