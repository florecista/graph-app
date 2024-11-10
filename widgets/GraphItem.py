import base64
import uuid
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect, QPointF, QByteArray, QRectF, QPoint
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPainterPath
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem

import constants


class GraphItem(QGraphicsPixmapItem):
    pen = QtGui.QPen(Qt.red, 2)
    brush = QtGui.QBrush(QtGui.QColor(31, 176, 224))
    controlBrush = QtGui.QBrush(QtGui.QColor(214, 13, 36))

    def __init__(self, pixmap=None, label="", attributes=None, position=QPointF(), image=None, image_scale=False):
        super().__init__(pixmap)

        self.identifier = uuid.uuid4()
        self.show_label = False
        self.label_position = constants.LabelPosition.Below
        self.label_size = 8
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
        self.lines = []
        self.edges = []  # Initialize the edges list

        self.parent = None  # Parent reference
        self.children = []  # List to hold child nodes

        self.label = label
        self.attributes = attributes or {}
        self.image = image  # Base64 string for the image
        self.image_scale = image_scale  # Boolean to indicate whether scaling is applied
        self.setPos(position)

        self.node_type = None

        # If there's an image provided, handle decoding and scaling here
        # if self.image:
        #     self.set_image(self.image, self.image_scale)

        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)

    # def set_image(self, image_base64, scale):
    #     image_data = QByteArray.fromBase64(image_base64.encode())
    #     pixmap = QPixmap()
    #     pixmap.loadFromData(image_data)
    #     if scale:
    #         pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)
    #     self.setPixmap(pixmap)

    def set_label(self, label):
        """Public method to set the label."""
        self._set_label(label)
        # If necessary, you can trigger any update or repaint here
        self.update()  # For example, to refresh the view after changing the label

    def hoverEnterEvent(self, event):
        self._is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Check if an image is provided and should be used
        if self.use_image and self.image:
            image_pixmap = self.decode_base64_image(self.image)
            if not image_pixmap.isNull():
                if self.node_shape == constants.NodeShapes.Circle:
                    path = QPainterPath()
                    rect = QRectF(0, 0, self.node_size, self.node_size)
                    path.addEllipse(rect)
                    painter.setClipPath(path)

                if self.image_scale:
                    scaled_pixmap = image_pixmap.scaled(self.node_size, self.node_size, Qt.KeepAspectRatio,
                                                        Qt.SmoothTransformation)
                    painter.drawPixmap(0, 0, scaled_pixmap)
                else:
                    image_rect = QRectF(0, 0, image_pixmap.width(), image_pixmap.height())
                    painter.drawPixmap(image_rect, image_pixmap)

        elif self.show_icon:
            super().paint(painter, option, widget)

        else:
            pen = QtGui.QPen(self.node_background_color)
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QtGui.QBrush(self.node_foreground_color))

            shape_rect = QRect(0, 0, self.node_size, self.node_size)

            if self.node_shape == constants.NodeShapes.Circle:
                painter.drawEllipse(shape_rect)
            elif self.node_shape == constants.NodeShapes.Square:
                painter.drawRect(shape_rect)
            else:
                painter.drawEllipse(shape_rect)

        # Draw label if show_label is True and label key is set
        if self.show_label and self.label:
            label_text = ''

            # Access the nested Attributes list within self.attributes
            attributes_list = self.attributes.get('Attributes', [])
            if isinstance(attributes_list, list):
                # Find the attribute in attributes_list matching self.label
                label_text = next((attr['description'] for attr in attributes_list if attr.get('name') == self.label),
                                  '')

            if label_text:  # Only draw if label_text is found
                font = painter.font()
                font.setPointSize(int(self.label_size))
                painter.setFont(font)
                painter.setPen(QtGui.QPen(Qt.black))  # Set text color to black

                # Determine label position
                text_rect = painter.boundingRect(QRect(0, 0, self.node_size, self.node_size), Qt.AlignCenter,
                                                 label_text)
                if self.label_position == constants.LabelPosition.Below:
                    text_rect.moveTop(self.node_size + 5)  # Position below node
                elif self.label_position == constants.LabelPosition.Above:
                    text_rect.moveBottom(-5)  # Position above node
                else:  # Center position
                    text_rect.moveCenter(QPoint(self.node_size / 2, self.node_size / 2))

                painter.drawText(text_rect, Qt.AlignCenter, label_text)

        painter.restore()

    def decode_base64_image(self, base64_string):
        # Decode the base64 string into image bytes
        image_data = base64.b64decode(base64_string)
        pixmap = QPixmap()
        # Load the image data into a QPixmap
        pixmap.loadFromData(image_data)
        return pixmap

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

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for line in self.lines:  # Assuming the node has a list of connected lines
                line.updateLine()  # Just call updateLine without passing the node
        return super().itemChange(change, value)

    def addLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                # another line with the same control points already exists
                return False
        self.lines.append(lineItem)
        return True

    def removeLine(self, lineItem):
        for existing in self.lines:
            if existing.controlPoints() == lineItem.controlPoints():
                self.scene().removeItem(existing)
                self.lines.remove(existing)
                return True
        return False


    # Parent-child relationship methods
    def has_parent(self):
        """Check if the node has a parent."""
        return self.parent is not None

    def add_child(self, child):
        """Add a child node and set the parent reference."""
        child.parent = self  # Set the parent of the child
        self.children.append(child)

        # Debugging prints to verify relationship
        # print(f"Child {child.identifier} added to parent {self.identifier}")
        # print(f"Parent {self.identifier} now has children: {[c.identifier for c in self.children]}")
        # print(f"Child {child.identifier} parent set to {child.parent.identifier}")

    def get_children(self):
        """Return the list of child nodes."""
        return self.children