__author__ = 'weigl'

import msml.ext.xnat as X

X.xnat_get(filename="Bunny6000Surface.vtk",
           resource = "first_session",
           project='MSML_TEST',
           subject="Bunny",
           localname="/tmp/B6S.vtk")

X.xnat_get(filename="LiverSurface.stl",
           resource = "tr",
           project='MSML_TEST',
           localname="/tmp/LS.stl")


X.xnat_put(localname="/tmp/LS.stl",
           project="MSML_TEST",
           resource="tr", subject="Bunny",
           filename="TestUpload.stl",
           _content = "Triangles", _format = "STL", _tags="Test,Weigl"
)

X.xnat_put(localname="/tmp/B6S.vtk",
           project="MSML_TEST",
           resource="tr",
           filename="a.stl",
           _content = "Surface", _format = "VTK", _tags="Test,Weigl"
)