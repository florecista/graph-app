from PyQt5.QtCore import QLineF, QPointF, Qt
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QColor, QPainter, QFont
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem
from math import atan2, cos, sin, radians

class GraphEdge(QGraphicsLineItem):
    def __init__(self, source, target, label=None, weight=None, parent=None, arrow_enabled=False, show_label=False):
        super().__init__(parent)
        self.start = source
        self.end = target if isinstance(target, QGraphicsItem) else None
        self.targetPos = target if isinstance(target, QPointF) else None
        self.arrow_enabled = arrow_enabled  # To control arrow visibility
        self.show_label = show_label  # To control label visibility
        self.node_size = 30  # Assuming the node size is 30x30
        self.arrow_size = 20  # Adjust arrow size
        self.label = label  # Store the edge label
        self.weight = weight  # Store the edge weight
        self.updatePosition()

    def controlPoints(self):
        """Return the start and end points of the line."""
        start_point = self.getCenterPos(self.start)
        end_point = self.getCenterPos(self.end) if self.end else self.targetPos
        return start_point, end_point

    def updatePosition(self):
        """Update the line position between source and target or QPointF."""
        sourceCenter = self.getCenterPos(self.start)
        if self.end:
            targetCenter = self.getCenterPos(self.end)
        else:
            targetCenter = self.targetPos

        if targetCenter:
            source_edge_pos = self.adjust_position(sourceCenter, targetCenter, self.node_size / 2)
            target_edge_pos = self.adjust_position(targetCenter, sourceCenter, self.node_size / 2)
            self._line = QLineF(source_edge_pos, target_edge_pos)
            self.setLine(self._line)

    def adjust_position(self, center, target, radius):
        """Adjust the line to stop at the edge of the node instead of its center."""
        angle = atan2(target.y() - center.y(), target.x() - center.x())
        new_x = center.x() + radius * cos(angle)
        new_y = center.y() + radius * sin(angle)
        return QPointF(new_x, new_y)

    def getCenterPos(self, item):
        """Get the center of the GraphItem or QPointF."""
        if isinstance(item, QGraphicsItem):
            rect = item.boundingRect()
            center_x = item.pos().x() + rect.width() / 2
            center_y = item.pos().y() + rect.height() / 2
            return QPointF(center_x, center_y)
        elif isinstance(item, QPointF):
            return item
        return None

    def setEnd(self, end):
        self.end = end
        self.targetPos = None
        self.updatePosition()

    def paint(self, painter, option, widget=None):
        """Custom paint function to handle drawing the line, optional arrow, and label."""
        super().paint(painter, option, widget)

        # Draw the base line
        painter.save()
        painter.setPen(QPen(QColor("black"), 2))  # Set line thickness and color
        painter.drawLine(self.line())  # Draw the line
        painter.restore()

        # Draw the arrow if enabled
        if self.arrow_enabled and self.line().length() > 5:
            self._draw_arrow(painter)

        # Draw the label if show_label is enabled
        if self.show_label and self.label:
            self._draw_label(painter)

    def _draw_arrow(self, painter):
        """Draws an arrow at the end of the edge."""
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        line = self.line()
        angle = atan2(line.dy(), line.dx())
        arrow_size = self.arrow_size

        arrow_p1 = line.p2()
        arrow_p2 = arrow_p1 + QPointF(arrow_size * cos(angle + radians(150)),
                                      arrow_size * sin(angle + radians(150)))
        arrow_p3 = arrow_p1 + QPointF(arrow_size * cos(angle - radians(150)),
                                      arrow_size * sin(angle - radians(150)))

        arrow_head = QPolygonF([arrow_p1, arrow_p2, arrow_p3])

        painter.setBrush(QBrush(QColor("black")))
        painter.setPen(Qt.NoPen)  # No border for the arrowhead
        painter.drawPolygon(arrow_head)

        painter.restore()

    def _draw_label(self, painter):
        """Draws the label for the edge."""
        painter.save()

        # Position the label at the midpoint of the line
        mid_point = self.line().pointAt(0.5)

        painter.setPen(QPen(QColor("blue")))  # Label text color
        painter.drawText(mid_point, self.label)  # Draw the label at the midpoint

        painter.restore()

    def updateLine(self):
        if self.start:
            self._line.setP1(self.getCenterPos(self.start))
        if self.end:
            self._line.setP2(self.getCenterPos(self.end))
        self.setLine(self._line)
