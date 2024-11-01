from PyQt5.QtCore import QLineF, QPointF, Qt
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QColor, QPainter
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsItem
from math import atan2, cos, sin, radians

class GraphEdge(QGraphicsLineItem):
    def __init__(self, source, target, label=None, weight=None, parent=None, arrow_enabled=False, show_label=False):
        super().__init__(parent)
        self.start = source
        self.end = target if isinstance(target, QGraphicsItem) else None
        self.targetPos = target if isinstance(target, QPointF) else None
        self.arrow_enabled = arrow_enabled
        self.show_label = show_label
        self.node_size = 30
        self.arrow_size = 20
        self.label = label
        self.weight = weight
        self.is_hovered = False
        self.is_selected = False
        self.updatePosition()

        # Enable hover events
        self.setAcceptHoverEvents(True)
        # Allow the item to be selectable
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)

    def setEnd(self, end: 'GraphItem'):
        """Set the target GraphItem at the end of the edge."""
        self.end = end  # Store the reference to the target GraphItem
        self.targetPos = None  # Reset target position (optional)
        self.updatePosition()  # Update the graphical representation

    def setP2(self, point: QPointF):
        """Update the graphical end point of the edge."""
        self._line.setP2(point)
        self.setLine(self._line)

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

    def hoverEnterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_selected = not self.is_selected
            self.update()
        super().mousePressEvent(event)

    def paint(self, painter, option, widget=None):
        painter.save()

        # Choose color based on hover and selection states
        if self.is_selected:
            pen_color = QColor("green")
        elif self.is_hovered:
            pen_color = QColor("blue")
        else:
            pen_color = QColor("black")

        painter.setPen(QPen(pen_color, 2))
        painter.drawLine(self.line())
        painter.restore()

        # Draw the arrow if enabled
        if self.arrow_enabled and self.line().length() > 5:
            self._draw_arrow(painter)

        # Draw the label if show_label is enabled
        if self.show_label and self.label:
            self._draw_label(painter)

    def controlPoints(self):
        """Return the start and end points of the line."""
        start_point = self.getCenterPos(self.start)
        end_point = self.getCenterPos(self.end) if self.end else self.targetPos
        return start_point, end_point

    def updateLine(self):
        """Update the position of the line based on the current positions of start and end nodes."""
        if self.start:
            self._line.setP1(self.getCenterPos(self.start))
        if self.end:
            self._line.setP2(self.getCenterPos(self.end))
        self.setLine(self._line)

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
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(arrow_head)

        painter.restore()

    def _draw_label(self, painter):
        """Draws the label for the edge."""
        painter.save()
        mid_point = self.line().pointAt(0.5)
        painter.setPen(QPen(QColor("blue")))
        painter.drawText(mid_point, self.label)
        painter.restore()
