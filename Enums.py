from enum import Enum

class EdgeStyle(Enum):
    straight                    = 1
    orthogonal                  = 2
    elbow                       = 3
    elbow_vertical              = 4
    isometric                   = 5
    isometric_vertical          = 6
    isometric_vertical_curved   = 7
    entityRelation_vertical     = 8