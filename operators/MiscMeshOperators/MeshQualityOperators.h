/*
 * MeshQualityOperators.h
 *
 *  Created on: Jun 23, 2014
 *      Author: bungartz
 */

#ifndef MESHQUALITYOPERATORS_H_
#define MESHQUALITYOPERATORS_H_

#include "../MSML_Operators.h"
#include <string>
#include <vector>

namespace MSML {
namespace MeshQuality {
struct MeshQualityStats {
    double min;
    double max;
    double avg;
    double var;
    long long n;

    std::string qualityMeasureName;
    bool errorQualityMeasureNotFound;

    MeshQualityStats();
};

// Define constants in c file to ensure values are up to date with the VTK version actually used.
extern const std::vector<std::string> TET_QUALITY_MEASURE_TYPE_NAMES;

LIBRARY_API MeshQualityStats MeasureTetrahedricMeshQuality(std::string infile, std::string qualityMeasureName);
LIBRARY_API std::vector<MeshQualityStats> MeasureTetrahedricMeshQuality(std::string infile, std::vector<std::string> qualityMeasureNames);
}
}

#endif /* MESHQUALITYOPERATORS_H_ */
