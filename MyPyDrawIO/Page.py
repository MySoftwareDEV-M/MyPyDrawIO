import json
import uuid

import MyFramework.DE               as DE
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos
import MyPyDrawIO.Edge              as Edge
import MyPyDrawIO.Element           as Element
import MyPyDrawIO.ElementDefinition as ElementDefinition
import MyPyDrawIO.ElementTree       as ElementTree
import MyPyDrawIO.Library           as Library
import MyPyDrawIO.Vertex            as Vertex

class Page(dict):
    """
    Reprasentation of a draw.io page.
    
    ## manage the page
    Functions to manage the pages name and retrieve the pages id.
    - [Page()](./Page.html#Page.__init__)
    <br> HINT: Your should not create pages directly, but use [File.insertPage()](./File.html#File.insertPage) instead.
    - [id()](./Page.html#Page.id)
    - [name()](./Page.html#Page.name)
    - [setName()](./Page.html#Page.setName)

    ## manage elements (vertices & edges)
    Functions to create and delete elements and to access the elementTree.
    - [createVertex()](./Page.html#Page.createVertex)
    - [createEdge()](./Page.html#Page.createEdge)
    - [elementTree()](./Page.html#Page.elementTree)

    ## ToDos
    - LÖSCHEN VON ELEMENTS EINBAUEN
    - Suchen von Elementen einbauen
    
    """
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, input):
        """
        Your should not create pages directly, but use [File.insertPage()](./File.html#File.insertPage) instead.
        """
        ###########################################################################################
        # Page accepts two kinds of input                                                         #
        # a) a string representing the name of a page to be created.                              #
        #-----------------------------------------------------------------------------------------#
        # b) a dictionary representing the content of a draw.io page.                             #
        #   this dictionary is expected to be a "mxFile > diagram" taken from the draw.io         #
        #   file with the path. Compare with the picture in the MyPyDrawIO documentation          #
        #   "MyPyDrawIO classes and the file structure > draw.io files"                           #
        #                                                                                         #
        # Attributes expected for a page are                                                      #
        # - id                                                                                    #
        # - name                                                                                  #
        # - mxGraphModel                                                                          #
        #                                                                                         #
        # The mxGraphModel should contain the general information about the page like its size,   #
        # grid, background color, ... Additionaly it has to contain the 'root' element, which     #
        # itself contains all the elements of the page.                                           #
        #                                                                                         #
        # Since I cannot rule out the possibility that there are further attributes,              #
        # such potential further attributes are saved within the basicPage attribute.             #
        ###########################################################################################

        self.__elementTree = None

        # 1. create the root element of the page
        self.__rootElement = Element.Element()
        self.__rootElement["@id"] = "1"
        self.__rootElement["content"] = {"@id" : "1", "@parent" : "0"}

        # 2. a) if input is a string, a new page has to be created.
        if( type(input) == str ):
            self["@name"]    = input
            self["@id"]      = str(uuid.uuid4())

            self["basicPage"] = {}
            self["mxGraphModel"] = {
                    "@dx": "780",
                    "@dy": "542",
                    "@grid": "1",
                    "@gridSize": "10",
                    "@guides": "1",
                    "@page": "1",
                    "@pageScale": "1",
                    "@pageWidth": "1169",
                    "@pageHeight": "1654",
                    "@math": "0",
                    "@shadow": "0",
                }
        
        # 2. b) if input is a dict, a page from a draw.io file has to be loaded
        elif( type(input) == dict ):           
            # Retrieve solely the page attributes
            self["@name"]   = input["@name"]
            self["@id"]     = input["@id"]
            mxGraphModel    = input["mxGraphModel"]

            del input["@name"]
            del input["@id"]
            del input["mxGraphModel"]
            
            self["basicPage"] = input

            # Retrieve solely the mxGraphModel attributes
            root = mxGraphModel["root"]
            del mxGraphModel["root"]
            self["mxGraphModel"] = mxGraphModel

            self.__evaluateRoot(root)

        # 2. c) should not happen
        else:
            Infos.announceError("Unsupported data type")

    #----------------------------------------------------------------------------------------------
    def __evaluateRoot(self, root : dict):
        """
        Private function to evaluate the "root" of a draw.io file.
        
        root is expected to be a dictionary taken from the draw.io file with the path
        "mxFile > diagram > mxGraphModel > root".
        Compare with [image](../MyPyDrawIO.html#drawio-files).
        """
        parentChildRelations = Page.__getParentChildRelations(root)
        Page.__createChildren(root, self.__rootElement, parentChildRelations)
    
    #----------------------------------------------------------------------------------------------
    def _content(self) -> dict:
        """
        This function returns the content of this page in a way it can be used for saving to a draw.io file.
        This function will be used by [File.save()](./File.html#File.save) function.
        """
        # The lists to gether the mxCells and the objects
        mxCells = []
        objects = []

        # Add the mxCell with id = 0, which is always there
        mxCells.append(
            {
                "@id" : "0"
            }
        )

        # Let all elements add themself to the mxCells or objects
        self.__rootElement._retrieveContent(mxCells, objects)

        # Assemble root
        root = {
            "mxCell" : mxCells,
            "object" : objects
            }

        # Assemble the mxGraphModel
        mxGraphModel        = self["mxGraphModel"]
        mxGraphModel["root"] = root

        # Assemble the page
        pageDict            = self["basicPage"]     # The stuff that might have come aditionally with a page from a loaded file
        pageDict["@name"]   = self["@name"]         # name          <-- always
        pageDict["@id"]     = self["@id"]           # id            <-- always        
        pageDict["mxGraphModel"] = mxGraphModel     # mxGraphModel  <-- always

        return pageDict
    
    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def createVertex(self, element : ElementDefinition.ElementDefinition, parent : Element.Element = None) -> Vertex.Vertex:
        """
        Creates a [eertex](./Vertex.html) and adds it to the page using the given [ElementDefinition](./MyPyDrawIO/ElementDefinition.html).
        This new vertex will be the child of parent if one is provided. 
        Otherwise this vertex is added at the top level of the page.
        """
        if(parent == None):
            parent = self.__rootElement
        vertex = Vertex.Vertex(element, parent)

        if("children" in element):
            for child in element["children"]:
                if(child["type"] == "vertex"):
                    Vertex.Vertex(child, vertex)

                elif(child["type"] == "edge"):
                    Infos.announceDebug("HIER IST NOCH ZU PRÜFEN, DASS ALS SOURCE UND TARGET DIE RICHTIGEN VERTICES ANGEGEBEN WERDEN. IRGENDWIE DIE GENERIERTEN IDS ABFANGEN UND ÜBERGEBEN.")
                    Edge.Edge(child, parent=vertex)
        
        return vertex

    #----------------------------------------------------------------------------------------------
    def createEdge(self, element : ElementDefinition.ElementDefinition, sourceID : str = None, targetID : str = None, parent : Element.Element = None) -> Edge.Edge:
        """
        Creates an [edge](./Vertex.html) and adds it to the page using the given [ElementDefinition](./MyPyDrawIO/ElementDefinition.html).
        This new edge will be the child of parent if one is provided. 
        Otherwise this edge is added at the top level of the page.
        """
        if(parent == None):
            parent = self.__rootElement
        edge = Edge.Edge(element, sourceID, targetID, parent)
        return edge

    #----------------------------------------------------------------------------------------------
    def elementTree(self) -> ElementTree.ElementTree:
        """
        Returns the element tree for this page.
        """
        if self.__elementTree == None:
            self.__elementTree = ElementTree.ElementTree(self)
        return self.__elementTree
    
    #----------------------------------------------------------------------------------------------
    def rootElement(self) -> Element.Element:
        """
        Returns the root element of the page.
        """
        return self.__rootElement
    
    #----------------------------------------------------------------------------------------------
    def id(self) -> str:
        """
        Returns the id of the page.
        """
        return self["@id"]

    #----------------------------------------------------------------------------------------------
    def name(self) -> str:
        """
        Returns the name of the page.
        """
        return self["@name"]

    #----------------------------------------------------------------------------------------------
    def setName(self, name : str):
        """
        Sets the name of this page.
        """
        self["@name"] = name

###################################################################################################
# Public global functions / Helper functions
    #----------------------------------------------------------------------------------------------
    def __getParentChildRelations(root : dict) -> dict:
        """
        Private helper function.

        This function iterates the mxCells and objects within root and returns a dictionary
        listing all children for a given parent.

        root is expected to be a dictionary taken from the draw.io file with the path
        "mxFile > diagram > mxGraphModel > root".
        Compare with [image](../MyPyDrawIO.html#drawio-files).

        returns {

        }
        """
        parentChildRelations = {}
        
        # 1. Since the XML element "root" should always have a list of "mxCell", we can check these ...
        for mxCell in root["mxCell"]:
            # ... we have to skip the only mxCell with id = 0, which has no parent ...
            if not "@parent" in mxCell:
                continue
            # ... all other mxCells should have parents, so we can add then to the parentChildRelations.
            Data.addListToDict(parentChildRelations, mxCell["@parent"], mxCell["@id"])

        # 2. If there is no XML element "object", there is nothing more to to do.
        if not "object" in root:
            return parentChildRelations

        # 3. If we come here there is a XML element "object", ...
        # 3.1 ... which can be a dict, meaning there is only one onject, which we can add to the parentChildRelations.
        if type(root["object"]) == dict:
            Data.addListToDict(parentChildRelations, root["object"]["mxCell"]["@parent"], root["object"]["@id"])
        
        # 3.2 ... which should be a list otherwise. This list, we iterate to add to add all objects to the parentChildRelations.
        else:
            for object in root["object"]:
                Data.addListToDict(parentChildRelations, object["mxCell"]["@parent"], object["@id"])

        # 4. Finally return.
        return parentChildRelations

    #----------------------------------------------------------------------------------------------
    def __getElementXMLDefinitionByID(root : dict, id : str) -> dict:
        """
        Private helper function.

        This function returns the element xml definition for the given id within root.

        root is expected to be a dictionary taken from the draw.io file with the path
        "mxFile > diagram > mxGraphModel > root".
        Compare with [image](../MyPyDrawIO.html#drawio-files).
        """
        
        # 1. Since the XML element "root" should always have a list of "mxCell", 
        # we can check, if the element we search for is within this list.
        for mxCell in root["mxCell"]:
            if mxCell["@id"] == id:
                return mxCell

        # 2. If there is no XML element "object", there is nothing more to to do.
        if not "object" in root:
            return None

        # 3. If we come here there is a XML element "object", ...
        # 3.1 ... which can be a dict, meaning there is only one onject.
        # So this object might be the element we search for.
        if type(root["object"]) == dict:
            if root["object"]["@id"] == id:
                return root["object"]

        # 3.2 ... which should be a list otherwise.
        # So let's search within this list for the element.
        else:
            for object in root["object"]:
                if object["@id"] == id:
                    return object
        
        # 4. If we came here, there is no element with that id.
        return None
    
    #----------------------------------------------------------------------------------------------
    def __createChildren(root : dict, parent, parentChildRelations : dict):
        """
        Private helper function.

        Creates the child elements for the given parent.
        """
        # 1. If the parent has no children, there is nothin to do.
        if not parent["@id"] in parentChildRelations:
            return
        
        # 2. If we came here, the parent has children. ...
        for id in parentChildRelations[parent["@id"]]:

            # 2.1 ... So we retrive the elements XML definition ...
            elementXMLDefinition = Page.__getElementXMLDefinitionByID(root, id)

            # 2.2.1. ... and check, if element is an object.
            if "mxCell" in elementXMLDefinition: 
                # 2.2.1.1 If the element is a vertex,
                # - we have to construct a vertex
                # - and (recursively) create it's children.
                if "@vertex" in elementXMLDefinition["mxCell"]:
                    vertex = Vertex.Vertex(elementXMLDefinition, parent)
                    Page.__createChildren(root, vertex, parentChildRelations)

                # 2.2.1.2 If the element is an edge,
                # - we have to construct an edge
                # - and (recursively) create it's children.
                elif "@edge" in elementXMLDefinition["mxCell"]:
                    edge = Edge.Edge(elementXMLDefinition, parent=parent)
                    Page.__createChildren(root, edge, parentChildRelations)

            # 2.2.2. ... or the element will be a plain mxCell.
            else:
                # 2.2.2.1 If the element is a vertex,
                # - we have to construct a vertex
                # - and (recursively) create it's children.
                if "@vertex" in elementXMLDefinition:
                    vertex = Vertex.Vertex(elementXMLDefinition, parent)
                    Page.__createChildren(root, vertex, parentChildRelations)
                    
                # 2.2.2.2 If the element is an edge,
                # - we have to construct an edge
                # - and (recursively) create it's children.
                elif "@edge" in elementXMLDefinition:
                    edge = Edge.Edge(elementXMLDefinition, parent=parent)
                    Page.__createChildren(root, edge, parentChildRelations)
