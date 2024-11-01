from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt

class EdgePropertyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.edge = None  # This will store the selected edge

    def set_edge(self, edge):
        """Sets the edge to display/edit in the table view."""
        self.beginResetModel()
        self.edge = edge
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return 1 if self.edge else 0  # Only one property, the label

    def columnCount(self, parent=QModelIndex()):
        return 2  # "Property" and "Value" columns

    def data(self, index, role=Qt.DisplayRole):
        if not self.edge or not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return "Label"  # Column 0 shows the property name
            elif index.column() == 1:
                return self.edge.label  # Column 1 shows the label value
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not self.edge or not index.isValid():
            return False

        if index.column() == 1 and role == Qt.EditRole:
            self.edge.label = value  # Update the label property on the edge
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == 1:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled
