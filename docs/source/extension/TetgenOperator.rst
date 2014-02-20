TetgenOperator Extension
--------------------------

Test cpp

.. cpp:type:: MSML::TetgenOperators

	This ist my great class

    .. cpp:member:: TetgenOperators()
	
	    Constructor

    .. cpp:member::  ~TetgenOperators()

    .. cpp:member:: static bool CreateVolumeMesh(const char* infile, const char* outfile, bool preserveBoundary, bool isQuadratic )

    .. cpp:member:: static std::string CreateVolumeMeshPython(std::string infile, std::string outfile, bool preserveBoundary);

    .. cpp:member:: static bool CreateVolumeMesh(vtkPolyData* inputMesh, vtkUnstructuredGrid* outputMesh, bool preserveBoundary, bool isQuadratic );


``Test from documentation``

.. cpp:function:: bool namespaced::theclass::method(int arg1, std::string arg2)

   Describes a method with parameters and types.

.. cpp:function:: bool namespaced::theclass::method(arg1, arg2)

   Describes a method without types.

.. cpp:function:: const T &array<T>::operator[]() const

   Describes the constant indexing operator of a templated array.

.. cpp:function:: operator bool() const

   Describe a casting operator here.

.. cpp:function:: constexpr void foo(std::string &bar[2]) noexcept

   Describe a constexpr function here.

.. cpp:member:: std::string theclass::name

.. cpp:member:: std::string theclass::name[N][M]

.. cpp:type:: theclass::const_iterator

	  
