"""
Represants a draw.io library and provides access to the 
[vertices](./Vertex.html) and
[edges](./Edge.html)
as an
[ElementDefinition](./ElementDefinition.html). 
Forward them to the
[Page.createVertex()](./Page.html#Page.createVertex) and
[Page.createEdge()](./Page.html#Page.createEdge)
functions.
"""
import json
import xmltodict

import MyFramework.Informations     as Infos

import MyPyDrawIO.ElementDefinition as ElementDefinition


class Library(dict):
    ###############################################################################################
    # class variables
    __edges     = dict()
    __vertices  = dict()

    ###############################################################################################
    # private functions
    def __init__(self):
        """
        """
        self["name"] = "<no name>"

    ###############################################################################################
    # non-public functions
    #----------------------------------------------------------------------------------------------
    def _load(self, filePath : str) -> bool:
        """
        Loads the draw.io library file at the given filePath
        and creates an element definition for each shape defined within that library file.
        """
        elementsWithNoTitle = 0

        # 1. load the file
        try:
            file = open(filePath)
            content = xmltodict.parse(file.read())
            file.close()
        except:
            Infos.announceWarning("Library \"" + filePath + "\"can not be loaded.")
            return False

        # 2. get the library name
        name = filePath.split("/")
        name = name[len(name)-1]
        index = name.index(".")
        self["name"] = name[:index]

        # 3. get the content --> all the elements within the library ...
        content = content["mxlibrary"]
        content = json.loads(content)

        # ... and iterate the elements
        for elementDefinition in content:

            element = None
            try:
                title = elementDefinition["title"]
            except:
                elementsWithNoTitle += 1
                title = "No Title " + str(elementsWithNoTitle)

            element = ElementDefinition.ElementDefinition()
            success = element.parse(elementDefinition["xml"])

            if(success):
                if element["type"] == "vertex":
                    self.__vertices[title] = element

                elif element["type"] == "edge":
                    self.__edges[title] = element

                else:
                    Infos.announceWarning("An element within the library \"" + self["name"] + "\" could not be assigned as 'vertex' nor 'edge'.")

            else:
                Infos.announceWarning("An element within the library \"" + self["name"] + "\" could not be parsed.")

        return True

    ###############################################################################################
    # public functions
    #----------------------------------------------------------------------------------------------
    def vertex(self, title : str) -> ElementDefinition.ElementDefinition:
        """
        Returns the [ElementDefinition](./ElementDefinition.html) for the requested vertex.
        Forward this to
        [Page.createVertex()](./Page.html#Page.createVertex)
        to create a reqpective vertex on that page.
        """
        return self.__vertices[title]

    #----------------------------------------------------------------------------------------------
    def edge(self, title : str) -> ElementDefinition.ElementDefinition:
        """
        Returns the [ElementDefinition](./ElementDefinition.html) for the requested edge.
        Forward this to
        [Page.createEdge()](./Page.html#Page.createEdge)
        to create a reqpective edge on that page.
        """
        return self.__edges[title]

    #----------------------------------------------------------------------------------------------
    def vertices(self) -> list[str]:
        """
        Returns a list of names of all
        [vertices](./Vertex.html)
        provided by the library.
        """
        return self.__vertices.keys()

    #----------------------------------------------------------------------------------------------
    def edges(self) -> list[str]:
        """
        Returns a list of names of all
        [edges](./Edge.html)
        provided by the library.
        """
        return self.__edges.keys()

###################################################################################################
# Public global functions / Helper functions
