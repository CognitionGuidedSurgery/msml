#include "../MSML_Operators.h"
#include <vtkUnstructuredGrid.h>
#include <vtkSmartPointer.h>
#include <vtkPolyData.h>

namespace MSML
{
  namespace SurfaceToVoxelDataOperator 
  {
      LIBRARY_API std::string SurfaceToVoxelDataOperator(const char* infile, const char* outfile, float accuracy_level, float smoothing);
      LIBRARY_API double computeAvLengthCount(vtkSmartPointer<vtkPolyData> pd);
  }
}


