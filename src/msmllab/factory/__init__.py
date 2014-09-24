"""This should demonstrate a beautiful python API for MSML


"""

__author__ = 'Alexander Weigl'


# # First define what we need:
# * defintition: workflow, env, scene


from  collections import namedtuple

_E = namedtuple("_E", "solver, steps")


def Environment(solver, steps=None):
    return _E(solver, steps)


def Solver(linearSolver="CG",
           preconditioner="SGAUSS_SEIDEL",
           processingUnit="CPU",
           numParallelProcessesOnCPU="4",
           timeIntegration="Newmark",
           dampingRayleighRatioMass="0.2",
           dampingRayleighRatioStiffness="0.4"):
    pass


def Step(dt, iterations, name=None):
    pass


def Scene(objects=None):
    pass


def Object(mesh,
           constraints=None,
           material_regions=None,
           sets=None,
           id=None):
    pass


def ConSet(for_step=None, *constraints):
    pass


_M = namedtuple("_M", "t,p")


def Mesh(type, promise):
    return _M(type, promise)


def MaterialRegion(indices, *materials):
    pass


class MeshType(object):
    LinearTetraeder = 1
    LinearHexaeder = 1


def Sets(surface=None, nodes=None, elements=None):
    pass


def Simulation(workflow=None, scene=None, environment=None):
    pass


# ## From alphabet generated
def displacementConstraint(indices, displacement): pass


def surfacePressure(indices, pressure): pass


def springMeshToFixed(stiffness, rayleighStiffnes, fixedPoints, movingPoints): pass


def fixedConstraint(time, indices): pass


def pressureConstraint(indices, pressure): pass


def forceConstraint(indices, force): pass


def supportingMesh(youngModulus, poissonRatio, filename): pass


def mass(massDensity): pass


def linearElasticMaterial(poissonRatio, youngModulus): pass


def illumination(color): pass

class Workflow(object):
    def mesherTetgen(self, *args, **kwargs):
        pass

# #############################################

# environment
env = Environment(
    Solver(),
    steps=(
        Step(dt=0.05, iterations=20),
        Step(dt=0.05, iterations=20),
        Step(dt=0.05, iterations=20))
)

wf = Workflow()
tetgen = wf.tetgenMesher(mesh = "bunnyVolume.vtk", output_name ="blubb.vtk" )

# just dummy variables
force = [1] * 3
mat_ind = fixed_indices = force_indices = range(0, 100)


## Scene:
bunny = Object(
    Mesh(MeshType.LinearTetraeder, tetgen.mesh),
    constraints=[
        ConSet(fixedConstraint(fixed_indices),
               pressureConstraint(force_indices, force),
               for_step=0)
    ],
    material_regions=[
        MaterialRegion(
            mass(1),
            springMeshToFixed(42, 42, 42, 42),
            indices=mat_ind
        )
    ],

    sets=Sets(
        surface=None,
        # ...
    ),
)


s = Simulation(scene=Scene([bunny]),
     workflow=wf, environment=env)

# ############################################