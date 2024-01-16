from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

from managers import graphm, js_manager
from utils import signal_throttle

class EdgePropertyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.selected_edge_index: int = -1

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        if self.__is_index_valid():
            return len(list(list(graphm.cur_G.edges(data=True))[0][-1].keys()))
        else:
            return 0

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        if self.__is_index_valid():
            return 2
        else:
            return 0

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
        return f

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if index.isValid() and self.__is_index_valid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                if index.column() == 0:
                    keys = list(list(graphm.cur_G.edges(data=True))[self.selected_edge_index][-1].keys())
                    return keys[index.row()].capitalize() + ':'
                elif index.column() == 1:
                    values = list(list(graphm.cur_G.edges(data=True))[self.selected_edge_index][-1].values())
                    return str(values[index.row()])
            elif role == Qt.UserRole and index.column() == 1:
                values = list(list(graphm.cur_G.edges(data=True))[self.selected_edge_index][-1].values())
                return values[index.row()]
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole):
        if index.isValid() and self.__is_index_valid() and role == Qt.EditRole and index.column() == 1:

            current_value = graphm.get_cur_edge_value(self.selected_edge_index, index.row())

            if isinstance(current_value, float):
                value = float.value.replace(',', '.')
                graphm.set_cur_edge_value(self.selected_edge_index, index.row(), value)

            elif isinstance(current_value, str):
                graphm.set_cur_edge_value(self.selected_edge_index, index.row(), value)

            self.dataChanged.emit(index, index)
            return True
        return False

    def __is_index_valid(self) -> bool:
        return -1 < self.selected_edge_index < graphm.cur_G.number_of_edges()

    @signal_throttle()
    def edge_selection_changed(self, index: int):
        if index == self.selected_edge_index:
            return
        self.beginResetModel()
        self.selected_edge_index = index
        self.endResetModel()

    def current_graph_changed(self):
        self.beginResetModel()
        self.endResetModel()
