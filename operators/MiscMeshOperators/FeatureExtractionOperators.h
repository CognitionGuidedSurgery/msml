/*
 * FeatureExtractionOperators.h
 *
 *  Created on: Jun 25, 2014
 *      Author: bungartz
 */

#ifndef FEATUREEXTRACTIONOPERATORS_H_
#define FEATUREEXTRACTIONOPERATORS_H_

#include "../MSML_Operators.h"
#include <string>

namespace MSML {
namespace FeatureExtractionOperators {

typedef struct {
    double surfaceArea;
    double volume;
} Features;

LIBRARY_API Features ExtractFeatures(std::string infile);

}
}


#endif /* FEATUREEXTRACTIONOPERATORS_H_ */
