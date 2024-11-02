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
        model = index.model()

        # Determine the key based on row to identify the editor type
        if index.row() < len(model.node_valid_keys):
            key = model.node_valid_keys[index.row()]
        else:
            # Extract key from 'Attributes' based on the adjusted row index
            attr_index = index.row() - len(model.node_valid_keys)
            attributes = model.node.attributes.get("Attributes", [])
            key = attributes[attr_index].get("name", "") if attr_index < len(attributes) else ""

        print(f"[DEBUG] Key determined as '{key}' at row {index.row()}")

        # Handle QDateEdit for Date fields
        if key == "Date of Birth":
            editor = QDateEdit(parent)
            editor.setDisplayFormat("dd/MM/yyyy")
            editor.setMinimumDate(QDate(1, 1, 1))
            return editor

        # Handle QComboBox for Group and Type
        if key == "Group":
            editor = QComboBox(parent)
            editor.addItems(js_manager.groups())
            return editor
        elif key == "Type":
            editor = QComboBox(parent)
            group = model.node.attributes.get("Group", "") if isinstance(model.node, GraphItem) else model.node.get("Group", "")
            editor.addItems(js_manager.types(group))
            return editor

        # QLineEdit for string attributes
        attribute = next((attr for attr in model.node.attributes.get("Attributes", []) if attr.get("name") == key), None)
        if attribute and attribute.get("type") == "string":
            editor = QLineEdit(parent)
            print(f"[DEBUG] QLineEdit created for '{key}' at row {index.row()}")
            return editor

        # Default editor handling
        data = index.data(Qt.UserRole)
        if isinstance(data, dict) and 'image' in data.keys():
            editor = ImagePropertyWidget(parent)
        elif isinstance(data, bool):
            editor = QCheckBox(parent)
        elif isinstance(data, str):
            editor = QLineEdit(parent)
        else:
            print(f"[DEBUG] No editor created for key: {key}, row: {index.row()}, data type: {type(data)}")
            return None

        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        data = index.data(Qt.UserRole)
        if isinstance(editor, QLineEdit):
            editor.setText(data)
            editor.editingFinished.connect(self.__editing_finished)
        elif isinstance(editor, QDateEdit) and isinstance(data, datetime.date):
            editor.setDate(QDate(data.year, data.month, data.day))
        elif isinstance(editor, QCheckBox):
            editor.setChecked(data)
            editor.clicked.connect(self.__editing_finished)
        elif isinstance(editor, QComboBox):
            editor.setCurrentText(data)
            editor.currentIndexChanged.connect(self.__editing_finished)
        elif isinstance(editor, ImagePropertyWidget):
            editor.set_data(data)
            editor.image_changed.connect(self.__editing_finished)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        key = model.node_valid_keys[index.row()] if index.row() < len(model.node_valid_keys) else ""

        # Handle QDateEdit
        if isinstance(editor, QDateEdit):
            date = editor.date()
            date_str = date.toString("dd/MM/yyyy")
            model.setData(index, date_str, Qt.EditRole)

        # Handle QLineEdit
        elif isinstance(editor, QLineEdit):
            print(f"[DEBUG] Setting QLineEdit data for '{key}': {editor.text()}")
            model.setData(index, editor.text(), Qt.EditRole)

        # Handle QComboBox
        elif isinstance(editor, QComboBox):
            selected_value = editor.currentText()
            model.setData(index, selected_value, Qt.EditRole)

        # Handle QCheckBox
        elif isinstance(editor, QCheckBox):
            model.setData(index, editor.isChecked(), Qt.EditRole)

        # Handle ImagePropertyWidget
        elif isinstance(editor, ImagePropertyWidget):
            data = editor.get_data()
            if data['image']:
                model.setData(index, data, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    @pyqtSlot()
    def __editing_finished(self) -> None:
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())
