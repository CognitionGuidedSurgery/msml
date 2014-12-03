#!/bin/bash -x

mkdir cbuild;
cd cbuild;
cmake -DVTK_DIR=../cache/VTK-6.1.0-BUILD/ \
      -DTETGEN_INCLUDE_DIRS=../cache/tetgen1.5.0 \
      -DTETGEN_LIBRARY=../cache/tetgen-build/libtet.a \
      ../operators
make -j 3;
exit 
