%module TetgenOperatorsPython
%{
#include "TetgenOperators.h"
    %}

namespace MSML{ namespace Tetgen {
        std::string CreateVolumeMeshPython(std::string infile,
                                           std::string outfile,
                                           bool preserveBoundary);
    }}
