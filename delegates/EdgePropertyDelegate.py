from PySide2.QtWidgets import QItemDelegate, QLineEdit, QWidget, QStyleOptionViewItem
from PySide2.QtCore import Qt, QModelIndex, QAbstractItemModel, Slot, QRegExp
from PySide2.QtGui import QRegExpValidator


# from PySide2.QtGui import QDoubleValidator


class EdgePropertyDelegate(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        editor = None
        data = index.data(Qt.UserRole)
        if isinstance(data, str):
            editor = QLineEdit(parent)
        elif isinstance(data, float):
            editor = QLineEdit(parent)

            validator = QRegExpValidator(QRegExp("[+-]?\\d*[\\.,]?\\d+"), parent)
            # validator = QDoubleValidator(parent)
            # validator.setNotation(QDoubleValidator.StandardNotation)
            # validator.setBottom(0)
            # validator.setDecimals(6)

            editor.setValidator(validator)
        return editor

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        if isinstance(editor, QLineEdit):
            if editor.hasAcceptableInput():
                model.setData(index, editor.text(), Qt.EditRole)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        if isinstance(editor, QLineEdit):
            editor.setText(str(index.data(Qt.UserRole)))
            editor.editingFinished.connect(self.__editing_finished)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    @Slot()
    def __editing_finished(self) -> None:
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())
