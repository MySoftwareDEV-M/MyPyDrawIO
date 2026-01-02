from typing import cast

import MyPyDrawIO.File              as File
import MyPyDrawIO.Libraries         as Libraries
import MyPyDrawIO.Page              as Page
import MyPyDrawIO.Vertex            as Vertex
import MyPyDrawIO.Edge              as Edge
import MyPyDrawIO.Element           as Element
import MyPyDrawIO.Geometry          as Geometry
import MyPyDrawIO.EdgeStyle         as EdgeStyle
import MyPyDrawIO.Points            as Points

import json
import os
import xmltodict
import copy

###################################################################################################
# Libraries
libraries = Libraries.Libraries()
libraries.loadLibrary("./Libraries/MainLibrary.xml")

mainlibrary = libraries.library("MainLibrary")
definition_edge = mainlibrary.edge("EDGE")
definition_list = mainlibrary.vertex("LIST")
definition_list_item = mainlibrary.vertex("LIST ITEM")
# for vertex in mainlibrary.vertices():
    # print(json.dumps(vertex, indent=3))

###################################################################################################
# File
fileName_open   = "./TEST Edges.xml"
fileName_saveAs = "./TEST Edges Modified.xml"
# fileName_open   = fileName_saveAs

file = File.File(fileName_open)
page = file.pages()[0]
root = page.rootElement()

# print("###################################")
elementTree = page.elementTree()
# print("###################################")
# elementTree.dump(["@id", "@style"])

criterias = {
    # "@id" : "iDYZMT0QqaAdwt2RhsGk-5",
    "@value" : "target",
    # "@vertex" : "1",

    # "style" : {
    #     "rounded" : "1",
    #     # "strokeColor" : "none",
    #     # "text" : None
    # },

    "mode" : "ANY"
}
elements = elementTree.getElements(criterias)
# elementTree.dump(["@label", "@value"])

print("ELEMENTS: ")
# sourceVertex = Vertex.Vertex()
# vertex = Vertex.Vertex()
vertex = None
# edge = None
for _element in elements:
    # _element.dump(keys=["@id", "@value", "@label", "@style"], descandents=1)
    vertex = _element
    # _element.dump()

# vertexStyle = (_element["content"]["@style"])

vertexStyle = vertex.style()
print(json.dumps(vertexStyle.points(), indent=3))

points = Points.Points.CORNERS
points.append(Points.Points.N)
points.append(Points.Points.NEE)

vertexStyle.setPoints(points)
vertex.setStyle(vertexStyle)



file.saveAs(fileName_saveAs)