
#set(TETGEN_INCLUDE_PATHS "$ENV{TETGEN_PATH}" "/opt/TETGEN/include/TETGEN3" "/usr/include")
#set(TETGEN_LIB_PATHS "$ENV{TETGEN_PATH}/lib" "/opt/TETGEN/lib" "/usr/lib/")

set(TETGEN_INCLUDE_PATHS "/usr/include")


FIND_LIBRARY (TETGEN_LIBRARY NAMES tet Tetgen.lib HINTS ${TETGEN_LIB_PATHS}
    DOC "The directory where the Tetgen libraries reside"
    )    

FIND_PATH(TETGEN_INCLUDE_DIRS tetgen.h ${TETGEN_INCLUDE_PATHS})    
SET( TETGEN_FOUND "YES" )
SET( TETGEN_LIBRARIES          
            ${TETGEN_LIBRARY}         
          )




MARK_AS_ADVANCED(
	TETGEN_LIBRARY
  )



  
    

    
