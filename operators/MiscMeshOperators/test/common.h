#ifndef COMMON_TEST_H
#define COMMON_TEST_H

#include <vector>
#include <iostream>
#include <string>
#include <sstream>

#include <boost/filesystem.hpp>

#include "PostProcessingOperators.h"
#include "MiscMeshOperators.h"
#include "IndexRegionOperators.h"

#include "VTKMeshgen.h"
#include "IOHelper.h"

#define SMOKE_TEST_DIR_PREFIX smoke

using namespace MSML;


#define REQUIRE_FILE_EXISTS(x) \
    BOOST_REQUIRE_MESSAGE( boost::filesystem::exists( x ), \
                           std::string("Could not find file: ") +  x)
//    BOOST_REQUIRE(boost::filesystem::exists(x))

#include <iostream>
#include <algorithm>
#include <boost/iostreams/device/mapped_file.hpp>
	
namespace io = boost::iostreams;
bool file_cmp(const char* f, const char* g) {
	io::mapped_file_source f1(f);
	io::mapped_file_source f2(g);

	return f1.size() == f2.size()
		&& std::equal(f1.data(), f1.data() + f1.size(), f2.data());
}
#endif
