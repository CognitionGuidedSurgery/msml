%module NetgenOperatorsPython
%{

#include "NetgenOperators.h"

%}

%include "../std.i"

%include "NetgenOperators.h"


%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}