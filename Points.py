"""
Points are use to define where edges connect to vertices.

A point consists of four values, defining x and y in absolute and relative coordinates.
[dx in %, dy in %, x in pt, y in pt]

In draw.io, this can best be observed in the dialog box for editing the connection points of a vertex.
The origin for connection points is in the top left corner as encircled in yellow.

In the image there is a connection point (black arrow), which will stay 40 points (pts) away from the left side
and -20 points from the bottom regardless of resizing the vertex.
- x coordinate: 
    - `dx = 0 % and x = 40 pts`.
    - `connection point x = vertex.width * dx [%] + x [pts]`
- y coordinate: 
    - `dy = 100 % and y = -20 pts`.
    - `connection point y = vertex.height * dy [%] + y [pts]`

<img src="./images/MyPyDrawIO-Connection Points.png", width=400>

## Default points
This Points class defines the default points used as connection points in draw.io.

- CARDINALS   = [N, S, E, W]
- CORNERS     = [NE, NW, SE, SW]
- MAINS       = [N, S, E, W, NE, NW, SE, SW]
- ALL         = [N, S, E, W, NE, NW, SE, SW, NNE, NNW, SEE, NNE, NEE, SSE, SSW, SWW, NWW]
"""
class Points():
    # [Dx in %, Dy in %, x in pt, y in pt]
    NW  = [0   ,0   ,0,0]
    NNW = [0.25,0   ,0,0]
    N   = [0.5 ,0   ,0,0]
    NNE = [0.75,0   ,0,0]
    NE  = [1   ,0   ,0,0]
    NEE = [1   ,0.25,0,0]
    E   = [1   ,0.5 ,0,0]
    SEE = [1   ,0.75,0,0]
    SE  = [1   ,1   ,0,0]
    SSE = [0.75,1   ,0,0]
    S   = [0.5 ,1   ,0,0]
    SSW = [0.25,1   ,0,0]
    SW  = [0   ,1   ,0,0]
    SWW = [0   ,0.75,0,0]
    W   = [0   ,0.5 ,0,0]
    NWW = [0   ,0.25,0,0]

    CARDINALS   = [N, S, E, W]
    CORNERS     = [NE, NW, SE, SW]
    MAINS       = [N, S, E, W, NE, NW, SE, SW]
    ALL         = [N, S, E, W, NE, NW, SE, SW, NNE, NNW, SEE, NNE, NEE, SSE, SSW, SWW, NWW]

def toDict(points : list) -> dict:
    """
    Expects a list [dx, dy, x, y] and rturns a dict with keys
    - dx
    - dy
    - x
    - y 
    """
    return {
        "dx" : points[0],
        "dy" : points[1],
        "x" : points[2],
        "y" : points[3]
    }

def points(theDict : dict) -> list:
    """
    Expects a dict with keys
    - dx
    - dy
    - x
    - y

    and returns it as a list [dx, dy, x, y]
    """
    return [
        theDict["dx"],
        theDict["dy"],
        theDict["x"],
        theDict["y"]
        ]