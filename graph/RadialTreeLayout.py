import math

from PySide6.QtCore import QPointF


class RadialTreeLayout:
    def __init__(self, nodes, edges, height, width):
        self.nodes = nodes
        self.edges = edges
        self.height = height
        self.width = width

    def get_node_depth(self, node):
        """Calculate the depth of a node in the graph."""
        depth = 0
        current_node = node

        while current_node.has_parent():  # Replace this with your actual check
            current_node = current_node.parent  # Replace with your method to get the parent
            depth += 1

        return depth

    def layout(self):
        center_x = self.width / 2
        center_y = self.height / 2
        radius_increment = 100

        depth_dict = {}
        for node in self.nodes:
            depth = self.get_node_depth(node)
            if depth not in depth_dict:
                depth_dict[depth] = []
            depth_dict[depth].append(node)

        for depth, nodes_at_depth in depth_dict.items():
            radius = (depth + 1) * radius_increment
            angle_increment = 360 / len(nodes_at_depth) if nodes_at_depth else 0

            for index, node in enumerate(nodes_at_depth):
                angle = angle_increment * index
                x = center_x + radius * math.cos(math.radians(angle))
                y = center_y + radius * math.sin(math.radians(angle))
                node.setPos(float(x), float(y))  # Set node position

                # After moving the node, update its edges
                for edge in node.lines:  # Assuming you have a 'lines' attribute for edges
                    edge.updateLine()  # Update the edge's position
