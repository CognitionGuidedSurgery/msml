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

namespace MSML {
namespace MeshQuality {
typedef struct {
    double min;
    double max;
    double avg;
    double var;
    long long n;
} MeshQualityStats;

LIBRARY_API MeshQualityStats MeasureTetrahedricMeshQuality(std::string infile);
}
}

#endif /* MESHQUALITYOPERATORS_H_ */
