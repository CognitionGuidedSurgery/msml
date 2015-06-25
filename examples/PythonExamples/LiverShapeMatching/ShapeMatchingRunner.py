import os
import msml.api.simulation_runner as api
import msml.ext.misc
import matplotlib.pyplot as plt

# define charge
# test: 1000, 10, 2500, 5000
charge="1000"

# define pathes and files
msml_outdir= os.path.abspath("/tmp/MSMLResultsLiverShapeMatching_charge"+charge+"/")
msml_file = os.path.abspath("LiverShapeMatching.msml.xml")

msml_mesh = os.path.abspath("Liver5Low.vtk")
msml_mesh_shape = os.path.abspath("Liver5Def.stl") # for shape matching
msml_mesh_shape_reference = os.path.abspath("Liver5LowReference.vtk") # for compare meshes

# run simulation
myRunner = api.SimulationRunner(msml_file, "sofa", msml_outdir)
myRunner.update_variable('vol_mesh', msml_mesh)
myRunner.update_variable('msml_mesh_shape', msml_mesh_shape)
myRunner.update_variable('msml_mesh_shape_ref', msml_mesh_shape_reference)
myRunner.update_variable('chargeNum', charge)
myRunner.run()

# compare meshes
errorVec = myRunner.get_results('compMesh', 'errorVec')
dispVec = myRunner.get_results('compMeshDisp', 'errorVec')

# plotting
fig1, ax1 = plt.subplots(figsize=(10,6))
bp1 = plt.boxplot(errorVec)
ax1.set_ylabel('Error [mm]')
plt.xticks( [1], ['Deformation Error'] )

fig2, ax2 = plt.subplots(figsize=(10,6))
bp2 = plt.boxplot(dispVec)
ax2.set_ylabel('Error [mm]')
plt.xticks( [1], ['Displacement'] )

plt.show()