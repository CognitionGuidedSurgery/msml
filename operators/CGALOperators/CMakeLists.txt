project( CGALOperators )

SET(CGALOperatorsPython_SRCS
       PythonWrappers.cpp
   )


SET(CGALOperators_SRCS
	CGALOperators.h
        CGALOperators.cpp
	cgal_tet_to_vtk.h
   )

cmake_minimum_required(VERSION 2.6.2)
if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" VERSION_GREATER 2.6)
  if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}.${CMAKE_PATCH_VERSION}" VERSION_GREATER 2.8.3)
    cmake_policy(VERSION 2.8.4)
  else()
    cmake_policy(VERSION 2.6)
  endif()
endif()

#find_package(CGAL QUIET COMPONENTS Core )

if ( CGAL_FOUND )
  include( ${CGAL_USE_FILE} )
  find_package(Boost)
  if ( Boost_FOUND AND Boost_VERSION GREATER 103400 )
    IF(WIN32 AND NOT CYGWIN)
	    ADD_LIBRARY(CGALOperators STATIC ${CGALOperators_SRCS})
    ELSE()
	    ADD_LIBRARY(CGALOperators SHARED ${CGALOperators_SRCS})
    ENDIF(WIN32 AND NOT CYGWIN)
	
	ADD_LIBRARY(CGALOperatorsPython SHARED ${CGALOperatorsPython_SRCS})
	SET_TARGET_PROPERTIES(CGALOperatorsPython PROPERTIES PREFIX "")
	IF(WIN32 AND NOT CYGWIN)
		SET_TARGET_PROPERTIES(CGALOperatorsPython PROPERTIES SUFFIX ".pyd")
	ENDIF(WIN32 AND NOT CYGWIN)

	INCLUDE_DIRECTORIES(
		${CMAKE_SOURCE_DIR}/MiscMeshOperators
	)
	include( CGAL_CreateSingleSourceCGALProgram )
  	include_directories (BEFORE "../../include")

	TARGET_LINK_LIBRARIES(CGALOperators ${VTK_LIBRARIES}
		MiscMeshOperators
	)

	TARGET_LINK_LIBRARIES(CGALOperatorsPython ${VTK_LIBRARIES}
		${Boost_LIBRARIES}
		${PYTHON_LIBRARIES} 
		CGALOperators
	)

  else()
    message(STATUS "NOTICE: This program requires Boost >= 1.34.1, and will not be compiled.")
  endif()
else()
  message(STATUS "This program requires the CGAL library, and will not be compiled.")
endif()

if(MSVC)
# /bigobj is required for CGAL builds for windows
set ( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /bigobj" )
set ( CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /bigobj" )
endif()

