/*  =========================================================================

    Program:   The Medical Simulation Markup Language
    Module:    Operators, MiscMeshOperators
  Authors:   Markus Stoll, Stefan Suwelack, Nicolai Schoch

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

#include "MiscMeshOperators.h"
#include <iostream>
#include <sstream>

#include <string.h>

#include <stdio.h>

#include "vtkUnstructuredGrid.h"

#include "IOHelper.h"

#include <vtkXMLUnstructuredGridReader.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkTetra.h>
#include <vtkCellArray.h>
#include <vtkSmartPointer.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkUnstructuredGridWriter.h>
#include <vtkUnstructuredGridReader.h>
#include <vtkPolyDataWriter.h>
#include <vtkGenericDataObjectReader.h>

#include <vtkPointData.h>
#include <vtkIdList.h>
#include <vtkVertexGlyphFilter.h>
#include <vtkPoints.h>

#include "vtkSTLWriter.h"
#include "vtkPolyDataWriter.h"
#include "vtkPolyDataReader.h"
#include "vtkPolyData.h"
#include "vtkPoints.h"
#include "vtkCellArray.h"
#include <vtkCellData.h>
#include "vtkCleanPolyData.h"
#include "vtkUnsignedIntArray.h"

#include "vtkFloatArray.h"
#include "vtkIntArray.h"
#include "vtkCellData.h"
#include "vtkSTLReader.h"
#include "vtkKdTreePointLocator.h"
#include "vtkVoxelModeller.h"
#include "vtkImageWriter.h"
#include "vtkPNGWriter.h"


#include <vtkDataSetSurfaceFilter.h>
#include "vtkLongLongArray.h"
#include "vtkDoubleArray.h"


#include <vtkUnstructuredGridGeometryFilter.h>
#include <vtkUnstructuredGridWriter.h>
#include "vtkDataSetSurfaceFilter.h"
#include "vtkUnstructuredGridGeometryFilter.h"

#include <vtkXMLImageDataReader.h>
#include <vtkXMLImageDataWriter.h>
#include <vtkStructuredPointsWriter.h>

#include <vtkImageData.h>
#include <vtkPolyDataToImageStencil.h>
#include <vtkImageStencil.h>
#include "vtkFeatureEdges.h"
#include "vtkFillHolesFilter.h"
#include "vtkCleanPolyData.h"
#include "vtkAppendFilter.h"

#include "vtkTetra.h"
#include "vtkTriangle.h"
#include "vtkGenericCell.h"
#include "vtkCellLocator.h"


#include <vtkThreshold.h>
#include <vtkMergeCells.h>

#include <boost/filesystem.hpp>
#include <boost/lexical_cast.hpp>

#include "PostProcessingOperators.h"
#include "../vtk6_compat.h"
using namespace std;

namespace MSML {
namespace MiscMeshOperators {
std::string ConvertSTLToVTKPython(std::string infile, std::string outfile)
{
    ConvertSTLToVTK( infile.c_str(), outfile.c_str());

    return outfile;
}

bool ConvertSTLToVTK(const char* infile, const char* outfile)
{
    vtkSmartPointer<vtkPolyData> mesh =
        vtkSmartPointer<vtkPolyData>::New();

    ConvertSTLToVTK( infile, mesh);

    vtkSmartPointer<vtkPolyDataWriter> writer =
        vtkSmartPointer<vtkPolyDataWriter>::New();
    writer->SetFileName(outfile);

    __SetInput(writer, mesh);
    writer->Write();

    return true;
}

bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh)
{
    vtkSmartPointer<vtkSTLReader> reader =
        vtkSmartPointer<vtkSTLReader>::New();
    reader->SetFileName(infile);
    reader->Update();

    //deep copy
    outputMesh->DeepCopy(reader->GetOutput());

    return true;
}

std::string ConvertVTKToSTLPython(std::string infile, std::string outfile)
{
	ConvertVTKToVTU( infile.c_str(), outfile.c_str());

	return outfile;
}

bool ConvertVTKToSTL(const char* infile, const char* outfile)
{
    std::cout<<"Converting "<<infile <<" to STL\n";
    vtkSmartPointer<vtkPolyDataReader> reader =
        vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile);
    reader->Update();
    vtkPolyData* currentPolydata = reader->GetOutput();


    vtkSmartPointer<vtkSTLWriter> writer =
        vtkSmartPointer<vtkSTLWriter>::New();
    writer->SetFileTypeToBinary();
    writer->SetFileName(outfile);
    __SetInput(writer, reader->GetOutput());
    writer->Write();
    std::cout<<"STL file written\n";

    return true;
}

//---------------------------- start of new by Nico on 2014-05-10.
std::string ConvertVTKToVTUPython(std::string infile, std::string outfile)
{
	ConvertVTKToVTU( infile.c_str(), outfile.c_str());
	return outfile;
}

bool ConvertVTKToVTU(const char* infile, const char* outfile )
{
	std::cout<<"Converting "<<infile <<" to VTU\n";
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	    vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(infile);
	reader->Update();
	//vtkPolyData* currentPolydata = reader->GetOutput();
	// OR: ?!
	//vtkSmartPointer<vtkUnstructuredGrid> mesh = vtkSmartPointer<vtkUnstructuredGrid>::New();

	//write output
	vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer = vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New(); // vtkUnstructuredGridXML-Writer
	// OR: ?!
	//vtkSmartPointer<vtkUnstructuredGridWriter> writer = vtkSmartPointer<vtkUnstructuredGridWriter>::New(); // vtkUnstructuredGridXML-Writer
	writer->SetFileName(outfile);
	writer->SetDataModeToAscii();
	__SetInput(writer, reader->GetOutput());
	// OR: ?!
	//__SetInput(writer, mesh);
	writer->Write();
	std::cout<<"VTU file written\n";

	return true;
}

/*
bool ConvertVTKToVTU(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh) // is this needed at all?!
{
	  // Combine the two data sets
	  vtkSmartPointer<vtkAppendFilter> appendFilter = vtkSmartPointer<vtkAppendFilter>::New();

	  __AddInput(appendFilter, inputPolyData);

	  appendFilter->Update();

	  outputMesh->DeepCopy(appendFilter->GetOutput());

	 return true;
}
*/
//---------------------------- end of new by Nico on 2014-05-10.

bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile)
{
    vtkPoints* thePoints = inputMesh->GetPoints();
    vtkIdType noPoints = thePoints->GetNumberOfPoints();

    //open file and generate textstream
    std::ofstream file(outfile);

    if (!file.is_open())
    {
        return false;
    }


    // std::cout<<" number of points3"<<inputMesh->GetNumberOfPoints();
    //write Header
    file << "OFF\n"
         <<	 noPoints << " " << inputMesh->GetNumberOfCells() <<" 0\n";

    std::cout <<" write points \n";

    double* currentPoint;

    for(int i=0; i<noPoints; i++)
    {
        currentPoint = thePoints->GetPoint(i);
        file<<currentPoint[0]<<" "<<currentPoint[1]<<" "<<currentPoint[2]<<"\n";
    }

    inputMesh->BuildCells(); //this call caused an access violation when this method was part of a SHARED (.dll) library and the ConvertVTKtoOff was called from outside the dll .


    vtkIdType* currentCellPoints;
    //currentCellPoints = new vtkIdType[3];
    vtkIdType numberOfNodes=3;

    for(int i=0; i<inputMesh->GetNumberOfCells(); i++)
    {
        inputMesh->GetCellPoints(i,numberOfNodes,currentCellPoints);
        file<<3<<" "<<currentCellPoints[0]<<" "<<currentCellPoints[1]<<" "<<currentCellPoints[2]<<"\n";
    }

    // delete [] currentCellPoints;

    file.close();

    return true; //todo: add useful return value
}


bool ConvertInpToVTK(const char* infile, const char* outfile)
{
    return true;
}

bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh )
{
    return true;
}

std::string VTKToInpPython( std::string infile, std::string outfile)
{
	VTKToInp( infile.c_str(),  outfile.c_str());
	return outfile;
}

bool VTKToInp( const char* infile, const char* outfile)
{
    vtkSmartPointer<vtkUnstructuredGridReader> reader =
        vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(infile);
    reader->Update();


    return VTKToInp(reader->GetOutput(),  outfile);

}

bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile)
{
    //open file and generate textstream
    //		 QFile file(GetCompleteFilename(filename));
    //		 if (!file.open(QFile::WriteOnly | QFile::Truncate))
    //			 return false;
    //
    //		 QTextStream out(&file);

    std::ofstream out(outfile);

    if (!out.is_open())
    {
        return false;
    }

    out << ConvertVTKMeshToAbaqusMeshString(inputMesh, std::string("Part1"), std::string("Neo-Hookean"));
    return true;
}

std::string ExtractAllSurfacesByMaterial(const char* infile, const char* outfile, bool theCutIntoPieces)
{
    //load the vtk volume mesh
    vtkSmartPointer<vtkGenericDataObjectReader> reader =
        vtkSmartPointer<vtkGenericDataObjectReader>::New();
    reader->SetFileName(infile);
    reader->Update();

    if (!reader->IsFileUnstructuredGrid())
    {
        cerr << infile << " is not a vtkUnstructuredGrid";
        exit (1);
    }

    vtkUnstructuredGrid* inputGrid = reader->GetUnstructuredGridOutput();

    //cut model in pieces
    if (theCutIntoPieces)
    {
        cerr << "Cutting" << std::endl;
        map<int, int> belongstTo;
        std::map<std::pair<int,int>, int> newPrivatePoints; // <oldKey, MaterialId> => newKey
        vtkIntArray* cellMaterialArray0 = (vtkIntArray*) inputGrid->GetCellData()->GetArray("Materials");


        for (int kk= 0; kk<10; kk++)
        {
            belongstTo.clear();

            for(vtkIdType i = 0; i < inputGrid->GetNumberOfCells(); i++)
            {
                ;//cerr << "Checking element " << i << std::endl;
                vtkCell* currentCell = inputGrid->GetCell(i);
                vtkIdList* currentPointIds = currentCell->GetPointIds();

                for(vtkIdType pointId = 0; pointId < currentPointIds->GetNumberOfIds(); pointId++)
                {
                    vtkIdType currentPoint = currentPointIds->GetId(pointId);

                    if (belongstTo[currentPoint] == 0)
                    {
                        belongstTo[currentPoint] = (int)*cellMaterialArray0->GetTuple(i);
                        ;//cerr << "   empty <- " << (int)*cellMaterialArray0->GetTuple(i) << std::endl;
                    }

                    else if (belongstTo[currentPoint] == (int)*cellMaterialArray0->GetTuple(i))
                        ;//cerr << "   same <-" << (int)*cellMaterialArray0->GetTuple(i) << std::endl;

                    else
                    {
                        cerr << "   replace needed" << pointId << std::endl;
                        double* cords = currentCell->GetPoints()->GetPoint(pointId);

                        if ( newPrivatePoints[std::make_pair(currentPoint,(int)*cellMaterialArray0->GetTuple(i))] == 0 )
                        {
                            vtkIdType aNewPointId = inputGrid->GetPoints()->InsertNextPoint(cords[0], cords[1], cords[2] + 0.01 * (int)*cellMaterialArray0->GetTuple(i));
                            *(currentPointIds->GetPointer(pointId)) = aNewPointId;
                            inputGrid->ReplaceCell(i,currentPointIds->GetNumberOfIds(), currentPointIds->GetPointer(0));
                            newPrivatePoints[std::make_pair(currentPoint,(int)*cellMaterialArray0->GetTuple(i))] = aNewPointId;
                        }

                        else
                        {
                            *(currentPointIds->GetPointer(pointId)) = newPrivatePoints[std::make_pair(currentPoint,(int)*cellMaterialArray0->GetTuple(i))] ;
                            inputGrid->ReplaceCell(i,currentPointIds->GetNumberOfIds(), currentPointIds->GetPointer(0));
                        }

                    }
                }
            }

            std::cout << "There are " << inputGrid->GetNumberOfCells()  << std::endl;
        }

        vtkSmartPointer<vtkUnstructuredGridWriter> cutGridWriter = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
        cutGridWriter->SetFileName((string(outfile) + "-cut.vtk").c_str());
        __SetInput(cutGridWriter,inputGrid);
        cutGridWriter->Write();
    }

    //done cutting



    std::cout << "There are " << reader->GetUnstructuredGridOutput()->GetNumberOfCells()  << " cells before thresholding." << std::endl;

    //get alle surfaces
    vtkIntArray* cellMaterialArray = (vtkIntArray*) reader->GetUnstructuredGridOutput()->GetCellData()->GetArray("Materials");
    map<int,int>* cellDataHist = createHist(cellMaterialArray);


    //create a surface for each material
    std::vector<vtkSmartPointer<vtkPolyData> > surfaces;

    for (map<int,int>::iterator it=cellDataHist->begin(); it!=cellDataHist->end(); it++) //filter for each material
    {
        cout << it->second << " cells of MaterialId=" << it->first << " found." << std::endl;
        vtkSmartPointer<vtkThreshold> threshold = vtkSmartPointer<vtkThreshold>::New();
        __SetInput(threshold, inputGrid);
        threshold->ThresholdBetween(it->first, it->first);
        threshold->SetInputArrayToProcess(0, 0, 0, vtkDataObject::FIELD_ASSOCIATION_CELLS, "Materials");
        threshold->Update();

        //debug out surface
        vtkSmartPointer<vtkUnstructuredGridWriter> aUGridWriter = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
        stringstream itFirst;
        itFirst << it->first;
        aUGridWriter->SetFileName((string(outfile) + "-volume" + itFirst.str() + ".vtk").c_str());
        __SetInput(aUGridWriter, threshold->GetOutput());
        aUGridWriter->Write();
        //done debug out

        cout << "There are " << threshold->GetOutput()->GetNumberOfCells() << " cells after thresholding with " <<  it->first << std::endl;
        //extract surface
        vtkSmartPointer<vtkPolyData> mesh = vtkSmartPointer<vtkPolyData>::New();

        string error_message;
        bool result = ExtractSurfaceMesh(threshold->GetOutput(), mesh);

        //debug out surface
        vtkSmartPointer<vtkPolyDataWriter> aGridWriter = vtkSmartPointer<vtkPolyDataWriter>::New();
        aGridWriter->SetFileName((string(outfile) + "-surface" + itFirst.str() + ".vtk").c_str());
        __SetInput(aGridWriter, mesh);
        aGridWriter->Write();
        //done debug out

        surfaces.push_back(mesh);
    }

    //merge all surfaces back into a single unstuctured grid - togther with volume cells. Points are unified.
    int numberOfMehes = surfaces.size()+1;
    int numberOfPoints=inputGrid->GetNumberOfPoints();
    int numberOfCells=inputGrid->GetNumberOfCells();

    for (int i=0; i<surfaces.size(); i++)
    {
        numberOfPoints+=surfaces[i]->GetNumberOfPoints();
        numberOfCells+=surfaces[i]->GetNumberOfCells();
    }

    vtkSmartPointer<vtkMergeCells> merger = vtkSmartPointer<vtkMergeCells>::New();
    vtkSmartPointer<vtkUnstructuredGrid> unionMesh = vtkSmartPointer<vtkUnstructuredGrid>::New();
    merger->SetUnstructuredGrid(unionMesh);
    merger->SetTotalNumberOfCells(numberOfCells);
    merger->SetTotalNumberOfPoints(numberOfPoints);
    merger->MergeDuplicatePointsOn();
    merger->SetPointMergeTolerance(0.00001);
    merger->SetTotalNumberOfDataSets(numberOfMehes);

    //merge it
    for (int i=0; i<surfaces.size(); i++)
    {
        int error = merger->MergeDataSet(surfaces[i]);

        if (error)
        {
            cerr << "vtkMergeCells error during MergeDataSet with surfaces " << i;
            exit(2);
        }
    }

    int error = merger->MergeDataSet(inputGrid);

    if (error)
    {
        cerr << "vtkMergeCells error during MergeDataSet with volume.";
        exit(2);
    }

    merger->Finish();

    //save the merged data
    vtkSmartPointer<vtkUnstructuredGridWriter> unioGridWriter = vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    unioGridWriter->SetFileName(outfile);
    __SetInput(unioGridWriter, unionMesh);
    unioGridWriter->Write();
    return outfile;
}


map<int,int>* createHist(vtkDataArray* theVtkDataArray)
{
    map<int,int>* hist = new map<int,int>();
    int N = theVtkDataArray->GetNumberOfTuples();

    for (int i=0; i<N; i++)
    {
        double* v = theVtkDataArray->GetTuple(i);

        //hist[(int)*v] =  hist[(int)*v] + 1 ;
        if (hist->find(*v)!=hist->end())
        {
            hist->at(*v) = hist->at(*v) + 1;
        }

        else
        {
            hist->insert(pair<int,int>(*v,1));
        }
    }

    return hist;
}

std::string  ExtractSurfaceMeshPython( std::string infile, std::string outfile)
{
    ExtractSurfaceMesh(infile.c_str(), outfile.c_str());
    return outfile;
}

bool ExtractSurfaceMesh( const char* infile, const char* outfile)
{
    //load the vtk quadratic mesh
    vtkSmartPointer<vtkUnstructuredGridReader> reader =
        vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(infile);
    reader->Update();

    vtkSmartPointer<vtkPolyData> mesh =
        vtkSmartPointer<vtkPolyData>::New();

    bool result = ExtractSurfaceMesh( reader->GetOutput(), mesh);



    //save the subdivided polydata
    vtkSmartPointer<vtkPolyDataWriter> polywriter =
        vtkSmartPointer<vtkPolyDataWriter>::New();
    polywriter->SetFileName(outfile);
    __SetInput(polywriter, mesh);
    polywriter->Write();

    return result;


}

bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)
{

    //extract the surface as unstructured grid
    vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
        vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
    __SetInput(geom, inputMesh);
    geom->Update();


    //color the polydata elements

    vtkUnstructuredGrid* currentGrid = geom->GetOutput();

    int cellType = currentGrid->GetCellType(1);
    bool isQuadratic = false;

    std::cout<<"CellType is "<<cellType<<"\n";

    if(cellType == 22)
    {
        isQuadratic = true;
    }

    if(isQuadratic)
    {
        std::cout<<"QuadraticMeshDetected\n";
    }

    vtkSmartPointer<vtkDataSetSurfaceFilter> surfaceTessellator =
        vtkSmartPointer<vtkDataSetSurfaceFilter>::New();

    __SetInput(surfaceTessellator, currentGrid);

    if(isQuadratic)
    {
        surfaceTessellator->SetNonlinearSubdivisionLevel(3);
    }

    surfaceTessellator->Update();



    outputMesh->DeepCopy(surfaceTessellator->GetOutput());

    return true; //todo: add useful return value
}

bool AssignSurfaceRegion( const char* infile, const char* outfile,  std::vector<std::string> regionMeshes )
{
    //load the vtk  mesh
    vtkSmartPointer<vtkUnstructuredGridReader> reader =
        vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(infile);
    reader->Update();

    vtkSmartPointer<vtkUnstructuredGrid> mesh =
        vtkSmartPointer<vtkUnstructuredGrid>::New();

    unsigned int meshCount = regionMeshes.size();

    std::vector<vtkSmartPointer<vtkPolyData> > regionMeshesVec;

    for(unsigned int i=0; i<meshCount; i++)
    {
        vtkSmartPointer<vtkPolyDataReader> tempReader =
            vtkSmartPointer<vtkPolyDataReader>::New();
        tempReader->SetFileName(regionMeshes[i].c_str());
        tempReader->Update();

        vtkSmartPointer<vtkPolyData> currentMesh =
            vtkSmartPointer<vtkPolyData>::New();

        currentMesh->DeepCopy(tempReader->GetOutput());
        regionMeshesVec.push_back(currentMesh);


    }


    bool result = AssignSurfaceRegion( reader->GetOutput() , mesh, regionMeshesVec);



    //save the subdivided polydata
    vtkSmartPointer<vtkUnstructuredGridWriter> polywriter =
        vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    polywriter->SetFileName(outfile);
    __SetInput(polywriter, mesh);
    polywriter->Write();

    return result;
}

bool AssignSurfaceRegion( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh,
                          std::vector<vtkSmartPointer<vtkPolyData> >& regionMeshes)
{
    unsigned int numberOfVolumePoints = inputMesh->GetNumberOfPoints();

    //deep copy to output mesh
    outputMesh->DeepCopy(inputMesh);

    //create point data with indices
    vtkSmartPointer<vtkUnsignedIntArray> indexData =
        vtkSmartPointer<vtkUnsignedIntArray>::New();
    indexData->SetNumberOfComponents(1);
    indexData->SetName("indices");

    //create point data and reset to 0
    //create point data with indices
    vtkSmartPointer<vtkUnsignedIntArray> regionData =
        vtkSmartPointer<vtkUnsignedIntArray>::New();
    regionData->SetNumberOfComponents(1);
    regionData->SetName("indices");

    for(unsigned int i=0; i<numberOfVolumePoints; i++)
    {
        indexData->InsertNextTuple1(i);
        regionData->InsertNextTuple1(0);
    }

    inputMesh->GetPointData()->SetScalars(indexData);




    //extract surface as ug
    vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
        vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
    __SetInput(geom,inputMesh);
    geom->Update();

    vtkUnstructuredGrid* currentSurfaceMesh = geom->GetOutput();


    //for each region mesh
    unsigned int meshCount = regionMeshes.size();
    double* currentPoint = new double[3];

    vtkSmartPointer<vtkKdTreePointLocator> kDTree =
        vtkSmartPointer<vtkKdTreePointLocator>::New();
    kDTree->SetDataSet(currentSurfaceMesh);
    kDTree->BuildLocator();


    for(unsigned int i=0; i<meshCount; i++)
    {
        vtkPoints* currentPoints = regionMeshes[i]->GetPoints();


        //iterate over points
        for( unsigned int iterPoint = 0; iterPoint < currentPoints->GetNumberOfPoints(); iterPoint++)
        {
            //for each point:: assign region to point closest to that point
            currentPoints->GetPoint(iterPoint, currentPoint);

            vtkIdType iD = kDTree->FindClosestPoint(currentPoint);

            unsigned int realId = currentSurfaceMesh->GetPointData()->GetScalars()->GetTuple1(iD);

            regionData->SetTuple1(realId, i+1);

        }

    }


    outputMesh->GetPointData()->SetScalars(regionData);


    return true;

}

std::string ConvertVTKMeshToAbaqusMeshStringPython(std::string inputMesh,  std::string partName, std::string materialName)
{
    //load the vtk  mesh
    vtkSmartPointer<vtkUnstructuredGridReader> reader =
        vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(inputMesh.c_str());
    reader->Update();
    std::string output = ConvertVTKMeshToAbaqusMeshString( reader->GetOutput(),   partName,  materialName);
    return output;

}

std::string ConvertVTKMeshToAbaqusMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName, std::string materialName)
{
    std::stringstream out;
    //write Header
    out << "*HEADING\n"
        << "**  \n"
        <<	 "**  ABAQUS Input Deck Generated by MediAssist FEM Plugin \n"
        <<	 "** \n";

    //part name
    out << "*Part, name="<<partName<<"-Part\n";

    //nodes
    out << "*Node \n";
    double* currentPoint;

    for(int i=0; i<inputMesh->GetNumberOfPoints(); i++)
    {
        currentPoint = inputMesh->GetPoint(i);
        out<<i+1<<", "<<currentPoint[0]<<" , "<<currentPoint[1]<<" , "<<currentPoint[2]<<"\n";
    }

    //elements
    out << "*Element, type=";
    vtkIdType* currentCellPoints;
    vtkIdType numberOfNodesPerElement;
    vtkIdType cellType = inputMesh->GetCellType(0);

    if(cellType == 24)
    {
        out<<"C3D10\n";
        numberOfNodesPerElement = 10;
        //currentCellPoints = new double[10];
    }

    else
    {
        out<<"C3D4\n";
        numberOfNodesPerElement = 4;
        // currentCellPoints = new double[4];
    }

    for(int i=0; i<inputMesh->GetNumberOfCells(); i++)
    {
        inputMesh->GetCellPoints(i, numberOfNodesPerElement,currentCellPoints);
        out<<i+1;

        for(int j=0; j<numberOfNodesPerElement; j++)
        {
            out<<" ,"<<currentCellPoints[j]+1;
        }

        out<<"\n";
    }

    ////////////////////
    out<<"*Elset, elset=SolidSectionSet, internal, generate\n";
    out<<"  1,  "<<inputMesh->GetNumberOfCells()<<",     1\n";
    out<<"** Section: "<<partName<<"-Section\n";
    out<<"*Solid Section, elset=SolidSectionSet, material="<<materialName<<"\n";

    ////////////////////////////

    //end part
    out<<"*End Part\n";

    return out.str();
}

std::string ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile)
{
    std::cout<< " Converting vtkPolydata "<<infile.c_str()<<" to vtkUnstructuredGrid "<<outfile.c_str()<<"\n";
    bool result = ConvertVTKPolydataToUnstructuredGrid(infile.c_str(), outfile.c_str());
    return outfile;
}

bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile )
{
    vtkSmartPointer<vtkPolyDataReader> reader =
        vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile);
    reader->Update();
    vtkPolyData* currentPolydata = reader->GetOutput();

    //load surface model to solid
    vtkSmartPointer<vtkUnstructuredGrid> mesh =
        vtkSmartPointer<vtkUnstructuredGrid>::New();

    //	vtkSmartPointer<vtkPolyData> mesh =
    //	 vtkSmartPointer<vtkPolyData>::New();

    bool returnValue = ConvertVTKPolydataToUnstructuredGrid(currentPolydata ,  mesh);

    //write output
    vtkSmartPointer<vtkUnstructuredGridWriter> writer =
        vtkSmartPointer<vtkUnstructuredGridWriter>::New();
    writer->SetFileName(outfile);
    writer->SetFileTypeToBinary();
    __SetInput(writer, mesh);
    writer->Write();

    return returnValue;
}

bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh)
{

    // Combine the two data sets
    vtkSmartPointer<vtkAppendFilter> appendFilter =
        vtkSmartPointer<vtkAppendFilter>::New();

    __AddInput(appendFilter, inputPolyData);

    appendFilter->Update();

    outputMesh->DeepCopy(appendFilter->GetOutput());

    return true;

}

std::string ProjectSurfaceMeshPython(std::string infile, std::string outfile, std::string referenceMesh)
{
    std::cout<< " Projecting surface mesh "<<infile.c_str()<<" to "<<referenceMesh<<" and writing results to "<<outfile<<"\n";
    bool result = ProjectSurfaceMesh(infile.c_str(), outfile.c_str(), referenceMesh.c_str());
    return outfile;
}


bool ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh )
{
    vtkSmartPointer<vtkPolyDataReader> reader =
        vtkSmartPointer<vtkPolyDataReader>::New();
    reader->SetFileName(infile);
    reader->Update();
    vtkPolyData* currentGrid = reader->GetOutput();

    //load surface model to solid
    vtkPolyDataReader* readerSTL = vtkPolyDataReader::New();
    readerSTL->SetFileName(referenceMesh);
    readerSTL->Update();

    vtkPolyData* reference = readerSTL->GetOutput();

    //	vtkSmartPointer<vtkPolyData> mesh =
    //	 vtkSmartPointer<vtkPolyData>::New();

    ProjectSurfaceMesh(currentGrid,  reference);

    //write output
    vtkSmartPointer<vtkPolyDataWriter> writer =
        vtkSmartPointer<vtkPolyDataWriter>::New();
    writer->SetFileName(outfile);
    writer->SetFileTypeToBinary();
    __SetInput(writer,currentGrid);
    writer->Write();

    return true;
}

bool ProjectSurfaceMesh(vtkPolyData* inputMesh,  vtkPolyData* referenceMesh )
{
	std::cout<<"Start surface projection\n";

//	outputMesh->BuildCells();
	//
	//first add a point data id to each point
	vtkPoints* thePoints = inputMesh->GetPoints();
	vtkIdType numberOfPoints = inputMesh->GetNumberOfPoints();



	//prepare octree data structure for reference mesh
	referenceMesh->BuildCells();
    vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
    cellLocatorRef->SetDataSet ( referenceMesh);
    cellLocatorRef->BuildLocator();


	//iterate over all surface point

    double currentPoint[3];
    double currentClosestPoint[3];
    double currentDisplacement[3];
    vtkSmartPointer<vtkGenericCell> currentTriangle = vtkSmartPointer<vtkGenericCell>::New();
    currentTriangle->SetCellTypeToTriangle();
    vtkIdType currentCellId;
    int currentSubId;
    double currentDistance;



	for(int i=0; i<numberOfPoints; i++)
	{
		thePoints->GetPoint ( i, currentPoint );


        cellLocatorRef->FindClosestPoint ( currentPoint, currentClosestPoint,
                                           currentTriangle, currentCellId,currentSubId,currentDistance );


        thePoints->SetPoint(i, currentClosestPoint[0], currentClosestPoint[1], currentClosestPoint[2]);
	}




    return true;
}

std::string VoxelizeSurfaceMeshPython(std::string infile, std::string outfile, int resolution, const char* referenceCoordinateGrid, bool multipleInputMesh)
{
    if (multipleInputMesh)
    {
        return VoxelizeMultipleSurfaceMesh(infile.c_str(), outfile.c_str(), resolution, referenceCoordinateGrid);
    }

    else
    {
        VoxelizeSurfaceMesh(infile.c_str(), outfile.c_str(), resolution, referenceCoordinateGrid);
        return outfile;
    }

}

std::string VoxelizeMultipleSurfaceMesh(const char* infile, const char* outfile, int resolution, const char* referenceCoordinateGrid)
{
    vector<pair<int, string> >* allRefs = IOHelper::getAllFilesOfSeries(infile);
    string currenOutputFile;
    boost::filesystem::path aPath(outfile);

    for (int i=0; i<allRefs->size(); i++)
    {
        boost::filesystem::path curentPath = aPath.parent_path() / (aPath.filename().stem().string() + boost::lexical_cast<string>(allRefs->at(i).first) + aPath.extension().string());
        currenOutputFile = curentPath.string();
        cout << "Generating Voxel image " << currenOutputFile << std::endl;
        VoxelizeSurfaceMesh(allRefs->at(i).second.c_str(), currenOutputFile.c_str(), resolution, referenceCoordinateGrid);
    }

    return currenOutputFile;
}

bool VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution, const char* referenceCoordinateGrid)
{
    std::cout<<"Creating image from surface mesh (voxelization)...";
    std::cout<<"Resolution of the longest bound is "<<resolution<<"\n";
    vtkSmartPointer<vtkPolyData> inputMesh = IOHelper::VTKReadPolyData(infile);

    vtkSmartPointer<vtkImageData> outputImage =
        vtkSmartPointer<vtkImageData>::New();

    bool result = VoxelizeSurfaceMesh(inputMesh, outputImage, resolution, referenceCoordinateGrid);

    vtkSmartPointer<vtkStructuredPointsWriter> writer =
        vtkSmartPointer<vtkStructuredPointsWriter>::New();
    writer->SetFileName(outfile);
    __SetInput(writer, outputImage);
    writer->Write();

    //	vtkSmartPointer<vtkPNGWriter> writer2 =
    //	 vtkSmartPointer<vtkPNGWriter>::New();
    //	writer2->SetFilePrefix(outfile);
    //	writer2->SetInput(outputImage);
    //	writer2->Write();

    return true;
}

bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int resolution, const char* referenceCoordinateGrid)
{
    vtkSmartPointer<vtkImageData> whiteImage = vtkSmartPointer<vtkImageData>::New();

    //Method A: Generate bounds, spacing and origine based on mesh:
    if (resolution>0)
    {
      double bounds[6];
      double spacingArray[3]; // desired volume spacing
      double origin[3];
      int dim[3];
      double spacing = -1;
      //find longest bound
      double longestBoundValue = 0;
      inputMesh->GetBounds(bounds);
      for (int i = 0; i < 3; i++)
      {
          double currentValue = (bounds[i * 2 + 1] - bounds[i * 2]);

          if(currentValue>longestBoundValue)
          {
              longestBoundValue = currentValue;
              spacing = currentValue / (double)resolution;
          }
      }    
         
      spacingArray[0] = spacing;
      spacingArray[1] = spacing;
      spacingArray[2] = spacing;
      std::cout<<"Longest bound is "<<longestBoundValue<<"\n";
      std::cout<<"Spacing is "<<spacing<<"\n";

      // compute dimensions 
      for (int i = 0; i < 3; i++)
      {
          dim[i] = static_cast<int>(ceil((bounds[i * 2 + 1] - bounds[i * 2]) / spacing));
      }
      //Compute origin
      origin[0] = bounds[0] + spacing / 2;
      origin[1] = bounds[2] + spacing / 2;
      origin[2] = bounds[4] + spacing / 2;
      
      whiteImage->SetSpacing(spacingArray);
      whiteImage->SetDimensions(dim);
      whiteImage->SetExtent(0, dim[0] - 1, 0, dim[1] - 1, 0, dim[2] - 1);
      whiteImage->SetOrigin(origin);
    }

    //Method B: Get bounds, spacing and origin from given grid:
    else
    {
      vtkSmartPointer<vtkImageData> referenceImage =  IOHelper::VTKReadImage(referenceCoordinateGrid);
      whiteImage->SetDimensions(referenceImage->GetDimensions());
      whiteImage->SetOrigin(referenceImage->GetOrigin());
      whiteImage->SetSpacing(referenceImage->GetSpacing());
    }

#if VTK_MAJOR_VERSION <= 5
    whiteImage->SetScalarTypeToUnsignedChar();
    whiteImage->AllocateScalars();
#else
    whiteImage->AllocateScalars(VTK_UNSIGNED_CHAR,3);
    // 3 could be wrong, no   image->SetNumberOfScalarComponents(3); found /Weigl
#endif



    //detect holes
    vtkSmartPointer<vtkFeatureEdges> featureEdges =
        vtkSmartPointer<vtkFeatureEdges>::New();

    featureEdges->FeatureEdgesOff();
    featureEdges->BoundaryEdgesOn();
    featureEdges->NonManifoldEdgesOn();
    __SetInput(featureEdges, inputMesh);
    featureEdges->Update();
    int num_open_edges = featureEdges->GetOutput()->GetNumberOfCells();

    if(num_open_edges)
    {
        double holeSize = 1e20;//bounds[1]-bounds[0];
        std::cout<<"Number of holes is "<<num_open_edges<<", trying to close with hole filler and size of "<< holeSize<<"\n";

        //fill holes
        vtkSmartPointer<vtkFillHolesFilter> fillHolesFilter =
            vtkSmartPointer<vtkFillHolesFilter>::New();

        __SetInput(fillHolesFilter, inputMesh);

        fillHolesFilter->SetHoleSize(holeSize);;

        vtkSmartPointer<vtkCleanPolyData> cleanFilter =
            vtkSmartPointer<vtkCleanPolyData>::New();

        __SetInput(cleanFilter, fillHolesFilter->GetOutput());
        cleanFilter->Update();

        //test again
        __SetInput(featureEdges, fillHolesFilter->GetOutput());
        featureEdges->Update();
        num_open_edges = featureEdges->GetOutput()->GetNumberOfCells();
        std::cout<<"Number of holes ofter filling is "<<num_open_edges<<"\n";

        //replace inputMesh with cleaned data
        inputMesh->DeepCopy(cleanFilter->GetOutput());

    }
    std::cout<<"Performing voxelization (this might take while)...\n";
    // fill the image with foreground voxels:
    unsigned char inval = 255;
    unsigned char outval = 0;
    vtkIdType count = whiteImage->GetNumberOfPoints();

    for (vtkIdType i = 0; i < count; ++i)
    {
        whiteImage->GetPointData()->GetScalars()->SetTuple1(i, inval);
    }

    // polygonal data --> image stencil:
    vtkSmartPointer<vtkPolyDataToImageStencil> pol2stenc =
        vtkSmartPointer<vtkPolyDataToImageStencil>::New();

    __SetInput(pol2stenc, inputMesh);


    pol2stenc->SetOutputOrigin(whiteImage->GetOrigin());
    pol2stenc->SetOutputSpacing(whiteImage->GetSpacing());
    pol2stenc->SetOutputWholeExtent(whiteImage->GetExtent());
    pol2stenc->Update();

    // cut the corresponding white image and set the background:
    vtkSmartPointer<vtkImageStencil> imgstenc =
        vtkSmartPointer<vtkImageStencil>::New();

    __SetInput(imgstenc, whiteImage);
    __SetStencil(imgstenc,pol2stenc->GetOutput());

    imgstenc->ReverseStencilOff();
    imgstenc->SetBackgroundValue(outval);
    imgstenc->Update();

    outputImage->DeepCopy(imgstenc->GetOutput());

    return true;
}

//boost::python::list ExtractPointPositionsPython( boost::python::list indices, std::string infile)
//{
//	unsigned int indicesSize = boost::python::len(indices);
//	std::vector<int> c_indices;
//	for(int i=0; i<indicesSize; i++)
//	{
//		unsigned int currentIndex = boost::python::extract<int>(indices[i]);
//		c_indices.push_back(currentIndex);
//		std::cout<<"Current index "<<currentIndex;
//	}
//
//	std::vector<double> pointPositions = ExtractPointPositions( c_indices, infile.c_str());
//	boost::python::list positionsPython;
//
//	for(int i=0; i< pointPositions.size();i++)
//	{
//		positionsPython.append(pointPositions[i]);
//	}
//
//
//}

std::vector<double> ExtractPointPositions( std::vector<int> indices, const char* infile)
{
    vtkSmartPointer<vtkUnstructuredGridReader> reader =
        vtkSmartPointer<vtkUnstructuredGridReader>::New();
    reader->SetFileName(infile);
    reader->Update();


    return ExtractPointPositions(indices ,reader->GetOutput());
}

std::vector<double> ExtractPointPositions( std::vector<int> indices, vtkUnstructuredGrid* inputMesh)
{
    std::vector<double> outputPositions;

    vtkPoints* thePoints = inputMesh->GetPoints();
    double currentPoint[3];

    for(int i=0; i<indices.size(); i++)
    {
        thePoints->GetPoint(indices[i],currentPoint);
        outputPositions.push_back(currentPoint[0]);
        outputPositions.push_back(currentPoint[1]);
        outputPositions.push_back(currentPoint[2]);

    }

    return outputPositions;

}

LIBRARY_API  bool ConvertLinearToQuadraticTetrahedralMesh(std::string infile, std::string outfile)
{

	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	 vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(infile.c_str());
	reader->Update();

	//deep copy
	vtkUnstructuredGrid* inputMesh = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGrid> outputMesh =
	 vtkSmartPointer<vtkUnstructuredGrid>::New();

	ConvertLinearToQuadraticTetrahedralMesh(inputMesh, outputMesh);


	vtkSmartPointer<vtkUnstructuredGridWriter> writer =
	 vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	writer->SetFileName(outfile.c_str());
#if VTK_MAJOR_VERSION <= 5
	writer->SetInput(outputMesh);
#else
	writer->SetInputData(outputMesh);
#endif
	writer->Write();

	return true;
}

LIBRARY_API  bool ConvertLinearToQuadraticTetrahedralMesh( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh)
{


	//get cells
    vtkPoints* thePoints = inputMesh->GetPoints();
    vtkCellArray* theCells = inputMesh->GetCells();
    vtkIdType numberOfPoints = inputMesh->GetNumberOfPoints();
    vtkIdType numberOfCells = inputMesh->GetNumberOfCells();


    //set of pairs that are already mapped
    typedef std::pair<unsigned int, unsigned int> PairType;
    typedef std::map< PairType, unsigned int > MapType;
    typedef std::pair< PairType, unsigned int > MapPairType;
    MapType pointMap;

    std::vector<PairType> edgeDefs;
    edgeDefs.push_back(std::make_pair(0,1));
    edgeDefs.push_back(std::make_pair(1,2));
    edgeDefs.push_back(std::make_pair(2,0));
    edgeDefs.push_back(std::make_pair(0,3));
    edgeDefs.push_back(std::make_pair(3,1));
    edgeDefs.push_back(std::make_pair(3,2));

    double currentVTKPoint[3];
    double currentVTKPoint1[3];
    double currentVTKPoint2[3];

	vtkSmartPointer<vtkPoints> newPoints =
	 vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkCellArray> newCells =
	 vtkSmartPointer<vtkCellArray>::New();




    for(unsigned int i=0; i<numberOfCells; i++) // iterate over all triangles
    {

        vtkSmartPointer<vtkIdList> cellPointIds =
            vtkSmartPointer<vtkIdList>::New();

        vtkSmartPointer<vtkIdList> newCellPointIds =
            vtkSmartPointer<vtkIdList>::New();

        inputMesh->GetCellPoints(i, cellPointIds);

        for(unsigned int j=0; j<4;j++) //original points
        {
        	unsigned int pointId = cellPointIds->GetId(j);
        	PairType currentPair = std::make_pair(pointId, pointId);

        	MapType::iterator it=pointMap.find(currentPair);

        	unsigned int currentId;

        	if(it != pointMap.end())
        	{
        		currentId = it->second;
        	}
        	else
        	{
				thePoints->GetPoint(pointId, currentVTKPoint);
				currentId = newPoints->InsertNextPoint(currentVTKPoint[0], currentVTKPoint[1], currentVTKPoint[2]);

				pointMap.insert(std::make_pair(currentPair, currentId));
        	}

        	newCellPointIds->InsertNextId(currentId);
        }


        for(unsigned int j=4; j<10;j++) //original points
        {
        	unsigned int pointId1 = cellPointIds->GetId(edgeDefs[j-4].first);
        	unsigned int pointId2 = cellPointIds->GetId(edgeDefs[j-4].second);
        	PairType currentPair = std::make_pair( pointId1, pointId2);
        	PairType currentPair2 = std::make_pair( pointId2, pointId1);

        	MapType::iterator it1=pointMap.find(currentPair);
        	MapType::iterator it2=pointMap.find(currentPair2);

        	unsigned int currentId;

        	if(it1 != pointMap.end() || it2 != pointMap.end())
        	{
        		if(it1 != pointMap.end())
        			currentId = it1->second;
        		else
        			currentId = it2->second;
        	}
        	else
        	{

				thePoints->GetPoint(pointId1, currentVTKPoint1);
				thePoints->GetPoint(pointId2, currentVTKPoint2);

				currentVTKPoint[0] = (currentVTKPoint1[0] + currentVTKPoint2[0])/2;
				currentVTKPoint[1] = (currentVTKPoint1[1] + currentVTKPoint2[1])/2;
				currentVTKPoint[2] = (currentVTKPoint1[2] + currentVTKPoint2[2])/2;

				currentId = newPoints->InsertNextPoint(currentVTKPoint[0], currentVTKPoint[1], currentVTKPoint[2]);
				pointMap.insert(std::make_pair(currentPair, currentId));

        	}


        	newCellPointIds->InsertNextId(currentId);
        }

        newCells->InsertNextCell(newCellPointIds);

    }


    outputMesh->SetPoints(newPoints);
    outputMesh->SetCells(VTK_QUADRATIC_TETRA, newCells);



	return true;
}

LIBRARY_API  bool ProjectSurfaceMesh(std::string inputVolumeMeshFile, std::string outputMeshFile, std::string referenceMeshFile)
{

	vtkSmartPointer<vtkPolyDataReader> reader =
	 vtkSmartPointer<vtkPolyDataReader>::New();
	reader->SetFileName(referenceMeshFile.c_str());
	reader->Update();

	//deep copy
	vtkPolyData* referenceMesh = reader->GetOutput();

	vtkSmartPointer<vtkUnstructuredGridReader> reader2 =
	 vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader2->SetFileName(inputVolumeMeshFile.c_str());
	reader2->Update();

	//deep copy
	vtkUnstructuredGrid* inputMesh = reader2->GetOutput();

	vtkSmartPointer<vtkUnstructuredGrid> outputMesh =
	 vtkSmartPointer<vtkUnstructuredGrid>::New();

	ProjectSurfaceMesh(inputMesh, outputMesh, referenceMesh);


	vtkSmartPointer<vtkUnstructuredGridWriter> writer =
	 vtkSmartPointer<vtkUnstructuredGridWriter>::New();
	writer->SetFileName(outputMeshFile.c_str());
	#if VTK_MAJOR_VERSION <= 5
		writer->SetInput(outputMesh);
	#else
		writer->SetInputData(outputMesh);
	#endif
	writer->Write();


	return true;
}

LIBRARY_API  bool ProjectSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, vtkPolyData* referenceMesh)
{

	std::cout<<"Start surface projection\n";
	outputMesh->DeepCopy(inputMesh);

	std::cout<<"deep copy finished\n";

//	outputMesh->BuildCells();
	//
	//first add a point data id to each point
	vtkPoints* thePoints = outputMesh->GetPoints();
	vtkCellArray* theCells = outputMesh->GetCells();
	vtkIdType numberOfPoints = outputMesh->GetNumberOfPoints();
	vtkIdType numberOfCells = outputMesh->GetNumberOfCells();

	vtkSmartPointer<vtkLongLongArray> pointIds =
	  vtkSmartPointer<vtkLongLongArray>::New();
	pointIds->SetNumberOfComponents(1);
	pointIds->SetName("pointIds");

	vtkSmartPointer<vtkLongLongArray> regionIds =
	  vtkSmartPointer<vtkLongLongArray>::New();
	regionIds->SetNumberOfComponents(1);
	regionIds->SetName("regionIds");

	vtkSmartPointer<vtkDoubleArray> displacements =
	  vtkSmartPointer<vtkDoubleArray>::New();
	displacements->SetNumberOfComponents(3);
	displacements->SetName("displacements");

	std::cout<<"filling tuples\n";

	for(unsigned int i=0; i<numberOfPoints;i++) // iterate over all triangles
	{
		pointIds->InsertNextTuple1(i);
		regionIds->InsertNextTuple1(0);

		displacements->InsertNextTuple3(0,0,0);
	}

	outputMesh->GetPointData()->SetGlobalIds(pointIds);


	//extract the surface
	vtkSmartPointer<vtkUnstructuredGridGeometryFilter> geom =
		vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
	
	__SetInput(geom, outputMesh);
	
	geom->PassThroughPointIdsOn();
	geom->SetOriginalPointIdsName("pointIds");
	geom->Update();




	//prepare octree data structure for reference mesh
	referenceMesh->BuildCells();
    vtkSmartPointer<vtkCellLocator> cellLocatorRef = vtkSmartPointer<vtkCellLocator>::New();
    cellLocatorRef->SetDataSet ( referenceMesh);
    cellLocatorRef->BuildLocator();




	//iterate over all surface point
	vtkUnstructuredGrid* surfaceGrid = geom->GetOutput();
	vtkPoints* thePointsSurface = surfaceGrid->GetPoints();
	vtkIdType numberOfPointsSurface = thePointsSurface->GetNumberOfPoints();
	vtkLongLongArray* realPointIds = (vtkLongLongArray*)surfaceGrid->GetPointData()->GetGlobalIds("pointIds");

    double currentPoint[3];
    double currentClosestPoint[3];
    double currentDisplacement[3];
    vtkSmartPointer<vtkGenericCell> currentTriangle = vtkSmartPointer<vtkGenericCell>::New();
    currentTriangle->SetCellTypeToTriangle();
    vtkIdType currentCellId;
    int currentSubId;
    double currentDistance;



	for(int i=0; i<numberOfPointsSurface; i++)
	{
		thePointsSurface->GetPoint ( i, currentPoint );


        cellLocatorRef->FindClosestPoint ( currentPoint, currentClosestPoint,
                                           currentTriangle, currentCellId,currentSubId,currentDistance );


        unsigned int realPointId = realPointIds->GetTuple1(i);

        thePoints->SetPoint(realPointId,  currentClosestPoint[0],currentClosestPoint[1],currentClosestPoint[2] );

        currentDisplacement[0] = currentClosestPoint[0] - currentPoint[0];
        currentDisplacement[1] = currentClosestPoint[1] - currentPoint[1];
        currentDisplacement[2] = currentClosestPoint[2] - currentPoint[2];

        displacements->SetTuple3(realPointId, currentDisplacement[0],currentDisplacement[1],currentDisplacement[2]);
        regionIds->SetTuple1(realPointId, 1);
	}

	outputMesh->GetPointData()->SetScalars(regionIds);
	outputMesh->GetPointData()->SetVectors(displacements);








	return true;
}

std::vector<unsigned int> ExtractNodeSet(std::string inputVolumeMeshFile, std::string nodeSetName)
{
	vtkSmartPointer<vtkUnstructuredGridReader> reader =
	 vtkSmartPointer<vtkUnstructuredGridReader>::New();
	reader->SetFileName(inputVolumeMeshFile.c_str());
	reader->Update();

	//deep copy
	vtkUnstructuredGrid* inputMesh = reader->GetOutput();


	std::vector<unsigned int> result = ExtractNodeSet(inputMesh, nodeSetName);

	return result;

}

std::vector<unsigned int> ExtractNodeSet( vtkUnstructuredGrid* inputMeshFile, std::string nodeSetName)
{


	std::vector<unsigned int> idList;

	if(inputMeshFile->GetPointData()->HasArray(nodeSetName.c_str()))
	{
		vtkDataArray* nodeSet = inputMeshFile->GetPointData()->GetScalars(nodeSetName.c_str());

		unsigned int numberOfNodes = nodeSet->GetNumberOfTuples();

		for(int i=0; i<numberOfNodes; i++)
		{
			unsigned int myType = (unsigned int) nodeSet->GetTuple1(i);

			if(myType)
			{
				idList.push_back(i);
			}
		}

		return idList;
	}
	else
	{
		std::cout<<"Node set with name "<<nodeSetName<<" was not found\n";
		return idList;
	}


}

std::vector<double> ExtractVectorField(std::string inputVolumeMeshFile,  std::string vectorFieldName, std::vector<unsigned int> nodeList)
{

		vtkSmartPointer<vtkUnstructuredGridReader> reader =
		 vtkSmartPointer<vtkUnstructuredGridReader>::New();
		reader->SetFileName(inputVolumeMeshFile.c_str());
		reader->Update();

		//deep copy
		vtkUnstructuredGrid* inputMesh = reader->GetOutput();


		std::vector<double> result = ExtractVectorField(inputMesh, vectorFieldName, nodeList);

		return result;

}

std::vector<double> ExtractVectorField( vtkUnstructuredGrid* inputMeshFile,  std::string vectorFieldName, std::vector<unsigned int> nodeList)
{
	std::vector<double> vectorField;

	if(inputMeshFile->GetPointData()->HasArray(vectorFieldName.c_str()))
	{
		vtkDataArray* vectorFieldArray = inputMeshFile->GetPointData()->GetVectors(vectorFieldName.c_str());
		unsigned int numberOfNodes = nodeList.size();
		unsigned int numberOfFieldValues = vectorFieldArray->GetNumberOfTuples();

		if(numberOfNodes> numberOfFieldValues)
		{
			std::cout<<"Indices list and vector field does not match\n";
			return vectorField;
		}

		double currentDisplacement[3];

		for(int i=0; i<numberOfNodes; i++)
		{
			vectorFieldArray->GetTuple(nodeList[i], currentDisplacement);
			vectorField.push_back( currentDisplacement[0] );
			vectorField.push_back( currentDisplacement[1] );
			vectorField.push_back( currentDisplacement[2] );
		}

		return vectorField;
	}
	else
	{
		std::cout<<"Vector field with name "<<vectorFieldName<<" was not found\n";
		return vectorField;
	}

}

}//end namepace MiscMeshOperators
}//end namepace MSML
