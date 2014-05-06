%module TetgenOperatorsPython
%{

#include "TetgenOperators.h"

    using namespace MSML;

    static bool CreateVolumeMesh(const char* infile, const char* outfile,
                                 bool preserveBoundary, bool isQuadratic ) {
        return TetgenOperators::CreateVolumeMesh(infile, outfile, preserveBoundary, isQuadratic );
    }

    static std::string CreateVolumeMeshPython(std::string infile,
                                              std::string outfile,
                                              bool preserveBoundary) {
        return TetgenOperators::CreateVolumeMeshPython(infile, outfile, preserveBoundary);
    }

    static bool CreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh,
                                 bool preserveBoundary, bool isQuadratic ) {
        return TetgenOperators::CreateVolumeMesh(inputMesh, outputMesh, preserveBoundary, isQuadratic );
    }


%}


static bool CreateVolumeMesh(const char* infile, const char* outfile,
                             bool preserveBoundary, bool isQuadratic ) {
    return TetgenOperators::CreateVolumeMesh(infile, outfile, preserveBoundary, isQuadratic );
}

static std::string CreateVolumeMeshPython(std::string infile,
                                          std::string outfile,
                                          bool preserveBoundary) {
    return TetgenOperators::CreateVolumeMeshPython(infile, outfile, preserveBoundary);
}

static bool CreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh,
                             bool preserveBoundary, bool isQuadratic ) {
    return TetgenOperators::CreateVolumeMesh(inputMesh, outputMesh, preserveBoundary, isQuadratic );
}
