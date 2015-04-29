# -*- encoding: utf-8 -*-

"""

"""
__author__ = 'schoch', 'weigl'
__date__ = "2015-04-12"

import xml.etree.ElementTree as ET

import numpy as np
import vtk
from .msmlvtk import *
from msml.log import debug


def geometry_analyzer(surface, ring, target="geometry.txt"):
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
            f.write("midPtTop:(%s,%s,%s);\nannulusRadius:%s" % (
                midPtTop[0], midPtTop[1], midPtTop[2], midPtTop))  # produce outputAnalytics string and write into file

            debug("Write file %s", target)

    return [midPtTop[0], midPtTop[1], midPtTop[2], annulusRadius]


# TODOs:
# - delete double function arguments transformation into function variables;
# - delete print outputs and transform into debug information;

def bcdata_producer(volume_mesh, surface_mesh, ring, annulus_point_ids=16, target="output.vtk"):
    """Given the following input data w.r.t. a mitral valve setup:
     - a 3D volume mesh (vtu),
     - a 2D surface mesh representation of the MV segmentation (vtp), and
     - an Annuloplasty Ring representation including vertex IDs (vtp)
     this script computes and sets the Dirichlet Boundary Conditions (BCs)
     data for the HiFlow3-based MVR-Simulation.

    .. note:: Adding additional BC-points by means of linear interpolation
              requires the input IDs to be ordered and going around annulus once!!!

    .. authors::
        * Nicolai Schoch, EMCL; 2015-04-12.

    :param volume_mesh:
    :param surface_mesh:
    :param ring:
    :param annulus_point_ids:
    :return:
    """

    # ======================================================================
    # define number of given annulus point IDs -----------------------------
    # (see notation/representation of Annuloplasty Rings by DKFZ and corresponding addInfo)

    debug("=== Execute Python script to produce BCdata for the  HiFlow3-based MVR-Simulation ===")

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

    # ======================================================================
    # arrays for storage of coordinates of annulus points (and interpolated points) on the MV surface and on the ring -----------------
    ringPoints_ = np.zeros((2 * annulus_point_ids, 3))
    valvePoints_ = np.zeros((2 * annulus_point_ids, 3))

    # Store coordiantes in arrays ---------------------------------------------------------------------------
    # NOTE: Alternatively, instead of a loop over all points and looking for their IDs,
    # one could also loop over the array of vertexIDs and get the pointID.
    # find coordinates of points of ring_
    for i in range(ring_.GetNumberOfPoints()):
        pos = int(ringVertexIds_.GetTuple1(i))
        if 0 <= pos < annulus_point_ids:
            ringPoints_[pos] = np.array(ring_.GetPoint(i))

    # find coordinates of points of valve2d_
    for i in range(valve2d_.GetNumberOfPoints()):
        pos = int(valve2dVertexIds_.GetTuple1(i))
        if 0 <= pos < annulus_point_ids:
            valvePoints_[pos] = np.array(valve2d_.GetPoint(i))

    # find closest points to points stored in valvePoints_ on valve3dSurface_ and store (i.e. overwrite) them in valvePoints_
    for i in range(annulus_point_ids):
        iD = kDTree.FindClosestPoint(valvePoints_[i])
        kDTree.GetDataSet().GetPoint(iD, valvePoints_[i])

    # ======================================================================
    # add additional boundary conditions by linear interpolation -------------------------------------------
    # NOTE: this requires the IDs to be ordered and going around annulus once!!!
    for i in range(annulus_point_ids):
        valve_point = 0.5 * (valvePoints_[i] + valvePoints_[(i + 1) % annulus_point_ids])
        valvePoints_[annulus_point_ids + i] = valve_point

        ring_point = 0.5 * (ringPoints_[i] + ringPoints_[(i + 1) % annulus_point_ids])
        ringPoints_[annulus_point_ids + i] = ring_point

    # ======================================================================
    # Compute displacements ------------------------------------------------
    displacement_ = ringPoints_ - valvePoints_

    # ======================================================================
    # Transform points and displacements for HiFlow3-Exporter --------------
    flatten = lambda l: [item for sublist in l
                         for item in sublist]

    points = flatten(valvePoints_)
    displacements = flatten(displacement_)

    debug("Computing Dirichlet displacement BC datac")

    # ======================================================================
    # convert arrays to strings --------------------------------------------
    valvePointString_ = ""
    displacementString_ = ""
    for i in range(2 * annulus_point_ids):
        for j in range(3):
            valvePointString_ += str(valvePoints_[i][j])
            displacementString_ += str(displacement_[i][j])
            if j == 2:
                if i < 2 * annulus_point_ids - 1:
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
    numberOfDPoints.text = str(2 * annulus_point_ids)

    dDPoints = ET.SubElement(DisplacementConstraintsBCs, "dDPoints")
    dDPoints.text = valvePointString_

    dDisplacements = ET.SubElement(DisplacementConstraintsBCs, "dDisplacements")
    dDisplacements.text = displacementString_

    # wrap it in an ElementTree instance, and save as XML
    tree = ET.ElementTree(root)
    tree.write(target)

    # ======================================================================

    debug("Writing mvrSimBCdata.xml output file")

    return points, displacements


def von_misses_stress(surface, target):
    """Given vtu/pvtu file(s) resulting from an MVR elasticity simulation
    (the solution files hence contain three scalar valued arrays named
    'u0', 'u1' and 'u2' as PointData), this vtk-based python script
    warps the initial/original mesh geometry by means of the displacement
    vector, and computes the Cauchy strain tensor and the von Mises stress.

    The script's output is the following:
    - vtu file that contains all the data of the
       original file with modified coordinates of the points and the
       displacement vector as additional PointData and the strain tensor
       along with the von Mises stress (w.r.t. the Lame parameters
       lambda = 28466, mu = 700 for mitral valve tissue, according to
       [Mansi-2012]) as additional CellData.

    Author: Nicolai Schoch, EMCL; 2015-04-12.
            Alexander Weigl, KIT; 2015-04-19

    :param surface: a polydata surface
    :param target: a unstructured grid
    :return:
    """
    # ======================================================================
    # get system arguments -------------------------------------------------
    # Path to input file and name of the output file
    debug("=== Execute Python script to analyze MV geometry in order for the HiFlow3-based MVR-Simulation ===")

    # ======================================================================
    # Read file

    polydata = read_polydata(surface)

    # ======================================================================
    # Compute displacement vector
    calc = vtk.vtkArrayCalculator()
    calc.SetInput(polydata)
    calc.SetAttributeModeToUsePointData()
    calc.AddScalarVariable('x', 'u0', 0)
    calc.AddScalarVariable('y', 'u1', 0)
    calc.AddScalarVariable('z', 'u2', 0)
    calc.SetFunction('x*iHat+y*jHat+z*kHat')
    calc.SetResultArrayName('DisplacementSolutionVector')
    calc.Update()

    # ======================================================================
    # Compute strain tensor
    derivative = vtk.vtkCellDerivatives()
    derivative.SetInput(calc.GetOutput())
    derivative.SetTensorModeToComputeStrain()
    derivative.Update()

    # ======================================================================
    # Compute von Mises stress
    calc = vtk.vtkArrayCalculator()
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
    calc.SetFunction(
        'sqrt( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))^2 + (2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8))^2 + (2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8))^2 - ( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8)) ) - ( (2*700*Strain_0 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8)) ) - ( (2*700*Strain_4 + 28466*(Strain_0+Strain_4+Strain_8))*(2*700*Strain_8 + 28466*(Strain_0+Strain_4+Strain_8)) ) + 3 * ((2*700*Strain_3)^2 + (2*700*Strain_6)^2 + (2*700*Strain_7)^2) )')
    calc.SetResultArrayName('vonMisesStress_forMV_mu700_lambda28466')
    calc.Update()

    debug("Computation of displacement vectors, Cauchy strain and vom Mises stress")

    # ======================================================================
    # Define dummy variable; get output of calc filter
    dummy = calc.GetOutput()

    # Get point data arrays u0, u1 and u2
    pointData_u0 = dummy.GetPointData().GetArray('u0')
    pointData_u1 = dummy.GetPointData().GetArray('u1')
    pointData_u2 = dummy.GetPointData().GetArray('u2')

    # Set scalars
    dummy.GetPointData().SetScalars(pointData_u0)

    # ======================================================================
    # Warp by scalar u0
    warpScalar = vtk.vtkWarpScalar()
    warpScalar.SetInput(dummy)
    warpScalar.SetNormal(1.0, 0.0, 0.0)
    warpScalar.SetScaleFactor(1.0)
    warpScalar.SetUseNormal(1)
    warpScalar.Update()

    # Get output and set scalars
    dummy = warpScalar.GetOutput()
    dummy.GetPointData().SetScalars(pointData_u1)

    # ======================================================================
    # Warp by scalar u1
    warpScalar = vtk.vtkWarpScalar()
    warpScalar.SetInput(dummy)
    warpScalar.SetNormal(0.0, 1.0, 0.0)
    warpScalar.SetScaleFactor(1.0)
    warpScalar.SetUseNormal(1)
    warpScalar.Update()

    # Get output and set scalars
    dummy = warpScalar.GetOutput()
    dummy.GetPointData().SetScalars(pointData_u2)

    # ======================================================================
    # Warp by scalar u2
    warpScalar = vtk.vtkWarpScalar()
    warpScalar.SetInput(dummy)
    warpScalar.SetNormal(0.0, 0.0, 1.0)
    warpScalar.SetScaleFactor(1.0)
    warpScalar.SetUseNormal(1)
    warpScalar.Update()

    # Get ouput and add point data arrays that got deleted earlier
    dummy = warpScalar.GetOutput()
    dummy.GetPointData().AddArray(pointData_u0)
    dummy.GetPointData().AddArray(pointData_u1)

    # ======================================================================
    # Write output to vtu

    write_vtu(dummy, target)

    # ======================================================================
    debug("Writing Extended VTU incl. von Mises Stress information")


def get_surface_normals(surface):
    """returns the normal vectors for a surface

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


def vtu_To_hf3inp_inc_MV_matIDs_Producer(volume_mesh, surface_mesh, target="hf3inputvalues.inp"):
    """Given `volume_mesh` and `surface_mesh`

    The coordinates of the vertices, the connectivity information of the
    3D cells and 2D boundary faces will be written to the hf3-inp-file.
    The matIDs of the cells will be determined as follows:
    - every 3D cell gets the material id 10.
    - surface cells are subdivided into
      - upside surfaces on anterior leaflet: matID 17,
      - upside surfaces on posterior leaflet: matID 18,
      - downside surfaces: matID 20.


    .. todo:: documentation

    :param volume_mesh:
        a 3D unstructured grid (vtu file) representation of the MV segmentation (e.g. by CGAL meshing operator,
        followed by vtk2vtu-Converter), which only contains the connectivity information of 3D cells with four vertices
        (i.e. tetrahedrons) and no other cells of dimension different from three,

    :type volume_mesh: vtk.vtkUnstructuredGrid

    :param surface_mesh:
        a 2D polydata surface representation of the MV segmentation, which additionally contains matID-information
        on the MV leaflets and annulus points, this script produces a hf3-inp-file suitable for a HiFlow3-based MVR-simulation.

    :type surface_mesh: vtk.vtkPolyData

    :return: i do not know what the fuck blah

    ..note::
        The result of this script is NOT DETERMINISTIC! This means that it requires
        human assessment of the suitability of the results for the simulation algorithm.

    .. note::
        This version of the script uses CellNormals (as opposed to PointNormals).

    .. note::
        In order to avoid 'blurry' matID-distribution around the interface between
        between the leaflets (near the commissure points),
            - either use MITK-remeshing results (2 separate leaflets and 1 complete MV inc IDs),
            - or possibly use some vtk filter "subdivision" to refine mesh "smoothing"...

    .. author::
            Nicolai Schoch, EMCL; 2015-04-12.
            Alexander Weigl, KIT; 2015-04-19

    """

    # ======================================================================
    # Define matIDs --------------------------------------------------------

    ID_UP = 21  # preliminary result, which gets overwritten by ID_ANT and ID_POST.
    ID_DOWN = 20
    ID_ANT = 17
    ID_POST = 18


    # ======================================================================
    # read in files: -------------------------------------------------------
    # read in 3d valve
    # NOTE: ensure that the precedent meshing algorithm (CGAL or similar)
    # produces consistent/good results w.r.t. the 'normal glyphs'.

    valve3d_ = read_ugrid(volume_mesh)

    # get surface mesh of valve3d_
    valve3dSurface_ = get_surface(valve3d_)

    # get cell normals
    normalsSurfaceRetrieved_ = get_surface_normals(valve3dSurface_)


    # read in 2d valve
    valve2d_ = read_polydata(surface_mesh)

    # get cell normals
    normalsValve2dRetrieved_ = get_surface_normals(valve2d_)

    # ======================================================================
    # initialize cell locator for closest cell search ----------------------
    # (using vtk methods, that find the closest point in a grid for an arbitrary point in R^3)

    cellLocator = vtk.vtkCellLocator()
    cellLocator.SetDataSet(valve2d_)
    cellLocator.BuildLocator()

    # ======================================================================
    # allocate memory for cell_udlr_list_ (up-down-left-right) -------------
    cell_udlr_list_ = [0] * valve3dSurface_.GetNumberOfCells()

    # ======================================================================
    # iterate over the cells of the surface and compare normals ------------
    for i in range(valve3dSurface_.GetNumberOfCells()):
        # get cellId of closest point
        point_id = valve3dSurface_.GetCell(i).GetPointId(0)  # NOTE: only one (test)point (0) of respective cell
        testPoint = valve3dSurface_.GetPoint(point_id)
        closestPoint = np.zeros(3)
        closestPointDist2 = vtk.mutable(0)
        cellId = vtk.mutable(0)
        subId = vtk.mutable(0)
        cellLocator.FindClosestPoint(testPoint, closestPoint, cellId, subId, closestPointDist2)

        normalSurf_ = np.zeros(3)
        normalsSurfaceRetrieved_.GetTuple(i, normalSurf_)

        normalV2d_ = np.zeros(3)
        normalsValve2dRetrieved_.GetTuple(cellId, normalV2d_)

        # set cell_udlr_list_ entry to (preliminary) "1", if cell is on upper side of leaflet
        if np.dot(normalSurf_, normalV2d_) > 0.0:
            cell_udlr_list_[i] = 1  # NOTE: "cell_udlr_list_[i] = 1" means "cell on upside".

    # ======================================================================
    # iterate over cells on the upper side of the leaflet surface, and set ids for left/right ------------------
    kDTree = vtk.vtkKdTreePointLocator()
    kDTree.SetDataSet(valve2d_)
    kDTree.BuildLocator()

    VertexIDs_ = valve2d_.GetPointData().GetArray('VertexIDs')

    # allocate memory for upCellList_ (indicating if cell is on left/right side)
    upCellList_ = [i for i in range(valve3dSurface_.GetNumberOfCells()) if cell_udlr_list_[i]]

    for i in upCellList_:
        point_id = valve3dSurface_.GetCell(i).GetPointId(0)
        testPoint = valve3dSurface_.GetPoint(point_id)
        result_ = vtk.vtkIdList()
        counter = 1
        cond_ = True
        while cond_:
            kDTree.FindClosestNPoints(counter, testPoint, result_)
            for j in range(result_.GetNumberOfIds()):
                iD2 = result_.GetId(j)
                if int(VertexIDs_.GetTuple1(iD2)) == ID_ANT:
                    cond_ = False
                    cell_udlr_list_[i] = 2  # NOTE: "cell_udlr_list_[i] = 2" means "cell on ANT upside".
                if int(VertexIDs_.GetTuple1(iD2)) == ID_POST:
                    cond_ = False
                    cell_udlr_list_[i] = 3  # NOTE: "cell_udlr_list_[i] = 3" means "cell on POST upside".
            counter += 1

    debug("Computing hf3-inp MV matID information: DONE.")

    # ======================================================================
    # region write results to inp file

    material_ids = list()
    points = list()

    with  open(target, 'w') as f:
        # write first line
        f.write("%d %d 0 0 0\n" % (
            valve3d_.GetNumberOfPoints(),
            valve3dSurface_.GetNumberOfCells() + valve3d_.GetNumberOfCells()))

        # write point coordinates
        for i in range(valve3d_.GetNumberOfPoints()):
            pt = valve3d_.GetPoint(i)
            f.write(' '.join(pt))
            f.write("\n")

        point_material = list()

        # write connectivity information of triangles
        # integer, material id, vertex point ids
        for i in range(valve3dSurface_.GetNumberOfCells()):
            cell = valve3dSurface_.GetCell(i)
            iDs = cell.GetPointIds()
            if cell_udlr_list_[i] == 2:  # NOTE: "cell_udlr_list_[i] = 2" means "cell on ANT upside".
                matId = ID_ANT
            elif cell_udlr_list_[i] == 3:  # NOTE: "cell_udlr_list_[i] = 3" means "cell on POST upside".
                matId = ID_POST
            else:  # NOTE: "cell_udlr_list_[i] = 0" means "cell on downside".
                matId = ID_DOWN

            f.write("0 %d tri %d %d %d\n" % (
                matId, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2)))

            point_material.append(matId)
            points += (iDs.GetId(0), iDs.GetId(1), iDs.GetId(2))

        tet_material = list()
        tets = list()

        # write connectivity information of tetrahedrons
        # integer, material id, vertex point ids
        for i in range(valve3d_.GetNumberOfCells()):
            cell = valve3d_.GetCell(i)
            iDs = cell.GetPointIds()
            matId = 10

            f.write("0 %d tri %d %d %d\b" % (
                matId, iDs.GetId(0), iDs.GetId(1), iDs.GetId(2)))

            tet_material.append(10)
            tets += [iDs.GetId(0), iDs.GetId(1), iDs.GetId(2), iDs.GetId(3)]

        debug("Writing HiFlow3 inp output file (incl. MV matIDs): DONE.")

    return points, tets, point_material, tet_material


def vtu_To_Hf3inpWithBdyFacetMatID_Producer(mesh, target, behaviour = 0):
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
