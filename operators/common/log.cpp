#include "log.h"

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

Logger& log_info() {
    static Logger li = Logger("info");
    return li;
}

Logger& log_error() {
    static Logger le = Logger("error");
    return le;
}