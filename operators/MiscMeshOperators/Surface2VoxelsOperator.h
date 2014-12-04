#include "../MSML_Operators.h"
#include <vtkUnstructuredGrid.h>
#include <vtkSmartPointer.h>
#include <vtkPolyData.h>

namespace MSML
{
  namespace Surface2VoxelsOperator 
  {
      LIBRARY_API std::string Surface2VoxelDataOperator(const char* infile, const char* outfile, const double accuracy_level);
      LIBRARY_API double computeAvLengthCount(vtkSmartPointer<vtkPolyData> pd);
  };
}


