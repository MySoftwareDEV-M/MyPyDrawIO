"""
# Introduction
## The big picture
MyPyDrawIO provides convenient functions to read, create, and manipulate draw.io files.
Thereby it can also read draw.io libraries, 
so you can use the shapes provided by a library in MyPyDrawIO and insert them into files.

All you have to do is write “your Python program” using MyPyDrawIO and you’re done.

<img src="./images/MyPyDrawIO-Big Picture.png">

MyPyDrawIO writes to the draw.io files, which are saved somewhere ("disc" in the picture). 
These files can be accessed via some draw.io application (on the left) or via "your python program" (on the right).
The final result of creation and editing is always contained in the draw.io files.
Therefore the data structure in these files is central.

MyPyDrawIO is based on this understanding. 
Additionally, it is reverse engineered, using the data structure as anchor.
I make every effort to design MyPyDrawIO to be user-friendly and function-oriented 
without requiring users to know technical details.
But since MyPyDrawIO is essentially an interface for manipulating draw.io files, 
it's useful to know some technical details.

## Recommendations, using this documentation
Well, this project has become quite extensive.

This documentation helps to keep an overview myself but also will help you to use MyPyDrawIO.
So for you and me, let's give some guidance:

- Make yourself familiar with MyPyDrawIO by reading this page:
    - [MyPyDrawIO as class & component diagram](./MyPyDrawIO.html#mypydrawio-as-class-component-diagram)
    shows all classes in a continuous image. So this gives you a good overview what you are dealing with.
    - [Using MyPyDrawIO](./MyPyDrawIO.html#using-mypydrawio)
    explains best practices to use MyPyDrawIO, also referencing to other pages with more details on specific topics.
    - [Relationship between MyPyDrawIO and the file structure](./MyPyDrawIO.html#relationship-between-mypydrawio-and-the-file-structure)
    explains the technical details between MyPyDrawIO and the draw.io files that are helpful to use MyPyDrawIO.
    You don't need to understand that section in detail, as MyPyDrawIO tries to encapsulate the technical details.

- Go and play:
    - [Using MyPyDrawIO](./MyPyDrawIO.html#using-mypydrawio) 
    is a good starting point to explore different use cases.
    For use cases that require a higher level of understanding, 
    this understanding is described in that section.
    Pages are referenced that provide concrete code examples,
    allowing you to quickly try out the use cases.

# MyPyDrawIO as class & component diagram

## files, pages, vertices and edges
draw.io files are represented [files](./MyPyDrawIO/File.html).
Within one file there are one or more [pages](./MyPyDrawIO/Page.html).
On each page there can be [vertices](./MyPyDrawIO/Vertex.html) and
[edges](./MyPyDrawIO/Edge.html).

<img src="./images/MyPyDrawIO-Class & Component Diagram I.png">

## elements = vertices and edges
[Vertices](./MyPyDrawIO/Vertex.html) and [edges](./MyPyDrawIO/Edge.html) have certain things in common.
These common things are bundeled in the [element base class](./MyPyDrawIO/Element.html#Element).
This base class is a pure MyPyDrawIO concept.

The specific appearence and behavior of these elements can be controlled by their geometry and their style. 
Again the specific geometries and styles of the vertices and edges have some things in common.
Therefore there is also generalization for these. So we have
- the [geometry base class](./MyPyDrawIO/Geometry.html#Geometry) with
    - specific [vertex geometry](./MyPyDrawIO/VertexGeometry.html)
    - specific [edge geometry](./MyPyDrawIO/EdgeGeometry.html)

- the [style base class](./MyPyDrawIO/Style.html#Style) with
    - specific [vertex style](./MyPyDrawIO/VertexStyle.html)
    - specific [edge style](./MyPyDrawIO/EdgeStyle.html)

Anyway, when you use MyPyDrawIO, you should use the specific classes and not the base classes 
unless stated otherwise.

<img src="./images/MyPyDrawIO-Class & Component Diagram II.png">

## libraries
To use draw.io libraries, there is the [libraries class](./MyPyDrawIO/Libraries.html) which is a [singleton](https://en.wikipedia.org/wiki/Singleton_pattern).
To use specific draw.io libraries just [load](./MyPyDrawIO/Libraries.html#Libraries.loadLibrary) them.
For each draw.io library you load, there will be an [instance of a library](./MyPyDrawIO/Library.html).
All shapes of the draw.io library will be provided as [ElementDefinition](./MyPyDrawIO/ElementDefinition.html).
These can be used with the pages [createVertex()](./MyPyDrawIO/Page.html#Page.createVertex) 
and [createEdge()](./MyPyDrawIO/Page.html#Page.createEdge) functions to create vertices and edges.

<img src="./images/MyPyDrawIO-Class & Component Diagram III.png">

## the whole class & component diagram
To get an overall impression, here is the class & component diagram from MyPyDrawIO.
<img src="./images/MyPyDrawIO-Class & Component Diagram All.png">

# Using MyPyDrawIO
All examples use aliases for the MyPyDrawIO classes as shown in this code example:
```
import MyPyDrawIO.File              as File
import MyPyDrawIO.Libraries         as Libraries

file = File.File("./MyDrawIOFile.drawio)
...
```
If you find examples without the import and alias definition, you should add them yourself.

## Manipulating objects and extending MyPyDrawIO functionality
The MyPyDrawIO classes are derived from [dict](https://www.w3schools.com/python/python_dictionaries.asp) 
and most relevant data is stored as key value pairs within these dicts.
So in theory you could access and manipulate this data.
To manipulate data it is recommended to use spedific functions like 
[Element > value()](./MyPyDrawIO/Element.html#Element.value) and [Element > setValue()](./MyPyDrawIO/Element.html#Element.setValue)
or to use the 
[vertex geometry](./MyPyDrawIO/VertexGeometry.html), [edge geometry](./MyPyDrawIO/EdgeGeometry.html), 
[vertex style](./MyPyDrawIO/VertexStyle.html), or [edge style](./MyPyDrawIO/EdgeStyle.html) objects
to avoid inconsistent data.

Vertices and edges are the central elements in draw.io, since draw.io is about creating drawings 
where the elements are configured and connected in a specific way.
There are very many configurations for these elements (text, color, styles, geometry, behavior, ...).
MyPyDrawIO can only provide a limited set of specialized functions to use all of these features 
but does provide a framework to allow you to extend it for your needs.
So you can use functions like
[Element > dump()](./MyPyDrawIO/Element.html#Element.dump),
[Element > keyList()](./MyPyDrawIO/Element.html#Element.keyList),
[Element > keySet()](./MyPyDrawIO/Element.html#Element.keySet),
[Style > keys()](./MyPyDrawIO/Style.html#Style.keys)
to see which keys there are and then set and manipulate them to add functionality you need.

With respect to section [elements = vertices and edges](./MyPyDrawIO.html#elements-vertices-and-edges)
there are there levels to add functionality.
- element level, add functionality in
    - [Vertices](./MyPyDrawIO/Vertex.html) and
    - [edges](./MyPyDrawIO/Edge.html)
- style level, add functionality in
    - [vertex geometry](./MyPyDrawIO/VertexGeometry.html)
    - [edge geometry](./MyPyDrawIO/EdgeGeometry.html)
- gemometry level, add functionality in
    - [vertex style](./MyPyDrawIO/VertexStyle.html)
    - [edge style](./MyPyDrawIO/EdgeStyle.html)

## Identifier id()
draw.io uses identifier to identify objects like [pages](./MyPyDrawIO/Page.html#Page.id), 
and the [elements](./MyPyDrawIO/Element.html#Element.id) ([vertex](./MyPyDrawIO/Vertex.html), and [edge](./MyPyDrawIO/Edge.html)).
The identifiers should not be altered since they are used to create parent relationships between.
You can read their value and use it to search for elements or create relationships.

## File and page handling
Handling files is straight forward.
There are simple code examples on the [file page](./MyPyDrawIO/File.html).

## Parent child relationship
Each page provides a [rootElement](./MyPyDrawIO/Page.html#Page.rootElement).
All edges are direct children of this root element.
Top level vertices are also children of this root element.
If a vertex is a child of another vertex, it will be attached as its child,
resulting in a parent child relationship.

<img src="./images/MyPyDrawIO-Parent Child Relationship.png">

## Styles
As already mentioned in sections
[Manipulating objects and extending MyPyDrawIO functionality](./MyPyDrawIO.html#manipulating-objects-and-extending-mypydrawio-functionality)
and 
[elements = vertices and edges](./MyPyDrawIO.html#elements-vertices-and-edges)
there are many configurations for vertices and edges.

The gerneral aspects of styles are described on the [Style](./MyPyDrawIO/Style.html) page.
This includes
- configuring styles for vertices and edges.
- specifics of styles.

Aspects that are specific to vertices, or edges respectively are described on the pages:
- [vertex style](./MyPyDrawIO/VertexStyle.html) or
- [edge style](./MyPyDrawIO/EdgeStyle.html).

## Geometry
AUSSTEHEND
AUSSTEHEND
AUSSTEHEND

## Connecting edges with vertices
With MyPyDrawIO you can connect edges with vertices using python. 
This is done with functions provided by [edges](./MyPyDrawIO/Edge.html).
In draw.io you can connect them manually. 
This is supported by connection points to provide specific coordinates as explained on the [vertices](./MyPyDrawIO/Vertex.html) page.

Further information can be found on the [points](./MyPyDrawIO/Points.html) page.

## Using draw.io libraries

When creating libraries to be used with MyPyDrawIO I recommend to provide a title to the elements of the library.
This is simply done by editing the library (blue arrow) and adding a title (green arrows).

These titles are used in [Library.vertex()](.//MyPyDrawIO/Library.html#Library.vertex) and [Library.edge()](.//MyPyDrawIO/Library.html#Library.edge) functions
to select the shape you want to use.

<img src="./images/MyPyDrawIO-Libraries.png">

# Relationship between MyPyDrawIO and the file structure
This section describes the mapping between MyPyDrawIO and and the draw.io data structure.
This helps understanding the concepts of MyPyDrawIO which strongly follow the given data structure.

But for simply using MyPyDrawIO you can also skip this section.

## draw.io files
draw.io files are saved in XML format.
The relation of the MyPyDrawIO classes to this XML format is sketched in the picture below.
For the sake of clarity, I have not added the MyPyDrawIO : Geometry, MyPyDrawIO : Style, and their derived classes.
Highlighting the styles by the yellow rectangles and the geometry by the orange rectangle should do the job.

The structure of this XML is mostly intuitve. There are some aspects you just need to know. 
This is done within the subsections.

<img src="./images/MyPyDrawIO-MyPyDrawIO Modules with draw.io files.png", height = 700>

MyPyDrawIO maps to the data structure in this way:
- the [MyPyDrawIO : File](./MyPyDrawIO/File.html) maps to the mxFile XML element.
<br> The mxFile has some attributes, we do not have to care about.
- within one file the [MyPyDrawIO : Page](./MyPyDrawIO/Page.html) maps to the diagram XML element.
<br> For each page there will be one diagram XML element.
- each page has its elements. Within the XML file these elements are mxCells or objects (more on this below).
<br> if an element or object is a vertex or edge is controlled by the XML attributes "vertex" and "edge".
    - [MyPyDrawIO : Vertex](./MyPyDrawIO/Vertex.html) represents a mxCell or object, where the mxCell has the attribute "vertex".
        - the style of a vertex is represented by [MyPyDrawIO : VertexStyle](./MyPyDrawIO/VertexStyle.html)
        - the geometry of a vertex is represented by [MyPyDrawIO : VertexGeometry](./MyPyDrawIO/VertexGeometry.html)
    - [MyPyDrawIO : Edge](./MyPyDrawIO/Edge.html) represents a mxCell or object, where the mxCell has the attribute "edge".
        - the style of an edge is represented by [MyPyDrawIO : EdgeStyle](./MyPyDrawIO/EdgeStyle.html)
        - the geometry of an edge is represented by [MyPyDrawIO : EdgeGeometry](./MyPyDrawIO/EdgeGeometry.html)

### mxCells and object
In draw.io you can add data to an element (vertex or edge).
If you do this with an element that was previously stored as a mxCell, that mxCell will now be wrapped in an object.

In the picture below we have the "RECT" element. On the left side, this is saved as mxCell (see the XML data with the black background).
When you "Edit Data..." you can add properties as key value pairs.
On save this "RECT" element will be saved as object. 
The 'id' of the mxCell moves to the object level. 
The 'value' of the mxCell, which is the text displayed in the drawing of the element, also moves to the object level.
Thereby it is renamed to 'label'.
The properties are save as XML attributes on the object level.
All other properties will be kept on on the mxCell level.

<img src="./images/MyPyDrawIO-mxCell and object.png">

Since such elements (vertices or edges) that are stored as objects are still perceived as one unit, 
MyPyDrawIO wraps this (somehow complicated) behavior in the classes
- [MyPyDrawIO : Element](./MyPyDrawIO/Element.html)
- [MyPyDrawIO : Vertex](./MyPyDrawIO/Vertex.html)
- [MyPyDrawIO : Edge](./MyPyDrawIO/Edge.html)

Im most cases you can neglect the distingtion of mxCells and objects. 
For an element, you can check if an element is an object, using [MyPyDrawIO : Element.isObject()](./MyPyDrawIO/Element.html#Element.isObject).

### Parent child relationship
On the right side in the [image above](./MyPyDrawIO.html#drawio-files) we see the structure of the xml file.
Each element has an 'id'.
All elements except the element with 'id = 0' also have a reference to a 'parent'. 
So in a draw.io file a parent child relationship is established by referencing the 'id' of the parent by the 'parent' attribute.

In MyPyDrawIO the parent child relationships are realized by adding child elements as children to a parent element.
You can explore this in the pages [elementTree()](./MyPyDrawIO/Page.html#Page.elementTree).

## draw.io libraries
In a draw.io library file the content is some kind of, hm, list, json, xml, ... I do not exactly know.
Anyway: All the elements of the library are listed within the draw.io library file.

I do not know the use of 'w', 'h', 'aspect', so I ignore it.

'title' is used within [Library](./MyPyDrawIO/Library.html#Library) to access the element you need.
If you parse the 'xml' data, you will get a mxGraphModel, describing the specific element. 
This element can be very simple, consisting of only one mxCell or object.
But it also can be more complex, consisting of several mxCells and / or objects in a parent child relationship.
These informations are all handled by the [ElementDefinition](./MyPyDrawIO/ElementDefinition.html), so you do not have to care about it.

<img src="./images/MyPyDrawIO-Libraries - file content.png">

# Thanks to xmltodict
MyPyDrawIO uses the python module [xmltodict](https://pypi.org/project/xmltodict/) to convert the XML structure into dictionaries and lists.
Thanks for this module. It hepled a lot.


# TODOS
- DOKUMENTATION ZUR VERKNÜPFUNG VON EDGES UND VERTICES ÜBERARBEITEN!!!
    - in MyPyDrawIO.EdgeStyle
    - in MyPyDrawIO.doc.Connecting edges with vertices
- FORMATE IN STYLES AUFGEHEN LASSEN
    - anstelle der Formate deren Funktion in die Styles überführen
- die Connection Points auf den Vertices implementieren.
- Elemente löschen
    - mindestens auf der Page
    - wenn möglich auch bei dem Element selbst
- GRUPPIERUNG erklären und eine Funktion zum Gruppieren implementieren
- Auch ungroup auch bereitstellen (Einfach das Gruppen element löschen und die chldren an den parent der Gruppe hängen.)

# AKTUELLE AUFGABEN

"""