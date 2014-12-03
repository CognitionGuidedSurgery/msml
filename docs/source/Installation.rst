Installation
------------

MSML uses a lot of other libraries for its native operators and requires some Python packages for itself.
Following libraries are required:

* `Visualization Toolit <http://vtk.org>`_ (required)
* `Tetgen <http://wias-berlin.de/software/tetgen/>`_ (optional)
* `Computational Geometry Algorithms Library (CGAL) <https://www.cgal.org/>`_ (optional)

You should start with cloning the repository in your directory of choice (e.g. `$HOME/workspace`)::

    $ git clone https://github.com/CognitionGuidedSurgery/msml.git


Installation Linux
^^^^^^^^^^^^^^^^^^

This manual should work on common Linux systems. There is a `build script <https://github.com/CognitionGuidedSurgery/msml/blob/master/share/install_ubuntu12.04.sh>`_ for Ubuntu 12.04.

You can simply execute following commands. ::

    $ cd msml                              # change directory to msml root
    $ sudo pip install -r requirements.txt # install python requirements

You should consider the use of virtual environments for developtment
Probably the installation of `python-lxml` fails, because of missing `libxml-dev` headers.
You can `install it the headers <https://stackoverflow.com/questions/6504810/how-to-install-lxml-on-ubuntu>`_ or the precompiled version from your distribution: ::

    $ sudo apt-get install python-lxml

Operators Requirements
~~~~~~~~~~~~~~~~~~~~~~

You only need Python, Swig and VTK to run MSML.
However, more operators can be unlocked by installing the appropriate 3rd-party libraries.

0. Install Python and Swig. ::

     $ sudo apt-get install python-dev swig

1. You can install the VTK from your distribution ::

     $  sudo apt-get install libvtk6 libvtk6-dev # for UBUNTU 14.0x (in case your distribution is < 14, link vtk 6.x path in Cmake, see below.)

2. Tetgen  (optional) ::

     $ sudo apt-get install tetgen libtet1.5-dev libtet1.5 # for UBUNTU/DEBIAN 14.0x (in case your distribution is < 14, link vtk 6.x path in Cmake, see below.)

We recommend installing the newest `version 1.5 <http://wias-berlin.de/software/tetgen/#Download>`_.
Tetgen is in the *non-free* repository under Debian and Debian *Sid* provides tetgen1.5.

4. CGAL (optional) ::

     $ sudo apt-get install libcgal-dev

Compiling the C++ operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a folder for the build processing and execute `cmake`::

    $ mkdir cbuild && cd cbuild
    $ cmake ../operators
      # link vtk/tetgen with switch vtk_DIR (i.e. folder where vtkconfig.cmake is located) or tetgen_DIR.
      # link svn if necessary (can be installed by sudo apt-get install subversion)
    $ make -j


Installation of Simulation Environments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See separate notes on SOFA, HiFlow3, Abaqus and FeBIO.


Installation Windows
^^^^^^^^^^^^^^^^^^^^

Building the MSML Operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build for 64bit with Visual Studio 2010

* Download and install CMake (tested version 2.8.11.2)
* Download and install Boost (tested version: http://sourceforge.net/projects/boost/files/boost-binaries/1.55.0-build2/ - compatible with Python 2.7.5)
* Make sure you have a enviroment variable BOOST_ROOT pointing to your boost directory.
* In BOOST_ROOT: Rename the the folder which contains the compile libraries to lib.
* Download and build VTK with CMake (version 5.10.1 tested - 6.x does not work yet) http://www.vtk.org/files/release/5.10/vtk-5.10.1.zip
* Download and build CGAL with CMake (version 4.3 tested)  https://gforge.inria.fr/frs/download.php/32993/CGAL-4.3-Setup.exe
* Download and build Tetgen with CMake (version 1.5 tested)  http://wias-berlin.de/software/tetgen/1.5/src/tetgen1.5.0.zip
* Download VCG via SVN (https://svn.code.sf.net/p/vcg/code/trunk/vcglib)
* Use CMake to configure and generate the MSML visual studio .sln file
* Select the "operator" subdirectory of the msml repository as the source folder and choose build folder.
* Fill in all notFound paths

