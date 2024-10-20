import math
import random
from PyQt5.QtCore import QPoint
from graph.GraphLayout import GraphLayout
from widgets.GraphEdge import GraphEdge
from widgets.GraphItem import GraphItem


class ForceDirectedLayout(GraphLayout):
    def __init__(self, node_list, edge_list, height, width, default_eject_factor=0.1,
                 default_small_dist_eject_factor=0.05,
                 default_condense_factor=0.01, max_delta_x=10, max_delta_y=10):
        self.nodes = node_list
        self.edges = edge_list

        self.canvas_height = height
        self.canvas_width = width
        self.default_eject_factor = default_eject_factor
        self.default_small_dist_eject_factor = default_small_dist_eject_factor
        self.default_condense_factor = default_condense_factor
        self.max_delta_x = max_delta_x
        self.max_delta_y = max_delta_y

        self.node_map = {}
        self.dx_map = {}
        self.dy_map = {}

        # Initialize node positions and force constant
        self.all_to_random_positions()
        self.k = math.sqrt(self.canvas_height * self.canvas_width / len(self.nodes))

        # Initialize maps for dx and dy
        for node in self.nodes:
            self.node_map[node.identifier] = node
            self.dx_map[node.identifier] = 0  # Initialize for each node
            self.dy_map[node.identifier] = 0  # Initialize for each node

    def layout(self):
        # print("Starting layout...")
        # for node in self.nodes:
        #     print(f"Node {node.identifier} connected edges: {[edge for edge in node.lines]}")
        self.calculate_repulsive()
        self.calculate_traction()
        self.update_coordinates()

    def calculate_repulsive(self):
        for v in self.nodes:
            identifier = v.identifier
            self.dx_map[identifier] = 0.0
            self.dy_map[identifier] = 0.0
            for u in self.nodes:
                self.calculate_repulsive_for(u, v, identifier)

    def calculate_repulsive_for(self, u, v, target):
        if u != v:
            eject_factor = self.default_eject_factor
            dist_x = v.pos().x() - u.pos().x()
            dist_y = v.pos().y() - u.pos().y()
            dist = math.sqrt(dist_x * dist_x + dist_y * dist_y)
            if dist < 200:
                eject_factor = self.default_small_dist_eject_factor

            if 0 <= dist < 600:
                self.dx_map[target] += dist_x / dist * self.k * self.k / dist * eject_factor
                self.dy_map[target] += dist_y / dist * self.k * self.k / dist * eject_factor

    def calculate_traction(self):
        for edge in self.edges:
            # Ensure that 'start' and 'end' attributes exist and are valid GraphItems
            start_node = edge.start  # Directly access 'start' (no need to wrap in GraphItem)
            end_node = edge.end  # Directly access 'end'

            if start_node is None or end_node is None:
                print(f"Warning: Edge {edge} is missing start or end node.")
                continue

            source_identifier = start_node.identifier
            target_identifier = end_node.identifier

            # Retrieve nodes from node_map using identifiers
            start_node = self.node_map.get(source_identifier)
            end_node = self.node_map.get(target_identifier)

            # Check if nodes exist in the node_map
            if start_node is None:
                print(f"Warning: Missing start node for edge with identifier {source_identifier}")
                continue
            if end_node is None:
                print(f"Warning: Missing end node for edge with identifier {target_identifier}")
                continue

            # Proceed with traction calculations if both nodes are valid
            dist_x = start_node.pos().x() - end_node.pos().x()
            dist_y = start_node.pos().y() - end_node.pos().y()
            dist = math.sqrt(dist_x ** 2 + dist_y ** 2)

            if dist_x >= 150 and dist_y >= 350:
                adjustment = dist / self.k * self.default_condense_factor
                self.dx_map[source_identifier] -= dist_x * adjustment
                self.dy_map[source_identifier] -= dist_y * adjustment
                self.dx_map[target_identifier] += dist_x * adjustment
                self.dy_map[target_identifier] += dist_y * adjustment

    def update_coordinates(self):
        for node in self.nodes:
            identifier = node.identifier  # Already a GraphItem, so no need to wrap it again

            # Ensure dx and dy are properly calculated for the node
            dx = math.floor(self.dx_map.get(identifier, 0))  # Use .get() to avoid KeyErrors
            dy = math.floor(self.dy_map.get(identifier, 0))

            node.setPos(node.pos().x() + dx, node.pos().y() + dy)

        # After updating node positions, ensure the edges are updated
        for edge in self.edges:
            edge.updateLine()

    def all_to_random_positions(self):
        for node in self.nodes:
            new_pos = QPoint(int(random.random() * self.canvas_width), int(random.random() * self.canvas_height))
            node.setPos(new_pos)

    def run_iterations(self, num_iterations=50):
        for i in range(num_iterations):
            self.layout()
            self.update_coordinates()
