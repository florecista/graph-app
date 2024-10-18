import constants
from graph.CircularLayout import CircularLayout
from graph.ForceDirectedLayout import ForceDirectedLayout
from graph.HierarchicalTreeLayout import HierarchicalTreeLayout
from graph.RadialTreeLayout import RadialTreeLayout


# from graph.RadialTreeLayout import RadialTreeLayout  # You'll need to implement this
# from graph.HierarchicalTreeLayout import HierarchicalTreeLayout  # You'll need to implement this
# from graph.CircularLayout import CircularLayout  # You'll need to implement this
# from graph.GridLayout import GridLayout  # You'll need to implement this

class LayoutFactory:
    def create_layout(self, layout, nodes, edges, height, width):
        if layout == constants.GraphLayout.HierarchicalTree:
            return HierarchicalTreeLayout(nodes, width, height)
        elif layout == constants.GraphLayout.Circular:
            return CircularLayout(nodes, edges, height, width)
        elif layout == constants.GraphLayout.RadialTree:
            return RadialTreeLayout(nodes, edges, height, width)
        elif layout == constants.GraphLayout.ForceDirected:
            return ForceDirectedLayout(nodes, edges, height, width)
        else:
            raise ValueError(f"Unknown layout: {layout}")
