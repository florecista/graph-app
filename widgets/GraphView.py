from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt
from PyQt5.QtWidgets import QGraphicsView, QRubberBand

from widgets.GraphItem import GraphItem


## Reference - https://stackoverflow.com/questions/10770255/resize-qgraphicsview-doesnt-move-the-widgets
##
## Reference - https://stackoverflow.com/questions/47102224/pyqt-draw-selection-rectangle-over-picture
##
class GraphView(QGraphicsView):
    rectChanged = pyqtSignal(QRect)
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self._center = None

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

    def mousePressEvent(self, event):
        self.origin = event.pos()

        is_touching_icon = False

        graphEdgePointOffset = 50

        for child in self.items():

            if (isinstance(child, GraphItem)):
                childRect = QRect(int(child.x()), int(child.y()), int(child.boundingRect().width())+graphEdgePointOffset,
                                  int(child.boundingRect().height()))
                positionOffset = QPoint(self.origin.x()-32, self.origin.y())
                if childRect.contains(positionOffset):
                    is_touching_icon = True

        if not is_touching_icon:
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rectChanged.emit(self.rubberBand.geometry())
            self.rubberBand.show()
            self.changeRubberBand = True

        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.changeRubberBand = False
            if self.rubberBand.isVisible():
                self.rubberBand.hide()
                selected = []
                rect = self.rubberBand.geometry()
                for child in self.items():
                    if (isinstance(child, GraphItem)):
                        childRect = QRect(int(child.x()), int(child.y()), int(child.boundingRect().width()), int(child.boundingRect().height()))
                        if rect.intersects(childRect):
                            child.setSelected(True)
                            selected.append(child)

                print(str(len(selected)), 'nodes selected')
        self.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self,event)

    def apply_settings(self):
        print('apply_settings')

        count = 0
        for child in self.items():
            if (isinstance(child, GraphItem)):
                child.show_icon = False
                print(child.label)
                if child.isSelected():
                    print(child.label, 'selected')
                count = count + 1

        ## Reference - https://stackoverflow.com/questions/12439082/qgraphicssceneclear-clearing-scene-but-not-the-view
        self.viewport().update()

        print('changed ', str(count))

    def resizeEvent(self, event):
        super(GraphView, self).resizeEvent(event)
        if self._center:
            self.centerOn(self._center)

    def updateCenter(self):
        center = self.geometry().center()
        self._center = self.mapToScene(center)