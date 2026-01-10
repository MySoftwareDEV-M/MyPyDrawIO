import MyPyDrawIO.File              as File
import MyPyDrawIO.Libraries         as Libraries
import MyPyDrawIO.Page              as Page
import MyPyDrawIO.Vertex            as Vertex
import MyPyDrawIO.Edge              as Edge
import MyPyDrawIO.Element           as Element
import MyPyDrawIO.Geometry          as Geometry
import MyPyDrawIO.EdgeStyle         as EdgeStyle
import MyPyDrawIO.Points            as Points

###################################################################################################
# Libraries
libraries = Libraries.Libraries()

# access main library
libraries.loadLibrary("./Libraries/MainLibrary.xml")
mainlibrary = libraries.library("MainLibrary")

###################################################################################################
# File
fileName_open   = "./TEST Edges.xml"
fileName_saveAs = "./TEST Edges Modified.xml"

file = File.File(fileName_open)
page = file.pages()[0]
root = page.rootElement()

page.rootElement().dump()

# vertex = Vertex.Vertex(parent=root)
# geometry = vertex.geometry()
# geometry.setX(100)
# geometry.setY(100)
# geometry.setWidth(100)
# geometry.setHeight(100)
# vertex.setGeometry(geometry)

# style = vertex.style()
# style.setValue("rounded", "1")
# vertex.setStyle(style)

# print("###################################")
# vertex.dump()

edge = Edge.Edge(None, parent=root)


file.saveAs(fileName_saveAs)