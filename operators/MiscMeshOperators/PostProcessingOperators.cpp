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

#include <vtkTriangle.h>
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


#include <vtkPolyDataWriter.h>
#include <vtkGeometryFilter.h>
#include <vtkPlane.h>
#include <vtkCutter.h>
#include <vtkMassProperties.h>
#include <vtkBooleanOperationPolyDataFilter.h>


#include <vtkDataSetSurfaceFilter.h>
#include "vtkLongLongArray.h"

#include <vtkUnstructuredGridGeometryFilter.h>

#include <vtkStructuredPoints.h>
#include <vtkStructuredPointsReader.h>
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

LIBRARY_API double ComputeRelativeMeanErrorOfSolution( const char* initialMeshFilename, const char* referenceMeshFilename, const char* testMeshFilename, bool surfaceOnly)
{
	vector<double> dispVec;
	vector<double> errorVec;

	CompareMeshes(dispVec, initialMeshFilename, referenceMeshFilename,  surfaceOnly);
	CompareMeshes(errorVec, referenceMeshFilename, testMeshFilename,  surfaceOnly);

	unsigned int numberOfPointsError = errorVec.size();
	unsigned int numberOfPointsDisp = dispVec.size();

	double sum=0;
	double dispSum = 0;

	for(int i=0; i<numberOfPointsDisp; i++)
	{
		sum+= errorVec[i];
		dispSum += dispVec[i];
	}

	sum = sum / dispSum;
	sum = sum / (double)numberOfPointsError;

	log_error() <<"Relative mean error is " << sum << std::endl;

	return sum;

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

std::string ColorMeshFromComparison(std::string modelFilename, std::string referenceFilename, std::string coloredModelFilename)
{
    log_debug() <<"Coloring mesh with errors..." << std::endl;
    ColorMeshFromComparison(modelFilename.c_str(), referenceFilename.c_str(),coloredModelFilename.c_str());
    return coloredModelFilename;
}

std::string ColorMesh(std::string modelFilename, std::string coloredModelFilename)
{
    log_debug() << "Coloring mesh..." << std::endl;
    ColorMesh(modelFilename.c_str(), coloredModelFilename.c_str());
    return coloredModelFilename;
}

//should use polydata 
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

    vtkSmartPointer<vtkUnstructuredGrid> currentGrid = dynamic_cast <vtkUnstructuredGrid*> (geom->GetOutput());

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

//		if(i==163)
//			std::cout<<" Neighbors of triangle 163:";


        std::set<int>::iterator iter;

        for(iter=connectedElements.begin(); iter!=connectedElements.end(); ++iter)
        {
            Edge edge = Edge(i, *iter);
            edge_array.push_back(edge);

//			if(i==163)
//				std::cout<<", "<<(*iter);

        }

//		if(i==163)
//			std::cout<<" \n";

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


//Read positions of points from mesh1 and write them to mesh2.
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

 std::string ApplyDVF(const char* referenceImage, const char* DVF, const char* outputDeformedImage, bool reverseDirection, float voxelSize)
{
    vtkSmartPointer<vtkImageData> refImage =  IOHelper::VTKReadImage(referenceImage);
    vtkSmartPointer<vtkImageData> dvfVecImage = IOHelper::VTKReadImage(DVF);   
    vtkSmartPointer<vtkImageData> outputDefImage;

    outputDefImage = MiscMeshOperators::ImageCreate(refImage);
    if (voxelSize>0)
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
					//TODO: Is this correct, seems to be inversed? 
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

    vtkSmartPointer<vtkImageData> outputDVF = MiscMeshOperators::ImageCreateGeneric(referenceGrid, 0, spacingParam, referenceCoordinateGrid, 0); 

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
              double pInMM[3];
              pInMM[0] = origin[0]+x*spacing[0];
              pInMM[1] = origin[1]+y*spacing[1];
              pInMM[2] = origin[2]+z*spacing[2];

              float* vec = static_cast<float*>(outputDVF->GetScalarPointer(x,y,z));
              CalcVecBarycentric(pInMM, referenceGrid, cellLocatorRef, deformedGrid, interpolateOutsideDistance, vec);
            } //x
        } //y
    } //z

  }

string TransformMeshBarycentric(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* outMeshPath, float interpolateOutsideDistance)
  {
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceGridPath);
	  vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid(deformedGridPath);
    vtkSmartPointer<vtkUnstructuredGrid> refSurface = IOHelper::VTKReadUnstructuredGrid(meshPath);
	  vtkSmartPointer<vtkUnstructuredGrid> out_surface = vtkSmartPointer<vtkUnstructuredGrid>::New();
    PostProcessingOperators::TransformMeshBarycentric(refSurface, referenceGrid, deformedGrid, out_surface, interpolateOutsideDistance);

    //write output
    IOHelper::VTKWriteUnstructuredGrid(outMeshPath,out_surface);

    return string(outMeshPath);
  }

//Generate the displacment vector field (DVF) from reference to deformed mesh - sampled in reference. 
//The results can be used to transfom points and meshes from Reference mesh to deformed mesh.
//To transform voxel data, it is useful to generate the DFV using the deformed mesh as reference.
// pDef - pRef = d     =>     pRef + d = pDef
void TransformMeshBarycentric(vtkUnstructuredGrid* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkUnstructuredGrid* outMesh, float interpolateOutsideDistance)
{
  outMesh->DeepCopy(mesh);
    
  //octree
  vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
  cellLocatorRef->SetDataSet(referenceGrid);
  cellLocatorRef->BuildLocator();

  for (int i=0; i<outMesh->GetPoints()->GetNumberOfPoints();i++)
  {
    double pInMM[3];
    outMesh->GetPoints()->GetPoint(i, pInMM);
    float vec[3];
    PostProcessingOperators::CalcVecBarycentric(pInMM, referenceGrid, cellLocatorRef, deformedGrid, interpolateOutsideDistance, vec);
    pInMM[0]=pInMM[0]+vec[0];
    pInMM[1]=pInMM[1]+vec[1];
    pInMM[2]=pInMM[2]+vec[2];
    outMesh->GetPoints()->SetPoint(i, pInMM);
  }
  outMesh->GetPoints()->Modified();
  outMesh->Modified();
#if VTK_MAJOR_VERSION <= 5
  outMesh->Update();
#endif
}

string TransformSurfaceBarycentric(const char* meshPath, const char* referenceGridPath, const char* deformedGridPath, const char* outMeshPath, float interpolateOutsideDistance)
  {
    vtkSmartPointer<vtkUnstructuredGrid> referenceGrid = IOHelper::VTKReadUnstructuredGrid(referenceGridPath);
	  vtkSmartPointer<vtkUnstructuredGrid> deformedGrid = IOHelper::VTKReadUnstructuredGrid(deformedGridPath);
    vtkSmartPointer<vtkPolyData> refSurface = IOHelper::VTKReadPolyData(meshPath);
	  vtkSmartPointer<vtkPolyData> out_surface = vtkSmartPointer<vtkPolyData>::New();
    PostProcessingOperators::TransformSurfaceBarycentric(refSurface, referenceGrid, deformedGrid, out_surface, interpolateOutsideDistance);

    //write output
    IOHelper::VTKWritePolyData(outMeshPath,out_surface);

    return string(outMeshPath);
  }

//Generate the displacment vector field (DVF) from reference to deformed surface - sampled in reference. 
//The results can be used to transfom points and meshes from Reference mesh to deformed mesh.
//To transform voxel data, it is useful to generate the DFV using the deformed mesh as reference.
// pDef - pRef = d     =>     pRef + d = pDef
void TransformSurfaceBarycentric(vtkPolyData* mesh, vtkUnstructuredGrid* referenceGrid, vtkUnstructuredGrid* deformedGrid, vtkPolyData* outMesh, float interpolateOutsideDistance)
{
  outMesh->DeepCopy(mesh);
    
  //octree
  vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
  cellLocatorRef->SetDataSet(referenceGrid);
  cellLocatorRef->BuildLocator();

  for (int i=0; i<outMesh->GetPoints()->GetNumberOfPoints();i++)
  {
    double pInMM[3];
    outMesh->GetPoints()->GetPoint(i, pInMM);
    float vec[3];
    PostProcessingOperators::CalcVecBarycentric(pInMM, referenceGrid, cellLocatorRef, deformedGrid, interpolateOutsideDistance, vec);
    pInMM[0]=pInMM[0]+vec[0];
    pInMM[1]=pInMM[1]+vec[1];
    pInMM[2]=pInMM[2]+vec[2];
    outMesh->GetPoints()->SetPoint(i, pInMM);
  }
  outMesh->GetPoints()->Modified();
  outMesh->Modified();
#if VTK_MAJOR_VERSION <= 5
  outMesh->Update();
#endif
}

//map closest point to given point from ref mesh to deformed mesh and return displacement
void CalcVecBarycentric(double* pInMM, vtkUnstructuredGrid* referenceGrid, vtkCellLocator* cellLocatorRef, vtkUnstructuredGrid* deformedGrid, float interpolateOutsideDistance, float* vecOut)
{
  //locate closest cell.
  vtkIdType containingCellRefId;
  double closestPointInCell[3];
  int subId=0;
  double dist=0;
  cellLocatorRef->FindClosestPoint(pInMM,  closestPointInCell, containingCellRefId, subId, dist);

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

  vecOut[0] = scale_outside * ((x0[0] * bcords[0] + x1[0] * bcords[1] + x2[0] * bcords[2] + x3[0] * bcords[3]) - closestPointInCell[0]);
  vecOut[1] = scale_outside * ((x0[1] * bcords[0] + x1[1] * bcords[1] + x2[1] * bcords[2] + x3[1] * bcords[3]) - closestPointInCell[1]);
  vecOut[2] = scale_outside * ((x0[2] * bcords[0] + x1[2] * bcords[1] + x2[2] * bcords[2] + x3[2] * bcords[3]) - closestPointInCell[2]);

}

void ComputeOrganVolume(const char* volumeFilename){
	vtkUnstructuredGrid* inputMesh = IOHelper::VTKReadUnstructuredGrid(volumeFilename);
	vtkSmartPointer<vtkGeometryFilter> geometryFilter =
		vtkSmartPointer<vtkGeometryFilter>::New();

	__SetInput(geometryFilter,inputMesh);
	geometryFilter->Update();
	vtkPolyData* polydata = geometryFilter->GetOutput();

	vtkMassProperties* mass = vtkMassProperties::New();
	__SetInput(mass, polydata);
	mass->Modified();
	mass->Update();

	cout << "Volume: " << mass->GetVolume()  << " mm^3" << endl << "Surface: " << mass->GetSurfaceArea()<< " mm^2" << endl;
}

double ComputeDiceCoefficientPolydata(const char* filename, const char* filename2, const char *intersectionFile="")
{
		vtkSmartPointer<vtkPolyData> meshA = IOHelper::VTKReadPolyData(filename);		
		vtkSmartPointer<vtkPolyData> meshB = IOHelper::VTKReadPolyData(filename2);		

		//calculate volume of meshA
		vtkSmartPointer<vtkMassProperties> meshAProps = vtkMassProperties::New();
		__SetInput(meshAProps,meshA);
		meshAProps->Update();
		double meshAVolume = meshAProps->GetVolume();
		std::cout << "1.Volume : " << meshAVolume << std::endl;

		//calculate volume of mesB
		vtkSmartPointer<vtkMassProperties> meshBProps = vtkMassProperties::New();
		__SetInput(meshBProps,meshB);
		meshBProps->Update();
		double meshBVolume = meshBProps->GetVolume();
		std::cout << "2.Volume : " << meshBVolume << std::endl;

		//set up the boolean operation filter and compute intersection of meshA and meshB
		vtkSmartPointer<vtkBooleanOperationPolyDataFilter> booleanOperation =
		vtkSmartPointer<vtkBooleanOperationPolyDataFilter>::New();
#if VTK_MAJOR_VERSION < 6
		booleanOperation->SetInput(0, meshA);
		booleanOperation->SetInput(1, meshB);
#else
		booleanOperation->AddInputData(0, meshA);
		booleanOperation->AddInputData(1, meshB);
#endif
		booleanOperation->SetOperationToIntersection();
		booleanOperation->Modified();
		booleanOperation->Update();
		vtkSmartPointer<vtkPolyData> pol = booleanOperation->GetOutput();

		if(intersectionFile!="")
		{			
			IOHelper::VTKWritePolyData(intersectionFile,pol);
		}
		
		//calculate volume of intersection
		vtkSmartPointer<vtkMassProperties> meshIntersectionProps = vtkMassProperties::New();
		__SetInput(meshIntersectionProps,pol);
		meshIntersectionProps->Modified();	
		meshIntersectionProps->Update();
		double overlap = meshIntersectionProps->GetVolume();
		std::cout << "Overlapping Volume: " << overlap << std::endl;
	
		//calculate dice coefficent
		double diceCoeff = (2*overlap)/(meshAVolume + meshBVolume);
		cout << "DICE-Coefficient: " << diceCoeff << endl;
		return diceCoeff;
}

void ComputeDiceCoefficient(const char* filename, const char* filename2)
{
		log_error()<<"computing dice coefficient"<<std::endl;
		vtkUnstructuredGrid* currentGrid =  IOHelper::VTKReadUnstructuredGrid(filename);
		vtkUnstructuredGrid* referenceGrid = IOHelper::VTKReadUnstructuredGrid(filename2);
		log_error()<<"load ok"<<std::endl;

		vtkSmartPointer<vtkGeometryFilter> geometryFilter =
		vtkSmartPointer<vtkGeometryFilter>::New();
		log_error()<<"filter setup ok"<<std::endl;
		__SetInput(geometryFilter,currentGrid);
		geometryFilter->Update();
		vtkPolyData* polydata = geometryFilter->GetOutput();
		log_error()<<"filter ok"<<std::endl;

		vtkSmartPointer<vtkGeometryFilter> geometryFilter2 =
		vtkSmartPointer<vtkGeometryFilter>::New();

		__SetInput(geometryFilter2,referenceGrid);
		geometryFilter2->Update();
		vtkPolyData* polydata2 = geometryFilter2->GetOutput();

		vtkSmartPointer<vtkBooleanOperationPolyDataFilter> booleanOperation =
		vtkSmartPointer<vtkBooleanOperationPolyDataFilter>::New();
#if VTK_MAJOR_VERSION < 6
		booleanOperation->SetInput(0, polydata);
		booleanOperation->SetInput(1, polydata2);
#else
		booleanOperation->AddInputData(0, polydata);
		booleanOperation->AddInputData(1, polydata2);
#endif
		booleanOperation->SetOperationToIntersection();
		booleanOperation->Modified();
		booleanOperation->Update();
		vtkPolyData* pol = booleanOperation->GetOutput();
		vtkMassProperties* mass = vtkMassProperties::New();
		__SetInput(mass,pol);
		mass->Modified();
		mass->Update();
		int overlap = mass->GetVolume();
		std::cout << "Overlapping Volume: " << overlap << "mm^3" << endl;
		__SetInput(mass, polydata);
		mass->Modified();
		mass->Update();
		int volume1  =  mass->GetVolume();
		std::cout << "1.Volume : " << volume1 << "mm^3" << endl;
		__SetInput(mass, polydata2);
		mass->Modified();
		mass->Update();
		int volume2  =  mass->GetVolume();
		std::cout << "2.Volume : " << volume2 << "mm^3" << endl;
		float diceCoeff = (float)(2*overlap)/(volume1 + volume2);
		cout << "DICE-Coefficient: " << diceCoeff << endl;
}

void ComputeOrganCrossSectionArea(const char* volumeFilename){
  vtkUnstructuredGrid* inputMesh = IOHelper::VTKReadUnstructuredGrid(volumeFilename);

	vtkSmartPointer<vtkGeometryFilter> geometryFilter =
	vtkSmartPointer<vtkGeometryFilter>::New();

	__SetInput(geometryFilter,inputMesh);
	geometryFilter->Update();
	vtkPolyData* polydata = geometryFilter->GetOutput();

	double bounds[6];
	polydata->GetBounds(bounds);
	std::cout << "Bounds: "
        << bounds[0] << ", " << bounds[1] << " "
        << bounds[2] << ", " << bounds[3] << " "
        << bounds[4] << ", " << bounds[5] << std::endl;

	vtkSmartPointer<vtkPlane> plane =
	vtkSmartPointer<vtkPlane>::New();
	plane->SetOrigin((bounds[1] + bounds[0]) / 2.0,
		(bounds[3] + bounds[2]) / 2.0,
			(bounds[4] + bounds[5]) / 2.0);
	plane->SetNormal(0,0,1);

	vtkSmartPointer<vtkCutter> cutter =
	vtkSmartPointer<vtkCutter>::New();
  __SetInput(cutter,inputMesh);
	cutter->SetCutFunction(plane);
	cutter->Update();
	vtkPolyData *pCutterOutput = cutter->GetOutput();
	double area = 0;
	for(vtkIdType i = 0; i < pCutterOutput->GetNumberOfPolys(); i++)
	{
		vtkCell* cell = pCutterOutput->GetCell(i);
		int numberOfPoints = cell->GetNumberOfPoints();
		if(numberOfPoints == 3) {
			vtkTriangle* triangle = dynamic_cast<vtkTriangle*>(cell);
			double p0[3];
			double p1[3];
			double p2[3];
			triangle->GetPoints()->GetPoint(0, p0);
			triangle->GetPoints()->GetPoint(1, p1);
			triangle->GetPoints()->GetPoint(2, p2);
			area += vtkTriangle::TriangleArea(p0, p1, p2);
		}
	}

	cout << "Area of cross section: " << area << "mm^2" << endl;

}


string ImageSum(const char* imagedataFilePattern, bool normalize, const char* outfile)
{
 
  std::vector<std::string> imagedata = IOHelper::getAllFilesByMask(imagedataFilePattern);
  int numer_of_images = imagedata.size();
  std::vector<double> weights(numer_of_images);
  vtkSmartPointer<vtkImageWeightedSum> sumFilter = vtkSmartPointer<vtkImageWeightedSum>::New();
  if (!normalize) 
    sumFilter->NormalizeByWeightOff();
  vtkSmartPointer<vtkImageData> curentVoxelImage;

  for (int i=0; i<numer_of_images;i++)
  {
    curentVoxelImage = IOHelper::VTKReadImage(imagedata[i].c_str());
    __AddInput(sumFilter,curentVoxelImage);

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

  

