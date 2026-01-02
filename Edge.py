"""
Edges are derived from [Elements](./Element.html).
With respect to the Element base class, this derived class provides additional functionality related to edges.

- CONNECTION OF EDGES WITH VERTICES 
    - [source()](../MyPyDrawIO/Edge.html#Edge.source)
    - [setSource()](../MyPyDrawIO/Edge.html#Edge.setSource)
    - [exit()](../MyPyDrawIO/Edge.html#Edge.exit)
    - [setExit()](../MyPyDrawIO/Edge.html#Edge.setExit)
    - [target()](../MyPyDrawIO/Edge.html#Edge.target)
    - [setTarget()](../MyPyDrawIO/Edge.html#Edge.setTarget)
    - [entry()](../MyPyDrawIO/Edge.html#Edge.entry)
    - [setEntry()](../MyPyDrawIO/Edge.html#Edge.setEntry)
- STYLE & GEOMETRY
    - [style()](../MyPyDrawIO/Edge.html#Edge.style)
    - [geometry()](../MyPyDrawIO/Edge.html#Edge.geometry)

## Some vocabulary (start, end, source, target)
Since edges are lines, they have a start and an end.

In draw.io, when you use these little blue arrows to draw a new edge (green circle in the image below),
the edge will start at this vertex and this side of the edge will become the start of the edge.
This vertex is the source of the edge.
The vertex you connect the other side of the edge to will be its target and that side of the edge will be its end.

This wording "start" and "end" is used in draw.io on the edges style format panel as you can see in the picture below.

<img src="./images/MyPyDrawIO-Edges and Vertices.png">

As an overview, we get these terms:
- source / source vertex
<br>The vertex from which an edge starts.
- target / target vertex
<br>The vertex at which an edge ends.
- start / start of an edge
<br>The side of the edge that is defined as its start.
- end / end of an edge
<br>The side of the edge that is defined as its end.

## Connecting edges to vertices
So if you want to connect the start of an edge to a vertex, you have to set the source at least.
If you do not set any exit coordinates, the start will be floating around the vertex.
Otherwise the start will be fixed to the coordinate.

```
# set source vertex
edge.setSource(sourceVertex.id())

# set exit, using egde
exit = {
"x" : 0.5,
"y" : 0.0,
"dx" : 0,
"dy" : 0
}
# coordinates in dict
edge.setExit(exit)
# coordinates as list
edge.setExit([0.5, 0.0, 0.0, 0.0])
# coordinates as Point
edge.setExit(Points.Points.N)

# set exit, using egde style
edgeStyle = edge.style()
edgeStyle.setExit([0.5, 0.0, 0.0, 0.0])
edge.setStyle(edgeStyle)
```

As you can see in the code example, there are many ways to set the exit (and the entry coordinates respectively).
Actually the coordinates will be set on the edge style, since draw.io saves the coordinates there.
Since connecting edges with vertices has a strong connection to edges, the convinient functions
[exit()](../MyPyDrawIO/Edge.html#Edge.exit),
[setExit()](../MyPyDrawIO/Edge.html#Edge.setExit),
[entry()](../MyPyDrawIO/Edge.html#Edge.entry), and
[setEntry()](../MyPyDrawIO/Edge.html#Edge.setEntry)
are provided for the edge class.
This way there is no need to retrieve the style object as shown in the code example above 
leading to cleaner code.

Furthermore there are three ways to set the coordinates, which are
- coordinates in dict
- coordinates as list
- coordinates as [Point](../MyPyDrawIO/Points.html)
"""
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

import MyPyDrawIO.Element           as Element
import MyPyDrawIO.EdgeStyle         as EdgeStyle
import MyPyDrawIO.EdgeGeometry      as EdgeGeometry

class Edge(Element.Element):
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, content : dict, sourceID : str = None, targetID : str = None, parent = None):
        """
        """
        super().__init__(content, parent)

        if(sourceID != None):
            self.setValue("@source", sourceID)
        if(targetID != None):
            self.setValue("@target", targetID)

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def entry(self):
        """
        Returns the entry point as list [dx, dy, x, y].

        If the entry does not exist None is returned.

        For details see description above.

        This is a wraper function which just calls
        [EdgeStyle entry()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.entry)
        """
        style = self.style()
        return style.entry()
    
    #----------------------------------------------------------------------------------------------
    def exit(self):
        """
        Returns the exit point as list [dx, dy, x, y].

        If the exit does not exist None is returned.

        For details see description above.

        This is a wraper function which just calls
        [EdgeStyle exit()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.exit)
        """
        style = self.style()
        return style.exit()
    
    #----------------------------------------------------------------------------------------------
    def geometry(self) -> EdgeGeometry.EdgeGeometry:
        """
        Returns an edge geometry instance.
        """
        if(self.isObject()):
            if "mxGeometry" in self["content"]["mxCell"]:
                return EdgeGeometry.EdgeGeometry(self["content"]["mxCell"]["mxGeometry"])
        else:
            if "mxGeometry" in self["content"]:
                return EdgeGeometry.EdgeGeometry(self["content"]["mxGeometry"])
        
        return EdgeGeometry.EdgeGeometry()
    
    #----------------------------------------------------------------------------------------------
    def setSource(self, sourceID : str = None):
        """
        Sets the source (the vertex the start of the edge) is connected to.
        
        If sourceID is None, the source will be deleted.
        """
        if(sourceID == None):
            self.deleteKey("@source")
        else:
            self.setValue("@source", sourceID)
    
    #----------------------------------------------------------------------------------------------
    def setEntry(self, entry : dict):
        """
        Set coordinates, to connect the edge to the target vertex.

        entry can be a list, dict, or None
        - list --> [x, y, dx, dy]
        - dict --> dictionary with keys x, y, dx, and dy.
        - None --> coordinates will be deleted.

        For details see description obove.

        This is a wraper function which just calls
        [EdgeStyle setEntry()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.setEntry)
        """
        style = self.style()
        style.setEntry(entry)
        self.setStyle(style)
            
    #----------------------------------------------------------------------------------------------
    def setExit(self, exit : dict):
        """
        Set coordinates, to connect the edge to the target vertex.

        entry can be a list, dict, or None
        - list --> [x, y, dx, dy]
        - dict --> dictionary with keys x, y, dx, and dy.
        - None --> coordinates will be deleted.

        For details see description obove.

        This is a wraper function which just calls
        [EdgeStyle setExit()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.setExit)
        """
        style = self.style()
        style.setExit(exit)
        self.setStyle(style)
    
    #----------------------------------------------------------------------------------------------
    def setTarget(self, targetID : str = None):
        """
        Sets the target (the vertex the end of the edge) is connected to.
        
        If targetID is None, the source will be deleted.
        """
        if(targetID == None):
            self.deleteKey("@target")
        else:
            self.setValue("@target", targetID)
    
    #----------------------------------------------------------------------------------------------
    def source(self):
        """
        Returns the source (the vertex the start of the edge) is connected to.
        
        Retruns None if there is no connection to a source.
        """
        if(self.containsKey("@source")):
            return self.value("@source")
        
        return None
    
    #----------------------------------------------------------------------------------------------
    def style(self) -> EdgeStyle.EdgeStyle:
        """
        Returns an edge style instance.
        """
        if(self.isObject()):
            if "@style" in self["content"]["mxCell"]:
                return EdgeStyle.EdgeStyle(self["content"]["mxCell"]["@style"])
        else:
            if "@style" in self["content"]:
                return EdgeStyle.EdgeStyle(self["content"]["@style"])
        
        return EdgeStyle.EdgeStyle()
    
    #----------------------------------------------------------------------------------------------
    def target(self):
        """
        Returns the target (the vertex the end of the edge) is connected to.
        
        Retruns None if there is no connection to a target.
        """
        if(self.containsKey("@source")):
            return self.value("@source")
        
        return None

# ###################################################################################################
# # Public global functions / Helper functions
