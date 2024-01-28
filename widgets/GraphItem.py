import uuid

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QApplication

import constants
from widgets.GraphEdgePoint import GraphEdgePoint


class GraphItem(QGraphicsPixmapItem):
    pen = QtGui.QPen(Qt.red, 2)
    brush = QtGui.QBrush(QtGui.QColor(31, 176, 224))
    controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))

    def __init__(self, parent, left=False, right=False):
        super().__init__(parent)

        self.identifier = uuid.uuid4()

        self.node_size = 30

        self.node_shape = constants.NodeShapes.Circle

        self.show_icon = True
        self.use_image = False

        self._is_hovered = False

        self.node_foreground_color = QColor(255, 0, 0)
        self.node_background_color = QColor(255, 255, 0)
        self.node_highlight_color = QColor(0, 0, 255)
        self.node_label_text_color = QColor(0, 255, 0)

        self.startPosition = None

        self.controls = []

        for onLeft, create in enumerate((right, left)):
            if create:
                control = GraphEdgePoint(self, onLeft)
                self.controls.append(control)
                control.setPen(self.pen)
                control.setBrush(self.controlBrush)
                if onLeft:
                    control.setX(50)
                control.setY(20)

    ## Adding hover
    ## Reference - https://stackoverflow.com/questions/56266185/painting-qgraphicspixmapitem-border-on-hover
    def hoverEnterEvent(self, event):
        self._is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        if self._is_hovered:
            painter.save()

            # Looks better with this
            painter.setRenderHint(QPainter.Antialiasing, True)

            # Outline
            pen = QtGui.QPen(QtGui.QColor("blue"))
            pen.setWidth(3)
            painter.setPen(pen)

            new_rect = QRect(0, 0, self.node_size, self.node_size)

            ## Shape
            # Square
            #painter.drawRect(self.boundingRect())
            # Circle
            painter.drawEllipse(new_rect)

            painter.restore()
        elif not self.show_icon:
            painter.save()

            # Looks better with this
            painter.setRenderHint(QPainter.Antialiasing, True)

            ## Colors
            # Fill
            brush = QtGui.QBrush(self.node_foreground_color)
            painter.setBrush(brush)
            # Outline
            pen = QtGui.QPen(QtGui.QColor("black"))
            pen.setWidth(2)
            painter.setPen(pen)

            new_rect = QRect(0, 0, self.node_size, self.node_size)

            ## Shape
            if self.node_shape == constants.NodeShapes.Circle:
                painter.drawEllipse(new_rect)
            elif self.node_shape == constants.NodeShapes.Square:
                painter.drawRect(new_rect)
            else:
                painter.drawEllipse(self.boundingRect())
        else:
            super().paint(painter, option, widget)

    def _get_identifier(self):
        return self.identifier

    def _set_identifier(self, _identifier):
        self.identifier = _identifier

    def _get_shape(self):
        return self.node_shape

    def _set_shape(self, _shape):
        self.node_shape = _shape

    def _get_use_image(self):
        return self.use_image

    def _set_use_image(self, _use_image):
        self.use_image = _use_image

    def _get_show_icon(self):
        return self.show_icon

    def _set_show_icon(self, _show_icon):
        self.show_icon = _show_icon

    def _get_label(self):
        return self.label

    def _set_label(self, _label):
        self.label = _label

    def _get_attributes(self):
        return self.attributes

    def _set_attributes(self, _attributes):
        self.attributes = _attributes

    def _get_pixmap(self):
        return self.pixmap

    def _set_pixmap(self, _pixmap):
        self.pixmap = _pixmap

    # Reference - https://stackoverflow.com/questions/72535825/pyqt5-qgraphicsscene-mouse-item-with-click-and-drop-without-holding-press
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