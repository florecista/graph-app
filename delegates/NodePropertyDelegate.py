
import datetime

from PyQt5.QtCore import QModelIndex, Qt, QDate, QAbstractItemModel, pyqtSlot
from PyQt5.QtWidgets import QItemDelegate, QWidget, QComboBox, QDateEdit, QCheckBox, QLineEdit
from widgets.ImagePropertyWidget import ImagePropertyWidget


class NodePropertyDelegate(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        data = index.data(Qt.UserRole)
        if isinstance(data, tuple):
            editor = QComboBox(parent)
        elif isinstance(data, datetime.date):
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
        if isinstance(editor, QLineEdit):
            if editor.hasAcceptableInput():
                model.setData(index, editor.text(), Qt.EditRole)
        elif isinstance(editor, QDateEdit):
            date: QDate = editor.date()
            model.setData(index, datetime.date(date.year(), date.month(), date.day()).strftime('%m/%d/%Y'), Qt.EditRole)
        elif isinstance(editor, QComboBox):
            model.setData(index, editor.currentText(), Qt.EditRole)
        elif isinstance(editor, QCheckBox):
            model.setData(index, editor.isChecked(), Qt.EditRole)
        elif isinstance(editor, ImagePropertyWidget):
            data = editor.get_data()
            if data['image']:
                model.setData(index, data, Qt.EditRole)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        if isinstance(editor, QLineEdit):
            editor.setText(index.data(Qt.UserRole))
            editor.editingFinished.connect(self.__editing_finished)
        elif isinstance(editor, QDateEdit):
            date: datetime.date = index.data(Qt.UserRole)
            editor.setDate(QDate(date.year, date.month, date.day))
        elif isinstance(editor, QCheckBox):
            editor.setChecked(index.data(Qt.UserRole))
            editor.clicked.connect(self.__editing_finished)
        elif isinstance(editor, QComboBox):
            data: tuple = index.data(Qt.UserRole)
            index = 0
            has_icon = len(data) == 3
            for value in data[1]:
                if has_icon:
                    editor.addItem(data[2][index], value)
                else:
                    editor.addItem(value)
                index += 1
            editor.setCurrentIndex(editor.findText(data[0]))
            editor.currentIndexChanged.connect(self.__editing_finished)
        elif isinstance(editor, ImagePropertyWidget):
            editor.set_data(index.data(Qt.UserRole))
            editor.image_changed.connect(self.__editing_finished)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        if isinstance(editor, QCheckBox):
            option.rect.adjust(3,0,0,0)
        editor.setGeometry(option.rect)

    @pyqtSlot()
    def __editing_finished(self) -> None:
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())
