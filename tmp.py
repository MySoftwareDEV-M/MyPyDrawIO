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
# fileName_open = fileName_saveAs

file = File.File(fileName_open)
page = file.pages()[0]
root = page.rootElement()

for element in root.children():
    print(element.label())
    for key in element.keys():
        print("- " + key)
    
    content = element["content"]
    for entry in content:
        print("  > " + entry)
    
    if "mxCell" in content:
        for key in content["mxCell"].keys():
            print("    - " + key)
    
    if not element.isObject():
        element.convertToObject()
        element.setProperty("@NEU", "HALLO")
    # element.deleteProperty("@NEU")


file.saveAs(fileName_saveAs)