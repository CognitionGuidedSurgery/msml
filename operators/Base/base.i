%module BasePython
%{
#include <vector>
#include <string>
#include <cstring>


#include "../common/log.h"
void log_test() {
    //_log("info", "test info level");
    log_error() << "test errrrrr level" << std::endl;
}
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


void log_test();


%begin %{
#ifdef _MSC_VER
#define SWIG_PYTHON_INTERPRETER_NO_DEBUG
#endif
%}

