"""
Vertices are derived from [Elements](./Element.html).
With respect to the Element base class, this derived class provides additional functionality related to vertices.

- CONNECTION POINTS
    - [source()](../MyPyDrawIO/Edge.html#Edge.source)
- STYLE & GEOMETRY
    - [style()](../MyPyDrawIO/Vertex.html#Vertex.style)
    - [geometry()](../MyPyDrawIO/Vertex.html#Vertex.geometry)

## Connection points
For vertices you can define connection points. Details on connection points can be found here at
the [Points](../MyPyDrawIO/Points.html) page.

Connection points are helpful for manually connecting edges to vertices in draw.io,
as the edges end can snap into place at the connection points.

For automatic creation of diagrams using MyPyDrawIO connection points of the vertices are of minor relevance, 
since connecting edges with vertices is something you do using
[edge functions](../MyPyDrawIO/Edge.html).

Use cases for connection points in the context of MyPyDrawIO might be:
- When creating a diagram with MyPyDrawIO, that will be edited manually in the further process, connection points will support in the manual process.
- You might read out the connection points of a vertex to determine the point to connect the edge to.

HINT:
<br>If you have no connection points defined for a vertex, within draw.io a default set of connection points will be displayed.

To set and get connection points of a vertex, use the
[vertex style](../MyPyDrawIO/VertexStyle.html).
"""
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

import MyPyDrawIO.Element           as Element
import MyPyDrawIO.VertexGeometry    as VertexGeometry
import MyPyDrawIO.VertexStyle       as VertexStyle

import uuid

class Vertex(Element.Element):
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, content : dict = None, parent = None):
        """
        """
        if content == None:
            content = {
                "@id" : str(uuid.uuid4()),
                "@vertex" : "1",
                "@value" : "",
                "@parent" : "1",
                "@style" : "rounded=0;whiteSpace=wrap;html=1;",
                "mxGeometry" : {
                    "@height" : 10,
                    "@width" : 10,
                    "@as" : "geometry"
                }
            }
            if parent != None:
                content["@parent"] = parent.id()

        super().__init__(content, parent)

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def geometry(self) -> VertexGeometry.VertexGeometry:
        """
        Returns a vertex geometry instance.
        """
        if(self.isObject()):
            if "mxGeometry" in self["content"]["mxCell"]:
                return VertexGeometry.VertexGeometry(self["content"]["mxCell"]["mxGeometry"])
        else:
            if "mxGeometry" in self["content"]:
                return VertexGeometry.VertexGeometry(self["content"]["mxGeometry"])
        
        return VertexGeometry.VertexGeometry()
    
    #----------------------------------------------------------------------------------------------
    def style(self) -> VertexStyle.VertexStyle:
        """
        Returns an vertex style instance.
        """
        if(self.isObject()):
            if "@style" in self["content"]["mxCell"]:
                return VertexStyle.VertexStyle(self["content"]["mxCell"]["@style"])
        else:
            if "@style" in self["content"]:
                return VertexStyle.VertexStyle(self["content"]["@style"])
        
        return VertexStyle.VertexStyle()
    
###################################################################################################
# Public global functions / Helper functions

