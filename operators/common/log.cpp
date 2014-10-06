#include "log.h"

#ifdef PYTHONLOGGING
#include <Python.h>


void _log(const char* category, const char* message) {
    const char* const m = message;
/*
    std:: stringstream buffer;

    buffer << "import msml.log" << std::endl
           << "msml.log." << category << "(\" " << message << " \" )" << std::endl;

    buffer.flush();

    const char* code = buffer.str().c_str();

    std::cout << code << std::endl << buffer.str() << std::endl;


    PyRun_SimpleString(code);
*/


    PyObject* msml_log = PyImport_ImportModule("msml.log");

    if(msml_log) {
        PyObject* msml_log_dict = PyModule_GetDict(msml_log);
        PyObject* fn = PyDict_GetItemString(msml_log_dict, category);
        if(fn) {
            //std::cout << message << std::endl;
            PyObject* args = Py_BuildValue("(s)" , m);
            PyObject* result = PyObject_Call(fn, args, NULL);
            //Py_DECREF(args);
            //Py_DECREF(result);
        } else{
            std::cerr << "could not find category '" << category << "' in msml.log" << std::endl;
        }
    } else{
        std::cerr << "could not import msml.log from c++ side" << std::endl;
    }
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

Logger& log_debug() {
    static Logger le = Logger("error");
    return le;
}