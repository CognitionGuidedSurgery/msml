%module TetgenOperatorsPython
%{
#include "TetgenOperators.h"
%}


%include "std_string.i"

%include "TetgenMeshQuality.h"
namespace MSML {
    namespace Tetgen {
        std::string CreateVolumeMeshPython(std::string infile,
                                           std::string outfile,
                                           MSML::Tetgen::TetgenMeshQuality settings);
    }
 }

%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}
