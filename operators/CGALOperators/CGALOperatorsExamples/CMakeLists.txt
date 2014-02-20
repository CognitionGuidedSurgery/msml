project( CGALOperatorsExamples )

SET(CGALOperatorsExamples_SRCS 
    CGALOperatorsExamples.cpp 
   )

find_package(CGAL QUIET COMPONENTS Core )

if ( CGAL_FOUND )
  include( ${CGAL_USE_FILE} )
  find_package(Boost)
  if ( Boost_FOUND AND Boost_VERSION GREATER 103400 )

	ADD_EXECUTABLE(CGALOperatorsExamples ${CGALOperatorsExamples_SRCS})
	INCLUDE_DIRECTORIES(
		${CMAKE_SOURCE_DIR}/CGALOperators
	)
	TARGET_LINK_LIBRARIES(CGALOperatorsExamples CGALOperators ${CGAL_LIBRARIES} ${Boost_LIBRARIES})

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

