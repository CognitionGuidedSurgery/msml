#TODO LICENSE

from lxml import etree
import os
import math

from .base_exporter import BaseExporter


__author__= ""  #TODO
__date__  = ""  #TODO
__version__= "" #TODO


class SOFAExporter(BaseExporter):
  
   def createMeshTopology(self,currentSofaNode, currentMsmlNode, msmlRootNode):
      currentMeshNode = currentMsmlNode.find("mesh")[0]
      currentMeshType = currentMeshNode.tag
      
      #print (currentMeshType)
      if currentMeshType == "linearTetMesh":
         loaderNode = etree.SubElement(currentSofaNode, "MeshVTKLoader")
         #loaderNode = etree.SubElement(currentSofaNode, "MeshExtendedVTKLoader")
         loaderNode.set("name", "LOADER") # currentMeshNode.get("name" )) - having a constant name for our the loader simplifies using it as source for nodes generated later.
         #find the filename
         theFilename = self.startDataNodeEvaluation( currentMeshNode)
         print theFilename
         
         loaderNode.set("filename", theFilename)
         loaderNode.set("createSubelements", "0") #does not work as expected. If a single triangle exists in mesh, then for each facet of all tets a triangle is ceated... SOFA bug?
         etree.SubElement(currentSofaNode,"MechanicalObject", name="dofs", template="undef", src="@LOADER")
         etree.SubElement(currentSofaNode,"MeshTopology", name="topo", src="@LOADER")
         #check if child is present
         
         #if so, check operator compatibility
         
         #execute operator
         
         #check if mesh is in MSML folder 
         
         #if not -> copy
      elif currentMeshType == "quadraticTetMesh":
         loaderNode = etree.SubElement(currentSofaNode, "MeshExtendedVTKLoader")
         loaderNode.set("name", "LOADER") # currentMeshNode.get("name" )) - having a constant name for our the loader simplifies using it as source for nodes generated later.
         #find the filename
         theFilename = self.startDataNodeEvaluation( currentMeshNode)
         print theFilename
         
         loaderNode.set("filename", theFilename)
         etree.SubElement(currentSofaNode,"MechanicalObject", name="dofs", template="undef", src="@LOADER")
         etree.SubElement(currentSofaNode,"QuadraticMeshTopology", name="topo", src="@LOADER")    
      
      else:
         print("Mesh type must be mesh.volume.linearTetrahedron.vtk or mesh.volume.quadraticTetrahedron.vtk")
         
   def createSolvers(self,currentSofaNode, currentMsmlNode, msmlRootNode):
      
      ODESolverType = currentMsmlNode.find("timeIntegration").text
  
      if(ODESolverType == None):
         print "Error, no ODE solver type specified"
         return
      LinearSolverType = currentMsmlNode.find("linearSolver").text
      if(LinearSolverType == None):
         print "Error, no linear solver type specified"
         return
      
      if(ODESolverType == "dynamicImplicit"):
         etree.SubElement(currentSofaNode,"MyNewmarkImplicitSolver", rayleighStiffness="0.2", rayleighMass="0.02", name="odesolver")
      elif(ODESolverType == "dynamicImplicitEuler"):
         etree.SubElement(currentSofaNode,"EulerImplicitSolver", name="odesolver")
      else:
         print "Error ODE solver ", ODESolverType, " not supported"
         
      if(LinearSolverType == "direct"):
         etree.SubElement(currentSofaNode,"SparseMKLSolver")
      elif(LinearSolverType == "iterativeCG"):
         etree.SubElement(currentSofaNode,"CGLinearSolver", iterations="100", tolerance="1e-06", threshold="1e-06")
      else:
         print "Error linear solver ", LinearSolverType, " not supported"

   def InsertAllTemplateAttributs(self, sofaRootNode, msmlSolverNode):
        processingUnit = msmlSolverNode.find("processingUnit").text;
        if (processingUnit == "CPU"):
            value = "Vec3f"
        elif (processingUnit == "GPU"):
            value = "CudaVec3f"
        else:
            print "Invalid processingUnit in solver."    
            return;
        
        for element in sofaRootNode.iter():
            if (element.get("template")):
                if (element.get("template").find("undef") != -1):
                    element.set("template", element.get("template").replace("undef", value));         
      
      
   def createMaterialRegions(self,currentSofaNode, currentMsmlNode, msmlRootNode):
     youngs =  {}
     poissons =  {}
     density =  {}
     for currentMaterialRegionNode in currentMsmlNode.findall("materialRegion"):
         indexGroupNode = currentMaterialRegionNode.find("indexGroup")
         print "index groupt", indexGroupNode.get("indices")
         print indexGroupNode.get("indices")
         if(indexGroupNode.get("indices")[0] == "@"):
             currentLinkedIndexGroup = indexGroupNode.get("indices")[1:]
             indices = self.evaluateNode(indexGroupNode, currentLinkedIndexGroup)      
         else:
             indices = indexGroupNode.get("indices")
        
         
         indices_int = [int(i) for i in indices.split(",")]

         #Get all materials
         for material in currentMaterialRegionNode.iterchildren():
             currentMaterialType = material.tag 
             if(currentMaterialType != "indexGroup"):
                   if currentMaterialType == "linearElastic":
                       currentYoungs = material.get("youngModulus")
                       currentPoissons = material.get("poissonRatio") # not implemented in sofa yet!
                       for i in indices_int:
                           youngs[i] = currentYoungs
                           poissons[ i] = currentPoissons
                   elif currentMaterialType == "mass":
                       currentDensity = material.get("density")
                       for i in indices_int:
                           density[ i ] = currentDensity
                   else:
                       print(currentMaterialType)
                       print("Material Type not supported!!!!!!!!!!!")
      
     keylist = density.keys()
     keylist.sort();
     density_str= ""
     youngs_str=""
     poissons_str=""
     for i in keylist:
         density_str = density_str + density[ i ] +   " "
         youngs_str = youngs_str + youngs[ i ] +   " "
         poissons_str = poissons_str + poissons[ i ] +   " "
         
     #merge all different materials to single forcefield/density entries.
     if currentSofaNode.find("MeshTopology") is not None:
         elasticNode = etree.SubElement(currentSofaNode, "TetrahedronFEMForceField", template="undef", name="FEM",  listening="true" )
         elasticNode.set("youngModulus", youngs_str)
         elasticNode.set("poissonRatio",  poissons[keylist[0]])                 
         etree.SubElement(currentSofaNode, "TetrahedronSetGeometryAlgorithms",  name="aTetrahedronSetGeometryAlgorithm", template="undef" );
         massNode = etree.SubElement(currentSofaNode, "DiagonalMass",  name="meshMass"  )
         massNode.set("massDensity", density_str)                  
     elif (currentSofaNode.find("QuadraticMeshTopology") is not None) :
         eelasticNode = etree.SubElement(currentSofaNode, "QuadraticTetrahedralCorotationalFEMForceField", template="undef", name="FEM",  listening="true" )
         eelasticNode.set("setYoungModulus", youngs_str)
         eelasticNode.set("setPoissonRatio", poissons[keylist[0]]) # TODO             
         emassNode = etree.SubElement(currentSofaNode, "QuadraticMeshMatrixMass",  name="meshMass"  )
         emassNode.set("massDensity", density_str)                 
     else:
         print "Current mesh topology not supported"
         
      
   def createConstraintRegions(self,currentSofaNode, currentMsmlNode, msmlRootNode):
      for constraintRegionNode in currentMsmlNode.findall("constraintRegion"):
          indexGroupNode = constraintRegionNode.find("indexGroup")
          if (indexGroupNode is not None):
              print indexGroupNode.get("indices")
              if(indexGroupNode.get("indices")[0] == "@"):
                 #in this case check the link
                 currentLinkedIndexGroup = indexGroupNode.get("indices")[1:]
                 indices = self.evaluateNode(indexGroupNode, currentLinkedIndexGroup)      
              else:
                 indices = indexGroupNode.get("indices")
          
          for constraint in constraintRegionNode.iterchildren():
             currentConstraintType = constraint.tag
             if(currentConstraintType != "indexGroup"):
                if (currentConstraintType == "fixedConstraints"):
                    constraintNode = etree.SubElement(currentSofaNode, "FixedConstraint" )
                    constraintNode.set("name", constraint.get("name"))                   
                    constraintNode.set("indices", indices)
    
                    #elasticNode.set("setPoissonRatio", material.get("poissonRatio"))        
                        
                    #check if child is present
                    
                    #if so, check operator compatibility
                
                    #execute operator
                
                    #check if mesh is in MSML folder 
                
                    #if not -> copy
                elif (currentConstraintType == "surfacePressure"):   
                    constraintNode = etree.SubElement(currentSofaNode, "Node", name= "SurfaceLoad")
                    etree.SubElement(constraintNode, "MeshTopology", name= "SurfaceTopo", position="@LOADER.position", triangles="@LOADER.triangles", quads="@LOADER.quads")
                    etree.SubElement(constraintNode, "MechanicalObject", template="Vec3f", name= "surfacePressDOF",  position= "@SurfaceTopo.position")
                    surfacePressureForceFieldNode = etree.SubElement(constraintNode, "SurfacePressureForceField", template="Vec3f", name= "surfacePressure",  pulseMode= "1")
                    surfacePressureForceFieldNode.set("pressureSpeed", str(float(constraint.get("pressure")) / 10.0)) 
                    surfacePressureForceFieldNode.set("pressure", constraint.get("pressure"));
                    surfacePressureForceFieldNode.set("triangleIndices", indices)
                    etree.SubElement(constraintNode, "BarycentricMapping", template="undef, Vec3f", name= "barycentricMapSurfacePressure",  input= "@..",  output="@.")
                    
                elif (currentConstraintType == "springMeshToFixed"):
                    constraintNode = etree.SubElement(currentSofaNode, "Node", name= "springMeshToFixed")
                    mechObj = etree.SubElement(constraintNode, "MechanicalObject", template="Vec3f", name= "pointsInDeformingMesh")
                    mechObj.set("position", constraint.get("movingPoints"));
                    etree.SubElement(constraintNode, "BarycentricMapping", template="undef, Vec3f", name= "barycentricMapSpringMeshToFixed",  input= "@..",  output="@.")
                    displacedLandLMarks = etree.SubElement(constraintNode, "Node", name= "fixedPointsForSpringMeshToFixed")
                    mechObj = etree.SubElement(displacedLandLMarks, "MechanicalObject", template="Vec3f", name= "fixedPoints")
                    mechObj.set("position", constraint.get("fixedPoints"));
                    forcefield = etree.SubElement(constraintNode, "RestShapeSpringsForceField", template="Vec3f", name="Springs", external_rest_shape="fixedPointsForSpringMeshToFixed/fixedPoints",  drawSpring="true")
                    forcefield.set("stiffness",  constraint.get("stiffness"));
                    forcefield.set("rayleighStiffnes",  constraint.get("rayleighStiffnes"));
                
                elif (currentConstraintType == "supportingMesh"):    
                    constraintNode = etree.SubElement(currentSofaNode, "Node", name= "support")
                    constraintNode.set("name", "support_" + constraint.get("name"))
                    loaderNode = etree.SubElement(constraintNode, "MeshVTKLoader", name="LOADER_supportmesh" , createSubelements="0")
                    loaderNode.set("filename", constraint.get("filename")) #workaround, because node evaluation is only possible for data/operator nodes.
                    etree.SubElement(constraintNode, "MechanicalObject", name="dofs", src="@LOADER_supportmesh", template="Vec3f", translation="0 0 0")
                    etree.SubElement(constraintNode, "MeshTopology", name="topo", src="@LOADER_supportmesh")
                    forcefield = etree.SubElement(constraintNode, "TetrahedronFEMForceField", listening="true", name="FEM", template="Vec3f")
                    forcefield.set("youngModulus", constraint.get("youngModulus"))
                    forcefield.set("poissonRatio", constraint.get("poissonRatio"))
                    etree.SubElement(constraintNode, "TetrahedronSetGeometryAlgorithms", name="aTetrahedronSetGeometryAlgorithm", template="Vec3f")
                    diagonalMass = etree.SubElement(constraintNode, "DiagonalMass", name="meshMass")
                    diagonalMass.set("massDensity", constraint.get("massDensity"))
                    etree.SubElement(constraintNode, "BarycentricMapping", input="@..", name="barycentricMap", output="@.", template="undef, Vec3f")

                else:
                    print(currentConstraintType)
                    print("Constraint Type not supported!!!!!!!!!!!")   
	  
   def createObject(self,currentSofaNode, currentMsmlNode, msmlRootNode):
      objectNode = etree.SubElement(currentSofaNode, "Node")
      objectNode.set("name", currentMsmlNode.get("name" ))

      return objectNode
	  
   def createScene(self, msmlRootNode):
      delta = self.rootNodeMSML.find(".//step").get("dt") #only one step supported
      root = etree.Element("Node", name="root", dt=delta) 
      theGravity = msmlRootNode.get("gravity")
      root.set("gravity",theGravity)
      return root
      
   #sofa_exporter handles displacementOutputRequest only. Other postProcessing operators need to be adressed in... ?
   def createPostProcessingRequests(self, currentSofaNode, currentMsmlNode):
      for request in currentMsmlNode.iterchildren():
         if(request.tag == "displacementOutputRequest"):
            if (currentSofaNode.find("MeshTopology") is not None) :
               #dispOutputNode = etree.SubElement(currentSofaNode, "ExtendedVTKExporter" )
               dispOutputNode = etree.SubElement(currentSofaNode, "VTKExporter" )
               filename = os.path.join ( self.outputDirectory, request.get("name") )
               dispOutputNode.set("filename", filename)
               exportEveryNumberOfSteps = request.get("timestep")
               dispOutputNode.set("exportEveryNumberOfSteps", exportEveryNumberOfSteps)
               dispOutputNode.set("XMLformat", "1") #using xml=0 still writes a .vtu file but in legacy text format.
               dispOutputNode.set("edges", "0")
               #dispOutputNode.set("tetras", "0") #exporting points only 
               #todo export material => allows extraction of surfaces in post processing
               dispOutputNode.set("tetras", "1")
               dispOutputNode.set("triangles", "0")
               dispOutputNode.set("listening", "true")
               dispOutputNode.set("exportAtEnd", "true")
               timeSteps =  int((self.rootNodeMSML.find(".//step").get("timesteps"))) #only one stimulation step supported
               #exportEveryNumberOfSteps = 1 in SOFA means export every second time step.
               #exportEveryNumberOfSteps = 0 in SOFA means do not export.
               if (exportEveryNumberOfSteps==0):
                  lastNumber = 1
               else:

                 lastNumber = int(math.floor(timeSteps/( int(exportEveryNumberOfSteps)  + 1))) 
               filenameLastOutput = filename + str(lastNumber) + ".vtu"
               request.set("filename", filenameLastOutput)
            elif (currentSofaNode.find("QuadraticMeshTopology") is not None) :   
               dispOutputNode = etree.SubElement(currentSofaNode, "ExtendedVTKExporter" )
               filename = os.path.join ( self.outputDirectory, request.get("name") )
               dispOutputNode.set("filename", filename)
               dispOutputNode.set("exportEveryNumberOfSteps", request.get("timestep"))
               dispOutputNode.set("tetras", "0")
               dispOutputNode.set("quadraticTetras", "1") 
               dispOutputNode.set("listening", "true")
               dispOutputNode.set("exportAtEnd", "true")
               #TODO: Fill "filename" of request taking output numbering into account (see VTKExporter)   
            else:
               print "Topolgy type not supported"            
      
   def writeSCN(self, alphabetNode, msmlRootNode, filename):
      sceneNode = self.createScene(msmlRootNode)
      for msmlObject in msmlRootNode.iterchildren():
         if(msmlObject.tag == "object"):
            #create object, the mesh, material regions and constraints
            objectNode = self.createObject(sceneNode, msmlObject, msmlRootNode)
            physicsElementNode = msmlObject.find("physicsElements") 
            self.createMeshTopology(objectNode,physicsElementNode,msmlRootNode)         
            self.createMaterialRegions(objectNode,physicsElementNode,msmlRootNode)
         
            #create simulation steps
            simulationStepsNode = msmlObject.find("simulationSteps")
            for simulationStepNode in simulationStepsNode.iterchildren():
               objectNode.set("dt", simulationStepNode.get("dt"))
               self.createConstraintRegions(objectNode,simulationStepNode,msmlRootNode)
               
            #creat post processing request
            if (msmlObject.find("postProcessing") is not None) :               
               self.createPostProcessingRequests( objectNode, msmlObject.find("postProcessing") )
            
            
         elif(msmlObject.tag == "solver") :         
            #create solvers
            msmlSolverObject = msmlObject; #remember this node to access processingUnit attribute during template (Vec3f/CudaVed3f) insertion
            self.createSolvers(objectNode,msmlObject,msmlRootNode)

            
      self.InsertAllTemplateAttributs(sceneNode, msmlSolverObject);
      
      tree = etree.ElementTree(sceneNode)
      tree.write(filename, pretty_print=True)
      treeMSML = etree.ElementTree( msmlRootNode)
      processedFilename = os.path.splitext(filename)[0]+"Processed.xml"
      treeMSML.write(processedFilename, pretty_print=True)
      