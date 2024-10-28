import math
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QGraphicsScene


class HierarchicalTreeLayout:
    def __init__(self, scene: QGraphicsScene, canvas_width: int, canvas_height: int):
        self.scene = scene
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.min_distance = 50  # Minimum distance to avoid overlap between nodes

    def layout(self, root_node):
        """Initiates the layout by calculating tree depth and positioning nodes."""
        depth = self.calculate_depth(root_node)
        occupied_positions = {}  # Track occupied x-positions per depth level

        # Start the root node positioning in the center of the canvas width
        root_position_x = self.canvas_width / 2
        self.position_nodes(root_node, 0, root_position_x, self.canvas_width, depth, occupied_positions)

        # Apply a final pass to resolve any overlaps
        self.apply_repulsion(root_node)

    def calculate_depth(self, node, depth=0):
        """Recursively calculate the maximum depth of the tree."""
        if not node.children:
            return depth
        return max(self.calculate_depth(child, depth + 1) for child in node.children)

    def position_nodes(self, node, generation, position, spacing, depth, occupied_positions):
        """Recursively position nodes in a hierarchical layout with non-overlapping x-positions."""
        if node is None:
            return

        # Initialize occupied positions list for the current generation level
        if generation not in occupied_positions:
            occupied_positions[generation] = []

        # Adjust position if it’s too close to any previously placed node at the same depth
        while any(abs(position - other_x) < self.min_distance for other_x in occupied_positions[generation]):
            position += self.min_distance  # Shift right until there's enough space

        # Set the position of the current node and mark this x position as occupied
        y_pos = (generation / (depth + 1)) * self.canvas_height
        node.setPos(QPointF(position, y_pos))
        occupied_positions[generation].append(position)

        # Update the lines connected to this node
        self.update_lines_for_node(node)

        # Position child nodes symmetrically
        num_children = len(node.children)
        if num_children > 0:
            child_spacing = spacing / (num_children + 1)

            for index, child in enumerate(node.children):
                # Calculate child position symmetrically and ensure no overlap using occupied positions
                child_position = position + (index - (num_children - 1) / 2) * child_spacing
                self.position_nodes(child, generation + 1, child_position, spacing, depth, occupied_positions)

    def apply_repulsion(self, node):
        """Adjust positions of nodes and their children to avoid overlaps."""
        for child in node.children:
            self.apply_repulsion(child)  # Recursively apply to children

            # Check for overlap with sibling nodes and apply repulsion if needed
            for sibling in node.children:
                if sibling != child and self.are_too_close(child, sibling):
                    self.repel_nodes(child, sibling)

    def are_too_close(self, node1, node2):
        """Check if two nodes are too close based on their x-axis positions."""
        pos1 = node1.pos()
        pos2 = node2.pos()
        return abs(pos1.x() - pos2.x()) < self.min_distance

    def repel_nodes(self, node1, node2):
        """Move nodes apart to avoid overlap on the x-axis."""
        pos1 = node1.pos()
        pos2 = node2.pos()
        midpoint = (pos1.x() + pos2.x()) / 2

        # Apply equal repulsion away from midpoint
        node1.setPos(QPointF(midpoint - self.min_distance / 2, pos1.y()))
        node2.setPos(QPointF(midpoint + self.min_distance / 2, pos2.y()))

    def update_lines_for_node(self, node):
        """Update the lines connected to the node."""
        for line in node.lines:  # Assuming node has a list of connected lines
            line.updateLine()  # Use the correct method to update the line's position
