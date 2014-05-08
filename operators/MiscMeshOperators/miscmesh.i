%module MiscMeshOperatorsPython
%{

#include "IOHelper.h"
#include "IndexRegionOperators.h"
#include "MiscMeshOperators.h"
#include "PostProcessingOperators.h"
#include "MappingOperators.h"

%}


%include "../MSML_Operators.h"

%include "IOHelper.h"
%include "IndexRegionOperators.h"
%include "PostProcessingOperators.h"
%include "MiscMeshOperators.h"
%include "MappingOperators.h"
