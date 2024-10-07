import math
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsScene


class HierarchicalTreeLayout:
    def __init__(self, scene: QGraphicsScene):
        self.scene = scene

    def layout(self, root_node):
        self.position_nodes(root_node, 0, 0, 100)

    def position_nodes(self, node, generation, position, spacing):
        """Recursively position nodes in a hierarchical layout."""
        if node is None:
            return

        # Set position of the current node
        node.setPos(QPointF(position, generation * spacing))

        # Calculate child positions
        num_children = len(node.children)  # Assuming each node has a children attribute
        if num_children > 0:
            child_spacing = spacing / num_children
            for index, child in enumerate(node.children):
                child_position = position - (child_spacing * (num_children - 1)) / 2 + child_spacing * index
                self.position_nodes(child, generation + 1, child_position, spacing)

