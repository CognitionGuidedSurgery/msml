%module TetgenOperatorsPython
%{
#include "TetgenOperators.h"
%}


%include "std_string.i"

namespace MSML {
    namespace Tetgen {
        std::string CreateVolumeMesh(std::string infile,
                                           std::string outfile,
                                           bool preserveBoundary,
                                           double maxEdgeRadiusRatio,
                                           int minDihedralAngleDegrees,
                                           double maxTetVolumeOrZero,
                                           int optimizationLevel,
                                           bool optimizationUseEdgeAndFaceFlips,
                                           bool optimizationUseVertexSmoothing,
                                           bool optimizationUseVertexInsAndDel);
    }
}


