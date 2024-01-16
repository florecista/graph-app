from enum import IntEnum, Enum

class GraphHideOrphans(IntEnum):
    No = 0
    Yes = 1

class CentralityGradient(IntEnum):
    Select = 0
    Viridis = 1
    RdBu = 2

class GraphLayout(IntEnum):
    Select = 0
    Circular = 1
    Radial = 2
    Tree = 3
    SubGraph = 4

class CentralityShowBy(IntEnum):
    Select = 0
    Size = 1
    Color = 2
    Both = 3

class CentralityType(IntEnum):
    Select = 0
    Degrees = 1
    Eigenvactor = 2
    Katz = 3
    PageRank = 4
    Closeness = 5
    Betweenness = 6

class LabelPosition(IntEnum):
    Above = 0
    Middle = 1
    Below = 2

class NodeShapes(str, Enum):
    Circle = "o"
    Square = "s"
    Triangle = "^"
    Diamond = "d"

