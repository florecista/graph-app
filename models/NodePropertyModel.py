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
        if not self.node:
            return 0
        # Get the number of valid keys and the count of 'Attributes' items if they exist
        attributes_count = len(self.node.attributes.get('Attributes', [])) if isinstance(self.node, GraphItem) else 0
        return len(self.node_valid_keys) + attributes_count

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

        total_rows = self.rowCount()  # Get the total number of rows
        if index.row() >= total_rows:
            return None

        # Retrieve the key based on the row index
        if index.row() < len(self.node_valid_keys):
            key = self.node_valid_keys[index.row()]
        else:
            # Handle attribute data if the row is beyond the high-level keys
            attr_index = index.row() - len(self.node_valid_keys)
            if 'Attributes' in self.node.attributes:
                attribute = self.node.attributes['Attributes'][attr_index]
                key = attribute.get('name', '')
            else:
                return None

        # Now use the 'key' to return the appropriate data based on the role
        if role in (Qt.DisplayRole, Qt.EditRole):
            if index.column() == 0:
                return key  # Property name
            elif index.column() == 1:
                if isinstance(self.node, GraphItem):
                    return self.node.attributes.get(key, '') if index.row() < len(
                        self.node_valid_keys) else attribute.get('description', '')
                elif isinstance(self.node, dict):
                    return self.node.get(key, '')

        # Handle other roles as needed...
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole or not self.node:
            return False

        if index.row() < len(self.node_valid_keys):
            # Update high-level attribute directly in the node attributes
            key = self.node_valid_keys[index.row()]
            self.node.attributes[key] = value
        else:
            # Update an item in the Attributes list
            attribute_index = index.row() - len(self.node_valid_keys)
            if 0 <= attribute_index < len(self.node.attributes['Attributes']):
                self.node.attributes['Attributes'][attribute_index]['description'] = value
            else:
                return False  # Prevent out-of-range errors

        self.dataChanged.emit(index, index)  # Notify the view of the data change
        return True

    def _get_user_role_data(self, key):
        if key == 'Group':
            return (self.node.attributes.get('Group', ''), self.groups)
        elif key == 'Type':
            return (self.node.attributes.get('Type', ''), self.types, js_manager.qt_icons(self.node.attributes.get('Group', '')))
        elif key == 'Label':
            return self.node.attributes.get('Label', '')

    def reset(self, node):
        self.beginResetModel()
        self.node = node.get('selected_node') if isinstance(node, dict) and 'selected_node' in node else node

        if isinstance(self.node, GraphItem):
            self.node_valid_keys = list(self.node.attributes.keys())
            self.node_valid_keys = [k for k in self.node_valid_keys if k not in ('Attributes', 'Position')]
            self.offset = len(self.node_valid_keys)
            group = self.node.attributes.get('Group', '')
            node_type = self.node.attributes.get('Type', '')
        else:
            self.node_valid_keys, self.groups, self.types, self.label_types = [], [], [], []
            self.endResetModel()
            return

        if group:
            self.groups = js_manager.groups()
            self.types = js_manager.types(group)
            self.label_types = js_manager.attribute_names(group, node_type)
        else:
            self.groups, self.types, self.label_types = [], [], []

        self.endResetModel()

    @staticmethod
    def __str_to_q_byte_array(val: str) -> QByteArray:
        return QByteArray.fromBase64(QByteArray(val.encode()))
