import datetime
from PyQt5.QtCore import QModelIndex, Qt, QDate, QAbstractItemModel, pyqtSlot
from PyQt5.QtWidgets import QItemDelegate, QWidget, QComboBox, QDateEdit, QCheckBox, QLineEdit

from widgets.GraphItem import GraphItem
from widgets.ImagePropertyWidget import ImagePropertyWidget
from managers import js_manager


class NodePropertyDelegate(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        data = index.data(Qt.UserRole)
        model = index.model()
        key = model.node_valid_keys[index.row()] if index.row() < len(model.node_valid_keys) else ""

        if key == "Group":  # Handle Group field explicitly
            editor = QComboBox(parent)
            groups = js_manager.groups()
            editor.addItems(groups)
            return editor

        elif key == "Type":  # Handle Type field based on selected Group
            editor = QComboBox(parent)
            if isinstance(model.node, GraphItem):
                group = model.node.attributes.get("Group", "")
            elif isinstance(model.node, dict):
                group = model.node.get("Group", "")
            else:
                group = ""

            types = js_manager.types(group)
            editor.addItems(types)
            return editor

        # Remaining conditions for other fields
        if isinstance(data, datetime.date):
            editor = QDateEdit(parent)
            editor.setDisplayFormat("MM.dd.yyyy")
            editor.setMinimumDate(QDate(1, 1, 1))
        elif isinstance(data, dict) and 'image' in data.keys():
            editor = ImagePropertyWidget(parent)
        elif isinstance(data, bool):
            editor = QCheckBox(parent)
        elif isinstance(data, str):
            editor = QLineEdit(parent)
        else:
            return None

        return editor

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        if isinstance(editor, QLineEdit) and editor.hasAcceptableInput():
            model.setData(index, editor.text(), Qt.EditRole)
        elif isinstance(editor, QDateEdit):
            date: QDate = editor.date()
            model.setData(index, datetime.date(date.year(), date.month(), date.day()).strftime('%m/%d/%Y'), Qt.EditRole)
        elif isinstance(editor, QComboBox):
            selected_value = editor.currentText()
            model.setData(index, selected_value, Qt.EditRole)
            if index.row() == self._group_index(index):  # Update Type options if Group changed
                js_manager.update_node_group(model.node, selected_value)
                model.dataChanged.emit(index, index)
        elif isinstance(editor, QCheckBox):
            model.setData(index, editor.isChecked(), Qt.EditRole)
        elif isinstance(editor, ImagePropertyWidget):
            data = editor.get_data()
            if data['image']:
                model.setData(index, data, Qt.EditRole)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        data = index.data(Qt.UserRole)
        if isinstance(editor, QLineEdit):
            editor.setText(data)
            editor.editingFinished.connect(self.__editing_finished)
        elif isinstance(editor, QDateEdit):
            date: datetime.date = data
            editor.setDate(QDate(date.year, date.month, date.day))
        elif isinstance(editor, QCheckBox):
            editor.setChecked(data)
            editor.clicked.connect(self.__editing_finished)
        elif isinstance(editor, QComboBox):
            editor.setCurrentText(data)
            editor.currentIndexChanged.connect(self.__editing_finished)
        elif isinstance(editor, ImagePropertyWidget):
            editor.set_data(data)
            editor.image_changed.connect(self.__editing_finished)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        if isinstance(editor, QCheckBox):
            option.rect.adjust(3, 0, 0, 0)
        editor.setGeometry(option.rect)

    @pyqtSlot()
    def __editing_finished(self) -> None:
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())

    def _group_index(self, index):
        return index.model().node_valid_keys.index("Group") if "Group" in index.model().node_valid_keys else -1

    def _type_index(self, index):
        return index.model().node_valid_keys.index("Type") if "Type" in index.model().node_valid_keys else -1

    def _label_index(self, index):
        return index.model().node_valid_keys.index("Label") if "Label" in index.model().node_valid_keys else -1
