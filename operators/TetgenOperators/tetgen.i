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
