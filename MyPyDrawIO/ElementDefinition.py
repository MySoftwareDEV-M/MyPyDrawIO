import xmltodict
import json
import uuid

import MyFramework.Informations   as Infos
import MyFramework.Data           as Data

class ElementDefinition(dict):
    """
    When loading a [Library](./Library.html#Library) the Library will create an ElementDefinition for each element within the library file as described [here](../MyPyDrawIO.html#libraries).
    The Library lists all titles of the elements. The ElementDefinitions can be retrieved by their titles.

    An ElementDefinition contains the definition of a [Vertice](./Vertex.html#Vertex) or [Edge](./Edge.html#Edge).
    These elements can be simple (just one mxCell or object) or complex (a more or less big parent child structure).
    
    To create an element just forwarded the ElementDefinition to the [createVertex()](./Page.html#Page.createVertex) or [createEdge()](./Page.html#Page.createEdge) function of the Page.
    These functions will return the created elements, which can be further manipulated by you.
    Keep in mind, these elements can be complex.

    
    NOCH ÜBERLEGEN, OB ICH DIESE TECHNISCHEN ERLÄUTERUNGEN HIER BEHALTE.
    If the ElementDefinition represents a complex element with parents and children [see here](../MyPyDrawIO.html#libraries),
    all the children are also created and added as children to the respective parent.

    If the content is a xml, the xml contains the definition of the specific element only. 
    As described [here](../MyPyDrawIO.html#parent-child-relationship) within the xml the parent child relationship 
    is realized by references. So it is in the responsibility of the Page to setup all elements
    with the correct parent child relationship.
    """
    ###############################################################################################
    # class variables of Element

    ###############################################################################################
    # private functions of Element
    #----------------------------------------------------------------------------------------------
    def __getElementsByParentID(self, parentID : str, definition : dict) -> list:
        """
        This function queries the mxGraphModel > root and returns a list containing all the 
        mxCells and objects whos parents have the parentID provided as argument.

        When querying the definition, the [special behavior of the transformation](../MyPyDrawIO.html#technical-deep-dive) has to be taken into account.
        """

        children = []
        # Since we deal with external data, we add some try catch.

        # 1. We query the mxCells...
        try:
            mxCells = definition["mxCell"]
            # ... actually the mxCells always should be a list...
            if(type(mxCells) == list):
                for mxCell in mxCells:
                    try:
                        # Except for the mxCell id = 0, there should always be a parent.
                        if(mxCell["@parent"] == parentID):
                            children.append(mxCell)
                    except:
                        pass

            else:
                # ... this should never occure. But in the case of... just add error handling.
                try:
                    if(mxCells["@parent"] == parentID):
                        children.append(mxCells)
                except:
                    pass

        except:
            pass
        
        # 2. Now we query the objects. There might be none. ...
        try:
            # ... If there are any ...
            objects = definition["object"]
            # 2.1 ... there could be more than one. In that case we would have a list.
            if(type(objects) == list):
                # ... and we iterate this list
                for _object in objects:
                    try:
                        if(_object["mxCell"]["@parent"] == parentID):
                            children.append(_object)
                    except:
                        pass
            
            # 2.2 ... there could be exactly on object. That should be represented by a dictionary.
            else:
                try:
                    if(objects["mxCell"]["@parent"] == parentID):
                        children.append(objects)
                except:
                    pass
        except:
            pass

        return children

    ###############################################################################################
    # public functions  of Element    
    #----------------------------------------------------------------------------------------------
    def parse(self, xmlDefinition : str) -> bool:
        """
        This function expects a xml definition of a library element as described [here](../MyPyDrawIO.html#libraries).

        Actually this function is used by the [Library](./Library.html#Library) so you do not need to call it.

        If the xml definition can be parsed True will be returned, otherwise False.
        """
        id = None

        # 1. Parse the "xml entry"
        xmlDefinition = xmltodict.parse(xmlDefinition)

        # 2. Navigate to the content we are interessted in.
        try:
            xmlDefinition = xmlDefinition["mxGraphModel"]["root"]
        except:
            Infos.announceWarning("Invalid xmlDefinition. (Expected ['mxGraphModel']['root'])")
            return False

        # 3. This function (parse()) should be called for the top level element definition.
        #   The parent of the top level element has the id = 1.
        # ...
        elements = self.__getElementsByParentID("1", xmlDefinition)
        # ... So if there is not exactly one element, with parent id 1, we do not have a top level element definition
        if(len(elements) != 1):
            Infos.announceWarning("No top level element definition.")
            return False
        # ... Just for convenience
        element = elements[0]

        return self.create(element, xmlDefinition)

    def create(self, element : dict, xmlDefinition : dict) -> bool:
        """
        This function expects a dictionary of a mxCell or an object.
        [Here](../MyPyDrawIO.html#the-drawio-file-and-its-representation-within-the-program) you can get an impression what they look like.

        Actually this function is used by ElementDefinitions so you do not need to call it.

        Returns True if all expected information exists, False otherwise.
        """
        # 1. Determine, if the element is an object (or mxCell) ...
        self["isObject"] = ("mxCell" in element.keys())

        # ... and retrieve the type (vertex or edge)
        if(self["isObject"]):
            if("@vertex" in element["mxCell"].keys()):
                self["type"] = "vertex"
            elif("@edge" in element["mxCell"].keys()):
                self["type"] = "edge"
            else:
                self["type"] = "unknown"
                return False
        else:
            if("@vertex" in element.keys()):
                self["type"] = "vertex"
            elif("@edge" in element.keys()):
                self["type"] = "edge"
            else:
                self["type"] = "unknown"
                return False

        # 2. Retrieve the content ...
        self["content"] = element
        # 3. ... and the id if there is one.
        if not "@id" in element.keys():
            return False
        id = element["@id"]

        # 4. Create children if there are some
        elements = self.__getElementsByParentID(id, xmlDefinition)
        children = []
        for element in elements:
            child = ElementDefinition()
            success = child.create(element, xmlDefinition)
            if not success:
                return False
            
            children.append(child)

        if(len(children)):
            self["children"] = children

        return True
###################################################################################################
# Public global functions / Helper functions
