import math
import random
from PyQt5.QtCore import QPointF

class FruchtermanReingoldLayout:
    def __init__(self, nodes, edges, height, width, iterations=50, area_factor=1.0, gravity=1.0, cooling_factor=0.95):
        self.nodes = nodes
        self.edges = edges
        self.height = height
        self.width = width
        self.iterations = iterations
        self.area_factor = area_factor
        self.gravity = gravity
        self.cooling_factor = cooling_factor

        self.area = self.width * self.height
        self.k = math.sqrt(self.area / len(self.nodes))  # Optimal distance between nodes
        self.temperature = self.width / 10  # Initial temperature

        # Initialize node positions and displacement maps
        self.positions = {node.identifier: QPointF(random.random() * self.width, random.random() * self.height) for node in self.nodes}
        self.displacements = {node.identifier: QPointF(0, 0) for node in self.nodes}

    def layout(self):
        for _ in range(self.iterations):
            self.apply_repulsive_forces()
            self.apply_attractive_forces()
            self.update_positions()

            # Cool down the temperature to reduce movements over time
            self.temperature *= self.cooling_factor

    def apply_repulsive_forces(self):
        for v in self.nodes:
            self.displacements[v.identifier] = QPointF(0, 0)  # Reset displacement
            for u in self.nodes:
                if v != u:
                    delta = self.positions[v.identifier] - self.positions[u.identifier]
                    dist = math.sqrt(delta.x() ** 2 + delta.y() ** 2)
                    if dist > 0:
                        repulsive_force = (self.k ** 2) / dist
                        self.displacements[v.identifier] += delta / dist * repulsive_force

    def apply_attractive_forces(self):
        for edge in self.edges:
            start_node = edge.start
            end_node = edge.end

            if start_node is None or end_node is None:
                print(f"Warning: Edge {edge} is missing start or end node.")
                continue

            delta = self.positions[start_node.identifier] - self.positions[end_node.identifier]
            dist = math.sqrt(delta.x() ** 2 + delta.y() ** 2)
            if dist > 0:
                attractive_force = (dist ** 2) / self.k
                self.displacements[start_node.identifier] -= delta / dist * attractive_force
                self.displacements[end_node.identifier] += delta / dist * attractive_force

    def update_positions(self):
        for node in self.nodes:
            displacement = self.displacements[node.identifier]
            dist = math.sqrt(displacement.x() ** 2 + displacement.y() ** 2)

            if dist > 0:
                limited_disp = displacement / dist * min(dist, self.temperature)
                new_x = min(self.width - 50,
                            max(50, self.positions[node.identifier].x() + limited_disp.x()))  # Add margin of 50 pixels
                new_y = min(self.height - 50,
                            max(50, self.positions[node.identifier].y() + limited_disp.y()))  # Add margin of 50 pixels
                self.positions[node.identifier] = QPointF(new_x, new_y)

                # Update the node's position in the scene
                node.setPos(self.positions[node.identifier].x(), self.positions[node.identifier].y())

        # Ensure edges are updated as well
        for edge in self.edges:
            edge.updateLine()

    def run_iterations(self, num_iterations=50):
        for _ in range(num_iterations):
            self.layout()
