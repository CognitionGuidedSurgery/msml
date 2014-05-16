%module BasePython
%{
#include <stdio.h>
#include <iostream>

FILE* outbak;

void begin_capture(int out) {
    std::cout.sync_with_stdio(true);
    outbak = stdout;
    stdout = fdopen(out, "w");;
    std::cout.sync_with_stdio(true);
}

void end_capture() {
    stdout = outbak;
}

void test_echo() {
    std::cout << "This is Sparta!" << std::endl;
    fprintf(stdout,"This is Sparta!");
}

%}

void test_echo();
void begin_capture(int);
void end_capture();

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

