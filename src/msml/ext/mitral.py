# -*- encoding: utf-8 -*-

"""
mitral.py contains miscellaneous operators for pre- and post-processing of 
mitral valve geometries into simulation input;
currently specifically for the HiFlow3Exporter-derived MitralExporter.
"""
__author__ = 'schoch', 'weigl'
__date__ = "2015-04-12"

import xml.etree.ElementTree as ET

import numpy as np
import vtk
from .msmlvtk import *
from msml.log import debug
import glob


def geometry_analyzer(surface, ring, target="mvGeometryInfo.txt"):
    """
    Given the 3D volume mesh of a mitral valve, this script computes
    - the bounds of bounding box,
    - the center of the bounding box,
    - the point in the middle of the top plane of the bounding box  (!!!)
    - the average 'radius' of the top plane of the bounding box     (!!!)
    for an automated setup of the HiFlow3-based MVR-Simulation.

    :param surface:
    :param ring:
    :param target:
    :return:

    .. note::   3dvolumeMesh.vtu is called uGrid here.

    .. authors:
        * Nicolai Schoch, EMCL; 2015-04-12.
        * Alexander Weigl, KIT; 2015-04-19
    """

    debug("=== Execute Python script to analyze MV geometry in order for the HiFlow3-based MVR-Simulation ===")

    # ======================================================================
    # read in files: -------------------------------------------------------
    # read in 3d valve mesh OR 3d ring mesh
    vtureader = vtk.vtkXMLPolyDataReader()  # read vtp-Ring
    vtureader.SetFileName(ring)
    vtureader.Update()
    uGrid = vtureader.GetOutput()

    # ======================================================================
    # compute bounding box, etc. -------------------------------------------
    # methods can be found in vtkDataSet

    # Get the center of the bounding box.
    center = np.zeros(3)
    uGrid.GetCenter(center)
    # Return a pointer to the geometry bounding box
    # (notation: [xmin,xmax, ymin,ymax, zmin,zmax].)
    bounds = np.zeros(6)
    uGrid.GetBounds(bounds)
    # compute point in the middle of top plane; raised by 0.5 * z-length of bounding box.
    midPtTop = np.zeros(3)
    midPtTop[0] = center[0]
    midPtTop[1] = center[1]
    midPtTop[2] = bounds[5] + 0.5 * (bounds[5] - bounds[4])
    # compute the average 'radius' of the top plane of the bounding box
    # compute x/y-distance-from-mid-to-border
    xDist = midPtTop[0] - bounds[0]
    yDist = midPtTop[1] - bounds[2]
    # compute average of x/y-distance-from-mid-to-border (corresponds to annulus radius)
    avDist = (xDist + yDist) / 2.0
    annulusRadius = avDist

    debug("MV geometry analysis: DONE.")

    if target is not None:
        with open(target, 'w') as f:
            # produce outputAnalytics string and write into file
            f.write("midPtTop:(%s,%s,%s);\nannulusRadius:%s" % (
                midPtTop[0], midPtTop[1], midPtTop[2], annulusRadius))

            debug("Write file %s", target)

    return [midPtTop[0], midPtTop[1], midPtTop[2], annulusRadius]


def bcdata_producer(volume_mesh, surface_mesh, ring, target="mvDirBCdataInfo.txt"): # before: ring, annulus_point_ids=16, target="mvBCdataInfo.txt"):
    """Given the following input data w.r.t. a mitral valve setup:
     - a 3D volume mesh (vtu),
     - a 2D surface mesh representation of the MV segmentation including vertex IDs (vtp),
     - an Annuloplasty Ring representation including (the same/corresponding) vertex IDs (vtp)
     this script computes and sets the Dirichlet Boundary Conditions (BCs) data
     for the HiFlow3-based MVR-Simulation.

    .. note:: Adding additional BC-points by means of linear interpolation
              requires the input IDs to be ordered and going around annulus once!!!
    
    .. note:: The vertex IDs on annulus and ring have the following meanings and encodings:
         0 - Anterolaterale Kommissur
         1 -3  Kontrollpunkt
         4 - Sattelhorn
         5 - 7 Kontrollpunkt
         8 - Posteromediale Kommissur
         9 - 11 Kontrollpunkt
         12 - Posterior Annulus
         13 - 15 Kontrollpunkt
         16  - sonstige Annuluspunkte (zwischen den Kontrollpunkten)
         (die IDs 0 - 15 werden im Uhrzeigersinn am Annulus gesetzt)
         17 - Anteriores Segel
         18 - Posteriores Segel

    .. authors::
        * Nicolai Schoch, Fabian Kissler, EMCL; 2015-04-12.

    :param volume_mesh:
    :param surface_mesh:
    :param ring:
    :param annulus_point_ids: DEPRECATED.
    :return: DBC-points and DBC-displacements.
    """

    # ======================================================================
    debug("=== Execute Python script to produce BCdata (Dirichlet BCs) for the  HiFlow3-based MVR-Simulation ===")

    valve3d_ = read_ugrid(volume_mesh)
    valve3dSurface_ = get_surface(valve3d_)

    # read in 2d valve
    valve2d_ = read_polydata(surface_mesh)

    # read in ring
    ring_ = read_polydata(ring)

    # get vertex ids of valve2d_ and ring_
    valve2dVertexIds_ = valve2d_.GetPointData().GetArray('VertexIDs')
    ringVertexIds_ = ring_.GetPointData().GetArray('VertexIDs')

    debug("Reading input files: DONE.")

    # ======================================================================
    # init. tree for closest point search ----------------------------------

    kDTree = vtk.vtkKdTreePointLocator()
    kDTree.SetDataSet(valve3dSurface_)
    kDTree.BuildLocator()
    
    # define number of given annulus point IDs -----------------------------
    # (see notation/representation of Annuloplasty Rings by DKFZ and corresponding addInfo)
    number_annulus_point_ids = 16

    # ======================================================================
    # arrays for storage of coordinates of annulus points (and interpolated points) on the MV surface and on the ring -----------------
    ringPoints_ = np.zeros((2 * number_annulus_point_ids, 3))
    valvePoints_ = np.zeros((2 * number_annulus_point_ids, 3))

    # Store coordiantes in arrays ---------------------------------------------------------------------------
    # NOTE: Alternatively, instead of a loop over all points and looking for their IDs,
    # one could also loop over the array of vertexIDs and get the pointID.
    # find coordinates of points of ring_
    for i in range(ring_.GetNumberOfPoints()):
        pos = int(ringVertexIds_.GetTuple1(i))
        if 0 <= pos < number_annulus_point_ids:
            ringPoints_[pos] = np.array(ring_.GetPoint(i))

    # find coordinates of points of valve2d_
    for i in range(valve2d_.GetNumberOfPoints()):
        pos = int(valve2dVertexIds_.GetTuple1(i))
        if 0 <= pos < number_annulus_point_ids:
            valvePoints_[pos] = np.array(valve2d_.GetPoint(i))

    # find closest points to points stored in valvePoints_ on valve3dSurface_ and store (i.e. overwrite) them in valvePoints_
    for i in range(number_annulus_point_ids):
        iD = kDTree.FindClosestPoint(valvePoints_[i])
        kDTree.GetDataSet().GetPoint(iD, valvePoints_[i])

    # ======================================================================
    # add additional boundary conditions by linear interpolation -------------------------------------------
    # NOTE: this requires the IDs to be ordered and going around annulus once!!!
    for i in range(number_annulus_point_ids):
        valve_point = 0.5 * (valvePoints_[i] + valvePoints_[(i + 1) % number_annulus_point_ids])
        valvePoints_[number_annulus_point_ids + i] = valve_point

        ring_point = 0.5 * (ringPoints_[i] + ringPoints_[(i + 1) % number_annulus_point_ids])
        ringPoints_[number_annulus_point_ids + i] = ring_point

    # ======================================================================
    # Compute displacements ------------------------------------------------
    displacement_ = ringPoints_ - valvePoints_
    
    # ======================================================================
    # write 'displacement lines' -------------------------------------------
    # (from the sewing points on the natural annulus to the artificial ring)
    f = open('aBCdataProducer_annuloplastyDisplacementLines.inp', 'w')
    
    # write inp-format-header-line
    s = str(valvePoints_.shape[0]+ringPoints_.shape[0]) + ' ' + str(displacement_.shape[0]) + ' 0 0 0\n'
    f.write(s)
    
    # write point coordinates
    # first, write valve points
    for i in range(valvePoints_.shape[0]):
        pt = valvePoints_[i]
        s = str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'
        f.write(s)
    
    # then, second, write ring points
    for i in range(valvePoints_.shape[0], valvePoints_.shape[0]+ringPoints_.shape[0]):
        pt = ringPoints_[i-valvePoints_.shape[0]]
        s = str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'
        f.write(s)
    
    # write "lines" into inp file
    for i in range(displacement_.shape[0]):
        s = '0' + ' ' + '10' + ' line ' + str(i) + ' ' + str(i+valvePoints_.shape[0]) + '\n'
        f.write(s)
    
    # close stream
    f.close()
    
    debug("Writing Visualization-Output for Testing BCdata-Producer-Operator into file: aBCdataProducer_annuloplastyDisplacementLines.inp .")

    # ======================================================================
    # Transform points and displacements for HiFlow3-Exporter --------------
    flatten = lambda l: [item for sublist in l
                         for item in sublist]

    points = flatten(valvePoints_)
    displacements = flatten(displacement_)

    debug("Computing Dirichlet displacement BC data.")

    # ======================================================================
    # convert arrays to strings --------------------------------------------
    valvePointString_ = ""
    displacementString_ = ""
    for i in range(2 * number_annulus_point_ids):
        for j in range(3):
            valvePointString_ += str(valvePoints_[i][j])
            displacementString_ += str(displacement_[i][j])
            if j == 2:
                if i < 2 * number_annulus_point_ids - 1:
                    valvePointString_ += ";"
                    displacementString_ += ";"
            else:
                valvePointString_ += ","
                displacementString_ += ","

    # ======================================================================
    # Write BC data to XML file --------------------------------------------
    # build a tree structure
    root = ET.Element("Param")
    BCData = ET.SubElement(root, "BCData")
    DisplacementConstraintsBCs = ET.SubElement(BCData, "DisplacementConstraintsBCs")

    numberOfDPoints = ET.SubElement(DisplacementConstraintsBCs, "NumberOfDisplacedDirichletPoints")
    numberOfDPoints.text = str(2 * number_annulus_point_ids)

    dDPoints = ET.SubElement(DisplacementConstraintsBCs, "dDPoints")
    dDPoints.text = valvePointString_

    dDisplacements = ET.SubElement(DisplacementConstraintsBCs, "dDisplacements")
    dDisplacements.text = displacementString_

    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    tree.write(target)

    # ======================================================================

    debug("Writing mvrSimDirBCdata.xml output file")

    return points, displacements


def bcdata_extender(volume_mesh, surface_mesh, target="mvNeumBCdataInfo.txt"): # before: intNumNeumPoints=16, floatDeltaZ=15.0):
    """Given the following input data w.r.t. a mitral valve setup:
     - a 3D volume mesh (vtu),
     - a 2D surface mesh representation of the MV segmentation including vertex IDs (vtp),
     this script computes and sets the pointwise Neumann Boundary Conditions (BCs) data
     representing the mitral valve apparatus chordae's pull forces
     for the HiFlow3-based MVR-Simulation.
     --> Neumann-BCs-Producer-Script to set Chordae Attachment Points and corresponding Forces on the MV leaflets.

    .. note:: ...
    
    .. authors::
        * Nicolai Schoch, EMCL; 2015-06-10.

    :param volume_mesh:
        a 3D unstructured grid (vtu file) representation of the MV segmentation (e.g. by CGAL meshing operator,
        followed by vtk2vtu-Converter), which only contains the connectivity information of 3D cells with four vertices
        (i.e. tetrahedrons) and no other cells of dimension different from three,
    :type volume_mesh: vtk.vtkUnstructuredGrid

    :param surface_mesh:
        a 2D polydata surface representation of the MV segmentation, which additionally contains matID-information
        on the MV leaflets and annulus points.
    :type surface_mesh: vtk.vtkPolyData

    :param BCDataXMLFilename: DEPRECATED. -> Default value: target="mvNeumBCdataInfo.txt"
           Name of the BCData file containing the von Neumann BCs;

    :param intNumNeumPoints: DEPRECATED. -> Default value: 16
           Number of von Neumann BCData points (representing the Chordae-attachment-points on the leaflets);

    :param floatDeltaZ: DEPRECATED. -> Default value: 15.0
           for specifying the direction of Neumann force, 
           i.e., this number will be subtracted from the z-coordinate of the center of the bottom of the bounding box of the valve;

    :return: (NBC-points and NBC-forces).
    """

    # =====================================================================
    debug("=== Execute Python script to extend BCdata (Neumann BCs) for the  HiFlow3-based MVR-Simulation ===")
    
    # get flexible MV-anatomy parameters (which are fixed as from then on): -------
    numberOfNeumannPoints = 16
    deltaZ = 15.0
    
    # get input mesh and surface  data: -------------------------------------------
    # we have: volume_mesh, surface_mesh, target="mvNeumBCdataInfo.txt" (where target corresponds to XMLFileName);
    
    # read in 3d valve volume_mesh
    valve3D_ = read_ugrid(volume_mesh)
    valve3Dsurface_ = get_surface(valve3D_)

    # read in 2d valve surface mesh
    valve2Dsurface_ = read_polydata(surface_mesh)
    # compute normals of valve2Dsurface_
    normalsFilter = vtk.vtkPolyDataNormals()
    if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
      normalsFilter.SetInputData(valve2Dsurface_)
    else:
      normalsFilter.SetInput(valve2Dsurface_)
    normalsFilter.SplittingOn()
    normalsFilter.ConsistencyOn()
    normalsFilter.ComputePointNormalsOff() # adapt here.
    normalsFilter.ComputeCellNormalsOn()
    normalsFilter.FlipNormalsOff()
    normalsFilter.NonManifoldTraversalOn()
    normalsFilter.Update()
    # get cell normals
    normalsValve2DsurfaceRetrieved = normalsFilter.GetOutput().GetCellData().GetNormals() # adapt here.
    
    debug("Reading input files: DONE.")

    # ======================================================================
    # init. cell locator for closest cell search ----------------------
    # (using vtk methods, that find the closest point in a grid for an arbitrary point in R^3)
    cellLocator = vtk.vtkCellLocator()
    cellLocator.SetDataSet(valve2Dsurface_)
    cellLocator.BuildLocator()
    
    
    # -------------------------------------------------------
    # Find the cells on the lower side of the valve's surface
    # -------------------------------------------------------
    
    plane = vtk.vtkPlane()
    
    lowerSideCells = [] # will contain ids of cells on the lower side of the surface
    upLowCellList = [] # the length of this array will be the number of cells on the surface. If a cell is on the upper side, the corresponding entry is 1, otherwise it is 0.
    
    # iterate over the cells on the surface
    for i in range(valve3Dsurface_.GetNumberOfCells()):
        
        cell = valve3Dsurface_.GetCell(i) # get the current cell
        
        upLowIndicator = 0 # if a cell's vertex is on the upper side then add 1 otherwise add -1. After the following iteration, if the indicator is negative the cell will be classified as a cell on the lower side, otherwise it will be classified as a cell on the upper side. Note that here it's important that the cells on the surface have an odd number of vertices.
        
        # iterate over the cell's vertices
        for j in range(cell.GetNumberOfPoints()):
            
            pointId = cell.GetPointId(j) # get a vertex id of the current cell
            point = valve3Dsurface_.GetPoint(pointId) # get the coordinates of the vertex
            
            closestPoint = [0., 0., 0.] # will contain coordinates of a closest point on valve2d
            closestPointDist2 = vtk.mutable(0) # will contain the squared Euclidean distance from point to closestPoint
            cellId = vtk.mutable(0) # will contain ID of a cell that contains closestPoint
            subId = vtk.mutable(0) # only needed for the function, besides that it has no use
            cellLocator.FindClosestPoint(point, closestPoint, cellId, subId, closestPointDist2) # find a closest point and a cell that contains that point
            
            cellNormal = [0., 0., 0.] # will be normal of cell with id cellId (defined above)
            normalsValve2DsurfaceRetrieved.GetTuple(cellId, cellNormal) # get the normal
            
            # modify upLowIndicator w.r.t. the point's position
            if plane.Evaluate(cellNormal, closestPoint, point) > 0.:
              upLowIndicator += 1
            else:
              upLowIndicator -= 1
        # update list
        if upLowIndicator < 0:
          lowerSideCells.append(i)
          upLowCellList.append(0)
        else:
          upLowCellList.append(1)
    
    debug("Finding cells on lower side of MV mesh: DONE.")
    
    
    # -----------------------------------------------------------------------------------------------------------------
    # Find the cells on the boundary of the surface, i.e., cells on the lower side neighboring a cell on the upper side
    # -----------------------------------------------------------------------------------------------------------------
    
    # list of cell ids on boundary
    boundaryCells = []
    
    # loop over all cells on downside
    for cellId in lowerSideCells:
        
        # get the point ids of the cell's vertices
        cellPointIds = vtk.vtkIdList()
        valve3Dsurface_.GetCellPoints(cellId, cellPointIds)
        
        # neighbours will contain ids of cells that share a vertex with current cell
        neighbours = []
        
        # loop over the cell's vertices
        for i in range(cellPointIds.GetNumberOfIds()):
            
            # list with the id of a vertex
            idList = vtk.vtkIdList()
            idList.InsertNextId(cellPointIds.GetId(i))
            
            # get the neighbours of the cell
            neighbourCellIds = vtk.vtkIdList()
            valve3Dsurface_.GetCellNeighbors(cellId, idList, neighbourCellIds)
            
            # write the neighbours' ids in a list
            for j in range(neighbourCellIds.GetNumberOfIds()):
                neighbours.append(int(neighbourCellIds.GetId(j)))
        
        # check if current cell has neighbour cells on upside
        for neighbour in neighbours:
            if upLowCellList[neighbour] != 0:
              boundaryCells.append(cellId)
              break
    
    
    # list with length number of cells; entry is
    # 0 if cell is not a boundary cell
    # 1 otherwise
    isOnBoundary = [0 for i in range(valve3Dsurface_.GetNumberOfCells())]
    
    for iD in boundaryCells:
        isOnBoundary[iD] = 1
    
    debug("Finding cells on boundary of surface (i.e. where upper side meets lower side): DONE.")
    
    
    # now we have the following arrays
    # 1. boundaryCells, contains ids of cells on the boundary
    # 2. isOnBoundary, has 0, 1 entries, 1 for cell is on boundary, 0 otherwise
    
    
    # ------------------------------------------------------------------------------------------------------------------------------------
    # Find a cell on the previously found boundary that has a vertex with a minimal z-coordinate among all cell's vertices on the boundary
    # ------------------------------------------------------------------------------------------------------------------------------------
    
    # iterate through boundaryCells, to find cell that has a vertex with minimal z-coordinate
    # save this id as minCellId
    # initial data for the search
    cellPointIds = vtk.vtkIdList()
    valve3Dsurface_.GetCellPoints(boundaryCells[0], cellPointIds)
    
    pt = valve3Dsurface_.GetPoint(cellPointIds.GetId(0))
    
    currentZCoord = pt[2]
    currentCellId = boundaryCells[0]
    
    for iD in boundaryCells:
        
        cellPointIds = vtk.vtkIdList()
        valve3Dsurface_.GetCellPoints(iD, cellPointIds)
        
        for i in range(cellPointIds.GetNumberOfIds()):
            pt = valve3Dsurface_.GetPoint(cellPointIds.GetId(i))
            if pt[2] < currentZCoord:
              currentZCoord = pt[2]
              currentCellId = iD
              break
        
    minCellId = currentCellId
    
    debug("Finding min-z-coord among all surface boundary cells: DONE.")
    
    # ------------------------------------------------------------------------------------
    # Find the connected component of the boundary that contains the previously found cell
    # ------------------------------------------------------------------------------------
    
    #### AUXILIARY FUNCTION: isElementOfList ...
    
    # find connected component
    connectedComponent = []
    connectedComponent.append(minCellId)
    elementAdded = 1
    
    while elementAdded == 1:
        elementAdded = 0
        for i in range(len(connectedComponent)):
            # for every cell in connectedComponent find neighbour cells
            # get the point ids of the cell's vertices
            cellPointIds = vtk.vtkIdList()
            valve3Dsurface_.GetCellPoints(connectedComponent[i], cellPointIds)
            
            # neighbours will contain ids of cells that share a vertex with current cell
            neighbours = []
            
            # loop over the cell's vertices
            for j in range(cellPointIds.GetNumberOfIds()):
                
                # list with the id of a vertex
                idList = vtk.vtkIdList()
                idList.InsertNextId(cellPointIds.GetId(j))
                
                # get the neighbours of the cell
                neighbourCellIds = vtk.vtkIdList()
                valve3Dsurface_.GetCellNeighbors(cellId, idList, neighbourCellIds)
                
                # write the neighbours' ids in a list
                for k in range(neighbourCellIds.GetNumberOfIds()):
                    neighbours.append(int(neighbourCellIds.GetId(k)))
            
            for neighbour in neighbours:
                if isOnBoundary[neighbour] == 1 and isElementOfList(neighbour, connectedComponent) == 0:
                   connectedComponent.append(neighbour)
                   elementAdded = 1
    
    
    isOnConnectedComponent = [0 for i in range(valve3Dsurface_.GetNumberOfCells())]
    
    for iD in connectedComponent:
        isOnConnectedComponent[iD] = 1
    
    # Note: at this point, the whole lower boundary is found, by means of having iterated over (connected component) neighbours, starting at min-z-value.
    
    debug("Finding connected component: DONE.")
    
    
    # -----------------------------------------------------------------------------------------------------------------------------------------------------
    # Solve the k-center clustering problem for the set of points in the previously defined connected component with the Farthest-First Traversal algorithm
    # -----------------------------------------------------------------------------------------------------------------------------------------------------
    
    # Note: alternatively to the k-center-algorithm, try with 3D coordinates and 2D coordinates, i.e., projection on x-y-plane;
    
    # create vtkidlist with ids of points in the connected component
    pointsInComponent = vtk.vtkIdList()
    
    for iD in connectedComponent:
        # get points of cell iD
        cellPointIds = vtk.vtkIdList()
        valve3Dsurface_.GetCellPoints(iD, cellPointIds)
        
        # add those points to list pointsInComponent
        for j in range(cellPointIds.GetNumberOfIds()):
            pointsInComponent.InsertUniqueId(cellPointIds.GetId(j))
    
    
    #### AUXILIARY FUNCTION: findMaximalElement ...
    
    #### AUXILIARY FUNCTION: kCenterCluster ...
    
    
    myCenterSet = kCenterCluster(numberOfNeumannPoints, pointsInComponent, valve3Dsurface_)
    
    debug("Solving k-center clustering problem and finding k-center-Set: DONE.")
    
    
    # --------------------------------
    # write the center set to inp file
    # --------------------------------
    
    f = open('aBCdataExtender_chordaeAttachmentPoints.inp', 'w')
    
    # write inp-format-header-line
    s = str(myCenterSet.GetNumberOfIds()) + ' ' + str(myCenterSet.GetNumberOfIds()) + ' 0 0 0\n'
    f.write(s)
    
    # write point coordinates
    for i in range(myCenterSet.GetNumberOfIds()):
        pt = valve3Dsurface_.GetPoint(myCenterSet.GetId(i))
        s = str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'
        f.write(s)
    
    for i in range(myCenterSet.GetNumberOfIds()):
        s = '0' + ' ' + '10' + ' pt ' + str(i) + '\n'
        f.write(s)
    
    # close stream
    f.close()
    
    debug("Writing Visualization-Output for Testing BCdata-Extender-Operator into file: aBCdataExtender_chordaeAttachmentPoints.inp .")
    
    
    # ---------------------
    # find the bounding box
    # ---------------------
    
    # methods can be found in vtkDataSet
    
    # Get the center of the bounding box.
    center = np.zeros(3)
    valve3D_.GetCenter(center)
    # Return a pointer to the geometry bounding box in the form (xmin,xmax, ymin,ymax, zmin,zmax).
    bounds = np.zeros(6)
    valve3D_.GetBounds(bounds)
    
    # specify point in \R^3 to compute the direction of vNeumann force
    NeumannPoint = np.zeros(3)
    NeumannPoint[0] = center[0]
    NeumannPoint[1] = center[1]
    NeumannPoint[2] = bounds[4] # this component is z_min 
    NeumannPoint[2] -= deltaZ
    
    
    # store coordinates of von Neumann points in array nBCPoints
    nBCPoints = np.zeros((numberOfNeumannPoints, 3))
    
    for i in range(myCenterSet.GetNumberOfIds()):
        currentPoint = valve3Dsurface_.GetPoint(myCenterSet.GetId(i))
        nBCPoints[i] = currentPoint
    
    # store the direction of the von Neumann force in the array nBCDirection
    nBCDirection = np.zeros((numberOfNeumannPoints, 3))
    
    for i in range(numberOfNeumannPoints):
        nBCDirection[i] = NeumannPoint
    
    nBCDirection -= nBCPoints
    
    debug("Finding bounding box and setting up nBC-direction array: DONE.")
    
    
    # ======================================================================
    # Transform nBCPoints and nBCDirection for HiFlow3-Exporter --------------
    flatten = lambda l: [item for sublist in l
                         for item in sublist]

    points = flatten(nBCPoints)
    forces = flatten(nBCDirection)
    
    debug("Transforming nBCPoints and nBCDirection for HiFlow3-Exporter: DONE.")
    
    
    # ======================================================================
    # the coordinates of the Neumann points are stored in nBCPoints, and the 
    # distinguished point under the valve is called NeumannPoint;
    # allow for visualization of the Neumann-Force-Vectors (representing the Chordae):
    # therefore write lines from the 'Neumann points' to the point under the valve
    
    f = open('aBCdataExtender_chordaeDirectionLines.inp', 'w')
    
    # write first line
    s = str(numberOfNeumannPoints+1) + ' ' + str(numberOfNeumannPoints) + ' 0 0 0\n'
    f.write(s)
    
    # write point coordinates
    # first, write Neumann points on valve
    for i in range(numberOfNeumannPoints):
        pt = nBCPoints[i]
        s = str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'
        f.write(s)
    
    # then, write coordinates of point under the valve
    pt = NeumannPoint
    s = str(numberOfNeumannPoints) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'
    f.write(s)
    
    # write lines
    for i in range(numberOfNeumannPoints):
        s = '0' + ' ' + '10' + ' line ' + str(i) + ' ' + str(numberOfNeumannPoints) + '\n'
        f.write(s)
    
    # close stream
    f.close()
    
    debug("Writing Visualization-Output for Testing BCdata-Extender-Operator into file: aBCdataExtender_chordaeDirectionLines.inp .")
    
    
    # ======================================================================
    # Write XML-File
    
    # convert arrays to strings --------------------------------------------
    nBCPointsString = ""
    nBCDirectionString = ""
    for i in range(numberOfNeumannPoints):
        for j in range(3):
            nBCPointsString += str(nBCPoints[i][j])
            nBCDirectionString += str(nBCDirection[i][j])
            if j == 2:
              if i < numberOfNeumannPoints-1:
                nBCPointsString += ";"
                nBCDirectionString += ";"
            else:
              nBCPointsString += ","
              nBCDirectionString += ","
    
    
    # Write BC data to XML file --------------------------------------------
    # build a tree structure
    
    root = ET.Element("Param")
    BCData = ET.SubElement(root, "BCData")
    NeumannForceBCs = ET.SubElement(BCData, "NeumannForceBCs")
    
    NumberOfNeumannForceBCs = ET.SubElement(NeumannForceBCs, "NumberOfNeumannForceBCs")
    NumberOfNeumannForceBCs.text = str(numberOfNeumannPoints)
    
    nBCPoints = ET.SubElement(NeumannForceBCs, "nBCPoints")
    nBCPoints.text = nBCPointsString
    
    nBCForce_ScaleAndDirection = ET.SubElement(NeumannForceBCs, "nBCForce_ScaleAndDirection")
    nBCForce_ScaleAndDirection.text = nBCDirectionString
    
    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    tree.write(target)
    
    debug("Writing mvrSimNeumBCdata.xml output file")
    
    # ======================================================================
    
    return points, forces


def von_mises_stress_evaluator(path_to_sim_results, matParam_Lambda, matParam_Mu, target="SimResults_with_vMstressVis"):
    """
    .. explanations::
    This python script evaluates the von Mises stress distribution
    preferably for mitral valve leaflets tissue:
    
    The script needs the following input:
    - a (series of) vtu/pvtu file(s), which contains 3 scalar-valued arrays 
      named {'u0', 'u1', 'u2'} as PointData.
     
    Using the arrays specified above, the program computes the 
    displacement vector, the strain tensor and the von Mises stress 
    for material parameters \lambda={28466-40666-56933} and \mu={700-1000-1400}, 
    which corresponds to mitral valve leaflets tissue (according to [Mansi-2012]).
    Furthermore, the displacement vector will be added to the given 
    coordinates of the points.
     
    The output is the following:
     - a (series of) vtu file(s) that contains all the data of the
       original file, however with modified coordinates of the points and the 
       displacement vector as additional PointData and the strain tensor 
       along with the von Mises stress distribution as additional CellData.
    
    .. execution command::
        To run the script outside the MSML, call:
        $ python vMStress.py <path_to_(series_of)_inputfile(s)> <lambda> <mu>
    
    .. authors::
        * Nicolai Schoch, EMCL; 2015-06-26.

    :param path_to_sim_results: the path to the directory containing the HiFlow3 MVR simulation results (pvtu and vtu files).
    :param matParam_Lambda: Lame constant \lambda
    :param matParam_Mu: Lame constant \mu
    :param target: SimResults_with_vMstressVis
    :return: new set of files containing the HiFlow3 MVR simulation results (vtu files) including the von Mises Stress distribution data.
    """
    
    # ======================================================================
    debug("=== Execute Python script to evaluate the von Mises Stress distribution on the HiFlow3 MVR Simulation results. ===")
    
    # ======================================================================
    # Get path/directory of simulation results, and set path combined with datatype:
    path = path_to_sim_results
    path_and_datatype = path + '*.pvtu'
    
    # Get set of files to be processed by vMStress-Evaluator-Script:
    files_to_be_iterated_over = glob.glob(path_and_datatype)
    
    debug("The following list contains the files to be iterated over by the vonMisesStressEvaluator-Operator: %s", files_to_be_iterated_over)
    
    # Get material parameters:
    matParamMVtissue_Lambda = float(matParam_Lambda)
    matParamMVtissue_Mu = float(matParam_Mu)
    
    # ======================================================================
    # Iterate over all pvtu-files in SimResults-directory and evaluate vonMises-Stress:
    for i in range(0,len(files_to_be_iterated_over)):
        
        # Get path and name of inputfile:
        inputfilename = files_to_be_iterated_over[i]
        
        # Get path and name of outputfile:
        if inputfilename[-4] == 'p':
          outputfilename = inputfilename[:-5] + '_outVis.vtu'
        else:
          #outputfilename = 'outVis_' + inputfilename
          print ('ERROR: THIS CASE IS NOT ALLOWED! PLEASE PROVIDE PVTU-FILES INSTEAD OF VTU-FILES.')
        
        debug("  - vMstress-iteration: - current outputfilename: %s", outputfilename)
        
        # Read (p)vtu file
        if inputfilename[-4] == 'p':
          reader = vtk.vtkXMLPUnstructuredGridReader()
          reader.SetFileName(inputfilename)
          reader.Update()
        else:
          print ('ERROR: THIS CASE IS NOT ALLOWED! PLEASE PROVIDE PVTU-FILES.')
          reader = vtk.vtkXMLUnstructuredGridReader()
          reader.SetFileName(inputfilename)
          reader.Update()
        
        grid = reader.GetOutput()
        
        
        # Get point data arrays u0, u1 and u2
        u0 = grid.GetPointData().GetArray('u0')
        u1 = grid.GetPointData().GetArray('u1')
        u2 = grid.GetPointData().GetArray('u2')
        
        # Set scalars
        grid.GetPointData().SetScalars(u0)
        
        # Warp by scalar u0
        warpScalar = vtk.vtkWarpScalar()
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          warpScalar.SetInputData(grid)
        else:
          warpScalar.SetInput(grid)
        warpScalar.SetNormal(1.0,0.0,0.0)
        warpScalar.SetScaleFactor(1.0)
        warpScalar.SetUseNormal(1)
        warpScalar.Update()
        
        # Get output and set scalars
        grid = warpScalar.GetOutput()
        grid.GetPointData().SetScalars(u1)
        
        # Warp by scalar u1
        warpScalar = vtk.vtkWarpScalar()
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          warpScalar.SetInputData(grid)
        else:
          warpScalar.SetInput(grid)
        warpScalar.SetNormal(0.0,1.0,0.0)
        warpScalar.SetScaleFactor(1.0)
        warpScalar.SetUseNormal(1)
        warpScalar.Update()
        
        # Get output and set scalars
        grid = warpScalar.GetOutput()
        grid.GetPointData().SetScalars(u2)
        
        # Warp by scalar u2
        warpScalar = vtk.vtkWarpScalar()
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          warpScalar.SetInputData(grid)
        else:
          warpScalar.SetInput(grid)
        warpScalar.SetNormal(0.0,0.0,1.0)
        warpScalar.SetScaleFactor(1.0)
        warpScalar.SetUseNormal(1)
        warpScalar.Update()
        
        # Get ouput and add point data arrays that were deleted before
        grid = warpScalar.GetOutput()
        grid.GetPointData().AddArray(u0)
        grid.GetPointData().AddArray(u1)
        grid.GetPointData().AddArray(u2)
        
        debug("  - vMstress-iteration: - Warping of simulation results for current file: DONE.")
        
        # Compute displacement vector
        calc = vtk.vtkArrayCalculator()
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          calc.SetInputData(grid)
        else:
          calc.SetInput(grid)
        calc.SetAttributeModeToUsePointData()
        calc.AddScalarVariable('x', 'u0', 0)
        calc.AddScalarVariable('y', 'u1', 0)
        calc.AddScalarVariable('z', 'u2', 0)
        calc.SetFunction('x*iHat+y*jHat+z*kHat')
        calc.SetResultArrayName('DisplacementSolutionVector')
        calc.Update()
        
        
        # Compute strain tensor
        derivative = vtk.vtkCellDerivatives()
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          derivative.SetInputData(calc.GetOutput())
        else:
          derivative.SetInput(calc.GetOutput())
        derivative.SetTensorModeToComputeStrain()
        derivative.Update()
        
        
        # Compute von Mises stress
        calc = vtk.vtkArrayCalculator()
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          calc.SetInputData(derivative.GetOutput())
        else:
          calc.SetInput(derivative.GetOutput())
        calc.SetAttributeModeToUseCellData()
        calc.AddScalarVariable('Strain_0', 'Strain', 0)
        calc.AddScalarVariable('Strain_1', 'Strain', 1)
        calc.AddScalarVariable('Strain_2', 'Strain', 2)
        calc.AddScalarVariable('Strain_3', 'Strain', 3)
        calc.AddScalarVariable('Strain_4', 'Strain', 4)
        calc.AddScalarVariable('Strain_5', 'Strain', 5)
        calc.AddScalarVariable('Strain_6', 'Strain', 6)
        calc.AddScalarVariable('Strain_7', 'Strain', 7)
        calc.AddScalarVariable('Strain_8', 'Strain', 8)
        
        #calc.SetFunction('sqrt( (2*1400*Strain_0 + 56933*(Strain_0+Strain_4+Strain_8))^2 + (2*1400*Strain_4 + 56933*(Strain_0+Strain_4+Strain_8))^2 + (2*1400*Strain_8 + 56933*(Strain_0+Strain_4+Strain_8))^2 - ( (2*1400*Strain_0 + 56933*(Strain_0+Strain_4+Strain_8))*(2*1400*Strain_4 + 56933*(Strain_0+Strain_4+Strain_8)) ) - ( (2*1400*Strain_0 + 56933*(Strain_0+Strain_4+Strain_8))*(2*1400*Strain_8 + 56933*(Strain_0+Strain_4+Strain_8)) ) - ( (2*1400*Strain_4 + 56933*(Strain_0+Strain_4+Strain_8))*(2*1400*Strain_8 + 56933*(Strain_0+Strain_4+Strain_8)) ) + 3 * ((2*1400*Strain_3)^2 + (2*1400*Strain_6)^2 + (2*1400*Strain_7)^2) )') # DEPRECATED.
        vMstressFunction_string = 'sqrt( (2*' + matParamMVtissue_Mu_string + '*Strain_0 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8))^2 + (2*' + matParamMVtissue_Mu_string + '*Strain_4 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8))^2 + (2*' + matParamMVtissue_Mu_string + '*Strain_8 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8))^2 - ( (2*' + matParamMVtissue_Mu_string + '*Strain_0 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8))*(2*' + matParamMVtissue_Mu_string + '*Strain_4 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8)) ) - ( (2*' + matParamMVtissue_Mu_string + '*Strain_0 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8))*(2*' + matParamMVtissue_Mu_string + '*Strain_8 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8)) ) - ( (2*' + matParamMVtissue_Mu_string + '*Strain_4 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8))*(2*' + matParamMVtissue_Mu_string + '*Strain_8 + ' + matParamMVtissue_Lambda_string + '*(Strain_0+Strain_4+Strain_8)) ) + 3 * ((2*' + matParamMVtissue_Mu_string + '*Strain_3)^2 + (2*' + matParamMVtissue_Mu_string + '*Strain_6)^2 + (2*' + matParamMVtissue_Mu_string + '*Strain_7)^2) )'
        calc.SetFunction(vMstressFunction_string)
        
        #calc.SetResultArrayName('vonMisesStress_forMV_mu1400_lambda56933') # DEPRECATED.
        vMstressArrayName_string = 'vonMisesStress_forMV_lambda' + matParamMVtissue_Lambda_string + '_mu' + matParamMVtissue_Mu_string
        calc.SetResultArrayName(vMstressArrayName_string)
        
        calc.Update()
        
        grid = calc.GetOutput()
        
        debug("  - vMstress-iteration: - Computation of displacement vectors, Cauchy strain and vom Mises stress for current file: DONE.")
        
        # Write output to vtu
        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetDataModeToAscii()
        writer.SetFileName(outputfilename)
        if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
          writer.SetInputData(grid)
        else:
          writer.SetInput(grid)
        writer.Write()
        
        debug("  - vMstress-iteration: - Writing Extended VTU incl. von Mises Stress information for current file: DONE.")
        # ----------------------------------------------------------------------
    
    # ======================================================================
    debug("Von Mises Stress computation: DONE for all files.")
    
#    # ======================================================================
#    # Read file
#    polydata = read_polydata(volume_mesh)
#
#    # ======================================================================
#    # Compute displacement vector
#    calc = vtk.vtkArrayCalculator()
#    calc.SetInput(polydata)
#    calc.SetAttributeModeToUsePointData()
#    calc.AddScalarVariable('x', 'u0', 0)
#    calc.AddScalarVariable('y', 'u1', 0)
#    calc.AddScalarVariable('z', 'u2', 0)
#    calc.SetFunction('x*iHat+y*jHat+z*kHat')
#    calc.SetResultArrayName('DisplacementSolutionVector')
#    calc.Update()
#
#    # ======================================================================
#    # Compute strain tensor
#    derivative = vtk.vtkCellDerivatives()
#    derivative.SetInput(calc.GetOutput())
#    derivative.SetTensorModeToComputeStrain()
#    derivative.Update()
#
#    # ======================================================================
#    # Compute von Mises stress
#    calc = vtk.vtkArrayCalculator()
#    calc.SetInput(derivative.GetOutput())
#    calc.SetAttributeModeToUseCellData()
#    calc.AddScalarVariable('Strain_0', 'Strain', 0)
#    calc.AddScalarVariable('Strain_1', 'Strain', 1)
#    calc.AddScalarVariable('Strain_2', 'Strain', 2)
#    calc.AddScalarVariable('Strain_3', 'Strain', 3)
#    calc.AddScalarVariable('Strain_4', 'Strain', 4)
#    calc.AddScalarVariable('Strain_5', 'Strain', 5)
#    calc.AddScalarVariable('Strain_6', 'Strain', 6)
#    calc.AddScalarVariable('Strain_7', 'Strain', 7)
#    calc.AddScalarVariable('Strain_8', 'Strain', 8)
#    calc.SetFunction(
#        'sqrt( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))^2 + (2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8))^2 + (2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8))^2 - ( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8)) ) - ( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8)) ) - ( (2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8)) ) + 3 * ((2*700*Strain_3)^2 + (2*700*Strain_6)^2 + (2*700*Strain_7)^2) )')
#    calc.SetResultArrayName('vonMisesStress_forMV_mu700_lambda28466')
#    calc.Update()
#
#    debug("Computation of displacement vectors, Cauchy strain and vom Mises stress")
#
#    # ======================================================================
#    # Define dummy variable; get output of calc filter
#    dummy = calc.GetOutput()
#
#    # Get point data arrays u0, u1 and u2
#    pointData_u0 = dummy.GetPointData().GetArray('u0')
#    pointData_u1 = dummy.GetPointData().GetArray('u1')
#    pointData_u2 = dummy.GetPointData().GetArray('u2')
#
#    # Set scalars
#    dummy.GetPointData().SetScalars(pointData_u0)
#
#    # ======================================================================
#    # Warp by scalar u0
#    warpScalar = vtk.vtkWarpScalar()
#    warpScalar.SetInput(dummy)
#    warpScalar.SetNormal(1.0, 0.0, 0.0)
#    warpScalar.SetScaleFactor(1.0)
#    warpScalar.SetUseNormal(1)
#    warpScalar.Update()
#
#    # Get output and set scalars
#    dummy = warpScalar.GetOutput()
#    dummy.GetPointData().SetScalars(pointData_u1)
#
#    # ======================================================================
#    # Warp by scalar u1
#    warpScalar = vtk.vtkWarpScalar()
#    warpScalar.SetInput(dummy)
#    warpScalar.SetNormal(0.0, 1.0, 0.0)
#    warpScalar.SetScaleFactor(1.0)
#    warpScalar.SetUseNormal(1)
#    warpScalar.Update()
#
#    # Get output and set scalars
#    dummy = warpScalar.GetOutput()
#    dummy.GetPointData().SetScalars(pointData_u2)
#
#    # ======================================================================
#    # Warp by scalar u2
#    warpScalar = vtk.vtkWarpScalar()
#    warpScalar.SetInput(dummy)
#    warpScalar.SetNormal(0.0, 0.0, 1.0)
#    warpScalar.SetScaleFactor(1.0)
#    warpScalar.SetUseNormal(1)
#    warpScalar.Update()
#
#    # Get ouput and add point data arrays that got deleted earlier
#    dummy = warpScalar.GetOutput()
#    dummy.GetPointData().AddArray(pointData_u0)
#    dummy.GetPointData().AddArray(pointData_u1)
#
#    # ======================================================================
#    # Write output to vtu
#
#    write_vtu(dummy, target)
#
#    # ======================================================================
#    debug("Writing Extended VTU incl. von Mises Stress information")
    
    # ======================================================================
    debug("Von Mises Stress computation: DONE for all files.")
    # ======================================================================


def isElementOfList(a, myList):
    """auxiliary function for BCdataExtender.
    returns 1 if the integer a is an element of the list myList
    returns 0 otherwise
    """
    for elem in myList:
        if elem == a:
          return 1
    
    return 0


def findMaximalElement(myList):
    """auxiliary function for BCdataExtender.
    returns index of maximal element of myList
    """
    index = 0
    maxElement = myList[index]
    
    for i in range(len(myList)):
        if myList[i] > maxElement:
          maxElement = myList[i]
          index = i
    
    return index


def kCenterCluster(k, pointSet, polydata):
    """auxiliary function for BCdataExtender.
    implementation:
       k-center clustering algorithm:
       according to lecture notes of Prof. Schnoerr, HCI, IWR, Heidelberg University.
    input: 
       integer k, vtkIdList of point ids, polydata that contains the points
    output: 
       vtkIdList centerSet, 2-approximation to the solution of the k-center clustering problem using Euclidean distance
    """
    
    # init math object to compute distance of points
    math = vtk.vtkMath()
    
    # initialize center set 
    centerSet = vtk.vtkIdList()
    
    # pick an arbitrary point c_1 in pointSet and add c_1 to centerSet
    centerSet.InsertNextId(pointSet.GetId(0))
    
    # compute the distance of all points to the center set
    # init array that contains distance for each point in pointSet to the center set
    distanceToCenterSet = []
    
    for i in range(pointSet.GetNumberOfIds()):
        distanceToCenterSet.append(math.Distance2BetweenPoints(polydata.GetPoint(pointSet.GetId(i)), polydata.GetPoint(centerSet.GetId(0))))
    
    while int(centerSet.GetNumberOfIds()) < k:
        
        # find maximal element of list distanceToCenterSet
        # this is a new center
        newCenterIndex = findMaximalElement(distanceToCenterSet)
        
        # add the new center point to the center set
        newCenterId = pointSet.GetId(newCenterIndex)
        centerSet.InsertNextId(newCenterId)
        
        # update the list distanceToCenterSet
        for i in range(pointSet.GetNumberOfIds()):
            
            currentPointId = pointSet.GetId(i)
            currentDistance = math.Distance2BetweenPoints(polydata.GetPoint(newCenterId), polydata.GetPoint(currentPointId))
            
            if distanceToCenterSet[i] > currentDistance:
              distanceToCenterSet[i] = currentDistance
    
    return centerSet


def get_surface_normals(surface):
    """returns the normal vectors for a surface (DEPRECATED VTU-2-HF3-INP-MatID-Setter HELPER FUNCTION)

    :param surface:
    :type surface:
    :return:
    :rtype:
    """
    normals_surface = vtk.vtkPolyDataNormals()

    if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
        normals_surface.SetInputData(surface)
    else:
        normals_surface.SetInput(surface)

    normals_surface.SplittingOn()
    normals_surface.ConsistencyOn()  # such that on a surface the normals are oriented either 'all' outward OR 'all' inward.
    normals_surface.AutoOrientNormalsOn()  # such that normals point outward or inward.
    normals_surface.ComputePointNormalsOff()  # adapt here. On/Off.
    normals_surface.ComputeCellNormalsOn()  # adapt here.
    normals_surface.FlipNormalsOff()
    normals_surface.NonManifoldTraversalOn()
    normals_surface.Update()

    return normals_surface.GetOutput().GetCellData().GetNormals()  # adapt here.


def vtu_To_hf3inp_inc_MV_matIDs_Producer(volume_mesh, surface_mesh, target="mvHf3InpInfo.inp"):
    """Given `volume_mesh` and `surface_mesh` 
       this script produces a hf3-inp-file suitable for a HiFlow3-based MVR-simulation.

    The coordinates of the vertices, the connectivity information of the
    3D cells and 2D boundary faces will be written to the hf3-inp-file.
    The matIDs of the cells will be determined as follows:
    - every 3D cell gets the material id 10.
    - surface cells are subdivided into
      - upside surfaces on anterior leaflet: matID 17,
      - upside surfaces on posterior leaflet: matID 18,
      - downside surfaces: matID 20.


    .. documentation:: see documentation in EMCL-Preprint No.2015.2 (in progress).

    :param volume_mesh:
        a 3D unstructured grid (vtu file) representation of the MV segmentation (e.g. by CGAL meshing operator,
        followed by vtk2vtu-Converter), which only contains the connectivity information of 3D cells with four vertices
        (i.e. tetrahedrons) and no other cells of dimension different from three,

    :type volume_mesh: vtk.vtkUnstructuredGrid

    :param surface_mesh:
        a 2D polydata surface representation of the MV segmentation, which additionally contains matID-information
        on the MV leaflets and annulus points.

    :type surface_mesh: vtk.vtkPolyData

    :return: (facets, facet_matIDs, tets, tet_matIDs) # actually not correct yet...?!

     ..note::
        It is important that the surface cells (facets of boundary cells) in the vtu-file 
        have an odd number of vertices (i.e. are triangles contained in tetrahedra),
        and that the surface cells in the vtp-file have an odd number of vertices (i.e. are triangles).

    .. note::
        This version of the script uses HalfSpaces (as opposed to CellNormals or PointNormals, 
        which produced non-deterministic results, and hence required subsequent human assessment).

    .. note::
        In order to avoid 'blurry' matID-distribution around the interface between
        between the leaflets (near the commissure points),
            - either use MITK-remeshing results (2 separate leaflets and 1 complete MV inc IDs),
            - or possibly use some vtk filter "subdivision" to refine mesh "smoothing"...

    .. author::
            Nicolai Schoch, EMCL; 2015-04-12.
            Alexander Weigl, KIT; 2015-04-19.
            Nicolai Schoch, EMCL; 2015-05-05.
            Nicolai Schoch, EMCL; 2015-06-10.

    """

    # ======================================================================
    # Define matIDs --------------------------------------------------------
    ID_DOWN = 20
    ID_ANT = 17
    ID_POST = 18

    # ======================================================================
    # read in files: -------------------------------------------------------
    # read in 3d valve
    # NOTE: when using Cell/PointNormals-based script version, do ensure 
    # that the precedent meshing algorithm (CGAL or similar)
    # produces consistent/good results w.r.t. the 'normal glyphs'.

    valve3DvolumeMesh = read_ugrid(volume_mesh)

    # get surface mesh of valve3DvolumeMesh
    valve3Dsurface = get_surface(valve3DvolumeMesh)

    # get cell normals
    #normalsSurfaceRetrieved_ = get_surface_normals(valve3Dsurface) # not needed in HalfSpace-based script version.

    # read in 2d valve
    valve2Dsurface = read_polydata(surface_mesh)

    # get cell normals
    #normalsValve2DsurfaceRetrieved = get_surface_normals(valve2Dsurface) # by Alexander. WRONG.
    normalsFilter = vtk.vtkPolyDataNormals()
    if vtk.vtkVersion().GetVTKMajorVersion() >= 6:
        normalsFilter.SetInputData(valve2Dsurface)
    else:
        normalsFilter.SetInput(valve2Dsurface)
    normalsFilter.SplittingOn()
    normalsFilter.ConsistencyOn()  # such that on a surface the normals are oriented either 'all' outward OR 'all' inward.
    #normalsFilter.AutoOrientNormalsOn()  # such that normals point outward or inward. WRONG.
    normalsFilter.ComputePointNormalsOff() # adapt here.
    normalsFilter.ComputeCellNormalsOn() # adapt here.
    normalsFilter.FlipNormalsOff()
    normalsFilter.NonManifoldTraversalOn()
    normalsFilter.Update()
    
    normalsValve2DsurfaceRetrieved = normalsFilter.GetOutput().GetCellData().GetNormals() # adapt here.
    
    # ---------------------------------------------------------------------------
    # CLASSIFICATION OF CELLS W.R.T. UPPER AND LOWER SIDE OF THE VALVE'S SURFACE.
    # ---------------------------------------------------------------------------

    # ======================================================================
    # initialize cell locator for closest cell search ----------------------
    # (using vtk methods, that find the closest point in a grid for an arbitrary point in R^3)
    cellLocator = vtk.vtkCellLocator()
    cellLocator.SetDataSet(valve2Dsurface)
    cellLocator.BuildLocator()
    
    # init plane object
    plane = vtk.vtkPlane()
    
    # allocate memory for upLowCells with the following entries:
    # "1" if cell is on the upper side, and
    # "0" if cell is on the lower side.
    upLowCells = [0 for i in range(valve3Dsurface.GetNumberOfCells())]
    
    # find cells on upper and lower side of the valve's surface
    # iterate over the cells of the surface and compare normals
    for i in range(valve3Dsurface.GetNumberOfCells()):
        
        # get cellId of closest point
        cell = valve3Dsurface.GetCell(i) # get the current cell
        
        upLowIndicator = 0 # if a cell's vertex is on the upper side then add 1 otherwise add -1. After the following iteration, if the indicator is negative the cell will be classified as a cell on the lower side, otherwise it will be classified as a cell on the upper side.
        # NOTE: it is important that the cells on the surface have an odd number of vertices (i.e. are represented by triangle-facets of the tetrahedra in the vtu-file).
        
        # iterate over the cell's vertices
        for j in range(cell.GetNumberOfPoints()):
            pointId = cell.GetPointId(j) # get a vertex id of the current cell
            point = valve3Dsurface.GetPoint(pointId) # get the coordinates of the vertex
            
            closestPoint = [0., 0., 0.] # will contain coordinates of a closest point on valve2d
            closestPointDist2 = vtk.mutable(0) # will contain the squared Euclidean distance from point to closestPoint
            cellId = vtk.mutable(0) # will contain ID of a cell that contains closestPoint
            subId = vtk.mutable(0) # only needed for the function, besides that it has no use 
            cellLocator.FindClosestPoint(point, closestPoint, cellId, subId, closestPointDist2) # find a closest point and a cell that contains that point
            
            cellNormal = [0., 0., 0.] # will be normal of cell with id cellId (defined above)
            normalsValve2DsurfaceRetrieved.GetTuple(cellId, cellNormal) # get the normal
            
            # modify upLowIndicator w.r.t. the point's position
            if plane.Evaluate(cellNormal, closestPoint, point) > 0.:
              upLowIndicator += 1
            else:
              upLowIndicator -= 1
            
        # update list
        if upLowIndicator > 0:
          upLowCells[i] = 1

    # ---------------------------------------------------------------------------
    # CLASSIFICATION OF CELLS W.R.T. ANTERIOR AND POSTERIOR LEAFLET 
    # ON UPPER SIDE OF THE VALVE'S SURFACE.
    # ---------------------------------------------------------------------------

    # ======================================================================
    # initialize search tree:
    kDTree = vtk.vtkKdTreePointLocator()
    kDTree.SetDataSet(valve2Dsurface)
    kDTree.BuildLocator()

    valve2DsurfaceVertexIDs = valve2Dsurface.GetPointData().GetArray('VertexIDs')

    # allocate memory for upCellList (indicating if cell is on left/right side)
    upCellList = [i for i in range(valve3Dsurface.GetNumberOfCells()) if upLowCells[i]]
    
    # iterate over cells on the upper side of the leaflet surface, and set ids for anterior/posterior
    for i in upCellList:
        
        cell = valve3Dsurface.GetCell(i)
        
        antPostIndicator = 0 # if a cell's vertex is on the anterior side then add 1 otherwise add -1. After the following iteration, if the indicator is negative the cell will be classified as a cell on the posterior side, otherwise it will be classified as a cell on the anterior side.
        # NOTE: it is important that the cells on the surface have an odd number of vertices (i.e. are represented by triangles in the vtp-file).
        
        # iterate over the cell's vertices
        for j in range(cell.GetNumberOfPoints()):
            
            pointId = cell.GetPointId(j)
            point = valve3Dsurface.GetPoint(pointId)
            
            closestNPoints = vtk.vtkIdList() # will contain ids of the closest N points
            N = 1 # the 'N' from above
            pointNotClassified = True
            
            # iterate until point is classified
            while pointNotClassified:
              
              kDTree.FindClosestNPoints(N, point, closestNPoints)
              
              for k in range(closestNPoints.GetNumberOfIds()):
                closestPointId = closestNPoints.GetId(k)
                
                if int(valve2DsurfaceVertexIDs.GetTuple1(closestPointId)) == ID_ANT:
                  pointNotClassified = False
                  antPostIndicator += 1
                
                if int(valve2DsurfaceVertexIDs.GetTuple1(closestPointId)) == ID_POST:
                  pointNotClassified = False
                  antPostIndicator -= 1
              
              N += 1
        
        # update list upLowCells
        if antPostIndicator > 0:
          upLowCells[i] = 2 # "2" stands for 'cell is on anterior upper side'
        else:
          upLowCells[i] = 3 # "3" stands for 'cell is on posterior upper side'

    debug("Computing hf3-inp MV matID information: DONE.")

    # ======================================================================
    # region write results to inp file

    points = list() # WRONG! # This actually is facets !!!!!

    with  open(target, 'w') as f:
        # write first line
        f.write("%d %d 0 0 0\n" % (
            valve3DvolumeMesh.GetNumberOfPoints(),
            valve3Dsurface.GetNumberOfCells() + valve3DvolumeMesh.GetNumberOfCells()))

        # write point coordinates
        for i in range(valve3DvolumeMesh.GetNumberOfPoints()):
            pt = valve3DvolumeMesh.GetPoint(i)
            f.write(str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2])) # NEW BY NICO.
            # f.write(' '.join(str(pt)))                                             # changed by Alexander, but does not work? or does it?
            f.write("\n") # changed by Alexander # NEW BY NICO.
            # s = str(i) + ' ' + str(pt[0]) + ' ' + str(pt[1]) + ' ' + str(pt[2]) + '\n'  # old by Nico.
            # f.write(s)                                                                  # old by Nico.

        point_material = list() # WRONG! # This actually is facet_material !!!!!!!!!

        # write connectivity information of triangles
        # integer, material id, vertex point ids
        for i in range(valve3Dsurface.GetNumberOfCells()):
            cell = valve3Dsurface.GetCell(i)
            iDs = cell.GetPointIds()
            if upLowCells[i] == 2:  # NOTE: "upLowCells[i] = 2" means "cell on ANT upside".
                matId = ID_ANT
            elif upLowCells[i] == 3:  # NOTE: "upLowCells[i] = 3" means "cell on POST upside".
                matId = ID_POST
            else:  # NOTE: "upLowCells[i] = 0" means "cell on downside".
                matId = ID_DOWN

            f.write("%d %d tri %d %d %d\n" % (
                i, matId, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2))) # new by Alexander; corrected by Nico.

            point_material.append(matId) # WRONG!!! - This actually is facet_material !!!!!!!!
            points += (iDs.GetId(0), iDs.GetId(1), iDs.GetId(2)) # and these are the 3 points on those triangular facets !!!
            
            # Old code below here:
            # s = str(0) + ' ' + str(matId) + ' tri ' + str(iDs.GetId(0)) + ' ' + str(iDs.GetId(1)) + ' ' + str(iDs.GetId(2)) + '\n'
            # list_of_matIDints+=[matID, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2)]
            # f.write(s)

        tet_material = list() # CORRECT!
        tets = list()

        # write connectivity information of tetrahedrons
        # integer, material id, vertex point ids
        for i in range(valve3DvolumeMesh.GetNumberOfCells()):
            cell = valve3DvolumeMesh.GetCell(i)
            iDs = cell.GetPointIds()
            matId = 10

            f.write("%d %d tet %d %d %d %d\n" % (
                i, matId, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2), iDs.GetId(3))) # new by Alexander, corrected by Nico.

            tet_material.append(10)
            tets += [iDs.GetId(0), iDs.GetId(1), iDs.GetId(2), iDs.GetId(3)]
            
            # Old code below here:
            # s = str(0) + ' ' + str(matId) + ' tet ' + str(iDs.GetId(0)) + ' ' + str(iDs.GetId(1)) + ' ' + str(iDs.GetId(2)) + ' ' + str(iDs.GetId(3)) + '\n'
            # list_of_point_matIDints+=[10, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2), iDs.GetId(3)]
            # f.write(s)

        debug("Writing HiFlow3 inp output file (incl. MV matIDs): DONE.")

    return target, points, tets, point_material, tet_material # WRONG names/representations; actually it is (facets, tets, facet_matIDs, tet_matIDs)


def vtu_To_Hf3inpWithBdyFacetMatID_Producer(mesh, target, behaviour = 0): # DEPRECATED!!!!
    """Given an unstructured grid (vtu file), which only contains the
    connectivity information of 3D cells with four vertices (i.e.
    tetrahedrons) and no other cells of dimension different from three,
    this script computes the cell normals of the 2D boundary faces of the
    mesh.
    The coordinates of the vertices, the connectivity information of the
    3D cells and 2D boundary faces will be written to an inp file. The
    material id of the cells will be determined as follows:
    - every 3D cell gets the material id 10.
    - if the z-coordinate of the boundary face's normal is greater than
    zero, the corresponding 2D cell gets the material id 30,
    - otherwise its material id will be 20.

    How to run the script:
    python vtuToHf3inpWithBdyFacetMatIDsProducer.py mesh.vtu <Integer>

    If `behavior` == 0 then the script writes the connectivity information
    of the tetrahedrons to the inp file. Otherwise it will write no
    information about 3D cells.
    The default value is 0 and one does not have to pass the argument.


    :param mesh:
    :type mesh:
    :param target:
    :type target:
    :param behaviour:
    :type behaviour: int
    :return:
    :rtype:

        .. author:: Nicolai Schoch, EMCL; 2014-12-10.
    """
    # ======================================================================
    # Define material ids
    # ======================================================================
    ID_TET = 10
    ID_FACET_UP_LEFT = 31
    ID_FACET_UP_RIGHT = 32
    ID_FACET_BELOW = 20

    # ======================================================================
    # Define separating hyperplane with normal n
    # x0 is an element of the plane
    # ======================================================================
    n = [1.0, -0.05, 0.5]
    x0 = [85.35, 93.7, 105.8]

    # ======================================================================
    # Get the name of the vtu file and set value for variable 'no3DCells'.
    # If no3DCells == 0 then the script writes the connectivity information
    # of the tetrahedrons to the inp file. Otherwise it will write no
    # information about 3D cells.
    # ======================================================================
    # mesh = sys.argv[1]

    # if len(sys.argv) > 2:
    # no3DCells = sys.argv[2]
    # else:
    #  no3DCells = 0

    no3DCells = 0

    # ======================================================================
    # Create an object of the class 'vtkXMLUnstructuredGridReader'.
    # Read in the vtu file, update the reader and get its output.
    # ======================================================================
    unstructuredGrid = read_ugrid(mesh) # NEW 2014-12-23

    # ======================================================================
    # Use 'vtkGeometryFilter' to extract 2D faces on the boundary of
    # 'unstructuredGrid'.
    # Update the filter and get its output, which is of type 'vtkPolyData'.
    # ======================================================================
    boundaryFaces = get_surface(unstructuredGrid)

    # ======================================================================
    # Create 'vtkPolyDataNormals' object in order to compute normals of
    # boundary faces. Set ComputePointNormals to 'off' and
    # ComputeCellNormals to 'on'. Update the filter.
    # ======================================================================
    normals = vtk.vtkPolyDataNormals()

    if vtk.version.GetVTKMajorVersion() >= 6:
        normals.SetInputData(boundaryFaces)
    else:
        normals.SetInput(boundaryFaces)

    normals.ComputePointNormalsOff()
    normals.ComputeCellNormalsOn()
    normals.Update()

    # ======================================================================
    # Retrieve array of normals of boundary cells and add data to
    # the polygonal mesh 'boundaryFaces'.
    # ======================================================================
    cellNormalArray = normals.GetOutput().GetCellData().GetNormals()
    boundaryFaces.GetCellData().SetNormals(cellNormalArray)

    # ======================================================================
    # Create inp file with the following content:
    # - coordinates of the vertices of the unstructured grid
    # - connectivity information of the 3D cells of the unstructured grid
    # - connectivity information of the 2D cells of the polygonal mesh
    # The file's name will be the name of the input file with the
    # appropriate ending.
    # ======================================================================
    #target = mesh[0:len(mesh)-3] + 'inp'
    with open(target, 'w') as f:
        # Write first line, i.e. total number of vertices, total number of cells and three times 0.
        if no3DCells == 0:
            print >> f, unstructuredGrid.GetNumberOfPoints(), \
                boundaryFaces.GetNumberOfCells() + unstructuredGrid.GetNumberOfCells(), \
                0, 0, 0
        else:
            print >> f, unstructuredGrid.GetNumberOfPoints(), \
                boundaryFaces.GetNumberOfCells(), 0, 0, 0

        # Write coordinates of vertices.
        for i in range(0, unstructuredGrid.GetNumberOfPoints()):
            point = unstructuredGrid.GetPoint(i)
            print >> f, i, point[0], point[1], point[2]

        # Write connectivity information of tetrahedrons, which are the 3D cells of the unstructured grid.
        if no3DCells == 0:
            for i in range(0, unstructuredGrid.GetNumberOfCells()):
                cellPointIds = unstructuredGrid.GetCell(i).GetPointIds()
                cellPointIdsString = ''
                for j in range(0, cellPointIds.GetNumberOfIds()):
                    cellPointIdsString += str(cellPointIds.GetId(j)) + ' '
                print >> f, i, ID_TET, 'tet', cellPointIdsString

        # Write connectivity information of triangles, which are the 2D cells of the polygonal mesh.
        cellNormalsRetrieved = boundaryFaces.GetCellData().GetNormals()
        for i in range(0, boundaryFaces.GetNumberOfCells()):
            cellNormal = cellNormalsRetrieved.GetTuple(i)
            cellPointIds = boundaryFaces.GetCell(i).GetPointIds()
            cellPointIdsString = ''
            for j in range(0, cellPointIds.GetNumberOfIds()):
                cellPointIdsString += str(cellPointIds.GetId(j)) + ' '
            # Set material id w.r.t. z-coordinate of normal vector
            material_id = ID_FACET_BELOW
            if cellNormal[2] > 0:
                material_id = ID_FACET_UP_RIGHT
                point = boundaryFaces.GetPoint(cellPointIds.GetId(0))
                if n[0] * (point[0] - x0[0]) + n[1] * (point[1] - x0[1]) + n[2] * (point[2] - x0[2]) < 0:
                    material_id = ID_FACET_UP_LEFT
            print >> f, i, material_id, 'tri', cellPointIdsString
