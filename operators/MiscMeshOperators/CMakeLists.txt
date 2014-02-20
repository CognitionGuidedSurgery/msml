PROJECT(MiscMeshOperators)

SET(MiscMeshOperators_SRCS
   IOHelper.h
   IOHelper.cpp
   MiscMeshOperators.h
   MiscMeshOperators.cpp
   PostProcessingOperators.h
   PostProcessingOperators.cpp
   IndexRegionOperators.h
   IndexRegionOperators.cpp
   MappingOperators.h
   MappingOperators.cpp
   #PythonWrappers.cpp
   )

INCLUDE_DIRECTORIES(
  ${MiscMeshOperators_SOURCE_DIR}
  ${MiscMeshOperators_BINARY_DIR}
  ${PYTHON_INCLUDE_DIRS}
  
  )
  
  SET(MiscMeshOperatorsExample_SRCS
    Example.cpp
   )
   
   SET(MiscMeshOperatorsPython_SRCS
       PythonWrappers.cpp
   )

 


  
IF(WIN32 AND NOT CYGWIN)
	ADD_LIBRARY(MiscMeshOperators STATIC ${MiscMeshOperators_SRCS})
ELSE()
	ADD_LIBRARY(MiscMeshOperators SHARED ${MiscMeshOperators_SRCS})
ENDIF(WIN32 AND NOT CYGWIN)



ADD_LIBRARY(MiscMeshOperatorsPython SHARED ${MiscMeshOperatorsPython_SRCS})
SET_TARGET_PROPERTIES(MiscMeshOperatorsPython PROPERTIES PREFIX "")
IF(WIN32 AND NOT CYGWIN)
	SET_TARGET_PROPERTIES(MiscMeshOperatorsPython PROPERTIES SUFFIX ".pyd")
ENDIF(WIN32 AND NOT CYGWIN)

TARGET_LINK_LIBRARIES(MiscMeshOperators ${VTK_LIBRARIES}
${TETGEN_LIBRARIES} 
${SOLID_LIBRARIES}
${Boost_LIBRARIES}
#${PYTHON_LIBRARIES} 
)


TARGET_LINK_LIBRARIES(MiscMeshOperatorsPython ${VTK_LIBRARIES}
${TETGEN_LIBRARIES} 
${Boost_LIBRARIES}
${PYTHON_LIBRARIES} 
${SOLID_LIBRARIES}
MiscMeshOperators
)

ADD_EXECUTABLE (MiscMeshOperatorsExample ${MiscMeshOperatorsExample_SRCS} )

TARGET_LINK_LIBRARIES(MiscMeshOperatorsExample MiscMeshOperators ${VTK_LIBRARIES}
${TETGEN_LIBRARIES}
${Boost_LIBRARIES}
MiscMeshOperators
)

