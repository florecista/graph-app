
from datetime import datetime
from datetime import date

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QByteArray, QBuffer
from PyQt5.QtGui import QImage, QPixmap, QIcon

from managers import js_manager
from utils import signal_throttle

class NodePropertyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.node: dict = {}
        self.node_valid_keys: list = []
        self.groups: list[str] = []
        self.types: list[str] = []
        self.label_types: list[str] = []
        self.offset = 0

    def index(self, row: int, column: int, parent: QModelIndex = ...):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, self.node)

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        if 'Attributes' in self.node.keys():
            return len(self.node_valid_keys) + len(self.node['Attributes'])
        else:
            return len(self.node_valid_keys)

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        return 2

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Property"
                if section == 1:
                    return "Value"
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex):
        f = QAbstractTableModel.flags(self, index)
        if index.column() == 1:
            f |= Qt.ItemIsEditable
            if isinstance(index.data(Qt.UserRole), bool):
                f |= Qt.ItemIsUserCheckable
        return f

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not self.node:
            return None
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if index.column() == 0:
                    if index.row() < self.offset:
                        return self.node_valid_keys[index.row()]
                    else:
                        return self.node['Attributes'][index.row() - self.offset]['name']
                elif index.column() == 1:
                    if index.row() < self.offset:
                        if self.node_valid_keys[index.row()] == 'Image':
                            return self.node['Image']['name']
                        else:
                            return self.node[self.node_valid_keys[index.row()]]
                    else:
                        return self.node['Attributes'][index.row() - self.offset]['description']
            elif role == Qt.ToolTipRole:
                if index.row() < self.offset and index.column() == 1:
                    if self.node_valid_keys[index.row()] == 'Image':
                        image = QImage.fromData(self.__str_to_q_byte_array(self.node['Image']['image']))
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
                        pxm.loadFromData(self.__str_to_q_byte_array(self.node['Image']['image']))
                        return QIcon(pxm)
                return None
            elif role == Qt.CheckStateRole:
                if index.row() < self.offset and index.column() == 1:
                    attr = self.node_valid_keys[index.row()]
                    if isinstance(self.node[attr], bool):
                        return self.node[attr]
                return None
            elif role == Qt.UserRole:
                if index.row() < self.offset:
                    attr = self.node_valid_keys[index.row()]
                    if attr == 'Group':
                        return self.node['Group'], self.groups
                    elif attr == 'Type':
                        assert js_manager is not None
                        return self.node['Type'], self.types, js_manager.qt_icons(self.node['Group'])
                    elif attr == 'Label':
                        return self.node['Label'], self.label_types
                    else:
                        return self.node[attr]
                else:
                    attr: dict = self.node['Attributes'][index.row() - self.offset]
                    if attr['type'] == 'date':
                        val = attr['description']
                        if not val:
                            return date(1, 1, 1)
                        return datetime.strptime(val, '%m/%d/%Y').date()
                    else:
                        return attr['description']
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        if not self.node:
            return False
        if index.isValid() and role == Qt.EditRole and index.column() == 1:
            if index.row() < self.offset:
                if self.node_valid_keys[index.row()] == 'Group':
                    assert js_manager is not None
                    js_manager.update_node_group(self.node, value)
                elif self.node_valid_keys[index.row()] == 'Type':
                    assert js_manager is not None
                    js_manager.update_node_type(node=self.node, node_type=value)
                else:
                    self.node[self.node_valid_keys[index.row()]] = value
                    self.dataChanged.emit(index, index)
                return True
            else:
                self.node['Attributes'][index.row() - self.offset]['description'] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    @signal_throttle()
    def reset(self, node: {}):
        if node == self.node:
            return
        self.beginResetModel()
        self.node = node
        if not node:
            self.node_valid_keys = []
            self.groups = []
            self.types = []
            self.label_types = []
        else:
            self.node_valid_keys = list(self.node.keys())
            if 'Attributes' in self.node_valid_keys:
                self.node_valid_keys.remove('Attributes')
            if 'Position' in self.node_valid_keys:
                self.node_valid_keys.remove('Position')
            self.offset = len(self.node_valid_keys)

            assert js_manager is not None
            group: str = self.node['Group']
            self.groups = js_manager.groups()
            self.types = js_manager.types(group)
            self.label_types = js_manager.attribute_names(group, self.node['Type'])
        self.endResetModel()


    @staticmethod
    def __str_to_q_byte_array(val: str) -> QByteArray:
        q_byte_array = QByteArray(val.encode())
        q_byte_array = QByteArray.fromBase64(q_byte_array)
        return q_byte_array
