from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QGraphicsView, QWidget

## Reference - https://stackoverflow.com/questions/10770255/resize-qgraphicsview-doesnt-move-the-widgets
class GraphView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self._center = None

    def resizeEvent(self, event):
        super(GraphView, self).resizeEvent(event)
        if self._center:
            self.centerOn(self._center)

    def updateCenter(self):
        center = self.geometry().center()
        self._center = self.mapToScene(center)