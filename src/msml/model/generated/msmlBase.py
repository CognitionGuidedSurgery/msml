class LogicalType(object):
    pass






class IndexSet(LogicalType):
    pass






class FaceSet(IndexSet):
    pass






class Mesh(LogicalType):
    pass






class PhysicalQuantity(LogicalType):
    pass






class TensorQuantity(PhysicalQuantity):
    pass






class CauchyStress(TensorQuantity):
    pass






class PhysicalType(object):
    pass






class MSMLUInt(PhysicalType):
    pass






class NodeSet(IndexSet):
    pass






class MSMLListI(PhysicalType):
    pass






class InFile(PhysicalType):
    pass






class ContainerFile(InFile):
    pass






class VTKContainerFile(ContainerFile):
    pass






class STL(ContainerFile):
    pass






class HDF5(ContainerFile):
    pass






class ScalarQuantity(PhysicalQuantity):
    pass






class VectorQuantity(PhysicalQuantity):
    pass






class CTX(ContainerFile):
    pass






class Displacement(VectorQuantity):
    pass






class DICOM(ContainerFile):
    pass






class VTU(ContainerFile):
    pass






class SurfaceMesh(Mesh):
    pass






class TriangularMesh(SurfaceMesh):
    pass






class VolumeMesh(Mesh):
    pass






class QuadraticTetrahedralMesh(VolumeMesh):
    pass






class Force(VectorQuantity):
    pass






class MSMLString(PhysicalType):
    pass






class VonMisesStress(ScalarQuantity):
    pass






class Velocity(VectorQuantity):
    pass






class LinearTetrahedralMesh(VolumeMesh):
    pass






class Image(LogicalType):
    pass






class Image3D(Image):
    pass






class ElementSet(IndexSet):
    pass






class MSMLFloat(PhysicalType):
    pass






class Image2D(Image):
    pass






class VTI(ContainerFile):
    pass






class MSMLInt(PhysicalType):
    pass






class MSMLListUI(PhysicalType):
    pass

	
	
	
	
	
class MSMLListS(PhysicalType):
    pass





class LinearHexahedralMesh(VolumeMesh):
    pass






class Indices(LogicalType):
    pass






class VTX(ContainerFile):
    pass






class MSMLListF(PhysicalType):
    pass






