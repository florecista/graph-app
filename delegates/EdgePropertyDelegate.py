from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QItemDelegate, QLineEdit

class EdgePropertyDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        return QLineEdit(parent)  # Create a QLineEdit for label editing

    def setEditorData(self, editor, index):
        editor.setText(index.model().data(index, Qt.EditRole))  # Set initial text

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)  # Update model with new text
