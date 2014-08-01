PROJECT(CLI)


SET(TetgenMesher_SRCS
     TetgenMesher.cpp
   )
   
   SET(ColorMesh_SRCS
     ColorMesh.cpp
   )
   
   SET(ConvertVTKToSTL_SRCS
     ConvertVTKToSTL.cpp
   )

INCLUDE_DIRECTORIES(
  ${MiscMeshOperators_SOURCE_DIR}
  ${MiscMeshOperators_BINARY_DIR}
    ${TetgenOperators_SOURCE_DIR}
  ${TetgenOperators_BINARY_DIR}
  
  )
  

 


ADD_EXECUTABLE (TetgenMesher ${TetgenMesher_SRCS} )

TARGET_LINK_LIBRARIES(TetgenMesher
${Boost_LIBRARIES}
${VTK_LIBRARIES}
${TETGEN_LIBRARIES}
MiscMeshOperators
TetgenOperators
)

ADD_EXECUTABLE (ColorMesh ${ColorMesh_SRCS} )

TARGET_LINK_LIBRARIES(ColorMesh
${Boost_LIBRARIES}
${VTK_LIBRARIES}
MiscMeshOperators
)

ADD_EXECUTABLE (ConvertVTKToSTL ${ConvertVTKToSTL_SRCS} )

TARGET_LINK_LIBRARIES(ConvertVTKToSTL
${Boost_LIBRARIES}
${VTK_LIBRARIES}
MiscMeshOperators
)

