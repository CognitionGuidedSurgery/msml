/*
 * TetgenSettings.h
 *
 *  Created on: 04.07.2014
 *      Author: sbungartz
 */

#ifndef TETGENSETTINGS_H
#define TETGENSETTINGS_H

namespace MSML {
namespace Tetgen {
struct TetgenSettings {
    bool preserveBoundary;
    double maxEdgeRadiusRatio;
    int minDihedralAngleDegrees;
    double maxTetVolumeOrZero;
    int optimizationLevel; // 0 to disable optimizations, 10 for maximum number of optimization iterations.
    bool optimizationUseEdgeAndFaceFlips;
    bool optimizationUseVertexSmoothing;
    bool optimizationUseVertexInsAndDel;

    LIBRARY_API TetgenSettings();
};
}
}

#endif /* TETGENSETTINGS_H */
