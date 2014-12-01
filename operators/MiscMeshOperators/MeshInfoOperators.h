/*
 * MeshInfoOperators.h
 *
 *  Created on: 01.08.2014
 *      Author: simon
 */

#ifndef MESHINFOOPERATORS_H_
#define MESHINFOOPERATORS_H_

#include "../MSML_Operators.h"
#include <string>
#include <vector>

namespace MSML {
namespace MeshInfo {

LIBRARY_API long long SurfaceMeshNumberOfPoints(std::string infile);
LIBRARY_API long long SurfaceMeshNumberOfElements(std::string infile);
LIBRARY_API double SurfaceMeshVolume(std::string infile);
LIBRARY_API double SurfaceMeshSurfaceArea(std::string infile);

}
}



#endif /* MESHINFOOPERATORS_H_ */
