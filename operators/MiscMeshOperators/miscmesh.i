%module MiscMeshOperatorsPython
%{

#include "IOHelper.h"
#include "IndexRegionOperators.h"
#include "MiscMeshOperators.h"
#include "PostProcessingOperators.h"
#include "MappingOperators.h"
#include "MeshQualityOperators.h"
#include "FeatureExtractionOperators.h"

%}

%include "../std.i"

%include "IOHelper.h"
%include "IndexRegionOperators.h"
%include "PostProcessingOperators.h"
%include "MiscMeshOperators.h"
%include "MappingOperators.h"
%include "MeshQualityOperators.h"
%include "FeatureExtractionOperators.h"
