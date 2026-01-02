import json

import MyFramework.Data             as Data
import MyPyDrawIO.Element           as Element
import MyFramework.Informations     as Infos
import MyPyDrawIO.Geometry          as Geometry

class EdgeGeometry(Geometry.Geometry):
    """
    EdgeGeometry are derived from [Geometry](./Geometry.html).
    With respect to the Geometry base class, this derived class provides additional functionality related to edges.

    - EINE FUNKTIONSGRUPPE
        - [entry()](../MyPyDrawIO/EdgeGeometry.html#EdgeGeometry.entry)
    """
    ###############################################################################################
    # class variables

    ###############################################################################################
    # private functions
    #----------------------------------------------------------------------------------------------
    def __init__(self, geometry = None):
        """
        """
        super().__init__(geometry)

    ###############################################################################################
    # Public functions
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
###################################################################################################
# Public global functions / Helper functions
#--------------------------------------------------------------------------------------------------
# 
