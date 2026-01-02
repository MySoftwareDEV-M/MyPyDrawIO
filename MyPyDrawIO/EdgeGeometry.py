"""
EdgeGeometry are derived from [Geometry](./Geometry.html).
With respect to the Geometry base class, this derived class provides additional functionality related to edges.
"""
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

import MyPyDrawIO.Element           as Element
import MyPyDrawIO.Geometry          as Geometry

class EdgeGeometry(Geometry.Geometry):
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
