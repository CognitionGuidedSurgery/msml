__author__ = 'weigl'

##
# Exception Hierarchy:
#    for exception that are not allowed to happen regulary,
#    iff. the program was correct.
#
#    Like type/format errors that should be checked by caller.
#


class MSMLException(Exception):
    pass


##
# Error Hierarchy:
#  for signaling to the user
#


class MSMLError(Exception):
    pass


class BindError(Exception):
    pass


class MSMLXMLParseError(MSMLError):
    pass


##
# Warning hierarchy
# http://docs.python.org/2/library/warnings.html#warnings.warn
#
# Things that should be an exception but, should not interrupt program flow.
#
#

class MSMLWarning(Warning):
    pass


class MSMLXMlWarning(MSMLWarning):
    pass


class MSMLXMLUnknownTagWarning(MSMLWarning):
    pass


class MSMLOperatorWarning(MSMLWarning):
    pass


class MSMLUnknownFunctionWarning(MSMLOperatorWarning):
    pass


class MSMLUnknownModuleWarning(MSMLOperatorWarning):
    pass
