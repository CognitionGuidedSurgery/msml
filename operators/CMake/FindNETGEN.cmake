set(NETGEN_INCLUDE_PATHS "$ENV{NETGEN_PATH}" "/opt/netgen/include" "/usr/include")
set(NETGEN_LIB_PATHS "$ENV{NETGEN_PATH}/lib" "/opt/netgen/lib" "/usr/lib/")

#set(NETGEN_INCLUDE_PATHS "/usr/include")


FIND_LIBRARY (NETGEN_LIBRARY NAMES nglib nglib.so HINTS ${NETGEN_LIB_PATHS}
  DOC "The directory where the Netgen libraries reside"
)    
  
FIND_PATH(NETGEN_INCLUDE_DIRS nglib.h ${NETGEN_INCLUDE_PATHS})
SET(NETGEN_FOUND "YES")
SET(NETGEN_LIBRARIES ${NETGEN_LIBRARY})
MARK_AS_ADVANCED(NETGEN_LIBRARY)



  
    

    
