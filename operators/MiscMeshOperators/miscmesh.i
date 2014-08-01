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

%}

%include "../std.i"

%include "IOHelper.h"
%include "IndexRegionOperators.h"
%include "PostProcessingOperators.h"
%include "MiscMeshOperators.h"
%include "MappingOperators.h"
%include "VTKMeshgen.h"
%include "MeshQualityOperators.h"
%include "MeshInfoOperators.h"
%include "FeatureExtractionOperators.h"

%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}

