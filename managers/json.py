import io
import json
import os
import xml.etree.ElementTree as ElementTree
from PIL import Image
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, Qt, QTemporaryFile, QBuffer
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QToolBox, QWidget, QSizePolicy, QSpacerItem, QGridLayout, QVBoxLayout, QLabel

from constants import ApplicationIconSize
from widgets.GraphItem import GraphItem


class JSONManager(QObject):
    node_updated = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.data: dict = {}
        self.images: dict = {}
        self.svgs: dict = {}
        self.icons: dict = {}
        self.pixmaps: dict = {}

    def init(self, file_name, icon_size=ApplicationIconSize.Small) -> None:
        with open(file_name) as json_file:
            self.data = json.load(json_file)

            for key in self.data.keys():
                for item in self.data[key]:
                    icon_name = item['icon']
                    svg_file_path = os.path.abspath('images\\' + icon_name)
                    f = open(svg_file_path)
                    contents = f.read()

                    tree = ElementTree.fromstring(contents)
                    tree.set('width', '32px')
                    tree.set('height', '32px')

                    byte_array = bytearray(contents.encode())
                    file = QTemporaryFile()
                    if file.open():
                        file.write(byte_array)
                        file.flush()

                        self.__create_svg(icon_name, contents)
                        self.__create_icon(icon_name, file.fileName())
                        self.__create_image(icon_name, file.fileName(), icon_size)

    def __create_svg(self, key, contents) -> None:
        self.svgs[key] = contents

    def __create_icon(self, key, file_name) -> None:
        self.icons[key] = QIcon(file_name)

    def __create_image(self, key, file_name, icon_size) -> None:
        q_pixmap = QPixmap(file_name)
        q_pixmap = q_pixmap.scaled(icon_size, icon_size, Qt.KeepAspectRatio)
        q_image = q_pixmap.toImage().convertToFormat(QImage.Format.Format_RGBA8888)

        # Convert QImage to PIL.Image
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        q_image.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        image = pil_im.resize((100, 100), Image.Resampling.LANCZOS)

        self.pixmaps[key] = q_pixmap
        self.images[key] = image

    def tool_box_widget(self, parent) -> QToolBox:
        assert len(self.data) > 0

        tool_box = QToolBox(parent)
        for key in self.data.keys():
            container = QWidget()
            box_layout = QVBoxLayout(container)
            grid_layout = QGridLayout(container)
            box_layout.addLayout(grid_layout)
            box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

            index = 0
            for item in self.data[key]:
                keys = item.keys()
                assert 'name' in keys
                assert 'label' in keys
                assert 'icon' in keys

                label = QLabel(container)
                label.setObjectName(item['name'])
                label.setMinimumSize(50, 50)
                label.setMaximumSize(100, 100)
                label.setPixmap(self.pixmaps[item['icon']])
                label.setAlignment(Qt.AlignCenter)
                label.setWordWrap(False)
                label.setMargin(0)

                label.setStyleSheet("QLabel::hover"
                                    "{"
                                    "background-color : lightgray;"
                                    "}")

                label.setToolTip(item['name'])

                label.setProperty('Group', key)
                label.setProperty('Type', item['label'])
                if 'attributes' in keys:
                    label.setProperty('Attributes', item['attributes'])
                else:
                    label.setProperty('Attributes', [])
                row = index // 2
                col = index % 2
                index += 1

                grid_layout.addWidget(label, row, col, 1, 1)

            tool_box.addItem(container, key.lower().capitalize())
            tool_box.setCurrentIndex(list(self.data.keys()).index('people'))
        return tool_box

    def icon_name(self, node_group: str, node_type: str) -> str:
        icons: list = [item['icon'] for item in self.data[node_group] if item['label'] == node_type]
        assert len(icons) == 1
        return icons[0]

    def qt_icons(self, node_group: str) -> [QIcon]:
        group: dict = self.data[node_group]
        icon_names: list = [item['icon'] for item in group]
        icons: list = [self.icons[key] for key in self.icons if key in icon_names]
        return icons

    def groups(self) -> [str]:
        return list(self.data.keys())

    def types(self, node_group):
        if node_group not in self.data:
            print(f"Error: Group '{node_group}' not found in data")
            return []  # Return an empty list or handle the error as needed
        return [item['label'] for item in self.data[node_group]]

    def attribute_names(self, node_group: str, node_type: str) -> [str]:
        element: dict = next(item for item in self.data[node_group] if item['label'] == node_type)
        attribute_names = ['Node Name']
        if 'attributes' in element.keys():
            attribute_names.extend([item['name'] for item in element['attributes']])
        return attribute_names

    def update_node_group(self, node, node_group: str) -> None:
        # Check if node is a GraphItem or a dict, and handle accordingly
        if isinstance(node, GraphItem):
            if node.attributes.get('Group') == node_group:
                return
            node.attributes['Group'] = node_group
            items = [item for item in self.data.get(node_group, [])]
            if items:
                self.update_node_type(node, items[0]['label'])  # Use the first available type
        elif isinstance(node, dict):
            if node['Group'] == node_group:
                return
            node['Group'] = node_group
            items = [item for item in self.data.get(node_group, [])]
            if items:
                self.update_node_type(node, items[0]['label'])

    def update_node_type(self, node, node_type: str) -> None:
        # Check if node is a GraphItem or a dict, and handle accordingly
        if isinstance(node, GraphItem):
            if node.attributes.get('Type') == node_type:
                return
            node.attributes['Type'] = node_type
            # Update node's attributes based on selected type
            items = [item for item in self.data.get(node.attributes.get('Group', ''), []) if item['label'] == node_type]
            if items:
                node.attributes['Attributes'] = items[0].get('attributes', []).copy()
                node.attributes['Label'] = node.attributes.get('Label', 'Node Name')
        elif isinstance(node, dict):
            if node['Type'] == node_type:
                return
            node['Type'] = node_type
            items = [item for item in self.data.get(node['Group'], []) if item['label'] == node_type]
            if items:
                node['Attributes'] = items[0].get('attributes', []).copy()
                node['Label'] = node.get('Label', 'Node Name')

    def update_node(self, node: dict) -> bool:
        #node_attributes = ('Group', 'Type', 'Label', 'Image', 'Position', 'Attributes')
        #for key in list(node.keys()):
        #    if key not in node_attributes:
        #        del node[key]

        #print(f"Updating node with data: {node}")

        if 'Group' not in node.keys() or node['Group'] not in self.groups():
            node['Group'] = 'object'
        if 'Type' not in node.keys() or node['Type'] not in self.types(node['Group']):
            node['Type'] = 'Unknown'
        if 'Label' not in node.keys() or node['Label'] not in self.attribute_names(node['Group'], node['Type']):
            node['Label'] = 'Node Name'
        if 'Image' not in node.keys():
            node['Image'] = str({'name': '', 'image': ''})
        if 'Image Scale' not in node.keys():
            node['Image Scale'] = True
        if 'Attributes' not in node.keys():
            element: dict = next(item for item in self.data['object'] if item['label'] == 'Unknown')
            if 'attributes' in element.keys():
                node['Attributes'] = ';'.join([json.dumps(item) for item in element['attributes']])
        if 'Position' not in node.keys() or len(list(map(float, node['Position'].split(';')))) != 2:
            node['Position'] = ';'.join(map(str, [0, 0]))

        return True


js_manager = JSONManager()