"""
Represents the geometry of an element.
"""
import json

import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

class Geometry(dict):
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, geometry = None):
        """
        """
        if geometry == None:
            return
        
        for key in geometry:
            self[key] = geometry[key]

    #----------------------------------------------------------------------------------------------
    def __dumpArray(self, array, indent):
        """
        Ich gehe hier von einem Format für die Geometry bei Edges aus, dass bei anderen Einstellungen anders sein kann.
        ==> Man kann Informationen übersehen, wenn man sich auf dump() verlässt.
        """
        print(indent + "- Array")
        indent = indent + "  "
        for key in array.keys():
            if key == "mxPoint":
                for mxPoint in array["mxPoint"]:
                    print(indent + "- mxPoint")
                    for key in mxPoint.keys():
                        print(indent + "  - " + key + ": " + str(mxPoint[key]))
                continue
            print(indent + "- " + key + ": " + str(array[key]))
        # for mxPoint in mxPoints:
            # print(indent + "- mxPoint")
            # for key in mxPoint.keys():
                # print(indent + "  - " + key + ": " + str(mxPoint[key]))

    #----------------------------------------------------------------------------------------------
    def __dumpMxPoints(self, mxPoints, indent):
        """
        Ich gehe hier von einem Format für die Geometry bei Edges aus, dass bei anderen Einstellungen anders sein kann.
        ==> Man kann Informationen übersehen, wenn man sich auf dump() verlässt.
        """
        print(indent + "- mxPoints")
        indent = indent + "  "
        for mxPoint in mxPoints:
            print(indent + "- mxPoint")
            for key in mxPoint.keys():
                print(indent + "  - " + key + ": " + str(mxPoint[key]))

    ###############################################################################################
    # Public functions
    #----------------------------------------------------------------------------------------------
    def dump(self, indent = ""):
        line = (60 - 11 - len(indent)) * '-'
        print(indent + "mxGeometry " + line)
        
        for key in self.keys():
            if key == "mxPoint":
                self.__dumpMxPoints(self[key], indent)
                continue

            if key == "Array":
                self.__dumpArray(self[key], indent)
                continue
            print(indent + "- " + key + ": " + str(self[key]))
    
    #----------------------------------------------------------------------------------------------
    def setHeight(self, height):
        """
        Sets the height.
        """
        self["@height"] = str(height)

    #----------------------------------------------------------------------------------------------
    def setWidth(self, width):
        """
        Sets the width.
        """
        self["@width"] = str(width)

    #----------------------------------------------------------------------------------------------
    def setX(self, x):
        """
        Sets the x coordinate.
        """
        self["@x"] = str(x)

    #----------------------------------------------------------------------------------------------
    def setY(self, y):
        """
        Sets the y coordinate.
        """
        self["@y"] = str(y)

    #----------------------------------------------------------------------------------------------
    def set(self, coords):
        """
        Sets [x, y, width, height].
        """
        self["@x"]      = str(coords[0])
        self["@y"]      = str(coords[1])
        self["@width"]  = str(coords[2])
        self["@height"] = str(coords[3])
    
    #----------------------------------------------------------------------------------------------
    def coords(self) -> list[int]:
        """
        Returns the coordinates in [x, y, width, height].
        """
        coords = []
        coords.append(self.x())
        coords.append(self.y())
        coords.append(self.width())
        coords.append(self.height())
        return coords
    
    #----------------------------------------------------------------------------------------------
    def height(self) -> int:
        """
        Returns the height.
        If the height does not exist, 0 will be returned.
        """
        if "@height" in self:
            return int(self["@height"])
        return 0
    
    #----------------------------------------------------------------------------------------------
    def width(self) -> int:
        """
        width.x coordinate.
        If the width does not exist, 0 will be returned.
        """
        if "@width" in self:
            return int(self["@width"])
        return 0
    
    #----------------------------------------------------------------------------------------------
    def x(self) -> int:
        """
        Returns the x coordinate.
        If the x coordinate does not exist, 0 will be returned.
        """
        if "@x" in self:
            return int(self["@x"])
        return 0
    
    #----------------------------------------------------------------------------------------------
    def y(self) -> int:
        """
        Returns the y coordinate.
        If the y coordinate does not exist, 0 will be returned.
        """
        if "@y" in self:
            return int(self["@y"])
        return 0

###################################################################################################
# Public global functions / Helper functions
