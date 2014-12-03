/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, VCGOperators
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

// ****************************************************************************
// Includes
// ****************************************************************************
#include "VCGOperators.h"




// stuff to define the mesh
#include <vcg/complex/complex.h>

// io
#include <wrap/io_trimesh/import.h>
#include <wrap/ply/plylib.cpp> //windows fix?
#include <wrap/io_trimesh/export.h>


// local optimization
#include <vcg/complex/algorithms/local_optimization.h>
#include <vcg/complex/algorithms/local_optimization/tri_edge_collapse_quadric.h>

using namespace vcg;
using namespace tri;
using namespace std;

namespace MSML
{


/**********************************************************
Mesh Classes for Quadric Edge collapse based simplification

For edge collpases we need verteses with:
- V->F adjacency
- per vertex incremental mark
- per vertex Normal


Moreover for using a quadric based collapse the vertex class
must have also a Quadric member Q();
Otherwise the user have to provide an helper function object
to recover the quadric.

******************************************************/
// The class prototypes.
class MyVertex;
class MyEdge;
class MyFace;

struct MyUsedTypes: public UsedTypes<Use<MyVertex>::AsVertexType,Use<MyEdge>::AsEdgeType,Use<MyFace>::AsFaceType>{};

class MyVertex  : public Vertex< MyUsedTypes,
  vertex::VFAdj,
  vertex::Coord3f,
  vertex::Normal3f,
  vertex::Mark,
  vertex::BitFlags  >{
public:
  vcg::math::Quadric<double> &Qd() {return q;}
private:
  math::Quadric<double> q;
  };

class MyEdge : public Edge< MyUsedTypes> {};

typedef BasicVertexPair<MyVertex> VertexPair;

class MyFace    : public Face< MyUsedTypes,
  face::VFAdj,
  face::VertexRef,
  face::BitFlags > {};

// the main mesh class
class MyMesh    : public vcg::tri::TriMesh<std::vector<MyVertex>, std::vector<MyFace> > {};


class MyTriEdgeCollapse: public vcg::tri::TriEdgeCollapseQuadric< MyMesh, VertexPair, MyTriEdgeCollapse, QInfoStandard<MyVertex>  > {
            public:
            typedef  vcg::tri::TriEdgeCollapseQuadric< MyMesh,  VertexPair, MyTriEdgeCollapse, QInfoStandard<MyVertex>  > TECQ;
            typedef  MyMesh::VertexType::EdgeType EdgeType;
            inline MyTriEdgeCollapse(  const VertexPair &p, int i, BaseParameterClass *pp) :TECQ(p,i,pp){}
};




// ****************************************************************************
// Methods
// ****************************************************************************
std::string VCGOperators::CoarseSurfaceMeshPython(std::string infile, std::string outfile, int numberOfElements)
{
	std::cout<<"Coarsing mesh using VCGlib...";
	CoarseSurfaceMesh(infile.c_str(), outfile.c_str(), numberOfElements);
	return outfile;
}


bool VCGOperators::CoarseSurfaceMesh(const char* infile, const char* outfile, unsigned int numberOfElements )
{
		//first create coarse mesh with vcglib
//		std::string outfileTemp = std::string(infile) + string("Temp.stl");
//		int currentNumberOfElements = 1e30;
//		int FinalSize = numberOfElements;
		// mesh to simplify
		MyMesh referenceMeshVCG;
		MyMesh currentMeshVCG;

		//int t0=clock();
		int err=vcg::tri::io::Importer<MyMesh>::Open(referenceMeshVCG,infile);
		if(err)
		{
		printf("Unable to open mesh %s : '%s'\n",infile,vcg::tri::io::Importer<MyMesh>::ErrorMsg(err));
		exit(-1);
		return false;
		}
		printf("mesh loaded %d %d \n",referenceMeshVCG.vn,referenceMeshVCG.fn);

		TriEdgeCollapseQuadricParameter qparams;// = MyTriEdgeCollapse::Params() ;
		//MyTriEdgeCollapse::SetDefaultParams();
		qparams.QualityThr  =.3;
		float TargetError=numeric_limits<float>::max();
		bool CleaningFlag =true;


		//	  qparams.SafeHeapUpdate=false;
			  qparams.QualityCheck	= true;
		//	   qparams.NormalCheck	= false;
			   qparams.OptimalPlacement	= true;
		//	    qparams.ScaleIndependent	= false;
			    qparams.PreserveBoundary	= true;
		//	  qparams.PreserveTopology	= false;
		//	 qparams.NormalThrRad = math::ToRad(90.0f);
		//	   qparams.BoundaryWeight  = 0.5;
			    qparams.QualityThr = 0.5;
			  //  qparams.QualityWeight = true;



		if(CleaningFlag){
		 int dup = tri::Clean<MyMesh>::RemoveDuplicateVertex(referenceMeshVCG);
		 int unref =  tri::Clean<MyMesh>::RemoveUnreferencedVertex(referenceMeshVCG);
		 printf("Removed %i duplicate and %i unreferenced vertices from mesh \n",dup,unref);
		}


		currentMeshVCG.Clear();
		tri::Append<MyMesh,MyMesh>::Mesh(currentMeshVCG,referenceMeshVCG);



		printf("reducing it to %i\n",numberOfElements);

		vcg::tri::UpdateBounding<MyMesh>::Box(currentMeshVCG);

		// decimator initialization
		vcg::LocalOptimization<MyMesh> DeciSession(currentMeshVCG, &qparams);

		int t1=clock();
		DeciSession.Init<MyTriEdgeCollapse >();
		int t2=clock();
		printf("Initial Heap Size %i\n",DeciSession.h.size());

		DeciSession.SetTargetSimplices(numberOfElements);
		DeciSession.SetTimeBudget(10.0f);
		if(TargetError< numeric_limits<float>::max() ) DeciSession.SetTargetMetric(TargetError);

		while(DeciSession.DoOptimization() && currentMeshVCG.fn>numberOfElements && DeciSession.currMetric < TargetError)
		printf("Current Mesh size %7i heap sz %9i err %9g \r",currentMeshVCG.fn,DeciSession.h.size(),DeciSession.currMetric);
		int t3=clock();
		printf("mesh  %d %d Error %g \n",currentMeshVCG.vn,currentMeshVCG.fn,DeciSession.currMetric);
		printf("\nCompleted in (%i+%i) msec\n",t2-t1,t3-t2);

		//save as stl
		vcg::tri::io::ExporterSTL<MyMesh>::Save(currentMeshVCG,outfile);

}


}
