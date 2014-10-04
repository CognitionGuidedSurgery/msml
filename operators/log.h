#ifndef LOG_H
#define LOG_H

#include <sstream>
#include <iostream>


#ifdef Py_PYTHON_H
void _log(const char* category, const char* message) {
    std:: stringstream buffer;

    buffer << "import msml.log\n"
           << "msml.log." << category << "('" << message << "')";

    const char* code = buffer.str().c_str();
    PyRun_SimpleString(code);
}
void _log_error(const char* message) { _log("error", message); }
void _log_info(const char* message) { _log("info", message);}
#endif


class Logger {
public:
    Logger(const char* cat) :category(cat), sstream() {

    }

    Logger(const Logger& other) : category(other.category), sstream() {

    }

    Logger& operator<<(std::string s) {
        sstream << s.c_str();
        return *this;
    }

    Logger& operator<<(const char* str) {
        sstream << str;
        return *this;
    }


    Logger& operator<<(int str) {
        sstream << str;
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

Logger& log_info() {
    static Logger li = Logger("info");
    return li;
}

Logger& log_error() {
    static Logger le = Logger("error");
    return le;
}

#endif