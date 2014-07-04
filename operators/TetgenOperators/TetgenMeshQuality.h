/*
 * TetgenMeshQuality.h
 *
 *  Created on: 04.07.2014
 *      Author: sbungartz
 */

#ifndef TETGENMESHQUALITY_H_
#define TETGENMESHQUALITY_H_

namespace MSML {
namespace Tetgen {
struct TetgenMeshQuality {
    bool preserveBoundary;
    double maxEdgeRadiusRatio;
    int minDihedralAngleDegrees;
    double maxTetVolumeOrZero;
    int optimizationLevel; // 0 to disable optimizations, 10 for maximum number of optimization iterations.
    bool optimizationUseEdgeAndFaceFlips;
    bool optimizationUseVertexSmoothing;
    bool optimizationUseVertexInsAndDel;

    TetgenMeshQuality();
};
}
}

#endif /* TETGENMESHQUALITY_H_ */
