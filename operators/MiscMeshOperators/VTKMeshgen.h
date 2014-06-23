#include "../MSML_Operators.h"
#include <vtkUnstructuredGrid.h>

namespace MSML
{

  class VTKMeshgen
  {
    public:
      LIBRARY_API std::string DiscreteMarchingCube(const char* infile, const char* outfile);
 
  };
}


