#ifdef _WIN32
#        define LIBRARY_API __declspec(dllexport)
#else
#    define LIBRARY_API
#endif