Installation
----------------------

MSML uses a lot of other libraries for his native operators and requires some Python packages for itself.
Following libraries are required:

* `Visualization Toolit <http://vtk.org>`_ (required)
* `Tetgen http://wias-berlin.de/software/tetgen/>`_ (optional)
* `Computational Geometry Algorithms Library (CGAL) <https://www.cgal.org/>`_ (optional)
* `VCG Library <http://vcg.isti.cnr.it/~cignoni/newvcglib/html/>`_ (optional)

You should start with cloning the repository in your directory of choice (e.g. `$HOME/workspace`)::

    $ git clone https://github.com/CognitionGuidedSurgery/msml.git


Installation Linux
^^^^^^^^^^^^^^^^^^

This manual should work on common Linux systems. There is a `build script <https://github.com/CognitionGuidedSurgery/msml/blob/master/share/install_ubuntu12.04.sh>`_ for Ubuntu 12.04.

You can simple execute following commands. ::

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

     $  sudo apt-get install libvtk5.8 libvtk5-dev # UBUNTU

2. Tetgen  (optional) ::

     $ apt-get install tetgen libtet1.4-dev libtet1.4 #UBUNTU/DEBIAN

We recommend installing the newest `version 1.5 <http://wias-berlin.de/software/tetgen/#Download>`_.
Tetgen is in the *non-free* repository under Debian and Debian *Sid* provides tetgen1.5.

3. VCG lib (optional) ::

     $ apt-get install meshlab vcglib # UBUNTU/DEBIAN -> library ist header-only

4. CGAL (optional) ::

     $ sudo apt-get install libcgal-dev

Compiling the C++ operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a folder for the build processing and execute `cmake`::

    $ mkdir cbuild && cd cbuild
    $ cmake ../operators && make -j


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

Configure the Python enviroment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Download and install Python (take care for boost compatibility, version 2.7.5 tested) http://www.python.org/ftp/python/2.7.5/python-2.7.5.amd64.msi
* Download and install Eclipse (Kepler Service Release 1 tested) http://artfiles.org/eclipse.org//technology/epp/downloads/release/kepler/SR1/eclipse-standard-kepler-SR1-win32-x86_64.zip
* Download and copy Pydev to eclipse folder (http://sourceforge.net/projects/pydev/files/pydev/PyDev%203.3.3/ tested)
* Use PIP or easy_install to install required python packages (see requirements.txt)


CMake Build Process
^^^^^^^^^^^^^^^^^^^

.. todo::

   Explain the MODULE_\* Variables
   Explain how to set own tetgen/vtk library
