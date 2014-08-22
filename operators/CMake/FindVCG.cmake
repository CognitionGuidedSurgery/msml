set(VCG_INCLUDE_DIRS "$ENV{VCG_PATH}/" "/opt/vcglib" "/usr/local/vcglib")

FIND_PATH(VCG_INCLUDE_DIR vcg/simplex/vertex/base.h  ${VCG_INCLUDE_DIRS})
SET( VCG_FOUND "YES" )



    
