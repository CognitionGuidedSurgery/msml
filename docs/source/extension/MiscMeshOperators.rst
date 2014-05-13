IndexRegionOperators
====================


.. cpp:namespace:: MSML::IndexRegionOperators

.. cpp:function:: vector\<unsigned int> computeIndicesFromBoxROI(string filename, vector\<double> box, string type)

    :param string filename:
    :param vector\<double> box:
    :param string type:

    :returns:
    :rtype:




.. cpp:function:: vector\<unsigned int> computeIndicesFromMaterialId(string filename, int id, string type)

    :param string filename:
    :param int id:
    :param string type:

    :returns:
    :rtype:


MiscMeshOperators
==================

.. cpp:namespace:: MSML::MiscMeshOperators


.. cpp:function:: std::string ConvertSTLToVTKPython(std::string infile, std::string outfile)

    :param std::string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertSTLToVTK(const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertSTLToVTK(const char* infile, vtkPolyData* outputMesh)

    :param const char* infile:
    :param vtkPolyData* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKToSTLPython(std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKToSTL(const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKToOFF(vtkPolyData* inputMesh, const char* outfile)

    :param vtkPolyData* inputMesh:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertInpToVTK(const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertInpToVTK(const char* infile, vtkUnstructuredGrid* outputMesh)

    :param const char* infile:
    :param vtkUnstructuredGrid* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKToVTUPython(std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool        ConvertVTKToVTU(const char* infile, const char* outfile )

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool VTKToInp( const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool VTKToInp( vtkUnstructuredGrid* inputMesh, const char* outfile)

    :param vtkUnstructuredGrid* inputMesh:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: std::string ExtractSurfaceMeshPython( std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ExtractSurfaceMesh( const char* infile, const char* outfile)

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ExtractSurfaceMesh( vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)

    :param vtkUnstructuredGrid* inputMesh:
    :param vtkPolyData* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string ExtractAllSurfacesByMaterial( const char* infile, const char* outfile, bool theCutIntoPieces)

    :param const char* infile:
    :param const char* outfile:
    :param bool theCutIntoPieces:

    :returns:
    :rtype:




.. cpp:function:: std::map\<int,int>* createHist(vtkDataArray* theVtkDataArray)

    :param vtkDataArray* theVtkDataArray:

    :returns:
    :rtype:




.. cpp:function:: bool AssignSurfaceRegion( const char* infile, const char* outfile, std::vector\<std::string> regionMeshes )

    :param const char* infile:
    :param const char* outfile:
    :param std\:\:vector\<std::string> regionMeshes:

    :returns:
    :rtype:




.. cpp:function:: bool AssignSurfaceRegion( vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* outputMesh, std::vector\<vtkSmartPointer\<vtkPolyData> > & regionMeshes)

    :param vtkUnstructuredGrid* inputMesh:
    :param vtkUnstructuredGrid* outputMesh:
    :param std\:\:vector\<vtkSmartPointer\<vtkPolyData> > & regionMeshes:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKMeshToAbaqusMeshString( vtkUnstructuredGrid* inputMesh,  std::string partName, std::string materialName)

    :param vtkUnstructuredGrid* inputMesh:
    :param std\:\:string partName:
    :param std\:\:string materialName:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKMeshToAbaqusMeshStringPython(std::string inputMesh,  std::string partName, std::string materialName)

    :param std\:\:string inputMesh:
    :param std\:\:string partName:
    :param std\:\:string materialName:

    :returns:
    :rtype:




.. cpp:function:: std::string ProjectSurfaceMeshPython(std::string infile, std::string outfile, std::string referenceMesh)

    :param std\:\:string infile:
    :param std\:\:string outfile:
    :param std\:\:string referenceMesh:

    :returns:
    :rtype:




.. cpp:function:: bool ProjectSurfaceMesh(const char* infile, const char* outfile, const char* referenceMesh )

    :param const char* infile:
    :param const char* outfile:
    :param const char* referenceMesh:

    :returns:
    :rtype:




.. cpp:function:: bool ProjectSurfaceMesh(vtkPolyData* inputMesh, vtkPolyData* referenceMesh)

    :param vtkPolyData* inputMesh:
    :param vtkPolyData* referenceMesh:

    :returns:
    :rtype:




.. cpp:function:: std::string VoxelizeSurfaceMeshPython(std::string infile, std::string outfile, int resolution)

    :param std\:\:string infile:
    :param std\:\:string outfile:
    :param int resolution:

    :returns:
    :rtype:




.. cpp:function:: bool VoxelizeSurfaceMesh(const char* infile, const char* outfile, int resolution)

    :param const char* infile:
    :param const char* outfile:
    :param int resolution:

    :returns:
    :rtype:




.. cpp:function:: bool VoxelizeSurfaceMesh(vtkPolyData* inputMesh, vtkImageData* outputImage, int spacing)

    :param vtkPolyData* inputMesh:
    :param vtkImageData* outputImage:
    :param int spacing:

    :returns:
    :rtype:




.. cpp:function:: std::string ConvertVTKPolydataToUnstructuredGridPython(std::string infile, std::string outfile)

    :param std\:\:string infile:
    :param std\:\:string outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKPolydataToUnstructuredGrid(const char* infile, const char* outfile )

    :param const char* infile:
    :param const char* outfile:

    :returns:
    :rtype:




.. cpp:function:: bool ConvertVTKPolydataToUnstructuredGrid(vtkPolyData* inputPolyData, vtkUnstructuredGrid* outputMesh)

    :param vtkPolyData* inputPolyData:
    :param vtkUnstructuredGrid* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: std::vector\<double> ExtractPointPositions( std::vector\<int> indices, const char* infile)

    :param std\:\:vector\<int> indices:
    :param const char* infile:

    :returns:
    :rtype:




.. cpp:function:: std::vector\<double> ExtractPointPositions( std::vector\<int> indices, vtkUnstructuredGrid* inputMesh)

    :param std\:\:vector\<int> indices:
    :param vtkUnstructuredGrid* inputMesh:

    :returns:
    :rtype:


IOHelper
========

.. cpp:namespace:: MSML::IOHelper

.. cpp:function:: vtkSmartPointer\<vtkImageData> VTKReadImage(const char* filename)

    :param const char* filename:

    :returns:
    :rtype:




.. cpp:function:: vtkSmartPointer\<vtkUnstructuredGrid> VTKReadUnstructuredGrid(const char* filename)

    :param const char* filename:

    :returns:
    :rtype:




.. cpp:function:: vtkSmartPointer\<vtkPolyData> VTKReadPolyData(const char* filename)

    :param const char* filename:

    :returns:
    :rtype:


Post Processing
===============

.. cpp:function:: void ColorMesh(const char* modelFilename, const char* coloredModelFilename)

    :param  const char* modelFilename:
    :param  const char* coloredModelFilename:

    :returns:
    :rtype:




.. cpp:function:: void ColorMesh(vtkUnstructuredGrid* inputMesh, vtkPolyData* outputMesh)

    :param  vtkUnstructuredGrid* inputMesh:
    :param  vtkPolyData* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: void CompareMeshes(double& errorRMS, double& errorMax, const char* referenceFilename, const char* testFilename, bool surfaceOnly)

    :param  double& errorRMS:
    :param  double& errorMax:
    :param  const char* referenceFilename:
    :param  const char* testFilename:
    :param  bool surfaceOnly:

    :returns:
    :rtype:




.. cpp:function:: void CompareMeshes(double& errorRMS, double& errorMax, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly)

    :param  double& errorRMS:
    :param  double& errorMax:
    :param  vtkUnstructuredGrid* referenceMesh:
    :param  vtkUnstructuredGrid* testMesh:
    :param  bool surfaceOnly:

    :returns:
    :rtype:




.. cpp:function:: void CompareMeshes(std::vector\<double>& errorVec, const char* referenceFilename, const char* testFilename, bool surfaceOnly)

    :param  std::vector\<double>& errorVec:
    :param  const char* referenceFilename:
    :param  const char* testFilename:
    :param  bool surfaceOnly:

    :returns:
    :rtype:




.. cpp:function:: void CompareMeshes(std::vector\<double>& errorVec, vtkUnstructuredGrid* referenceMesh, vtkUnstructuredGrid* testMesh, bool surfaceOnly)

    :param  std::vector\<double>& errorVec:
    :param  vtkUnstructuredGrid* referenceMesh:
    :param  vtkUnstructuredGrid* testMesh:
    :param  bool surfaceOnly:

    :returns:
    :rtype:




.. cpp:function:: void ColorMeshFromComparison(const char* modelFilename, const char* referenceFilename, const char* coloredModelFilename)

    :param  const char* modelFilename:
    :param  const char* referenceFilename:
    :param  const char* coloredModelFilename:

    :returns:
    :rtype:




.. cpp:function:: void ColorMeshFromComparison(vtkUnstructuredGrid* inputMesh, vtkUnstructuredGrid* referenceMesh,vtkUnstructuredGrid* coloredMesh)

    :param  vtkUnstructuredGrid* inputMesh:
    :param  vtkUnstructuredGrid* referenceMesh:
    :param  vtkUnstructuredGrid* coloredMesh:

    :returns:
    :rtype:




.. cpp:function:: void MergeMeshes(vtkUnstructuredGrid* pointsMesh, vtkUnstructuredGrid* cellsMesh, vtkUnstructuredGrid* outputMesh)

    :param  vtkUnstructuredGrid* pointsMesh:
    :param  vtkUnstructuredGrid* cellsMesh:
    :param  vtkUnstructuredGrid* outputMesh:

    :returns:
    :rtype:




.. cpp:function:: void MergeMeshes(const char* pointsMeshFilename, const char* cellsMeshFilename, const char* outputMeshFilename)

    :param  const char* pointsMeshFilename:
    :param  const char* cellsMeshFilename:
    :param  const char* outputMeshFilename:

    :returns:
    :rtype:




.. cpp:function:: std::string GenerateDVFPython(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename, bool multipleReferenceGrids)

    :param  const char* referenceGridFilename:
    :param  const char* outputDVFFilename:
    :param  const char* deformedGridFilename:
    :param  bool multipleReferenceGrids:

    :returns:
    :rtype:




.. cpp:function:: void GenerateDVF(const char* referenceGridFilename, const char* outputDVFFilename, const char* deformedGridFilename)

    :param  const char* referenceGridFilename:
    :param  const char* outputDVFFilename:
    :param  const char* deformedGridFilename:

    :returns:
    :rtype:




.. cpp:function:: void GenerateDVF(vtkUnstructuredGrid* referenceGrid, vtkImageData* outputDVF, vtkUnstructuredGrid* deformedGrid)

    :param  vtkUnstructuredGrid* referenceGrid:
    :param  vtkImageData* outputDVF:
    :param  vtkUnstructuredGrid* deformedGrid:

    :returns:
    :rtype:




.. cpp:function:: std::string ApplyDVFPython(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool multipleDVF, bool reverseDirection)

    :param  const char* referenceImage:
    :param  const char* outputDeformedImage:
    :param  const char* DVF:
    :param  bool multipleDVF:
    :param  bool reverseDirection:

    :returns:
    :rtype:




.. cpp:function:: void ApplyDVF(const char* referenceImage, const char* outputDeformedImage, const char* DVF, bool reverseDirection)

    :param  const char* referenceImage:
    :param  const char* outputDeformedImage:
    :param  const char* DVF:
    :param  bool reverseDirection:

    :returns:
    :rtype:




.. cpp:function:: void ApplyDVF(vtkImageData* refImage, vtkImageData* outputDefImage, vtkImageData* dvf, bool reverseDirection)

    :param  vtkImageData* refImage:
    :param  vtkImageData* outputDefImage:
    :param  vtkImageData* dvf:
    :param  bool reverseDirection:

    :returns:
    :rtype:


MappingOperators
================


.. cpp:function:: std::string MapMeshPython ( std::string meshIni, std::string meshDeformed, std::string meshToMap, std::string mappedMesh )

                :param std\:\:string meshIni:
                :param std\:\:string meshDeformed:
                :param std\:\:string meshToMap:
                :param std\:\:string mappedMesh:

                :rtype:
                :returns:


.. cpp:function:: bool MapMesh ( const char* meshIni, const char* meshDeformed, const char* meshToMap, const char* mappedMesh )

                :param const char* meshIni:
                :param const char* meshDeformed:
                :param const char* meshToMap:
                :param const char* mappedMesh:

                :rtype:
                :returns:


.. cpp:function:: bool MapMesh ( vtkUnstructuredGrid* meshIni,vtkUnstructuredGrid* meshDeformed, vtkUnstructuredGrid* meshToMap, vtkUnstructuredGrid* mappedMesh )

                :param vtkUnstructuredGrid* meshIni:
                :param vtkUnstructuredGrid* meshDeformed:
                :param vtkUnstructuredGrid* meshToMap:
                :param vtkUnstructuredGrid* mappedMesh:

                :rtype:
                :returns:
