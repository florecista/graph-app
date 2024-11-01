from PyQt5.QtCore import QModelIndex, Qt, QRegExp, QAbstractItemModel, pyqtSlot
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QItemDelegate, QWidget, QLineEdit

class EdgePropertyDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        editor = None
        data = index.data(Qt.UserRole)
        if isinstance(data, str):
            editor = QLineEdit(parent)
        elif isinstance(data, float):
            editor = QLineEdit(parent)
            validator = QRegExpValidator(QRegExp("[+-]?\\d*[\\.,]?\\d+"), parent)
            editor.setValidator(validator)
        return editor

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        if isinstance(editor, QLineEdit) and editor.hasAcceptableInput():
            model.setData(index, editor.text(), Qt.EditRole)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        if isinstance(editor, QLineEdit):
            editor.setText(str(index.data(Qt.UserRole)))
            editor.editingFinished.connect(self.__editing_finished)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    @pyqtSlot()
    def __editing_finished(self) -> None:
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())
