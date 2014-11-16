%module MiscExtOperatorsPython
%{

#include "AVCDOperators.h"

%}

%include "../std.i"

%include "AVCDOperators.h"


%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}

