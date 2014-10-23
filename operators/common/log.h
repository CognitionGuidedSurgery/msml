#ifndef LOG_H
#define LOG_H

#include <sstream>
#include <iostream>
#include <ostream>


#ifdef PYTHONLOGGING
void _log(const char* category, const char* message);
void _log_error(const char* message);
void _log_info(const char* message);

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
		_log(category, msg);
		sstream.str(std::string());
		return *this;
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
Logger& log_debug();
#else
std::ostream& log_info();
std::ostream& log_error();
std::ostream& log_debug();
#endif //PYTHONLOGGING


#endif