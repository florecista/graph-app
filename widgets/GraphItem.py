import uuid
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QGraphicsPixmapItem, QApplication
from PySide6.QtCore import QPointF

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

        self.parent = None  # Parent reference
        self.children = []  # List to hold child nodes

        for onLeft, create in enumerate((right, left)):
            if create:
                control = GraphEdgePoint(self, onLeft)
                self.controls.append(control)
                control.setPen(QtGui.QPen(Qt.black, 2))
                control.setBrush(QtGui.QBrush(Qt.black))
                if onLeft:
                    control.setX(50)
                control.setY(20)

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
            painter.setRenderHint(QPainter.Antialiasing, True)
            pen = QtGui.QPen(QtGui.QColor("blue"))
            pen.setWidth(3)
            painter.setPen(pen)
            new_rect = QRect(0, 0, self.node_size, self.node_size)
            painter.drawEllipse(new_rect)
            painter.restore()
        elif not self.show_icon:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            brush = QtGui.QBrush(self.node_foreground_color)
            painter.setBrush(brush)
            pen = QtGui.QPen(self.node_background_color)
            pen.setWidth(2)
            painter.setPen(pen)
            new_rect = QRect(0, 0, self.node_size, self.node_size)
            if self.node_shape == constants.NodeShapes.Circle:
                painter.drawEllipse(new_rect)
            elif self.node_shape == constants.NodeShapes.Square:
                painter.drawRect(new_rect)
            else:
                painter.drawEllipse(self.boundingRect())
        else:
            super().paint(painter, option, widget)

    # Identifier methods
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

    # Parent-child relationship methods
    def has_parent(self):
        """Check if the node has a parent."""
        return self.parent is not None

    def add_child(self, child):
        """Add a child node and set the parent reference."""
        child.parent = self  # Set the parent of the child
        self.children.append(child)

    def get_children(self):
        """Return the list of child nodes."""
        return self.children

    # Reference - https://stackoverflow.com/questions/72535825/pyqt5-qgraphicsscene-mouse-item-with-click-and-drop-without-holding-press
    moving = False

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.type() == Qt.MouseButton.LeftButton:
            event.accept()
            self.startPosition = event.screenPos()
            self.setPos(self.startPosition)

    def mouseMoveEvent(self, event):
        if self.moving:
            currentParentPos = self.mapToParent(self.mapFromScene(event.scenePos()))
            originParentPos = self.mapToParent(self.mapFromScene(event.buttonDownScenePos(Qt.LeftButton)))
            self.setPos(self.startPosition + currentParentPos - originParentPos)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.type() == Qt.MouseButton.LeftButton or event.pos() not in self.boundingRect():
            return

        distance = (event.screenPos() - self.pos()).manhattanLength()
        startDragDistance = QApplication.startDragDistance()
        if not self.moving and distance > startDragDistance:
            return

        self.moving = not self.moving
        self.setAcceptHoverEvents(self.moving)
        if self.moving:
            self.startPosition = self.pos()
            self.grabMouse()
        else:
            self.ungrabMouse()
