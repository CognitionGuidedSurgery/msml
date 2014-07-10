%module TetgenOperatorsPython
%{
#include "TetgenOperators.h"
%}


%include "std_string.i"

namespace MSML {
    namespace Tetgen {
        std::string CreateVolumeMeshPython(std::string infile,
                                           std::string outfile,
                                           bool preserveBoundary);
    }
 }

%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}
