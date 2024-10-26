import base64
import ast

from lxml import etree
from xml.etree.ElementTree import Element, SubElement, ElementTree, parse

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

        if 'Attributes' in node_data:
            attributes_raw = node_data.get('Attributes', '')

            if attributes_raw:
                try:
                    # Case 1: If 'Attributes' is a list (new format with nested dictionaries)
                    if isinstance(attributes_raw, str):
                        if attributes_raw.startswith("["):
                            # This is likely the new format (a list of dicts as a string)
                            node_data['Attributes'] = ast.literal_eval(attributes_raw)
                        else:
                            # Case 2: Handle the old format (semi-colon separated dictionaries)
                            node_data['Attributes'] = [ast.literal_eval(attr) for attr in attributes_raw.split(';') if
                                                       attr.strip()]
                        print(f"Parsed Attributes for node {node_id}: {node_data['Attributes']}")
                    else:
                        raise ValueError("Attributes field is not a valid string")
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing Attributes: {e}")
                    node_data['Attributes'] = []  # Fall back to empty attributes if parsing fails
            else:
                node_data['Attributes'] = []  # No attributes found

        # Handle image data safely
        image_data = node_data.get("Image", None)

        image_base64 = None

        # Safely handle the case where image_data is None or empty
        if image_data and image_data != '{}':  # Check if image_data is not empty
            try:
                image_data_dict = ast.literal_eval(image_data)
                image_base64 = image_data_dict.get('image', '')  # Use .get() to avoid KeyErrors
                image_name = image_data_dict.get('name', '')
                image_pixmap = load_base64_image(image_base64) if image_base64 else None
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing image data: {e}")
                image_data_dict = {}
                image_pixmap = None  # If there's an error, avoid loading an image
        else:
            image_data_dict = {}
            image_pixmap = None  # Set image to None if there's no valid data

        # Handle image scaling
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


def save_graphml(graph_scene, file_path):
    root = etree.Element("graphml")
    graph_element = etree.SubElement(root, "graph", edgedefault="undirected")

    # Define keys (using attrib to set 'for' because 'for' is a Python keyword)
    etree.SubElement(root, "key", id="d0", attrib={"for": "node", "attr.name": "Group", "attr.type": "string"})
    etree.SubElement(root, "key", id="d1", attrib={"for": "node", "attr.name": "Type", "attr.type": "string"})
    etree.SubElement(root, "key", id="d2", attrib={"for": "node", "attr.name": "Attributes", "attr.type": "string"})
    etree.SubElement(root, "key", id="d3", attrib={"for": "node", "attr.name": "Label", "attr.type": "string"})
    etree.SubElement(root, "key", id="d4", attrib={"for": "node", "attr.name": "Position", "attr.type": "string"})
    etree.SubElement(root, "key", id="d5", attrib={"for": "node", "attr.name": "Image", "attr.type": "string"})
    etree.SubElement(root, "key", id="d6", attrib={"for": "node", "attr.name": "Image Scale", "attr.type": "boolean"})
    etree.SubElement(root, "key", id="d7", attrib={"for": "edge", "attr.name": "label", "attr.type": "string"})

    for item in graph_scene.items():
        if isinstance(item, GraphItem):
            node = etree.SubElement(graph_element, "node", id=str(item.identifier))

            # Group (d0)
            etree.SubElement(node, "data", key="d0").text = item.attributes.get('Group', '')

            # Type (d1)
            etree.SubElement(node, "data", key="d1").text = item.attributes.get('Type', '')

            # Attributes (d2)
            etree.SubElement(node, "data", key="d2").text = str(item.attributes.get('Attributes', ''))

            # Label (d3)
            etree.SubElement(node, "data", key="d3").text = item.attributes.get('Label', '')

            # Position (d4)
            pos = item.pos()
            etree.SubElement(node, "data", key="d4").text = f"{pos.x()};{pos.y()}"

            # Image (d5)
            image_data = item.attributes.get('Image', {})
            etree.SubElement(node, "data", key="d5").text = str(image_data) if image_data else '{}'

            # Image Scale (d6)
            etree.SubElement(node, "data", key="d6").text = str(item.attributes.get('Image Scale', 'false')).lower()

    # Save edges
    for item in graph_scene.items():
        if isinstance(item, GraphEdge):
            edge = etree.SubElement(graph_element, "edge", source=str(item.start.identifier), target=str(item.end.identifier))

            # Edge label (d7)
            etree.SubElement(edge, "data", key="d7").text = item.label or ""

    # Write to file
    tree = etree.ElementTree(root)
    tree.write(file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

def save_gexf(scene, file_name):
    gexf = Element('gexf', xmlns="http://www.gexf.net/1.2draft", version="1.2")
    graph = SubElement(gexf, 'graph', mode="static", defaultedgetype="directed")

    # Nodes
    nodes = SubElement(graph, 'nodes')
    for node in scene.items():
        if isinstance(node, GraphItem):
            node_elem = SubElement(nodes, 'node', id=str(node.identifier), label=node.label)
            # Add more attributes as needed

    # Edges
    edges = SubElement(graph, 'edges')
    for edge in scene.items():
        if isinstance(edge, GraphEdge):
            edge_elem = SubElement(edges, 'edge',
                                   source=str(edge.start.identifier),
                                   target=str(edge.end.identifier))
            # Add more edge attributes as needed

    # Write to file
    ElementTree(gexf).write(file_name, encoding="utf-8", xml_declaration=True)

def open_gexf(scene, file_name):
    # Parse GEXF file
    tree = parse(file_name)
    root = tree.getroot()

    # Get GEXF namespace to handle XML elements correctly
    ns = {"gexf": "http://gexf.net/1.3", "viz": "http://gexf.net/1.3/viz"}

    # Find nodes
    for node_elem in root.findall(".//gexf:node", namespaces=ns):
        node_id = node_elem.get("id")
        label = node_elem.get("label", "")

        # Extract custom attributes (like code, city, latitude, longitude)
        attributes = {}
        for attvalue_elem in node_elem.findall(".//gexf:attvalue", namespaces=ns):
            attr_for = attvalue_elem.get("for")
            attr_value = attvalue_elem.get("value")
            if attr_for and attr_value:
                attributes[attr_for] = attr_value

        # Extract position if available
        pos_elem = node_elem.find(".//viz:position", namespaces=ns)
        x = float(pos_elem.get("x", "0")) if pos_elem is not None else 0
        y = float(pos_elem.get("y", "0")) if pos_elem is not None else 0

        # Create GraphItem with these values
        graph_item = GraphItem(label=label, attributes=attributes, position=QPointF(x, y))
        graph_item.identifier = node_id  # Ensure IDs match for edge referencing

        # Add to the scene
        scene.addItem(graph_item)

    # Find edges
    for edge_elem in root.findall(".//gexf:edge", namespaces=ns):
        source_id = edge_elem.get("source")
        target_id = edge_elem.get("target")

        # Find source and target GraphItems by ID
        source_item = next((item for item in scene.items() if isinstance(item, GraphItem) and item.identifier == source_id), None)
        target_item = next((item for item in scene.items() if isinstance(item, GraphItem) and item.identifier == target_id), None)

        # Create GraphEdge if both source and target are found
        if source_item and target_item:
            graph_edge = GraphEdge(source=source_item, target=target_item)
            scene.addItem(graph_edge)

    print("GEXF file loaded successfully into scene!")
