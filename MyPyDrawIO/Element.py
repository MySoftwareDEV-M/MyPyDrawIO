"""
Element is the base class for [Vertices](./Vertex.html) and [Edges](./Edge.html).
    
The element base class provides functionality common for both, vertices and edges as you can see in the sections below.

Anyone using myMyPyDrawIO should not need the element constructor, as it is used indirectly when creating vertices or edges or when loading files.

## Basic element information
- [id()](../MyPyDrawIO/Element.html#Element.id)
- [isVertex()](../MyPyDrawIO/Element.html#Element.isVertex)
- [isEdge()](../MyPyDrawIO/Element.html#Element.isEdge)
- [isObject()](../MyPyDrawIO/Element.html#Element.isObject)
    
## Parent child relation
- CHILDREN
    - [children()](../MyPyDrawIO/Element.html#Element.children)
    - [addChild()](../MyPyDrawIO/Element.html#Element.addChild)
    - [removeChild()](../MyPyDrawIO/Element.html#Element.removeChild)
- PARENT
    - [parent()](../MyPyDrawIO/Element.html#Element.parent)
    - [setParent()](../MyPyDrawIO/Element.html#Element.setParent)
    
## The element content
- CONTENT
    - [dump()](../MyPyDrawIO/Element.html#Element.dump)
    - [retrieveContent()](../MyPyDrawIO/Element.html#Element.retrieveContent)
- KEY & VALUE
    - [containsKey()](../MyPyDrawIO/Element.html#Element.containsKey)
    - [deleteKey()](../MyPyDrawIO/Element.html#Element.deleteKey)
    - [keyList()](../MyPyDrawIO/Element.html#Element.keyList)
    - [keySet()](../MyPyDrawIO/Element.html#Element.keySet)
    - [propertyKeys()](../MyPyDrawIO/Element.html#Element.propertyKeys)
    - [value()](../MyPyDrawIO/Element.html#Element.value)
    - [setValue()](../MyPyDrawIO/Element.html#Element.setValue)
- LABEL
    - [label()](../MyPyDrawIO/Element.html#Element.label)
    - [setLabel()](../MyPyDrawIO/Element.html#Element.setLabel)
- STYLE & GEOMETRY
<br> The general concept of styles and geometries is described [here](../MyPyDrawIO.html#elements-styles-and-geometries)
    - [geometry()](../MyPyDrawIO/Element.html#Element.geometry)
    - [setGeometry()](../MyPyDrawIO/Element.html#Element.setGeometry)
    - [style()](../MyPyDrawIO/Element.html#Element.style)
    - [setStyle()](../MyPyDrawIO/Element.html#Element.setStyle)

## Labels
As described
[here](../MyPyDrawIO.html#mxcells-and-object)
draw.io has a special behavior regarding the `value`and `label` within the context of mxCells and objects.
To encapsulate this behavior, in MyPyDrawIO there are the functions
- [label()](../MyPyDrawIO/Element.html#Element.label)
- [setLabel()](../MyPyDrawIO/Element.html#Element.setLabel)

to set and get the label of an element, even if it is a value within an mxCell.
"""

import copy
import json
import uuid

import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

import MyPyDrawIO.ElementDefinition as ElementDefinition
import MyPyDrawIO.Geometry          as Geometry
import MyPyDrawIO.Style             as Style

import sys
Element = sys.modules[__name__]

class Element(dict):
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, content = None, parent = None):
        """
        """
        self["@id"] = None
        self["isEdge"] = False
        self["isObject"] = False
        self["isVertex"] = False
        self["parent"] = None
        self["children"] = []
        self["content"]  = {}

        # a) wird genutzt, wenn ein element aus einer draw.io library erstellt wird.
        if(type(content) == ElementDefinition.ElementDefinition):
            _id = str(uuid.uuid4())
            self["@id"] = _id
            self["isEdge"] = (content["type"] == "edge")
            self["isObject"] = (content["isObject"] == True)
            self["isVertex"] = (content["type"] == "vertex")
            
            self["content"]  = copy.deepcopy(content["content"])
            self["content"]["@id"] = _id

            self["children"] = []
            if(parent != None):
                parent.addChild(self)

        # b) Wird genutzt, wenn ein Element aus einem draw.io file geladen wird.
        elif(type(content) == dict):
            self["@id"] = content["@id"]
            self["content"] = copy.deepcopy(content)
            
            if "mxCell" in content: # Element is an object
                self["isObject"] = True
                self["isEdge"] = ( "@edge" in content["mxCell"])
                self["isVertex"] = ( "@vertex" in content["mxCell"])

            else:                   # Element is a mxCell
                self["isObject"] = False
                self["isEdge"] = ( "@edge" in content)
                self["isVertex"] = ( "@vertex" in content)

            if(parent != None):
                parent.addChild(self)

        # c) wird nur für die Erstellung des rootElements genutzt
        elif(content == None):
            pass
            # Nothing to do here

        else:
            Infos.announceError("Invalid type of content.")

    #----------------------------------------------------------------------------------------------
    def __getKeys(self, theDict : dict, prefix = "") -> list:
        keys = []
        print(json.dumps(theDict, indent=3))
        tmp = theDict.keys()
        for t in tmp:
            if(t.startswith("@")):
                keys.append(prefix + t)
            else:
                keys.extend(self.__getKeys(theDict[t], prefix + t + ">"))

        return keys

    ###############################################################################################
    # Public functions
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # BASIC ELEMENT INFORMATION
    #----------------------------------------------------------------------------------------------
    def id(self) -> str:
        """
        Returns the id of the element.

        Corresponding key: @id
        """
        return self["@id"]
    
    #----------------------------------------------------------------------------------------------
    def isEdge(self) -> bool:
        """
        Returns if the element is an edge.

        Corresponding key: isEdge
        """
        return self["isEdge"]

    #----------------------------------------------------------------------------------------------
    def isObject(self) -> bool:
        """
        Returns if the element is an object.

        Corresponding key: isObject
        """
        return self["isObject"]

    #----------------------------------------------------------------------------------------------
    def isVertex(self) -> bool:
        """
        Returns if the element is a vertex.

        Corresponding key: isVertex
        """
        return self["isVertex"]
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # PARENT CHILD RELATION
    # CHILDREN
    #----------------------------------------------------------------------------------------------
    def children(self) -> list:
        """
        Returns a list of all the children of this element.

        Corresponding key: children
        """
        return self["children"]

    #----------------------------------------------------------------------------------------------
    def addChild(self, newChild):
        """
        Adds newChild to this element.

        If newChild is already related to an other parent element,
        that parent child relationship will be newChild deleted.
        """
        # 1. Check, if newChild is already a child of this element ...
        children = self["children"]
        for child in children:
            # ... if so, return.
            if(child == newChild):
                return
        
        # 2. If we are here, ...
        # 2.1 ... We check, if newChild already has an other parent.
        parent = newChild.parent()
        # ... If so, we remove child from that parent.
        if(parent != None):
            parent.removeChild(self)

        # 2.2 ... Now newChild shall become a child of this element.
        children.append(newChild)
        self["children"] = children

        # 2.3 ... Within the child, set self.id as the parents is
        if(newChild["isObject"]):
            newChild["content"]["mxCell"]["@parent"] = self["@id"]
        else:
            newChild["content"]["@parent"] = self["@id"]

        # 2.4 ... And finally we have to set this element as parent of newChild.
        newChild.setParent(self)

    #----------------------------------------------------------------------------------------------
    def removeChild(self, child):
        """
        Remove child from this element.
        Also sets the parent from child to None to avoid incorrect data relationships.
        """
        children = self["children"]
        children.remove(child)
        self["children"] = children

        child.setParent(None)

    # PARENT
    #----------------------------------------------------------------------------------------------
    def parent(self):
        """
        Returns the parent of the element.
        """
        return self["parent"]

    #----------------------------------------------------------------------------------------------
    def setParent(self, parent):
        """
        Sets the parent of this element.
        """
        self["parent"] = parent

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # THE ELEMENT CONTENT
    #----------------------------------------------------------------------------------------------
    def dump(self, keys = [], descandents = 100000, indent = ""):
        """
        Dumps a tree of this element and all its child elements.
        Use keys to select the key value pairs to be dumped. 
        If no keys are selected all key value pairs are dumped.
        """
        if(len(keys) == 0):
            _keys = list(self["content"].keys())
            if self.isObject():
                _keys.extend(list(self["content"]["mxCell"]))
        else:
            _keys = copy.deepcopy(keys)
        
        # Element ---------------------------------------------
        if self.isVertex():
            tmp = "vertex"
        else:
            tmp = "edge"
        if(self.isObject()):
            tmp = indent + "Element (object > " + tmp + ") "
            line = (60 - len(tmp)) * '-'
            print(tmp + line)
        else:
            tmp = indent + "Element (mxCell > " + tmp + ") "
            line = (60 - len(tmp)) * '-'
            print(tmp + line)
        
        for key in _keys:
            toBeUses = None
            if self.containsKey(key):
                toBeUses = self
            else:
                tmp = None
                if self.isObject():
                    tmp = self["content"]["mxCell"]
                else:
                    tmp = self["content"]
                if key in tmp:
                    toBeUses = tmp

            if toBeUses == None:
                continue

            if(key.startswith("@")):
                if key == "@style":
                    style = self.style()
                    if(style):
                        style.dump(indent + "  ")
                else:
                    print(indent + "- " + key + ": " + self.value(key))
            if key == "mxGeometry":
                geometry = self.geometry()
                if(geometry):
                    geometry.dump(indent + "  ")
        # free line -------------------------------------------
        print("")
        
        # Children --------------------------------------------
        descandents -= 1
        if descandents == 0:
            return
        for child in self.children():
            child.dump(indent = indent + "   ", keys = keys)

    #----------------------------------------------------------------------------------------------
    def _retrieveContent(self, mxCells : list, objects : list):
        """
        Extends the provided lists for the mxCells and objects with the content 
        of this element and all its children.
        """
        if(self["isObject"]):
            objects.append(self["content"])

        else:
            mxCells.append(self["content"])

        for child in self.children():
            child._retrieveContent(mxCells, objects)

    # KEY & VALUE
    #----------------------------------------------------------------------------------------------
    def containsKey(self, key) -> bool:
        """
        Checks if the key exists in this element.
        """
        if key in self["content"]:
            return True
        
        if(self.isObject()):
            if key in self["content"]["mxCell"]:
                return True

        return False

    #----------------------------------------------------------------------------------------------
    def deleteKey(self, key):
        """
        Deletes the key (with its value) if it exists.
        """
        if key in self["content"]:
            del self["content"][key]
            return
        
        if(self.isObject()):
            if key in self["content"]["mxCell"]:
                del self["content"]["mxCell"][key]

    #----------------------------------------------------------------------------------------------
    def keyList(self, flattenObject = True) -> list:
        """
        Returns a list with all keys of this node and its child nodes.

        flattenObject: Removes "mxCell>" from the keys.
        """
        allKeys = self.keySet()
        tmp = set()
        if(flattenObject):
            for key in allKeys:
                if(key.startswith("mxCell>")):
                    tmp.add(key[7:])
                else:
                    tmp.add(key)
            allKeys = tmp

        allKeys = list(allKeys)
        allKeys.sort()
        return allKeys

    #----------------------------------------------------------------------------------------------
    def keySet(self) -> set:
        """
        Returns a set with all keys of this node and its child nodes.
        """
        allKeys = set(self.__getKeys(self["content"]))

        for child in self.children():
            allKeys = allKeys.union(child.keySet())
        
        return allKeys
    
    #----------------------------------------------------------------------------------------------
    def propertyKeys(self) -> list:
        """
        If this element is an object, the keys to the properties of this object are returned.
        See [here](../MyPyDrawIO.html#mxcells-and-object).
        
        If this element is a mxCell, none will be returned.
        """
        if(self.isObject()):
            tmp = list(self["content"].keys())
            propertyKeys = []
            for key in tmp:
                if(key[0] != "@"):
                    continue
                if(key == "@id"):
                    continue
                if(key == "@label"):
                    continue
                
                propertyKeys.append(key)
            
            return propertyKeys

        else:
            return None
    
    #----------------------------------------------------------------------------------------------
    def value(self, key):
        """
        Returns the value for the key, if it exists.
        Otherwise None will be returned.
        """
        if key in self["content"]:
            return self["content"][key]
        
        if(self.isObject()):
            if key in self["content"]["mxCell"]:
                return self["content"]["mxCell"][key]
        return None
    
    #----------------------------------------------------------------------------------------------
    def setValue(self, key, value):
        """
        Adds the key value pair, if it does not exist yet or sets the value for the key.

        If the element is an object, the key value pair will be set in "mxCell".
        If the element is a mxCell, the key value pair will be set in directly the content.
        """
        if(self.isObject()):
            self["content"]["mxCell"][key] = value
        else:
            self["content"][key] = value

    # COMPLEX VALUES
    #----------------------------------------------------------------------------------------------
    def label(self) -> str:
        """
        Gets the value (if this element is a mxCell) or label (if this element is an object).

        Background knowledge, see [here](../MyPyDrawIO.html#mxcells-and-object).
        """
        if(self.isObject()):
            if "@label" in self["content"]:
                return self["content"]["@label"]
        else:
            if "@value" in self["content"]:
                return self["content"]["@value"]
        
        return "NO LABEL"

    #----------------------------------------------------------------------------------------------
    def setLabel(self, label : str):
        """
        Sets the value (if this element is a mxCell) or label (if this element is an object).

        Background knowledge, see [here](../MyPyDrawIO.html#mxcells-and-object).
        """
        if(self.isObject()):
            self["content"]["@label"] = label
        else:
            self["content"]["@value"] = label
    
    #----------------------------------------------------------------------------------------------
    def geometry(self) -> Geometry.Geometry:
        """
        Returns the geometry.
        """
        if(self.isObject()):
            if "mxGeometry" in self["content"]["mxCell"]:
                return Geometry.Geometry(self["content"]["mxCell"]["mxGeometry"])
        else:
            if "mxGeometry" in self["content"]:
                return Geometry.Geometry(self["content"]["mxGeometry"])
        
        return None

    #----------------------------------------------------------------------------------------------
    def setGeometry(self, geometry : Geometry.Geometry):
        """
        Sets the geometry.
        """
        if(self.isObject()):
            self["content"]["mxCell"]["mxGeometry"] = geometry
        else:
            self["content"]["mxGeometry"] = geometry
    
    #----------------------------------------------------------------------------------------------
    def style(self) -> Style.Style:
        """
        Returns the style.
        This function is overloaded within the derived classes [Edge > style()](../MyPyDrawIO/Edge.html#Edge.style) and 
        [Vertex > style()](../MyPyDrawIO/Vertex.html#Vertiex.style) to provide the specific style instances.
        """
        if(self.isObject()):
            if "@style" in self["content"]["mxCell"]:
                return Style.Style(self["content"]["mxCell"]["@style"])
        else:
            if "@style" in self["content"]:
                return Style.Style(self["content"]["@style"])
        
        return None

    #----------------------------------------------------------------------------------------------
    def setStyle(self, style : Style.Style):
        """
        Sets the style.
        """
        if(self.isObject()):
            self["content"]["mxCell"]["@style"] = style._content()
        else:
            self["content"]["@style"] = style._content()

###################################################################################################
# Public global functions / Helper functions
