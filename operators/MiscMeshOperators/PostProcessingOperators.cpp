/*  =========================================================================

    Program:   The Medical Simulation Markup Language
    Module:    Operators, MiscMeshOperators
    Authors:   Markus Stoll, Stefan Suwelack

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

#include "PostProcessingOperators.h"
#include "IOHelper.h"
#include <iostream>

#include <string.h>
#include <stdio.h>

#include "vtkUnstructuredGrid.h"

#include <vtkTetra.h>
#include <vtkCellArray.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSTLReader.h>

#include <vtkPointData.h>
#include <vtkIdList.h>
#include <vtkVertexGlyphFilter.h>
#include <vtkPoints.h>
#include <vtkUnstructuredGrid.h>
#include <vtkPointSet.h>

#include "vtkSTLWriter.h"
#include "vtkSTLReader.h"
#include "vtkPolyData.h"
#include "vtkImageData.h"
#include "vtkPoints.h"
#include "vtkCellArray.h"
#include "vtkCleanPolyData.h"

#include "vtkFloatArray.h"
#include "vtkDoubleArray.h"
#include "vtkCellData.h"

#include "vtkImageWeightedSum.h"


#include <vtkDataSetSurfaceFilter.h>
#include "vtkLongLongArray.h"

#include <vtkUnstructuredGridGeometryFilter.h>

#include <vtkCellLocator.h>

#include <vtkImageInterpolator.h>

#include "math.h"

#include <boost/graph/sequential_vertex_coloring.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/filesystem.hpp>
#include <boost/lexical_cast.hpp>

#include "MiscMeshOperators.h"

using namespace boost;

#include "../vtk6_compat.h"
#include "../common/log.h"


namespace MSML {
namespace PostProcessingOperators {

void CompareMeshes(std::vector<double>& errorVec, const char* referenceFilename, const char* testFilename, bool surfaceOnly)
{
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceFilename);
    vtkSmartPointer<vtkUnstructuredGrid> testGrid = IOHelper::VTKReadUnstructuredGrid(testFilename);

    CompareMeshes(errorVec, referenceGrid, testGrid, surfaceOnly);
}

void CompareMeshes(std::vector<double>& errorVec, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly)
{

    vtkPoints* refPoints = referenceMesh->GetPoints();
    vtkPoints* testPoints = testMesh->GetPoints();

    if(surfaceOnly)
    {
        vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
            vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
        __SetInput(geom, referenceMesh);
        geom->Update();

        vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom2 =
            vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
        __SetInput(geom2,testMesh);
        geom2->Update();

        refPoints->DeepCopy(geom->GetOutput()->GetPoints());
        testPoints->DeepCopy(geom2->GetOutput()->GetPoints());


    }


    //get the points
//	vtkPoints* refPoints = referenceMesh->GetPoints();
//	vtkPoints* testPoints = testMesh->GetPoints();

    unsigned int numberOfRefPoints = refPoints->GetNumberOfPoints();

    unsigned int numberOfTestPoints = testPoints->GetNumberOfPoints();

    if(numberOfRefPoints != numberOfTestPoints)
    {
        log_error() <<"Error, meshes have to be the same size!!" << std::endl;
        return;
    }

    //initialize errorVec
    errorVec.resize(numberOfRefPoints);




    double* currentTestPoint = new double[3];
    double* currentRefPoint = new double[3];
    double currentError;


    for(unsigned int i=0; i<numberOfRefPoints; i++)
    {
        refPoints->GetPoint(i, currentRefPoint);
        testPoints->GetPoint(i, currentTestPoint);
        currentError =  sqrt(pow((currentRefPoint[0]-currentTestPoint[0]), 2) + pow((currentRefPoint[1]-currentTestPoint[1]), 2) + pow((currentRefPoint[2]-currentTestPoint[2]), 2));// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );
        errorVec[i]= currentError;

    }





}

void CompareMeshes(double& errorRMS, double& errorMax, const char* referenceFilename, const char* testFilename, bool surfaceOnly)
{
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceFilename);
    vtkSmartPointer<vtkUnstructuredGrid> testGrid = IOHelper::VTKReadUnstructuredGrid(testFilename);

    CompareMeshes(errorRMS, errorMax, referenceGrid, testGrid, surfaceOnly);

}

void CompareMeshes(double& errorRMS, double& errorMax, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly)
{

    errorRMS = 0;
    errorMax = 0;

    vtkPoints* refPoints = referenceMesh->GetPoints();
    vtkPoints* testPoints = testMesh->GetPoints();

    if(surfaceOnly)
    {
        vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
            vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
        __SetInput(geom, referenceMesh);
        geom->Update();

        vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom2 =
            vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
        __SetInput(geom2, testMesh);
        geom2->Update();

        refPoints->DeepCopy(geom->GetOutput()->GetPoints());
        testPoints->DeepCopy(geom2->GetOutput()->GetPoints());


    }


    //get the points
//	vtkPoints* refPoints = referenceMesh->GetPoints();
//	vtkPoints* testPoints = testMesh->GetPoints();

    unsigned int numberOfRefPoints = refPoints->GetNumberOfPoints();

    unsigned int numberOfTestPoints = testPoints->GetNumberOfPoints();

    if(numberOfRefPoints != numberOfTestPoints)
    {
        log_error() <<"Error, meshes have to be the same size!!" << std::endl;
        return;
    }




    double* currentTestPoint = new double[3];
    double* currentRefPoint = new double[3];
    double currentError;


    for(unsigned int i=0; i<numberOfRefPoints; i++)
    {
        refPoints->GetPoint(i, currentRefPoint);
        testPoints->GetPoint(i, currentTestPoint);

        currentError =  sqrt(pow((currentRefPoint[0]-currentTestPoint[0]), 2) + pow((currentRefPoint[1]-currentTestPoint[1]), 2) + pow((currentRefPoint[2]-currentTestPoint[2]), 2));// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );
        //		currentError =  sqrt((currentRefPoint[0]-currentTestPoint[0])*(currentRefPoint[0]-currentTestPoint[0]) + (currentRefPoint[1]-currentTestPoint[1])*(currentRefPoint[1]-currentTestPoint[1]) + (currentRefPoint[2]-currentTestPoint[2])*(currentRefPoint[2]-currentTestPoint[2]) );// + pow(refPoints[1]-testPoints[1], 2) + pow(refPoints[2]-testPoints[2], 2) );
        errorRMS += currentError;

        if(currentError > errorMax)
        {
            errorMax = currentError;
        }

    }


    errorRMS = errorRMS / numberOfRefPoints;
    errorRMS = sqrt(errorRMS);






}

void ColorMeshFromComparison(const char* modelFilename, const char* referenceFilename, const char* coloredModelFilename)
{
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceFilename);
    vtkSmartPointer<vtkUnstructuredGrid> modelGrid = IOHelper::VTKReadUnstructuredGrid(modelFilename);

    vtkSmartPointer<vtkUnstructuredGrid> coloredGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();

    ColorMeshFromComparison(modelGrid, referenceGrid, coloredGrid);

    //write output
    IOHelper::VTKWriteUnstructuredGrid(coloredModelFilename, coloredGrid);
}

void ColorMeshFromComparison(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* referenceMesh,vtkUnstructuredGrid* coloredMesh)
{
    vtkSmartPointer<vtkUnstructuredGrid> theMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
    theMesh->DeepCopy(referenceMesh);

    std::vector<double> errorVec;
    CompareMeshes(errorVec, referenceMesh, inputMesh, false);

    if(errorVec.size() != inputMesh->GetNumberOfPoints())
    {
        log_error() <<"Size mismatch between errorVec and inputMesh size" << std::endl;
        return;
    }

    vtkSmartPointer<vtkDoubleArray> dataArray = vtkSmartPointer<vtkDoubleArray> ::New();
    dataArray->SetNumberOfComponents(1);
    dataArray->SetNumberOfTuples(errorVec.size());

    for(unsigned int i=0; i<errorVec.size(); i++)
    {
        dataArray->SetTuple1(i, errorVec[i]);
    }

    theMesh->GetPointData()->AddArray(dataArray);
    dataArray->SetName("Errors");

    coloredMesh->DeepCopy(theMesh);
}

std::string ColorMeshFromComparisonPython(std::string modelFilename, std::string referenceFilename, std::string coloredModelFilename)
{
    log_debug() <<"Coloring mesh with errors..." << std::endl;
    ColorMeshFromComparison(modelFilename.c_str(), referenceFilename.c_str(),coloredModelFilename.c_str());
    return coloredModelFilename;
}

std::string ColorMeshPython(std::string modelFilename, std::string coloredModelFilename)
{
    log_debug() << "Coloring mesh..." << std::endl;
    ColorMesh(modelFilename.c_str(), coloredModelFilename.c_str());
    return coloredModelFilename;
}


void ColorMesh(const char* modelFilename, const char* coloredModelFilename)
{
    //load the vtk quadratic mesh
    vtkSmartPointer<vtkUnstructuredGrid> currentGrid=  IOHelper::VTKReadUnstructuredGrid(modelFilename);

    vtkSmartPointer<vtkPolyData> surface =
        vtkSmartPointer<vtkPolyData>::New();

    ColorMesh(currentGrid, surface);

    //write output
    IOHelper::VTKWritePolyData(coloredModelFilename, surface);
}

void ColorMesh(vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)
{
    //extract the surface as unstructured grid
    vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
        vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
    __SetInput(geom, inputMesh);
    geom->Update();


    //color the polydata elements

    vtkUnstructuredGrid* currentGrid = geom->GetOutput();

    vtkPoints* thePoints = currentGrid->GetPoints();
    vtkCellArray* theCells = currentGrid->GetCells();
    vtkIdType numberOfPoints = thePoints->GetNumberOfPoints();
    vtkIdType numberOfCells = theCells->GetNumberOfCells();


    int cellType = currentGrid->GetCellType(1);
    bool isQuadratic = false;

    log_info() <<"CellType is "<<cellType<< std::endl;

    if(cellType == 22)
    {
        isQuadratic = true;
    }

    if(isQuadratic)
    {
        log_info() <<"QuadraticMeshDetected" << std::endl;
    }

    typedef adjacency_list<listS, vecS, undirectedS> Graph;
    typedef graph_traits<Graph>::vertex_descriptor vertex_descriptor;
    typedef graph_traits<Graph>::vertices_size_type vertices_size_type;
    typedef property_map<Graph, vertex_index_t>::const_type vertex_index_map;

    typedef std::pair<int, int> Edge;

    std::vector<Edge> edge_array;



    for(unsigned int i=0; i<numberOfCells; i++) // iterate over all triangles
    {
        // Returns the set of element indices connected to an input one (i.e. which can be reached by topological links)
        //vector<unsigned int> connectedElements = main->m_Topology->getConnectedElement(i); // seems not implemented in the topology!!

        std::set<int> connectedElements; // Set of all tetrahedra which are connected with the tetrahedra nr. "i"

        vtkSmartPointer<vtkIdList> cellPointIds =
            vtkSmartPointer<vtkIdList>::New();

        currentGrid->GetCellPoints(i, cellPointIds);

        for(int edgeIter=0; edgeIter<3; edgeIter++)// over 3 faces
        {
            vtkSmartPointer<vtkIdList> idList =
                vtkSmartPointer<vtkIdList>::New();
            idList->InsertNextId(cellPointIds->GetId((edgeIter+2)%3));
            idList->InsertNextId(cellPointIds->GetId((edgeIter)%3));

            vtkSmartPointer<vtkIdList> neighborCellIds =
                vtkSmartPointer<vtkIdList>::New();

            currentGrid->GetCellNeighbors(i, idList, neighborCellIds);

            for(vtkIdType j = 0; j < neighborCellIds->GetNumberOfIds(); j++)
            {
                connectedElements.insert(neighborCellIds->GetId(j));
            }

        }

        std::set<int>::iterator iter;

        for(iter=connectedElements.begin(); iter!=connectedElements.end(); ++iter)
        {
            Edge edge = Edge(i, *iter);
            edge_array.push_back(edge);
        }
    }

    // eliminating duplicate edges - needed? seems not!

    // generating the Graph
    Graph g(edge_array.begin(), edge_array.end(), edge_array.size());

//	printf("InternalData.m_nNodes = %d \n", InternalData.m_nNodes);
//	printf("InternalData.m_nElements = %d \n", InternalData.m_nElements);
//	printf("num_vertices(g) = %d \n", num_vertices(g));
//	printf("edge_array.size() = %d \n", edge_array.size());

    // generating the colorvector in normal order
    std::vector<vertices_size_type> color_vec( num_vertices(g));
    iterator_property_map<vertices_size_type*, vertex_index_map> color(&color_vec.front(), get(vertex_index, g));
    vertices_size_type num_colors = sequential_vertex_coloring(g, color);

    //InternalData.m_nColors = num_colors;
    log_debug() << "num_colors = "<<  num_colors << std::endl;

    vtkSmartPointer<vtkFloatArray> colorData =
        vtkSmartPointer<vtkFloatArray>::New();
    colorData->SetNumberOfComponents(1);
    colorData->SetName("colors");

    for(unsigned int i=0; i<numberOfCells; i++)
    {
        colorData->InsertNextTuple1(color_vec.at(i));
    }

    currentGrid->GetCellData()->SetScalars(colorData);

    //subdivide the elements into smaller triangles and edges

    vtkSmartPointer<vtkDataSetSurfaceFilter> surfaceTessellator =
        vtkSmartPointer<vtkDataSetSurfaceFilter>::New();

    __SetInput(surfaceTessellator, currentGrid);

    if(isQuadratic)
    {
        surfaceTessellator->SetNonlinearSubdivisionLevel(3);
        surfaceTessellator->Update();
        //outputMesh->DeepCopy(surfaceTessellator->GetOutput());
    }

    else
        //outputMesh->DeepCopy(currentGrid);

    {
        surfaceTessellator->Update();
    }

    outputMesh->DeepCopy(surfaceTessellator->GetOutput());

}



void MergeMeshes(vtkUnstructuredGrid* pointsMesh, vtkUnstructuredGrid* cellsMesh, vtkUnstructuredGrid* outputMesh)
{
    outputMesh->DeepCopy(cellsMesh);
    vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
    points->DeepCopy(pointsMesh->GetPoints());
    outputMesh->SetPoints(points);
#if VTK_MAJOR_VERSION <= 5
    outputMesh->Update();
    //TODO is there really no method in vtk 6 for Update?
    //     In documentation is nothing listed
#endif
}

void MergeMeshes(const char* pointsMeshFilename, const char* cellsMeshFilename, const char* outputMeshFilename)
{
    vtkSmartPointer<vtkUnstructuredGrid> pointsMesh = IOHelper::VTKReadUnstructuredGrid(pointsMeshFilename);
    vtkSmartPointer<vtkUnstructuredGrid> cellsMesh = IOHelper::VTKReadUnstructuredGrid(cellsMeshFilename);
    vtkSmartPointer<vtkUnstructuredGrid> mergedGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();

    MergeMeshes(pointsMesh, cellsMesh, mergedGrid);

    IOHelper::VTKWriteUnstructuredGrid(outputMeshFilename, mergedGrid);
}

 std::string ApplyDVFPython(const char* referenceImage, const char* DVF, const char* outputDeformedImage, bool reverseDirection, float voxelSize)
{
    vtkSmartPointer<vtkImageData> refImage =  IOHelper::VTKReadImage(referenceImage);
    vtkSmartPointer<vtkImageData> dvfVecImage = IOHelper::VTKReadImage(DVF);   
    vtkSmartPointer<vtkImageData> outputDefImage;

    outputDefImage = MiscMeshOperators::ImageCreate(refImage);
    MiscMeshOperators::ImageChangeVoxelSize(outputDefImage, voxelSize);
    #if VTK_MAJOR_VERSION <= 5
    outputDefImage->SetScalarTypeToFloat();
    outputDefImage->AllocateScalars();
    #else
    outputDefImage->AllocateScalars(VTK_FLOAT,1); //one value per 3d coordinate
    #endif

    ApplyDVF(refImage, dvfVecImage, outputDefImage, reverseDirection, voxelSize);
    log_debug() << "Writing Deformed image.. "  << std::endl;
    //write output
    IOHelper::VTKWriteImage(outputDeformedImage, outputDefImage);
    return outputDeformedImage;
}

/*
    Deform input image by dvf: For each voxel of outputDefImage: Follow dvf to voxel in input voxel grid.
    The dvf displacements will be inverted inside this method.
    pOut = pIn - d

    If GenerateDVF is used to create the DVF:
    - In GenerateDVF: Make sure the DVF is sampled on the output grid (output grid = Ref grid).
    - In ApplyDVF: Set reverseDirection=true

    - Areas outside definition zone of DVF or reference image are set to -1024
*/
void ApplyDVF(vtkImageData* inputImage, vtkImageData* dvf, vtkImageData* outputDefImage, bool reverseDirection, double voxelSize)
  {
    int* dims = outputDefImage->GetDimensions();
    double* origin = outputDefImage->GetOrigin();
    double* spacing = outputDefImage->GetSpacing();


    vtkSmartPointer<vtkImageInterpolator> dvfInterpolator = vtkSmartPointer<vtkImageInterpolator>::New();
    dvfInterpolator->SetOutValue(-1);
    dvfInterpolator->BreakOnError();
    dvfInterpolator->SetInterpolationModeToLinear();
    dvfInterpolator->Initialize(dvf);

    int M = dvf->GetNumberOfScalarComponents();
    int N  = dvfInterpolator->GetNumberOfComponents();

    vtkSmartPointer<vtkImageInterpolator> refImageInterpolator = vtkSmartPointer<vtkImageInterpolator>::New();
    refImageInterpolator->SetInterpolationModeToLinear();
    refImageInterpolator->Initialize(inputImage);


    //for each voxel of result image.
    for (int k=0; k<dims[2]; k++)
    {
        for (int j=0; j<dims[1]; j++)
        {
            for (int i=0; i<dims[0]; i++)
            {
                //default value for outsiders:
                double pixelValue = -1024; //CT air

                //current position in world coordinate system
                double pos[3] = {origin[0] + spacing[0]* i, origin[1] + spacing[1]* j, origin[2] + spacing[2]* k};
                double displacmentVec[3] = {-10,-10,-10};

                //get displacment vector (interpolated)
                bool inBoundsDVF = dvfInterpolator->Interpolate(pos, displacmentVec);
                displacmentVec[0] = dvfInterpolator->Interpolate(pos[0], pos[1], pos[2], 0);
                displacmentVec[1] = dvfInterpolator->Interpolate(pos[0], pos[1], pos[2], 1);
                displacmentVec[2] = dvfInterpolator->Interpolate(pos[0], pos[1], pos[2], 2);

                if (inBoundsDVF)
                {
                    double posInRef[3];

                    if (!reverseDirection)
                    {
                        posInRef[0] = pos[0] - displacmentVec[0];
                        posInRef[1] = pos[1] - displacmentVec[1];
                        posInRef[2] = pos[2] - displacmentVec[2];
                    }

                    else
                    {
                        posInRef[0] = pos[0] + displacmentVec[0];
                        posInRef[1] = pos[1] + displacmentVec[1];
                        posInRef[2] = pos[2] + displacmentVec[2];
                    }

                    double newPixelValue[1] = {0};
                    //Follow displacment vector in refImage.
                    bool inBoundsRef = refImageInterpolator->Interpolate(posInRef, newPixelValue);

                    if (inBoundsRef)
                    {
                        pixelValue = *newPixelValue;
                    }
                }

                //write pixel value refImage=>defImage
                float* pixel = static_cast<float*>(outputDefImage->GetScalarPointer(i,j,k));
                pixel[0] = pixelValue;
            }
        }
    }
}

std::string GenerateDVF(const char* referenceGridFilename, const char* deformedGridFilename, const char* outputDVFFilename, float spacingParam, const char* referenceCoordinateGrid, float interpolateOutsideDistance)
{

    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceGridFilename);
    vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid(deformedGridFilename);

    vtkSmartPointer<vtkImageData> outputDVF;
    if (strlen(referenceCoordinateGrid)>0)
    {
      outputDVF = MiscMeshOperators::ImageCreate(IOHelper::VTKReadImage(referenceCoordinateGrid));
      if (spacingParam>0)
      {
        MiscMeshOperators::ImageChangeVoxelSize(outputDVF, spacingParam);
      }
    }
    else
    {
      outputDVF = MiscMeshOperators::ImageCreateWithMesh(referenceGrid, 100);
    }

    if (spacingParam>0)
    {
      MiscMeshOperators::ImageChangeVoxelSize(outputDVF, spacingParam);
    }

    GenerateDVFImp(referenceGrid, deformedGrid, outputDVF, interpolateOutsideDistance);
 
    //write output
    IOHelper::VTKWriteImage(outputDVFFilename, outputDVF);
    return outputDVFFilename;
    //write raw data
    /*
        FILE * pFile;
        pFile = fopen(((string)outputDVFFilename + ".dvf").c_str(),"wb");
        int size = 3 * outputDVF->GetDimensions()[0] * outputDVF->GetDimensions()[1] * outputDVF->GetDimensions()[2];
        void* data = malloc(sizeof(float) * size);
        outputDVF->GetPointData()->GetScalars()->ExportToVoidPointer(data);
        int error = fwrite(data,sizeof(float),size,pFile);*/
}

//Generate the displacment vector field (DVF) from reference to deformed mesh - sampled in reference.
//The results can be used to transfom points and meshes from Reference mesh to deformed mesh.
//To transform voxel data, it is useful to generate the DFV using the deformed mesh as reference.
// pDef - pRef = d     =>     pRef + d = pDef
//Method: For each point in DVF: Find nearest point in reference mesh, calculate barycentric coordinates, find same point in deformed mesh, calculate displacment.
void GenerateDVFImp(vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkSmartPointer<vtkImageData> outputDVF, float interpolateOutsideDistance)
{
    int* dims = outputDVF->GetDimensions();
    double* origin = outputDVF->GetOrigin();
    double* spacing = outputDVF->GetSpacing();

#if VTK_MAJOR_VERSION <= 5
    outputDVF->SetScalarTypeToFloat();
    outputDVF->SetNumberOfScalarComponents(3);
    outputDVF->AllocateScalars();
#else
    outputDVF->AllocateScalars(VTK_FLOAT, 3); //3 component per voxel (vectors)
#endif


    //octree
    vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
    cellLocatorRef->SetDataSet(referenceGrid);
    cellLocatorRef->BuildLocator();

    for (int z = 0; z < dims[2]; z++)
    {
        for (int y = 0; y < dims[1]; y++)
        {
            for (int x = 0; x < dims[0]; x++)
            {
              double p_mm[3];
              p_mm[0] = origin[0]+x*spacing[0];
              p_mm[1] = origin[1]+y*spacing[1];
              p_mm[2] = origin[2]+z*spacing[2];

              float* vec = static_cast<float*>(outputDVF->GetScalarPointer(x,y,z));
              CalcVecBarycentric(p_mm, referenceGrid, cellLocatorRef, deformedGrid, interpolateOutsideDistance, vec);
            } //x
        } //y
    } //z

  }

string TransformMeshBarycentricPython(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* out_meshPath, float interpolateOutsideDistance)
  {
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceGridPath);
	  vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid(deformedGridPath);
    vtkSmartPointer<vtkUnstructuredGrid> refSurface = IOHelper::VTKReadUnstructuredGrid(meshPath);
	  vtkSmartPointer<vtkUnstructuredGrid> out_surface = vtkSmartPointer<vtkUnstructuredGrid>::New();
    PostProcessingOperators::TransformMeshBarycentric(refSurface, referenceGrid, deformedGrid, out_surface, interpolateOutsideDistance);

    //write output
    IOHelper::VTKWriteUnstructuredGrid(out_meshPath,out_surface);

    return string(out_meshPath);
  }

//Generate the displacment vector field (DVF) from reference to deformed mesh - sampled in reference. 
//The results can be used to transfom points and meshes from Reference mesh to deformed mesh.
//To transform voxel data, it is useful to generate the DFV using the deformed mesh as reference.
// pDef - pRef = d     =>     pRef + d = pDef
void TransformMeshBarycentric(vtkUnstructuredGrid* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkUnstructuredGrid* out_mesh, float interpolateOutsideDistance)
{
  out_mesh->DeepCopy(mesh);
    
  //octree
  vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
  cellLocatorRef->SetDataSet(referenceGrid);
  cellLocatorRef->BuildLocator();

  for (int i=0; i<out_mesh->GetPoints()->GetNumberOfPoints();i++)
  {
    double p_mm[3];
    out_mesh->GetPoints()->GetPoint(i, p_mm);
    float vec[3];
    PostProcessingOperators::CalcVecBarycentric(p_mm, referenceGrid, cellLocatorRef, deformedGrid, interpolateOutsideDistance, vec);
    p_mm[0]=p_mm[0]+vec[0];
    p_mm[1]=p_mm[1]+vec[1];
    p_mm[2]=p_mm[2]+vec[2];
    out_mesh->GetPoints()->SetPoint(i, p_mm);
  }
  out_mesh->GetPoints()->Modified();
  out_mesh->Modified();
#if VTK_MAJOR_VERSION <= 5
  out_mesh->Update();
#endif
}

string TransformSurfaceBarycentricPython(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* out_meshPath, float interpolateOutsideDistance)
  {
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceGridPath);
	  vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid(deformedGridPath);
    vtkSmartPointer<vtkPolyData> refSurface = IOHelper::VTKReadPolyData(meshPath);
	  vtkSmartPointer<vtkPolyData> out_surface = vtkSmartPointer<vtkPolyData>::New();
    PostProcessingOperators::TransformSurfaceBarycentric(refSurface, referenceGrid, deformedGrid, out_surface, interpolateOutsideDistance);

    //write output
    IOHelper::VTKWritePolyData(out_meshPath,out_surface);

    return string(out_meshPath);
  }

//Generate the displacment vector field (DVF) from reference to deformed surface - sampled in reference. 
//The results can be used to transfom points and meshes from Reference mesh to deformed mesh.
//To transform voxel data, it is useful to generate the DFV using the deformed mesh as reference.
// pDef - pRef = d     =>     pRef + d = pDef
void TransformSurfaceBarycentric(vtkPolyData* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkPolyData* out_mesh, float interpolateOutsideDistance)
{
  out_mesh->DeepCopy(mesh);
    
  //octree
  vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
  cellLocatorRef->SetDataSet(referenceGrid);
  cellLocatorRef->BuildLocator();

  for (int i=0; i<out_mesh->GetPoints()->GetNumberOfPoints();i++)
  {
    double p_mm[3];
    out_mesh->GetPoints()->GetPoint(i, p_mm);
    float vec[3];
    PostProcessingOperators::CalcVecBarycentric(p_mm, referenceGrid, cellLocatorRef, deformedGrid, interpolateOutsideDistance, vec);
    p_mm[0]=p_mm[0]+vec[0];
    p_mm[1]=p_mm[1]+vec[1];
    p_mm[2]=p_mm[2]+vec[2];
    out_mesh->GetPoints()->SetPoint(i, p_mm);
  }
  out_mesh->GetPoints()->Modified();
  out_mesh->Modified();
#if VTK_MAJOR_VERSION <= 5
  out_mesh->Update();
#endif
}

//map closest point to given point from ref mesh to deformed mesh and return displacement
void CalcVecBarycentric(double* p_mm, vtkUnstructuredGrid* referenceGrid, vtkCellLocator* cellLocatorRef, vtkUnstructuredGrid* deformedGrid, float interpolateOutsideDistance, float* vec_out)
{
  //locate closest cell.
  vtkIdType containingCellRefId;
  double closestPointInCell[3];
  int subId=0;
  double dist=0;
  cellLocatorRef->FindClosestPoint(p_mm,  closestPointInCell, containingCellRefId, subId, dist);

  //calculate bcords: The barycentric coordinate uses 4 coeff [0..1] to linear combine the vertices of the cell to represent a point inside the cell. 
  vtkTetra*  containingCellRef = (vtkTetra*) referenceGrid->GetCell(containingCellRefId);
  double bcords[4];
  double x0[3]; double x1[3]; double x2[3]; double x3[3];
  vtkPoints* cellPoints = containingCellRef->GetPoints();
  cellPoints->GetPoint(0, x0);
  cellPoints->GetPoint(1, x1);
  cellPoints->GetPoint(2, x2);
  cellPoints->GetPoint(3, x3);
  containingCellRef->BarycentricCoords(closestPointInCell, x0, x1, x2, x3, bcords);

  //apply bcords with deformed nodes to calculate the
  //cell id in reference and deformed mesh must be equal
  vtkTetra*  containingCellDef = (vtkTetra*) deformedGrid->GetCell(containingCellRefId); 
  cellPoints = containingCellDef->GetPoints();
  cellPoints->GetPoint(0, x0);
  cellPoints->GetPoint(1, x1);
  cellPoints->GetPoint(2, x2);
  cellPoints->GetPoint(3, x3);

  float scale_outside = 1;
  if (dist > interpolateOutsideDistance)
  {
    scale_outside = (interpolateOutsideDistance - dist) / interpolateOutsideDistance; //can be < 0 
    if (scale_outside < 0)
      scale_outside = 0;
  }

  vec_out[0] = scale_outside * ((x0[0] * bcords[0] + x1[0] * bcords[1] + x2[0] * bcords[2] + x3[0] * bcords[3]) - closestPointInCell[0]);
  vec_out[1] = scale_outside * ((x0[1] * bcords[0] + x1[1] * bcords[1] + x2[1] * bcords[2] + x3[1] * bcords[3]) - closestPointInCell[1]);
  vec_out[2] = scale_outside * ((x0[2] * bcords[0] + x1[2] * bcords[1] + x2[2] * bcords[2] + x3[2] * bcords[3]) - closestPointInCell[2]);

}

string ImageWeightedSum(std::vector<std::string> polydata, const char* referenceGrid, bool normalize, const char* outfile)
{
  int numer_of_images = polydata.size();
  std::vector<double> weights(numer_of_images);
  vtkSmartPointer<vtkImageWeightedSum> sumFilter = vtkSmartPointer<vtkImageWeightedSum>::New();
  vtkSmartPointer<vtkImageData> firstVoxelImage;
  
  //first iteration
  firstVoxelImage = vtkSmartPointer<vtkImageData>::New();
  MiscMeshOperators::VoxelizeSurfaceMesh(IOHelper::VTKReadPolyData(polydata[0].c_str()), firstVoxelImage, 0, referenceGrid, true);
  //debug//string firstImageFile = string(outfile) + "_voxels_0" +".vtk";
  //debug//IOHelper::VTKWriteImage(firstImageFile.c_str(), firstVoxelImage);
  sumFilter->AddInputData(firstVoxelImage);
  weights[0] = 1.0;

  //second..Nth iteration
  for (int i=1; i<numer_of_images;i++)
  {
    vtkSmartPointer<vtkImageData> curentVoxelImage = vtkSmartPointer<vtkImageData>::New();
    MiscMeshOperators::VoxelizeSurfaceMesh(IOHelper::VTKReadPolyData(polydata[i].c_str()), curentVoxelImage, 0, referenceGrid, true);
    //debug//char buffer_i_string [10];
    //debug//itoa (i, buffer_i_string, 10);
    //debug//string firstImageFile = string(outfile) + "_voxels_" + string(buffer_i_string)  +".vtk";
    //debug//IOHelper::VTKWriteImage(firstImageFile.c_str(), firstVoxelImage);
    sumFilter->AddInputData(curentVoxelImage);
    weights[i] = 1.0;
  }
  
  
  vtkSmartPointer<vtkDoubleArray> vtkWeights = vtkDoubleArray::New();
  vtkWeights->SetArray(&weights[0], numer_of_images, 1);
  sumFilter->SetWeights(vtkWeights);
  sumFilter->Update();
  IOHelper::VTKWriteImage(outfile, sumFilter->GetOutput());
  return outfile;

}
}
}
  
