from datetime import datetime, date
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QByteArray, QBuffer
from PyQt5.QtGui import QImage, QPixmap, QIcon
from managers import js_manager
from widgets.GraphItem import GraphItem


class NodePropertyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.node = None  # Can be a GraphItem or dict
        self.node_valid_keys = []
        self.groups = []
        self.types = []
        self.label_types = []
        self.offset = 0

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, self.node)

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.node_valid_keys)

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        return 2

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "Property" if section == 0 else "Value"
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        flags = super().flags(index)
        if index.column() == 1:
            flags |= Qt.ItemIsEditable
            if isinstance(index.data(Qt.UserRole), bool):
                flags |= Qt.ItemIsUserCheckable
        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not self.node or not index.isValid():
            return None

        key = self.node_valid_keys[index.row()]
        if role in (Qt.DisplayRole, Qt.EditRole):
            if index.column() == 0:
                return key  # Property name
            elif index.column() == 1:
                if isinstance(self.node, GraphItem):
                    return self.node.attributes.get(key, '')
                elif isinstance(self.node, dict):
                    return self.node.get(key, '')

        elif role == Qt.ToolTipRole and key == 'Image' and index.column() == 1:
            image_data = self.node.attributes.get('Image', {}).get('image', '') if isinstance(self.node, GraphItem) else self.node.get('Image', {}).get('image', '')
            image = QImage.fromData(self.__str_to_q_byte_array(image_data)).scaled(300, 300, Qt.KeepAspectRatio)
            if not image.isNull():
                data = QByteArray()
                buffer = QBuffer(data)
                image.save(buffer, 'PNG')
                return f"<img src='data:image/png;base64,{bytes(data.toBase64()).decode()}'>"

        elif role == Qt.DecorationRole and key == 'Type' and index.column() == 1:
            if isinstance(self.node, GraphItem):
                return js_manager.icons[js_manager.icon_name(self.node.attributes.get('Group', ''), self.node.attributes.get('Type', ''))]
            elif isinstance(self.node, dict):
                return js_manager.icons[js_manager.icon_name(self.node.get('Group', ''), self.node.get('Type', ''))]

        elif role == Qt.CheckStateRole and isinstance(self.node.get(key, None), bool):
            return Qt.Checked if self.node.get(key) else Qt.Unchecked

        elif role == Qt.UserRole:
            if key == 'Group':
                return (self.node.attributes.get('Group', ''), self.groups) if isinstance(self.node, GraphItem) else (self.node.get('Group', ''), self.groups)
            elif key == 'Type':
                return (self.node.attributes.get('Type', ''), self.types, js_manager.qt_icons(self.node.attributes.get('Group', ''))) if isinstance(self.node, GraphItem) else (self.node.get('Type', ''), self.types, js_manager.qt_icons(self.node.get('Group', '')))
            elif key == 'Label':
                return self.node.attributes.get('Label', '') if isinstance(self.node, GraphItem) else self.node.get('Label', '')

        return None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not self.node:
            return None

        if index.isValid():
            key = self.node_valid_keys[index.row()]

            # Handle display and edit roles for both columns
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if index.column() == 0:  # Property name
                    return key
                elif index.column() == 1:  # Property value
                    if isinstance(self.node, dict):
                        return self.node.get(key, '')
                    elif isinstance(self.node, GraphItem):
                        return self.node.attributes.get(key, '')

            # Handle check state role specifically for boolean values
            elif role == Qt.CheckStateRole:
                if isinstance(self.node, dict):
                    value = self.node.get(key, None)
                elif isinstance(self.node, GraphItem):
                    value = self.node.attributes.get(key, None)
                if isinstance(value, bool):
                    return Qt.Checked if value else Qt.Unchecked
            elif role == Qt.ToolTipRole:
                if index.row() < self.offset and index.column() == 1:
                    if self.node_valid_keys[index.row()] == 'Image':
                        # Convert direct Base64 string to image
                        image = QImage.fromData(self.__str_to_q_byte_array(self.node['Image']))
                        image = image.scaled(300, 300, Qt.KeepAspectRatio)
                        if not image.isNull():
                            data = QByteArray()
                            buffer = QBuffer(data)
                            image.save(buffer, 'PNG')
                            buffer.close()
                            return "<img src='data:image/png;base64,{}]'>".format(bytes(data.toBase64()).decode())
            elif role == Qt.DecorationRole:
                if index.row() < self.offset and index.column() == 1:
                    if self.node_valid_keys[index.row()] == 'Type':
                        assert js_manager is not None
                        return js_manager.icons[js_manager.icon_name(self.node['Group'], self.node['Type'])]
                    if self.node_valid_keys[index.row()] == 'Image':
                        pxm = QPixmap()
                        # Load from direct Base64 string
                        pxm.loadFromData(self.__str_to_q_byte_array(self.node['Image']))
                        return QIcon(pxm)
                return None
            elif role == Qt.UserRole:
                if key == 'Group':
                    return (self.node.get('Group', ''), self.groups) if isinstance(self.node, dict) else (
                    self.node.attributes.get('Group', ''), self.groups)
                elif key == 'Type':
                    return (self.node.get('Type', ''), self.types) if isinstance(self.node, dict) else (
                    self.node.attributes.get('Type', ''), self.types)
                elif key == 'Label':
                    return (self.node.get('Label', ''), self.label_types) if isinstance(self.node, dict) else (
                    self.node.attributes.get('Label', ''), self.label_types)
                else:
                    return self.node.get(key) if isinstance(self.node, dict) else self.node.attributes.get(key)

        return None

    def reset(self, node):
        self.beginResetModel()

        # Check if 'selected_node' exists and set self.node accordingly
        self.node = node.get('selected_node') if isinstance(node, dict) and 'selected_node' in node else node

        if isinstance(self.node, GraphItem):
            self.node_valid_keys = list(self.node.attributes.keys())
            if 'Attributes' in self.node_valid_keys:
                self.node_valid_keys.remove('Attributes')
            if 'Position' in self.node_valid_keys:
                self.node_valid_keys.remove('Position')
            group = self.node.attributes.get('Group', '')
            node_type = self.node.attributes.get('Type', '')
        elif isinstance(self.node, dict):
            self.node_valid_keys = list(self.node.keys())
            group = self.node.get('Group', '')
            node_type = self.node.get('Type', '')
        else:
            # Handle case where node is neither GraphItem nor dict
            self.node_valid_keys = []
            self.groups = []
            self.types = []
            self.label_types = []
            self.endResetModel()
            return

        # Populate groups, types, and label_types based on group and node_type
        if group:
            self.groups = js_manager.groups()
            self.types = js_manager.types(group)
            self.label_types = js_manager.attribute_names(group, node_type)
        else:
            self.groups = []
            self.types = []
            self.label_types = []

        self.endResetModel()

    @staticmethod
    def __str_to_q_byte_array(val: str) -> QByteArray:
        return QByteArray.fromBase64(QByteArray(val.encode()))
