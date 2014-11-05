/*  =========================================================================

    Program:   The Medical Simulation Markup Language
    Module:    Operators, MiscMeshOperators, FeBioSupport
    Authors:   Sarah Grimm, Alexander Weigl

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


    =========================================================================*/

#ifndef FEBIOSUPPORT_H
#define FEBIOSUPPORT_H

#include "../MSML_Operators.h"

#include <vtkUnstructuredGrid.h>
#include <vtkSmartPointer.h>
#include <string>
#include <vector>

// should be after VTK imports
#include "../vtk6_compat.h"
#include "../common/log.h"


namespace MSML {
    namespace FeBioSupport
    {
        LIBRARY_API void ConvertFEBToVTK(const std::string modelFilename, const std::string lastStep, std::string inputMesh);
		LIBRARY_API std::string ConvertVTKMeshToFeBioMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName);
		LIBRARY_API std::string ConvertVTKMeshToFeBioMeshStringPython(std::string inputMesh,  std::string partName);

		LIBRARY_API std::string createFeBioPressureOutput(vtkUnstructuredGrid* inputMesh, std::vector<unsigned int> indices, std::string id, std::string pressure);
		LIBRARY_API std::string createFeBioPressureOutputPython(std::string inputMesh, std::vector<unsigned int> indices, std::string id, std::string pressure);
    }
}

#endif