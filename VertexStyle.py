"""
Represents the style of a vertex.

Functions of Element can be grouped by their purpose.
- CONNECTION POINTS
    - [points()](../MyPyDrawIO/VertexStyle.html#VertexStyle.points)
    - [setPoints()](../MyPyDrawIO/VertexStyle.html#VertexStyle.setPoints)
"""
import MyFramework.Data             as Data
import MyFramework.Informations     as Infos

import MyPyDrawIO.Style             as Style

class VertexStyle(Style.Style):
    ###############################################################################################
    # class variables

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
    def points(self) -> list:
        """
        Returns the conection points of a vertex as a list [Dx, Dy, x, y].

        Further details on connection points can be found on the
        [Point](../MyPyDrawIO/Points.html) page.

        Helpful technical information can be found 
        [here](https://www.drawio.com/doc/faq/shape-connection-points-customise).
        """
        if "points" in self["keyValuePairs"]:
            points = []
            tmp = self["keyValuePairs"]["points"]
            tmp = tmp[1:-1]

            tmp = tmp.split("],[")

            for t in tmp:
                t = t.replace("[", "")
                t = t.replace("]", "")
                t = t.split(",")
                point = {}
                # [Dx in %, Dy in %, ???, Dx in pt, Dy in %]
                point["Dx"]  = float(t[0])
                point["Dy"]  = float(t[1])
                point["x"] = float(t[3])
                point["y"] = float(t[4])

                points.append(point)

            return points

        return None
    
    #----------------------------------------------------------------------------------------------
    def setPoints(self, points):
        """
        Expects a list of conection points
        ```
        [
            [Dx1, Dy1, x1, y1],
            [Dx2, Dy2, x2, y2],
            ...
        ]
        ```
        and sets them as connection points for the vertex.
        
        The [Points class](../MyPyDrawIO/Points.html) provides a set of default points also used by draw.io.
        That page also provides further details on connection points.

        Helpful technical information can be found 
        [here](https://www.drawio.com/doc/faq/shape-connection-points-customise).
        """
        tmp = []
        for point in points:                
            t = [point[0], point[1], 0.0, point[2], point[3]]
            tmp.append(t)
        
        self["keyValuePairs"]["points"] = str(tmp)

###################################################################################################
# Public global functions / Helper functions
