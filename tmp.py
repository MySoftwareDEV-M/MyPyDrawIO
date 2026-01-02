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

###################################################################################################
# Libraries
libraries = Libraries.Libraries()

# access main library
libraries.loadLibrary("./Libraries/MainLibrary.xml")
mainlibrary = libraries.library("MainLibrary")

# print content of main library
print("Vertices provided by MainLibrary")
for vertex in mainlibrary.vertices():
    print(" - " + vertex)

print("Edges provided by MainLibrary")
for edge in mainlibrary.edges():
    print(" - " + edge)

# some get element definitions
definition_edge = mainlibrary.edge("EDGE")
definition_vertex = mainlibrary.vertex("RECTANGLE")

###################################################################################################
# File
file = File.File("./MyDrawIOFile.drawio")
page = file.pages()[0]

# create vertices and edge, using the element definitions
rect_01 = page.createVertex(definition_vertex)

rect_02 = page.createVertex(definition_vertex)
geometry = rect_02.geometry()
geometry.setX(300)
rect_02.setGeometry(geometry)

page.createEdge(definition_edge, rect_01.id(), rect_02.id())

file.save()

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