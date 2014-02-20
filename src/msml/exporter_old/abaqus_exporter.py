#TODO LICENSE

from lxml import etree

__author__= ""  #TODO
__date__  = ""  #TODO
__version__= "" #TODO



class AbaqusExporter(BaseExporter):

   def writeINP(self, alphabetNode, msmlRootNode, filename):

      for msmlObject in msmlRootNode.iterchildren():
         if(msmlObject.tag == "object"):
            #create mesh
            physicsElementNode = msmlObject.find("physicsElements") 
            currentMeshNode = physicsElementNode.find("mesh")[0]
            theFilename = self.startDataNodeEvaluation( currentMeshNode)
            print theFilename           
            #creat node for operator processing
            targetNode = etree.Element("convertVTKMeshToAbaqusMeshString", name="converter", partName=msmlObject.get("name"), materialName="Neo-Hooke")
            inputValue = theFilename
            targetNodeAlphabet = self.findNodeTypeInAlphabet(targetNode.tag)
            theInpString = self.executeOperator(targetNodeAlphabet, targetNode, inputValue)
            #print theInpString
            
            #writing boundary conditions         
            currentLine = [theInpString, "**\n", "** \n", "** ASSEMBLY \n", "**\n", "*Assembly, name=" ,msmlObject.get("name"), "-Assembly\n"] 
            currentLine += [ "**\n", "*Instance, name=" ,msmlObject.get("name"), "-Instance, part=", msmlObject.get("name"), "-Part\n"]            
            currentLine += ["*End Instance\n", "**\n"]
            theInpString = ''.join(currentLine)
            
            
            
            simulationStepsNode = msmlObject.find("simulationSteps")
            for simulationStepNode in simulationStepsNode.iterchildren():  
               globalIndices =[]
               globalConstraintType =[] 
               globalDisplacements=[]
               for constraintRegionNode in simulationStepNode.findall("constraintRegion"):
                  indexGroupNode = constraintRegionNode.find("indexGroup")
                  print indexGroupNode.get("indices")
                  if(indexGroupNode.get("indices")[0] == "@"):
                     #in this case check the link
                     currentLinkedIndexGroup = indexGroupNode.get("indices")[1:]
                     indices = self.evaluateNode(indexGroupNode, currentLinkedIndexGroup)      
                  else:
                     indices = indexGroupNode.get("indices")
                  indices = indices.split(",")                  
                  for constraint in constraintRegionNode.iterchildren():
                     currentConstraintType = constraint.tag
                     if(currentConstraintType != "indexGroup"):
                        if (currentConstraintType == "fixedConstraints"):
                           iter=0
                           #print len(indices)
                           #print indices
                           for index in indices:
                              globalIndices.append(index);
                              globalConstraintType.append(0)
                              globalDisplacements.extend([0, 0, 0])  
                              iter += 1
                        elif (currentConstraintType == "displacementConstraints"):
                           displacements = constraint.get("displacements")
                           displacements = displacements.split(" ")
                           #print displacements
                           #print indices
                           #print len(indices)
                           iter=0
                           #print len(indices)
                           #print indices
                           for index in indices:
                              print iter
                              globalIndices.append(index);
                              globalConstraintType.append(1)
                              globalDisplacements.append(float(displacements[3*iter+0])) 
                              globalDisplacements.append(float(displacements[3*iter+1]))   
                              globalDisplacements.append(float(displacements[3*iter+2]))   
                              iter += 1                              
                        else:
                           print(currentConstraintType)
                           print("Constraint Type not supported!!!!!!!!!!!")
            
               #print the sets for the bcs
               currentLine = [theInpString]
               #print len(indices)
               #print indices
               iter=0
               for index in globalIndices:
                  currentLine +=  [ "*Nset, nset=_StaticPickedSet", str(iter) ,", internal, instance=", msmlObject.get("name") ,"-Instance\n ,", str(int(index)+1) ,"\n"]
                  iter += 1
               
               
               theInpString = ''.join(currentLine)   
                  
               currentLine = [theInpString]
               currentLine += [ "*End Assembly\n"]

               currentLine += ["**\n" ,"** MATERIALS\n" ,"**\n"]
               currentLine += ["*Material, name=Neo-Hooke\n"]
               currentLine += ["*Damping, beta=0.21\n"]
               currentLine += ["*Density\n1070.,\n"]
               currentLine += ["*Hyperelastic, neo hooke\n" ,"365., 0.000838\n"];

               currentLine += ["**\n" ,"** BOUNDARY CONDITIONS\n" ,"**\n"];
               
               iter=0
               for index in globalIndices:
                  if (globalConstraintType[iter] == 0):
                     currentLine +=  ["** Name: Fixed Type: Symmetry/Antisymmetry/Encastre\n" ,"*Boundary\n"];
                     currentLine +=  ["_StaticPickedSet" ,str(iter) ,", PINNED \n"];                
                  iter += 1
          
           
               currentLine += ["** ----------------------------------------------------------------\n"];
               currentLine += ["**\n" ,"** STEP: CustomLoad" ,"**\n" ,"*Step, name=CustomLoad, nlgeom=YES, inc=5000\n"];
               currentLine += ["DiaLoad\n" ,"*Dynamic,alpha=-0.05,haftol=0.1\n" ,"0.01,3.,3e-05,3.\n"];
               
               currentLine += ["**\n" ,"** BOUNDARY CONDITIONS\n" ,"**\n"];
               
               iter=0
               for index in globalIndices:
                  if (globalConstraintType[iter] == 1):
                     currentLine +=  ["** Name: Disp Type: Displacement/Rotation\n" ,"*Boundary\n"];
                     currentLine +=  ["_StaticPickedSet" ,str(iter) ,", 1 , 1, ", str( globalDisplacements[3*iter+0] ), "\n"];    
                     currentLine +=  ["_StaticPickedSet" ,str(iter) ,", 2 , 2, ", str( globalDisplacements[3*iter+1] ), "\n"]; 
                     currentLine +=  ["_StaticPickedSet" ,str(iter) ,", 3 , 3, ", str( globalDisplacements[3*iter+2] ), "\n"];                      
                  iter += 1


            theInpString = ''.join(currentLine) 

            
            #print theInpString
            
            
            
            f = open(filename,'w')
            f.write(theInpString)
