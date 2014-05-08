%module MiscMeshOperatorsPython
%{
#include "IndexRegionOperators.h"
#include "MiscMeshOperators.h"
#include "IndexRegionOperators.h"
#include "PostProcessingOperators.h"
#include "MappingOperators.h"
#include "../MSML_Operators.h"
%}


%include "../MSML_Operators.h"

%include "std_vector.i"

namespace std {
    %template(vectori) vector<int>;
    %template(vectord) vector<double>;
    %template(vectorf) vector<float>;
    %template(vectorui) vector<unsigned int>;
    %template(vectorul) vector<unsigned long>;
    %template(vectorl) vector<long>;
    %template(vectorull) vector<unsigned long long>;
    %template(vectorb) vector<bool>;
};

%include "IndexRegionOperators.h"
%include "PostProcessingOperators.h"
%include "MiscMeshOperators.h"
%include "MappingOperators.h"
