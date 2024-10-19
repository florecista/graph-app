import networkx as nx
from managers.json import js_manager
from widgets.GraphItem import GraphItem
from widgets.GraphEdge import GraphEdge
from PyQt5.QtCore import QPointF, Qt
import ast


import os
from PyQt5.QtGui import QPixmap

def load_graphml_to_scene(graph_scene, file_path):
    # Step 1: Read the GraphML file using NetworkX
    graph = nx.read_graphml(file_path)

    node_map = {}  # To keep track of GraphItems and their corresponding GraphML nodes

    # Step 2: Iterate over the nodes in the GraphML file
    for node_id, node_data in graph.nodes(data=True):
        # Extract Group and Type attributes to fetch the icon
        group = node_data.get("Group", "")
        node_type = node_data.get("Type", "")
        icon = ""

        # Fetch the appropriate icon using js_manager logic
        for item in js_manager.data.get(group, []):
            if item['label'] == node_type:
                icon = item.get('icon', '')
                break

        # Build the pixmap for the GraphItem
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", icon)
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)

        # Create a new GraphItem using the pixmap
        graph_item = GraphItem(pixmap)

        # Set the identifier for the GraphItem based on GraphML node ID
        graph_item.identifier = node_id

        # Update node data using js_manager logic
        js_manager.update_node(node_data)

        # Handle 'Attributes', 'Image', and other attributes if they exist
        if 'Attributes' in node_data:
            node_data['Attributes'] = [ast.literal_eval(item) for item in node_data['Attributes'].split(';')]
            graph_item.attributes = node_data['Attributes']

        # Set default node label or use the one provided
        graph_item.label = node_data.get('Label', 'Node Name')

        # Set the position of the node (assuming GraphItem has setPos method)
        pos_x, pos_y = map(float, node_data.get('Position', '0;0').split(';'))
        graph_item.setPos(QPointF(pos_x, pos_y))

        # Add the node to the scene and keep track of it
        graph_scene.addItem(graph_item)
        node_map[node_id] = graph_item

    # Step 3: Iterate over the edges in the GraphML file
    for edge_source, edge_target, edge_data in graph.edges(data=True):
        # Create a new GraphEdge for each edge
        start_item = node_map[edge_source]
        end_item = node_map[edge_target]

        graph_edge = GraphEdge(start_item, end_item)

        # Add the edge to the scene and link it to the start and end nodes
        graph_scene.addItem(graph_edge)
        start_item.addLine(graph_edge)
        end_item.addLine(graph_edge)

    print("GraphML data successfully loaded into the scene.")