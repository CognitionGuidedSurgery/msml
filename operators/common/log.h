#ifndef LOG_H
#define LOG_H



#include <sstream>
#include <iostream>


#ifdef Py_PYTHON_H
void _log(const char* category, const char* message);
void _log_error(const char* message);
void _log_info(const char* message);
#endif



class Logger {
public:
    Logger(const char* cat) :category(cat), sstream() {

    }

    Logger(const Logger& other) : category(other.category), sstream() {

    }

    Logger& operator<<(const char* str) {
        sstream << str;
        return *this;
    }

    Logger& operator<<(std::string str) {
        sstream << str;
        return *this;
    }


    template<typename T>
    Logger& operator<<(T s) {
        sstream << s;
        return *this;
    }

    Logger& operator<<(std::ostream&(*f)(std::ostream&)) {
        const char* msg = sstream.str().c_str();
#ifdef Py_PYTHON_H
        _log(category, msg);
#else
        std::cerr << msg << std::endl;
#endif
        sstream.str(std::string());
    }

    void flush() {
        sstream.flush();
    }

private:
    std::stringstream sstream;
    const char * category;


};

Logger& log_info();
Logger& log_error();
#endif