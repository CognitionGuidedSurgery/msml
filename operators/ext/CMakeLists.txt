
## Modules
# 


option(MODULES_MiscExtOperators "Should MiscExtOperators be built?" "OFF")

IF(NOT MODULES_MiscExtOperators)
  MESSAGE(STATUS "MiscExtOperators disabled")
  RETURN()
ENDIF()


ADD_SUBDIRECTORY(ACVD)
ADD_SUBDIRECTORY(MiscExtOperators)

