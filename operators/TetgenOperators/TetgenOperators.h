/*=========================================================================

  Program:   The Medical Simulation Markup Language
  Module:    Operators, TetgenOperators
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


#ifndef __TetgenOperators_h
#define __TetgenOperators_h

// ****************************************************************************
// Includes
// ****************************************************************************
#include <vector>
#include <limits>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#include <vtkPolyData.h>
#include <vtkUnstructuredGrid.h>

#include "../MSML_Operators.h"
#include "TetgenSettings.h"

using namespace std;

/*MSMLDOC

TetgenOperators
===============

.. cpp:namespace:: MSML::Tetgen

Weit hinten, hinter den Wortbergen, fern der Länder Vokalien und Konsonantien leben die Blindtexte. Abgeschieden wohnen sie in Buchstabhausen an der Küste des Semantik, eines großen Sprachozeans. Ein kleines Bächlein namens Duden fließt durch ihren Ort und versorgt sie mit
Weit hinten, hinter den Wortbergen, fern der Länder Vokalien und Konsonantien leben die Blindtexte. Abgeschieden wohnen sie in Buchstabhausen an der Küste des Semantik, eines großen Sprachozeans. Ein kleines Bächlein namens Duden fließt durch ihren Ort und versorgt sie mit

See: :py:mod:`msml.ext.tetgen`

*/

namespace MSML {
    namespace Tetgen {
    /*MSMLDOC
        .. cpp:function:: bool CreateVolumeMesh(const char* infile, const char* outfile, bool preserveBoundary, bool isQuadratic )

          :param const char* infile:  Weit hinten, hinter den Wortbergen,
          :param const char* outfile: Weit hinten, hinter den Wortbergen,
          :param bool preserveBoundary: Weit hinten, hinter den Wortbergen,
          :param bool isQuadratic: Weit hinten, hinter den Wortbergen,


    */

    LIBRARY_API bool TetgenCreateVolumeMesh(const char* infile, const char* outfile, TetgenSettings settings, bool isQuadratic );

    /*MSMLDOC
        .. cpp:function:: std::string CreateVolumeMeshPython(std::string infile, std::string outfile, bool preserveBoundary)

            Jemand musste Josef K. verleumdet haben, denn ohne dass er etwas Böses getan hätte, wurde er eines Morgens verhaftet. »Wie ein Hund!« sagte er, es war, als sollte die Scham ihn überleben. Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren.
    */

    LIBRARY_API std::string TetgenCreateVolumeMeshPython(std::string infile, std::string outfile,
        bool preserveBoundary,
        double maxEdgeRadiusRatio,
        int minDihedralAngleDegrees,
        double maxTetVolumeOrZero,
        int optimizationLevel, // range from 0 to disable optimizations to 10 for maximum number of optimization iterations.
        bool optimizationUseEdgeAndFaceFlips,
        bool optimizationUseVertexSmoothing,
        bool optimizationUseVertexInsAndDel);

    /*MSMLDOC
        .. cpp:function:: bool CreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh, bool preserveBoundary, bool isQuadratic );

            Jemand musste Josef K. verleumdet haben, denn ohne dass er etwas Böses getan hätte, wurde er eines Morgens verhaftet. »Wie ein Hund!« sagte er, es war, als sollte die Scham ihn überleben. Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren.
    */
    LIBRARY_API bool TetgenCreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh, TetgenSettings settings, bool isQuadratic );
    }
}


#endif /* TetgenOperators_h */
