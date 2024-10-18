import math
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QGraphicsScene

class HierarchicalTreeLayout:
    def __init__(self, scene: QGraphicsScene, canvas_width: int, canvas_height: int):
        self.scene = scene
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def layout(self, root_node):
        """Initiates the layout by calculating tree depth and positioning nodes."""
        depth = self.calculate_depth(root_node)

        # Start the root node positioning in the center of the canvas width
        root_position_x = self.canvas_width / 2
        print(f"Root node positioned at: ({root_position_x}, {self.canvas_height / (depth + 1)})")
        self.position_nodes(root_node, 0, root_position_x, self.canvas_width, depth)

    def calculate_depth(self, node, depth=0):
        """Recursively calculate the maximum depth of the tree."""
        if not node.children:
            return depth
        return max(self.calculate_depth(child, depth + 1) for child in node.children)

    def position_nodes(self, node, generation, position, spacing, depth):
        """Recursively position nodes in a hierarchical layout."""
        if node is None:
            return

        # Print the screen (canvas) height to debug
        print(f"Screen (canvas) height: {self.canvas_height}")

        # Calculate y position for the node, relative to the depth
        y_pos = (generation / (depth + 1)) * self.canvas_height  # Divide height based on generation

        # Set the position of the current node
        node.setPos(QPointF(position, y_pos))

        # Print the node identifier and the calculated y-axis position for debugging
        print(f"Positioning node {node.identifier} at (x: {position}, y: {y_pos})")

        # Update the LineItems connected to this node
        self.update_lines_for_node(node)

        # Calculate child positions
        num_children = len(node.children)
        if num_children > 0:
            child_spacing = self.canvas_width / (num_children + 1)  # Adjust spacing for children across width
            for index, child in enumerate(node.children):
                child_position = child_spacing * (index + 1)

                print(f"Positioning child {child.identifier} at (x: {child_position}, y: {y_pos + spacing})")

                self.position_nodes(child, generation + 1, child_position, spacing, depth)

    def update_lines_for_node(self, node):
        """Update the lines connected to the node."""
        for line in node.lines:  # Assuming node has a list of connected lines
            line.updateLine()  # Use the correct method to update the line's position
