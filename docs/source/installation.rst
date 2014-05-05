Installation 
----------------------

.. todo::
    
    Test TODO!!!


Unter Linux werden die Bibliotheken recht gut von CMake gefunden, unter Windows muss man oft mit Umgebungsvariablen nachhelfen.

Falls ihr eine Bibliothek nicht habt:
  
   - Die entsprechende Zeile in der CMakelists.txt auskommentieren (z.B. FIND_PACKAGE(VCG REQUIRED) )
   - Den Ordner in der CMakeLists.txt auskommentieren (z.B. ADD_SUBDIRECTORY(VCGOperators) )

Für die Zukunft brauchen wir dafür einen automatischen Mechanismus (sollte eigentlich in CMake kein Problem sein)

Linux
============================

  #. VTK (apt-get install VTK)
  #. Tetgen (apt-get install tetgen libtet1.4.2-dev libtet1.4.2).
  #. VCG lib (apt-get install meshlab vcglib) -> library ist header-only
  #. CGAL (apt-get install CGAL ?), bisher nur unter Windows getestet
     - CGAL_USE_VTK in CMake setzen. Image_3.cpp, zeile 202 patchen: 
       int vtk_type = vtk_image->GetPointData()->GetScalars()->GetDataType();
  #. Python und lxml

Die linux Bibliothekennamen sind noch ohne Gewähr -> bitte testen und korrigieren

Windows
=============================

VTK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * VTK source runterladen
  * mit CMake/VS kompilieren
  * wird von CMake später ohne Umgebungsvariable gefunden.

Tetgen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * Tetgen source runterladen
  * neues VisualStudio "projekt win32 console" erstellen und dann Projekt auf 64Bit?/library stellen
  * #define TETLIBRARY setzen.
  * Kompilieren nach Tetgen/lib/
  * Umgebungsvariable TETGEN_PATH Tetgen-Verzeichnis setzen (verzeichnis muss .h enthalten, Unterverzeichnis /lib muss die Tetgen.lib enthalten)

VCG LIB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * VCG lib über SVN laden (siehe http://vcg.isti.cnr.it/~cignoni/newvcglib/html/install.html)
  * Umgebungsvariable CG_PATH auf VCG-lib-Verzeichnis setzen (muss VCG und einige anderen Ordner enthalten)

CGAL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * CGAL source runterladen
  * wird von CMake später ohne Umgebungsvariable gefunden.
  * Version 4.1 getestet

Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * Pyhton installieren (2.6 getestet)
  * lxml.de installieren (binaries für 2.6 von http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml getestet) 
  * CMake patch für FindPhyton unter Win7 64bit: http://www.mail-archive.com/cmake@cmake.org/msg46586.html anwenden
  * Aus den CMake targets werden mit Boost Phyton Module erzeugt. Version Boost<-->Phyton muss passen (Boost 1.51.0 getestet)

