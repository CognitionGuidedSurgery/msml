%module BasePython
%{
#include <vector>
#include <string>
%}

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

 %begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}
