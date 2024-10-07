import math
import random
from PyQt5.QtCore import QPoint
from graph.GraphLayout import GraphLayout
from widgets.GraphEdge import GraphEdge
from widgets.GraphItem import GraphItem

class ForceDirectedLayout(GraphLayout):
    def __init__(self, node_list, edge_list, height, width, default_eject_factor=0.1, default_small_dist_eject_factor=0.05,
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
            source_identifier = GraphItem(edge._get_source()).identifier  # Change to _get_source
            target_identifier = GraphItem(edge._get_target()).identifier  # Assuming you have _get_target

            start_node = self.node_map.get(source_identifier)
            end_node = self.node_map.get(target_identifier)

            if start_node is None:
                print("Missing start node for edge", source_identifier)
            if end_node is None:
                print("Missing destination node for edge", target_identifier)

            dist_x = start_node.pos().x() - end_node.pos().x()
            dist_y = start_node.pos().y() - end_node.pos().y()
            dist = math.sqrt(dist_x * dist_x + dist_y * dist_y)

            if dist_x >= 150 and dist_y >= 350:
                self.dx_map[source_identifier] -= dist_x * dist / self.k * self.default_condense_factor
                self.dy_map[source_identifier] -= dist_y * dist / self.k * self.default_condense_factor
                self.dx_map[target_identifier] -= dist_x * dist / self.k * self.default_condense_factor
                self.dy_map[target_identifier] -= dist_y * dist / self.k * self.default_condense_factor

    def update_coordinates(self):
        for node in self.nodes:
            identifier = GraphItem(node).identifier
            print(f"Node Identifier: {identifier}")  # Debug print

            # Check if the identifier exists in dx_map
            if identifier not in self.dx_map:
                print(f"Warning: Identifier {identifier} not found in dx_map")
                continue  # Skip this node or handle as necessary

            dx = math.floor(self.dx_map[identifier])
            dy = math.floor(self.dy_map[identifier])

            node.setPos(node.pos().x() + dx, node.pos().y() + dy)

    def all_to_random_positions(self):
        for node in self.nodes:
            new_pos = QPoint(int(random.random() * self.canvas_width), int(random.random() * self.canvas_height))
            node.setPos(new_pos)

    def run_iterations(self, num_iterations=50):
        for i in range(num_iterations):
            self.layout()
            self.update_coordinates()
