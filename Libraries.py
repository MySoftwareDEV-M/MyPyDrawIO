"""
Libraries is a
[singleton](https://en.wikipedia.org/wiki/Singleton_pattern)
to load draw.io libraries (xml files).

For each loaded library a
[library](./Library.html#Library)
object will be provided.
These provide access to the 
[vertices](./Vertex.html) and
[edges](./Edge.html)
as an
[ElementDefinition](./ElementDefinition.html). 
Forward them to the
[Page.createVertex()](./Page.html#Page.createVertex) and
[Page.createEdge()](./Page.html#Page.createEdge)
functions.

Adapt this code example to use your own libraries.
To provide a suitable draw.io library, see
[Creating draw.io libraries for MyPyDrawIO](../MyPyDrawIO.html#creating-drawio-libraries-for-mypydrawio).
```
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
```
"""
import os

import MyFramework.Informations as Infos
import MyPyDrawIO.Library       as Library
    
class Libraries:
    ###############################################################################################
    # class variables
    __infos     = Infos.Informations()
    __libraries = list[Library.Library]()

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __new__(cls):
        """
        """        
        if not hasattr(cls, 'instance'):
            cls.instance = super(Libraries, cls).__new__(cls)
        return cls.instance

    ###############################################################################################
    # public functions
    #----------------------------------------------------------------------------------------------
    def library(self, name) -> Library.Library:
        """
        Returns the [library](./Library.html) object for the requested library.

        If there is no library for that name, None will be returned.
        """
        for library in self.__libraries:
            if(library["name"] == name):
                return library
        
        return None
    
    #----------------------------------------------------------------------------------------------
    def libraries(self) -> list[Library.Library]:
        """
        Returns a list of all [library](./Library.html) objects.
        """        
        return self.__libraries
    
    #----------------------------------------------------------------------------------------------
    def loadLibrary(self, filePath : str) -> bool:
        """
        Loads the draw.io library file.
        If it exists, a [library](./Library.html) object will be created.

        Returns True, if the library could be loaded, otherwise false.
        """
        # 1. Check if the file exists, otherwise return with a warning
        if(not os.path.exists(filePath)):
            Infos.announceWarning("Library \"" + filePath + "\"does not exist.")
            return False
            
        # 2. Create the library object
        library = Library.Library()
        successCode = library._load(filePath)
        if(successCode):
            self.__libraries.append(library)
            
        return successCode

###################################################################################################
# Public global functions / Helper functions