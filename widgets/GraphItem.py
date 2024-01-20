from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem


class GraphItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)

    def _get_attributes(self):
        return self.attributes

    def _set_attributes(self, _attributes):
        self.attributes = _attributes

    def _get_pixmap(self):
        return self.pixmap

    def _set_pixmap(self, _pixmap):
        self.pixmap = _pixmap
