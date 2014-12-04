%module MiscMeshOperatorsPython
%{
#include "IOHelper.h"
#include "IndexRegionOperators.h"
#include "MiscMeshOperators.h"
#include "PostProcessingOperators.h"
#include "MappingOperators.h"
#include "VTKMeshgen.h"
#include "MeshQualityOperators.h"
#include "MeshInfoOperators.h"
#include "FeatureExtractionOperators.h"
#include "FeBioSupport.h"
#include "SurfaceToVoxelDataOperator.h"
%}

%include "../std.i"

namespace std {
	%template(vectorMeshQualityStats) vector<MSML::MeshQuality::MeshQualityStats>;
}

%include "IOHelper.h"
%include "IndexRegionOperators.h"
%include "PostProcessingOperators.h"
%include "MiscMeshOperators.h"
%include "MappingOperators.h"
%include "VTKMeshgen.h"
%include "MeshQualityOperators.h"
%include "MeshInfoOperators.h"
%include "FeatureExtractionOperators.h"
%include "FeBioSupport.h"
%include "SurfaceToVoxelDataOperator.h"

 
