from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QApplication


class GraphItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)
        self.startPosition = None

    def _get_attributes(self):
        return self.attributes

    def _set_attributes(self, _attributes):
        self.attributes = _attributes

    def _get_pixmap(self):
        return self.pixmap

    def _set_pixmap(self, _pixmap):
        self.pixmap = _pixmap

    moving = False
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.type() == Qt.MouseButton.LeftButton:
            # by defaults, mouse press events are not accepted/handled,
            # meaning that no further mouseMoveEvent or mouseReleaseEvent
            # will *ever* be received by this item; with the following,
            # those events will be properly dispatched
            event.accept()
            self.startPosition = event.screenPos()
            self.setPos(self.startPosition)

    def mouseMoveEvent(self, event):
        if self.moving:
            # map the position to the parent in order to ensure that the
            # transformations are properly considered:
            currentParentPos = self.mapToParent(
                self.mapFromScene(event.scenePos()))
            originParentPos = self.mapToParent(
                self.mapFromScene(event.buttonDownScenePos(Qt.LeftButton)))
            self.setPos(self.startPosition + currentParentPos - originParentPos)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print('GraphItem.mouseReleaseEvent')
        if event.type() == Qt.MouseButton.LeftButton or event.pos() not in self.boundingRect():
            return

        # the following code block is to allow compatibility with the
        # ItemIsMovable flag: if the item has the flag set and was moved while
        # keeping the left mouse button pressed, we proceed with our
        # no-mouse-button-moved approach only *if* the difference between the
        # pressed and released mouse positions is smaller than the application
        # default value for drag movements; in this way, small, involuntary
        # movements usually created between pressing and releasing the mouse
        # button will still be considered as candidates for our implementation;
        # if you are *not* interested in this flag, just ignore this code block
        distance = (event.screenPos() - self.pos()).manhattanLength()
        startDragDistance = QApplication.startDragDistance()
        if not self.moving and distance > startDragDistance:
            return
        # end of ItemIsMovable support

        self.moving = not self.moving
        # the following is *mandatory*
        self.setAcceptHoverEvents(self.moving)
        if self.moving:
            self.startPosition = self.pos()
            self.grabMouse()
        else:
            self.ungrabMouse()