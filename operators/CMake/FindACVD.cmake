set(ACVD_INCLUDE_PATHS "$ENV{ACVD_PATH}" "/opt/ACVD/include" "/usr/include")
set(ACVD_LIB_PATHS "$ENV{ACVD_PATH}/lib" "/opt/ACVD/lib" "/usr/lib/")

#set(ACVD_INCLUDE_PATHS "/usr/include")


FIND_LIBRARY (ACVD_LIBRARY NAMES vtkDiscreteRemeshing vtkDiscreteRemeshingLibrary HINTS ${ACVD_LIB_PATHS}
  DOC "The directory where the ACVD libraries reside"
)    
  
FIND_PATH(ACVD_INCLUDE_DIR vtkDiscreteRemeshing/vtkAnisotropicDiscreteRemeshing.h ${ACVD_INCLUDE_PATHS})

SET(ACVD_INCLUDE_DIRS
${ACVD_INCLUDE_DIR}/vtkDiscreteRemeshing/
${ACVD_INCLUDE_DIR}/vtkSurface/
${ACVD_INCLUDE_DIR}/vtkVolumeProcessing/
${ACVD_INCLUDE_DIR}/ACVD/Common/
${ACVD_INCLUDE_DIR}/ACVD/DiscreteRemeshing/
${ACVD_INCLUDE_DIR}/ACVD/VolumeProcessing/
)

IF("${ACVD_LIBRARY}" STREQUAL "ACVD_LIBRARY-NOTFOUND")
SET(ACVD_FOUND "NO")
ELSE()
SET(ACVD_FOUND "YES")
ENDIF ()

SET(ACVD_LIBRARIES ${ACVD_LIBRARY})
MARK_AS_ADVANCED(ACVD_LIBRARIES)



  
    

    
