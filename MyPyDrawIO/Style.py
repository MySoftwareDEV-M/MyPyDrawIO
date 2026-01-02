"""
Represents the style of an element.

Functions of Style can be grouped by their purpose.
- CONTENT
    - [content()](../MyPyDrawIO/Style.html#Style.content)
    - [dump()](../MyPyDrawIO/Style.html#Style.dump)
- ATTRIBUTES & KEY VALUE PAIRS
    - [attributeExists()](../MyPyDrawIO/Style.html#Style.attributeExists)
    - [attributes()](../MyPyDrawIO/Style.html#Style.attributes)
    - [deleteAttribute()](../MyPyDrawIO/Style.html#Style.deleteAttribute)
    - [deleteKey()](../MyPyDrawIO/Style.html#Style.deleteKey)
    - [keyExists()](../MyPyDrawIO/Style.html#Style.keyExists)
    - [keys()](../MyPyDrawIO/Style.html#Style.keys)
    - [value()](../MyPyDrawIO/Style.html#Style.value)
    - [setValue()](../MyPyDrawIO/Style.html#Style.setValue)

## attributes and keyValuePairs
A style can be configured by attributes or by key value pairs.
(I use this wording, not knowing if draw.io developer use a different wording.)

An example for a attributes is the `swimlane` which configures a vertex to be, well, a swimlane.
Within the style this attribute has no asigned value.

An example for key value pairs is `rounded` which configures if the line of the vertex has rounded or sharp corners.
Within the style you set `rounded = 0` or `rounded = 1`. Values can be more complex then just `0` or `1`.

On the left in the image you see a vertex configured as a swimlane with no key value pair rounded or `rounded = 0`.
On the right you see a vertex configured as a swimlane with `rounded = 1`.

<img src="./images/MyPyDrawIO-Style - Attributes and KeyValuePairs.png">

## Configure styles
Configure the style of an element is a three step process.
Setting a style, can always be done directly using functions like 
[setValue()](../MyPyDrawIO/Style.html#Style.setValue). 
For some configurations convinient functions are implemented for the
[vertex style](./VertexStyle.html)
and
[edge style](./EdgeStyle.html).
Using these, you do not need to the details on the attributes, keys, and their values,
but you can just call one function with one or two parameter.

1. Retrieve the specific style from the vertex or edge by using 
- [Vertex : style()](./Vertex.html#Vertex.style) or
- [Edge : style()](./Edge.html#Edge.style).
2. Configure the style, using the general
[Style : setValue()](./Style.html#Style.setValue) function or specific functions like
[EdgeStyle : setArrow()](./EdgeStyle.html#EdgeStyle.setArrow).
3. Set the style at the vertex or edge, you retrieved it from.

Example using convinient functions:
```

edgeStyle = edge.style()
edgeStyle.setArrow("halfCircle", "start")
edgeStyle.setArrow("openThin", "end")
edgeStyle.setWaypoints("orthogonal vertical curved")
# ...
edge.setStyle(edgeStyle)

```
Example using direct functions, resulting in configuration achieved with `edgeStyle.setArrow("halfCircle", "start")`:
```
edgeStyle = edge.style()
edgeStyle.setValue("startArrow", "halfCircle")
edgeStyle.setValue("startFill", "0")
edge.setStyle(edgeStyle)
```

## Convinient functions
As explained above, there are convinient functions to set some configurations and 
(as mentioned 
[here](../MyPyDrawIO.html#manipulating-objects-and-extending-mypydrawio-functionality))
you are welcomed to implement your own functions for specific configurations.

The recommended structure for implementation consists of there parts:
1. definition
2. access functions for the definition
3. get and set function to use the configurations

Define the configuration as class variables within the respective
[vertex style](./VertexStyle.html) or [edge style](./EdgeStyle.html):
```
_way_points = {
"straight"  : [None,None,   None],
"orthogonal": ["orthogonalEdgeStyle",   None,   None],
...
"elbow vertical": ["elbowEdgeStyle",None,   "vertical"],
...
}
_way_points_keys = ["edgeStyle", "curved", "elbow"]
```

Provide global access functions to these class variables:
```
def supported_waypoints():
return list(EdgeStyle._way_points.keys())

def supported_waypoints_keys():
return EdgeStyle._way_points_keys
```

Provide the get and set functions.
These shall use the private functions Style.__getFormat__(...) and Style.__setFormat__(...)
and act as a wrapper around them.
```
def getWaypoints(self) -> str:
return self.__getFormat__(EdgeStyle._way_points_keys, self._way_points)

def setWaypoints(self, waypoint : tuple):
self.__setFormat__(waypoint, EdgeStyle._way_points_keys, self._way_points)
```

HINT:
The same structure is applied for configuring arrows for edges.
But the functions and definitions take into respect, that arrows can be configured for both sides of
edges (start and end).
```
def getArrow(self, side = "end") -> str:
if(side == "start"):
return self.__getFormat__(EdgeStyle._arrow_start_keys, self._arrows)
if(side == "end"):
return self.__getFormat__(EdgeStyle._arrow_end_keys, self._arrows)

```
"""
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

class Style(dict):
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, style):
        """
        style is a string representing a semicolon seperated list of style attributes and key value pairs.
        """
        attributes = []
        keyValuePairs = {}
        style = style.split(";")
        for element in style:
            if(element == ""):
                continue
            keyValue = element.split("=")
            
            if(len(keyValue) == 1):
                attributes.append(keyValue[0])

            elif(len(keyValue) == 2):
                keyValuePairs[keyValue[0]] = keyValue[1]
            else:
                Infos.announceError(str(keyValue))
        
        self["attributes"] = attributes
        self["keyValuePairs"] = keyValuePairs

    ###############################################################################################
    # Public functions
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # CONTENT
    #----------------------------------------------------------------------------------------------
    def _content(self) -> str:
        """
        Used in Element to retrieve the content of the style to be saved in a draw.io file.
        """
        content = ""

        for value in self["attributes"]:
            content += value + ";"

        keyValuePairs = self["keyValuePairs"]
        for key in keyValuePairs:
            content += key + "=" + keyValuePairs[key] + ";"
        
        return content
    
    #----------------------------------------------------------------------------------------------
    def dump(self, indent = ""):
        """
        Prints all attributes and key value pairs.
        """
        line = (60 - 7 - len(indent)) * '-'
        print(indent + "@style " + line)
        for value in self["attributes"]:
            print(indent + "- " + value) 
        
        keyValuePairs = self["keyValuePairs"]
        for key in keyValuePairs:
            print(indent + "- " + key + ": " + str(keyValuePairs[key]))

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # KEY & VALUE
    #----------------------------------------------------------------------------------------------
    def attributeExists(self, attribute) -> bool:
        """
        Returns if the attribute exists.
        """
        return (attribute in self["attributes"])
    
    #----------------------------------------------------------------------------------------------
    def attributes(self) -> list:
        """
        Returns a list of all attributes.
        """
        return list(self["attributes"])
    
    #----------------------------------------------------------------------------------------------
    def deleteAttribute(self, attribute):
        """
        Deletes the attribute if it exists.
        """
        if attribute in self["attributes"]:
            self["attributes"].remove(attribute)
        
    #----------------------------------------------------------------------------------------------
    def deleteKey(self, key):
        """
        Deletes the key (with its value) if it exists.
        """        
        keyValuePairs = self["keyValuePairs"]
        if key in keyValuePairs:
            del keyValuePairs[key]

    #----------------------------------------------------------------------------------------------
    def keyExists(self, key) -> bool:
        """
        Returns if the key exists.
        """
        return (key in self["keyValuePairs"].keys())
    
    #----------------------------------------------------------------------------------------------
    def keys(self) -> list:
        """
        Returns a list of all keys.
        """
        return list(self["keyValuePairs"].keys())

    #----------------------------------------------------------------------------------------------
    def value(self, key) -> str:
        """
        Returns the value to the key if it exists.
        Otherwise None will be returned.
        """
        keyValuePairs = self["keyValuePairs"]
        if key in keyValuePairs:
            return keyValuePairs[key]
    
        return None
    
    #----------------------------------------------------------------------------------------------
    def setAttribute(self, attribute):
        """
        Adds the attribute, if it does not exist yet.
        """
        self["attributes"].append(attribute)
    
    #----------------------------------------------------------------------------------------------
    def setValue(self, key, value = None):
        """
        Adds the key value pair, if it does not exist yet otherwise the value for the key is just set.
        """
        keyValuePairs = self["keyValuePairs"]
        keyValuePairs[key] = str(value)
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # FORMATS
    #----------------------------------------------------------------------------------------------
    def __getFormat__(self, keys : list, formats : dict):
        """
        Leider setzt DrawIO nicht immer alle Werte sauber zurück, wenn zwischen einigen Formaten gewechselt wird.
        Deswegen kann
            a) keine Prüfung auf exakte Gleichheit durchgeführt werden.
            b) ist die Reihenfolge der keys manchmal entscheidend, um das richtige Format zu finden.

        - Für den ersten Key wird geprüft, ob bereits nur ein Format zutrifft. 
            - Wenn ja, wird dieses ausgegeben.
            - Wenn nein, wird die Prüfung für den nächsten Key mit den verbleibenden möglichen Formaten geprüft.
            - Dies wird für alle Keys durchgeführt, bis nur ein Format übrig bleibt.
        - Es wird NICHT darauf geprüft, dass alle Key-Value Paare zutreffen. 
            Begründung: Nicht immer werden von DrawIO Key-Value Paare gelöscht, wenn diese für ein Format nicht benötigt werden.
        """
        keyValuePairs = self["keyValuePairs"]
        formatCandidates = list(formats.keys())
        index = 0
        for key in keys:
            remaining = []
            for format in formatCandidates:
                if key in keyValuePairs:

                    if keyValuePairs[key] == formats[format][index]:
                        remaining.append(format)
                else:
                    if None == formats[format][index]:
                        remaining.append(format)

            if len(remaining) == 1:
                return remaining[0]
            if len(remaining) == 0:
                return None
                
            formatCandidates = remaining
            index = index + 1
        
        return None
    
    #----------------------------------------------------------------------------------------------
    def __setFormat__(self, format : str, keys : list, formats : dict):
        """
        """
        if not format in formats.keys():
            Infos.announceError("There is no format \"" + format + "\"")
            return
        
        keyValuePairs = self["keyValuePairs"]

        for key in keys:
            if key in keyValuePairs:
                del keyValuePairs[key]

        formatDefinition = formats[format]

        for i in range(len(formatDefinition)):
            if formatDefinition[i] != None:
                keyValuePairs[keys[i]] = formatDefinition[i]
    
###################################################################################################
# Public global functions / Helper functions
