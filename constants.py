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
    RadialTree = 2
    HierarchicalTree = 3
    ForceDirected = 4
    FruchtermanReingold = 5

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

class ApplicationIconSize(IntEnum):
    Big = 64
    Medium = 48
    Small = 32