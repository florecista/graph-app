import math
from graph.GraphLayout import GraphLayout

class CircularLayout(GraphLayout):
    def __init__(self, node_list, edge_list, height, width):
        self.nodes = node_list
        self.edges = edge_list
        self.canvas_height = height
        self.canvas_width = width

        self.node_map = {}

        # Initialize node positions
        self.all_to_circular_positions()

        for node in self.nodes:
            self.node_map[node.identifier] = node

    def all_to_circular_positions(self):
        num_nodes = len(self.nodes)
        if num_nodes == 0:
            return

        radius = min(self.canvas_width, self.canvas_height) / 2 - 50  # Adjust for padding
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2

        for i, node in enumerate(self.nodes):
            angle = 2 * math.pi * i / num_nodes
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            node.setPos(x, y)  # Set node position

            # After moving the node, update its edges
            for edge in node.lines:
                edge.updateLine()

    def layout(self):
        # No additional layout adjustments needed for circular layout
        pass
