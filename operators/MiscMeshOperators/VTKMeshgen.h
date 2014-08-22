#include "../MSML_Operators.h"
#include <vtkUnstructuredGrid.h>

namespace MSML
{
  namespace VTKMeshgen 
  {
      LIBRARY_API std::string DiscreteMarchingCube(const char* infile, const char* outfile);
      LIBRARY_API std::string MarchingCube(const char* infile, const char* outfile, float isoValue);
  };
}


