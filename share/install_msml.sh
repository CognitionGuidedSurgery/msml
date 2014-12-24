#!/bin/bash -x

mkdir cbuild;
cd cbuild;
ROOT=/home/ubuntu/msml/
cmake -DVTK_DIR=$ROOT/cache/VTK-6.1.0-INSTALL/lib/cmake/vtk-6.1/ \
      -DTETGEN_INCLUDE_DIRS=$ROOT/cache/tetgen1.5.0 \
      -DTETGEN_LIBRARY=$ROOT/cache/tetgen-build/libtet.a \
      -DSOFA_EXECUTABLE=/home/ubuntu/msml/cache/sofa-build/bin/runSofa \
       $ROOT/operators
make -j 3;
exit 
