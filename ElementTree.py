"""
The element tree provides functionality to dump and search 
[elements](./Element.html) of a 
[page](./Page.html).

HINT:
You can also use the elements [dump()](./Element.html#dump) function to dump the the element tree. 
The element tree just gathers some functionality to dump and search.

## Dump
- [dump()](./ElementTree.html#ElementTree.dump)

## Search
- [getElement()](./ElementTree.html#ElementTree.getElement)
- [getElements()](./ElementTree.html#ElementTree.getElements)
"""
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

import MyPyDrawIO.Edge              as Edge
import MyPyDrawIO.Element           as Element
import MyPyDrawIO.Vertex            as Vertex

class ElementTree():
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, page):
        """
        """
        self.__rootElement = page.rootElement()
    
    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def dump(self, keys = [], descandents = 100000):
        """
        Dumps the element tree.

        Same as [element > dump()](./Element.html#Element.dump)
        """        
        self.__rootElement.dump(keys, descandents)

    #----------------------------------------------------------------------------------------------
    def getElement(self, id) -> Element.Element:
        """
        Returns the element with the given id.

        If there is no element with the given id, None will be returned.
        """
        return ElementTree.__getElement(self.__rootElement, id)
    
    #----------------------------------------------------------------------------------------------
    def getElements(self, criterias : dict) -> list[Element.Element]:
        """
        Returns the elements which match the criterias.

        Critierias can be defined based on the [content](./Element.html#the-element-content) of an element.
        This are
        - key value pairs
        - style
        - geometry

        If ALL criterias have to match, set mode == ALL.
        This can be understood as an AND combination of the criterias.
        Otherwise you can set mode = ANY, which is an OR combination of the criterias.

        Play with this example to get used to this function.
        ```
        criterias = {
            "@value" : "List (mxCell)",
            "@vertex" : "1",
            "@id" : "iDYZMT0QqaAdwt2RhsGk-5",

            "style" : {
                "rounded" : "1",
                "strokeColor" : "none",
                "text" : None
            },

            "geometry" : {
                "@width" : "120",
                "@height" : "60"
            },

            "mode" : "ANY"
        }
        elements = elementTree.getElements(criterias)

        print("ELEMENTS: ")
        for element in elements:
            element.dump(keys=["@id", "@value", "@label", "@vertex"], descandents=1)
        ```

        HINT: There is a lot of potential for improvement in this function.
        """
        return ElementTree.__getElements(self.__rootElement, criterias)

###################################################################################################
# Public global functions / Helper functions
    #----------------------------------------------------------------------------------------------
    def __getElement(parent : Element.Element, id):
        if parent.id() == id:
            return parent
        
        for child in parent.children():
            childID = ElementTree.__getElement(child, id)
            if childID != None:
                return childID
        
        return None
    
    #----------------------------------------------------------------------------------------------
    def __getElements(element : Element.Element, criterias : dict):
        elements = []
        toBeUsed = None
        criteria_keys = list(criterias.keys())

        if element.isObject():
            toBeUsed = element["content"]["mxCell"]
        else:
            toBeUsed = element["content"]
        
        # ANY -------------------------------------------------------------------------------------
        if (criterias["mode"] == "ANY"):
            haveMatch = False

            if "style" in criterias:
                if "@style" in toBeUsed:
                    haveMatch = ElementTree.__checkStyleCriteria(toBeUsed["@style"], criterias["style"], criterias["mode"])

            if "geometry" in criterias and not haveMatch:
                if "mxGeometry" in toBeUsed:
                    haveMatch = ElementTree.__checkGeometryCriteria(toBeUsed["mxGeometry"], criterias["geometry"], criterias["mode"])
 
            if not haveMatch:
                element_keys = list(toBeUsed.keys())
                for key in criteria_keys:
                    if not key.startswith("@"):
                        continue

                    if key == "@id":
                        if criterias[key] == element[key]:
                            haveMatch = True
                            break

                    if not key in element_keys:
                        continue
                    
                    if criterias[key] == toBeUsed[key]:
                        haveMatch = True
                        break
            
            if haveMatch:
                elements.append(element)
            
        # ALL -------------------------------------------------------------------------------------
        elif (criterias["mode"] == "ALL"):
            checkNext = True

            if checkNext:
                if "style" in criterias:
                    if "@style" in toBeUsed:
                        checkNext = ElementTree.__checkStyleCriteria(toBeUsed["@style"], criterias["style"], criterias["mode"])
                    else:
                        checkNext = False

            if checkNext:         
                if "geometry" in criterias:
                    if ("mxGeometry" in toBeUsed):
                        checkNext = ElementTree.__checkGeometryCriteria(toBeUsed["mxGeometry"], criterias["geometry"], criterias["mode"])
                    else:
                        checkNext = False
            
            if checkNext:
                element_keys = list(toBeUsed.keys())
                for key in criteria_keys:
                    if not checkNext:
                        break

                    if not key.startswith("@"):
                        continue

                    if key == "@id":
                        if criterias[key] != element[key]:
                            checkNext = False
                            break
                        continue

                    if not key in element_keys:
                        checkNext = False
                        break
                    
                    if criterias[key] != toBeUsed[key]:
                        checkNext = False
                        break

            if checkNext:
                elements.append(element)

        for child in element.children():
            elements.extend(ElementTree.__getElements(child, criterias))
        
        return elements

    #----------------------------------------------------------------------------------------------
    def __checkStyleCriteria(styleString : str, criteria, mode):
        """
        The string is expected to be a semicolon seperated list.
        """

        # Within the style string there are single values and (mainly) key value pairs.
        # These are seperated by semicolons.
        pairs = styleString.split(";")
        keys_in_criteria = list(criteria.keys())

        # 1. For mode ANY on the first match, we can return true
        if mode == "ANY":
            # 1.1 we look at each key value pair within the style string
            for pair in pairs:
                # 1.1.1 It can be an empty string. In that case, we continue.
                if pair == "":
                    continue

                # 1.1.2 Values are assigned by an equal sign to the keys
                key_value = pair.split("=")
                key = key_value[0]

                # 1.1.3 If the current key is not requested by the criteria, we continue
                if not key in keys_in_criteria:
                    continue

                # 1.1.4 If the current key has no assigned value, within the criteria the value should be None.
                # If that matches, we have a match
                if len(key_value) == 1:
                    if criteria[key] == None:
                        return True
                    else:
                        continue
                
                # 1.1.5 If we came here, we have a key value pair
                # If that does match, we return true. (For "ANY" any criteria must match)
                value = key_value[1]
                if value == criteria[key]:
                    return True

            return False         

        # 2. For mode ALL all criteria must match
        if mode == "ALL":
            num_of_criterias = len(keys_in_criteria)
            matches = 0
            # 2.1 we look at each key value pair within the style string
            for pair in pairs:
                # 2.1.1 It can be an empty string. In that case, we continue.
                if pair == "":
                    continue

                # 2.1.2 Values are assigned by an equal sign to the keys
                key_value = pair.split("=")
                key = key_value[0]

                # 2.1.3 If the current key is not requested by the criteria, we continue
                if not key in keys_in_criteria:
                    continue

                # 2.1.4 If the current key has no assigned value, within the criteria the value should be None.
                # If that does not match, we return false. (For "ALL" all criteria must match)
                if len(key_value) == 1:
                    if criteria[key] != None:
                        return False
                    else:
                        matches += 1
                        continue
                
                # 2.1.5 If we came here, we have a key value pair
                # If that does not match, we return false. (For "ALL" all criteria must match)
                value = key_value[1]
                if value != criteria[key]:
                    return False
                matches += 1

            # 2.2 For ALL all criteria must match ...
            if matches == num_of_criterias:
                return True
            else:
                return False
        # 3. This should not happen
        Infos.announceWarning("Select mode \"ANY\" or \"ALL\"")
        return False

    #----------------------------------------------------------------------------------------------
    def __checkGeometryCriteria(geometry : dict, criteria, mode):
        """
        
        """

        # # Within the style string there are single values and (mainly) key value pairs.
        # # These are seperated by semicolons.
        keys = list(geometry.keys())
        keys_in_criteria = list(criteria.keys())

        # 1. For mode ANY on the first match, we can return true
        if mode == "ANY":
            # 1.1 we look at each key value pair within the geometry
            for key in keys:
                # 1.1.1 If the current key is not requested by the criteria, we continue
                if not key in keys_in_criteria:
                    continue

                # 1.1.2 If the key is a criteria
                # If that does match, we return true. (For "ANY" any criteria must match)
                value = geometry[key]
                if value == criteria[key]:
                    return True
            return False         

        # 2. For mode ALL all criteria must match
        if mode == "ALL":
            num_of_criterias = len(keys_in_criteria)
            matches = 0
            # 1.1 we look at each key value pair within the geometry
            for key in keys:
                # 1.1.1 If the current key is not requested by the criteria, we continue
                if not key in keys_in_criteria:
                    continue

                # 1.1.2 If the key is a criteria
                # If that does match, we return true. (For "ANY" any criteria must match)
                value = geometry[key]
                if value != criteria[key]:
                    return False
                matches += 1
            if num_of_criterias == matches:
                return True
            else:
                return False

        # 3. This should not happen
        Infos.announceWarning("Select mode \"ANY\" or \"ALL\"")
        return False