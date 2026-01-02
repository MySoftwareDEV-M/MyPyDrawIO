"""
EdgeStyles are derived from [Style](./Style.html).
With respect to the Style base class, this derived class provides additional functionality related to edges.

- CONNECTION OF EDGES WITH VERTICES 
<br>The general concept is explained [here](../MyPyDrawIO/Edge.html)
- [entry()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.entry)
- [setEntry()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.setEntry)
- [exit()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.exit)
- [setExit()](../MyPyDrawIO/EdgeStyle.html#EdgeStyle.setExit)

"""
import json

import MyFramework.Data             as Data
import MyPyDrawIO.Element           as Element
import MyFramework.Informations     as Infos
import MyPyDrawIO.Style             as Style


class EdgeStyle(Style.Style):
    ###############################################################################################
    # class variables
    _arrows = {
        "none"                  : (None,            None),
        "classic filled"        : ("classic",       "1"),
        "classicThin filled"    : ("classicThin",   "1"),
        "open"                  : ("open",          "0"),
        "openThin"              : ("openThin",      "0"),
        "openAsync"             : ("openAsync",     "0"),
        "block filled"          : ("block",         "1"),
        "blockThin filled"      : ("blockThin",     "1"),
        "async filled"          : ("async",         "1"),
        "oval filled"           : ("oval",          "1"),
        "diamond filled"        : ("diamond",       "1"),
        "diamondThin filled"    : ("diamondThin",   "1"),
        "classic"               : ("classic",       "0"),
        "blockThin"             : ("blockThin",     "0"),
        "async"                 : ("async",         "0"),
        "oval"                  : ("oval",          "0"),
        "diamond"               : ("diamond",       "0"),
        "diamondThin"           : ("diamondThin",   "0"),
        "box"                   : ("box",           "0"),
        "halfCircle"            : ("halfCircle",    "0"),
        "dash"                  : ("dash",          "0"),
        "cross"                 : ("cross",         "0"),
        "circlePlus"            : ("circlePlus",    "0"),
        "circle"                : ("circle",        "0"),
        "baseDash"              : ("baseDash",      "0"),
        "ERone"                 : ("ERone",         "0"),
    }
    _arrow_start_keys = ["startArrow", "startFill"]
    _arrow_end_keys   = ["endArrow", "endFill"]
        
    _way_points = {
        "straight"                      : [None,                        None,   None],
        "orthogonal"                    : ["orthogonalEdgeStyle",       None,   None],
        "elbow"                         : ["elbowEdgeStyle",            None,   None],
        "elbow vertical"                : ["elbowEdgeStyle",            None,   "vertical"],
        "isometric"                     : ["isometricEdgeStyle",        None,   None],
        "isometric vertical"            : ["isometricEdgeStyle",        None,   "vertical"],
        "orthogonal vertical curved"    : ["orthogonalEdgeStyle",       "1",    "vertical"],
        "entityRelation vertical"       : ["entityRelationEdgeStyle",   None,   "vertical"],
    }
    _way_points_keys = ["edgeStyle", "curved", "elbow"]

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, style):
        """
        """
        super().__init__(style)

    ###############################################################################################
    # Public functions
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SPECIAL VALUES
    #----------------------------------------------------------------------------------------------
    def entry(self):
        """
        Returns the entry point as list [dx, dy, x, y].

        If the entry does not exist None is returned.

        For details see [Edge > Connecting edges to vertices](../MyPyDrawIO/edge.html).
        """
        x = 0
        y = 0
        dx = 0
        dy = 0
        matches = 0
        if "entryX" in self["keyValuePairs"]:
            x = float(self["keyValuePairs"]["entryX"])
            matches = matches + 1

        if "entryY" in self["keyValuePairs"]:
            y = float(self["keyValuePairs"]["entryY"])
            matches = matches + 1

        if "entryDx" in self["keyValuePairs"]:
            dx = float(self["keyValuePairs"]["entryDx"])
            matches = matches + 1

        if "entryDy" in self["keyValuePairs"]:
            dy = float(self["keyValuePairs"]["entryDy"])
            matches = matches + 1

        if(matches == 4):
            return [x, y, dx, dy]
            
        if(matches == 0):
            return None
        
        Infos.announceWarning("There should be four entries for exit coordinate or none.")
        return None
    
    #----------------------------------------------------------------------------------------------
    def setEntry(self, entry = None):
        """
        Set coordinates, to connect the edge to the target vertex.

        entry can be a list, dict, or None
        - list --> [x, y, dx, dy]
        - dict --> dictionary with keys x, y, dx, and dy.
        - None --> coordinates will be deleted.

        For details see [Edge > Connecting edges to vertices](../MyPyDrawIO/edge.html).
        """

        if type(entry) == list:
            if len(entry) == 4:
                self["keyValuePairs"]["entryX"] = str(entry[0])
                self["keyValuePairs"]["entryY"] = str(entry[1])
                self["keyValuePairs"]["entryDx"] = str(entry[2])
                self["keyValuePairs"]["entryDy"] = str(entry[3])
            
            return

        if(entry == None):
            if "entryX" in self["keyValuePairs"]:
                del self["keyValuePairs"]["entryX"]

            if "entryY" in self["keyValuePairs"]:
                del self["keyValuePairs"]["entryY"]

            if "entryDx" in self["keyValuePairs"]:
                del self["keyValuePairs"]["entryDx"]

            if "entryDy" in self["keyValuePairs"]:
                del self["keyValuePairs"]["entryDy"]
        
            return
        
        self["keyValuePairs"]["entryX"] = str(entry["x"])
        self["keyValuePairs"]["entryY"] = str(entry["y"])
        self["keyValuePairs"]["entryDx"] = str(entry["dx"])
        self["keyValuePairs"]["entryDy"] = str(entry["dy"])
    
    #----------------------------------------------------------------------------------------------
    def exit(self) -> dict:
        """
        Returns the exit point as list [dx, dy, x, y].

        If the exit does not exist None is returned.

        For details see [Edge > Connecting edges to vertices](../MyPyDrawIO/edge.html).
        """
        x = 0
        y = 0
        dx = 0
        dy = 0
        matches = 0
        if "exitX" in self["keyValuePairs"]:
            x = float(self["keyValuePairs"]["exitX"])
            matches = matches + 1

        if "exitY" in self["keyValuePairs"]:
            y = float(self["keyValuePairs"]["exitY"])
            matches = matches + 1

        if "exitDx" in self["keyValuePairs"]:
            dx = float(self["keyValuePairs"]["exitDx"])
            matches = matches + 1

        if "exitDy" in self["keyValuePairs"]:
            dy = float(self["keyValuePairs"]["exitDy"])
            matches = matches + 1

        if(matches == 4):
            return [x, y, dx, dy]
            
        if(matches == 0):
            return None
        
        Infos.announceWarning("There should be four entries for exit coordinate or none.")
        return None
    
    #----------------------------------------------------------------------------------------------
    def setExit(self, exit = None):
        """
        Set coordinates, to connect the edge to the source vertex.

        entry can be a list, or None
        - list --> [x, y, dx, dy]
        - dict --> dictionary with keys x, y, dx, and dy.
        - None --> coordinates will be deleted.

        For details see [Edge > Connecting edges to vertices](../MyPyDrawIO/edge.html).
        """
        if type(exit) == list:
            self["keyValuePairs"]["exitX"] = str(exit[0])
            self["keyValuePairs"]["exitY"] = str(exit[1])
            self["keyValuePairs"]["exitDx"] = str(exit[2])
            self["keyValuePairs"]["exitDy"] = str(exit[3])            
            return
        
        if(exit == None):
            if "exitX" in self["keyValuePairs"]:
                del self["keyValuePairs"]["exitX"]

            if "exitY" in self["keyValuePairs"]:
                del self["keyValuePairs"]["exitY"]

            if "exitDx" in self["keyValuePairs"]:
                del self["keyValuePairs"]["exitDx"]

            if "exitDy" in self["keyValuePairs"]:
                del self["keyValuePairs"]["exitDy"]
            return
        
        self["keyValuePairs"]["exitX"] = str(exit["x"])
        self["keyValuePairs"]["exitY"] = str(exit["y"])
        self["keyValuePairs"]["exitDx"] = str(exit["dx"])
        self["keyValuePairs"]["exitDy"] = str(exit["dy"])
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ARROWS
    #----------------------------------------------------------------------------------------------
    def getArrow(self, side = "end") -> str:
        """
        Returns the current arrow set for the specified side.
        """
        if(side == "start"):
            return self.__getFormat__(EdgeStyle._arrow_start_keys, self._arrows)
        if(side == "end"):
            return self.__getFormat__(EdgeStyle._arrow_end_keys, self._arrows)
    
    #----------------------------------------------------------------------------------------------
    def setArrow(self, arrow : tuple, side = "end"):
        """
        Sets the arrow for the specified side.
        """
        if side == "start":
            if arrow == None:
                Infos.announceDebug("Das Löschen implementieren")
            else:
                self.__setFormat__(arrow, EdgeStyle._arrow_start_keys, self._arrows)
            return
        
        if side == "end":
            if arrow == None:
                Infos.announceDebug("Das Löschen implementieren")
            else:
                self.__setFormat__(arrow, EdgeStyle._arrow_end_keys, self._arrows)
            return
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # WAY POINTS
    #----------------------------------------------------------------------------------------------
    def getWaypoints(self) -> str:
        """
        Returns the current way points.
        """
        return self.__getFormat__(EdgeStyle._way_points_keys, self._way_points)
    
    #----------------------------------------------------------------------------------------------
    def setWaypoints(self, waypoint : tuple):
        """
        Sets the way points.
        """
        if waypoint == None:
            Infos.announceDebug("Das Löschen implementieren")
        else:
            self.__setFormat__(waypoint, EdgeStyle._way_points_keys, self._way_points)

###################################################################################################
# Public global functions / Helper functions
#--------------------------------------------------------------------------------------------------
# Arrows
def supported_arrows():
    return list(EdgeStyle._arrows.keys())

def supported_arrows_keys(side = "end"):
    if side == "start":
        return EdgeStyle._arrow_start_keys
    if side == "end":
        return EdgeStyle._arrow_end_keys
    return "Side must be \"start\" or \"end\""

#--------------------------------------------------------------------------------------------------
# Way points
def supported_waypoints():
    return list(EdgeStyle._way_points.keys())

def supported_waypoints_keys():
    return EdgeStyle._way_points_keys
