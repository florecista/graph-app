import base64
import ast

import networkx as nx
from managers.json import js_manager
from widgets.GraphItem import GraphItem
from widgets.GraphEdge import GraphEdge
from PyQt5.QtCore import QPointF, Qt, QByteArray
import ast


import os
from PyQt5.QtGui import QPixmap


def load_graphml_to_scene(graph_scene, file_path):
    # Step 1: Read the GraphML file using NetworkX
    graph = nx.read_graphml(file_path)

    node_map = {}  # To keep track of GraphItems and their corresponding GraphML nodes
    has_positions = True  # Flag to track if all nodes have positions

    # Step 2: Iterate over the nodes in the GraphML file
    for node_id, node_data in graph.nodes(data=True):
        label = node_data.get("Label", "")

        # Handle image data
        image_data = node_data.get("Image", {})
        image_data_dict = ast.literal_eval(image_data)
        image_base64 = image_data_dict['image']
        image_name = image_data_dict['name']
        image_pixmap = load_base64_image(image_base64)

        image_scale = node_data.get("Image Scale", False)  # Boolean flag for image scaling

        # Fetch icon based on Group and Type
        group = node_data.get("Group", "")
        node_type = node_data.get("Type", "")
        icon = ""

        for item in js_manager.data.get(group, []):
            if item['label'] == node_type:
                icon = item.get('icon', '')
                break

        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", icon)
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)

        # Create the GraphItem
        graph_item = GraphItem(
            pixmap,
            label=label,
            attributes=node_data,
            image=image_base64,
            image_scale=image_scale
        )

        graph_item.setZValue(1)
        graph_item.identifier = node_id

        # Update node data using js_manager logic
        js_manager.update_node(node_data)

        if 'Attributes' in node_data:
            node_data['Attributes'] = [ast.literal_eval(item) for item in node_data['Attributes'].split(';')]
            graph_item.attributes = node_data['Attributes']

        graph_item.label = node_data.get('Label', 'Node Name')

        # Handle position data (detect both pixel and normalized formats)
        position = node_data.get('Position', None)
        if position:
            try:
                pos_x, pos_y = map(float, position.split(';'))

                # Check if the positions seem to be normalized (values between 0 and 1)
                if 0 <= pos_x <= 1 and 0 <= pos_y <= 1:
                    # Assuming scene width and height for scaling purposes
                    scene_width = graph_scene.width() or 800  # Default width
                    scene_height = graph_scene.height() or 600  # Default height

                    pos_x *= scene_width
                    pos_y *= scene_height

                # Set the position of the node
                graph_item.setPos(QPointF(pos_x, pos_y))
            except (ValueError, TypeError):
                # Invalid position format, flag as false
                has_positions = False
        else:
            # Position attribute is missing, flag as false
            has_positions = False

        graph_scene.addItem(graph_item)
        node_map[node_id] = graph_item

    # Step 3: Iterate over the edges in the GraphML file
    for edge_source, edge_target, edge_data in graph.edges(data=True):
        start_item = node_map[edge_source]
        end_item = node_map[edge_target]

        # Extract edge attributes (label and weight)
        edge_label = edge_data.get("label", None)
        edge_weight = edge_data.get("weight", None)

        # Create the GraphEdge with the label and weight
        graph_edge = GraphEdge(start_item, end_item, label=edge_label, weight=edge_weight)
        graph_edge.setZValue(-1)

        # Add the edge to the scene and link it to the start and end nodes
        graph_scene.addItem(graph_edge)
        start_item.addLine(graph_edge)
        end_item.addLine(graph_edge)

    print("GraphML data successfully loaded into the scene.")

    # Return the flag indicating whether all nodes had positions
    return has_positions


def load_base64_image(image_data):
    try:
        # Decode the base64 string into bytes
        image_bytes = base64.b64decode(image_data)
        byte_array = QByteArray(image_bytes)
        pixmap = QPixmap()

        # Load the pixmap from the byte array
        if pixmap.loadFromData(byte_array):
            return pixmap
        else:
            print("Error: Could not load pixmap from base64 data")
            return None
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None