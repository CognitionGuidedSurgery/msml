%module MiscExtOperatorsPython
%{

#include "MiscExtOperators.h"

%}

%include "../std.i"

%include "MiscExtOperators.h"


%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}

