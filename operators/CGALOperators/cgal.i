%module CGALOperatorsPython
%{
#include "CGALOperators.h"
%}

%include "../std.i"
%include "CGALOperators.h"

%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}