from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtWidgets import QGraphicsItem


from PyQt5 import QtWidgets, QtCore

class GraphEdge(QtWidgets.QGraphicsLineItem):
    def __init__(self, source, target, parent=None):
        super().__init__(parent)

        self.start = source
        self.end = target if isinstance(target, QtWidgets.QGraphicsItem) else None  # Store target if it's an item
        self.targetPos = target if isinstance(target, QPointF) else None  # Store position if it's a QPointF

        self.updatePosition()  # Update position of the line when created

    def updatePosition(self):
        """Update the line position between source and target or QPointF."""
        sourceCenter = self.getCenterPos(self.start)  # Get center of the start GraphItem
        if self.end:
            targetCenter = self.getCenterPos(self.end)  # Get center of the target GraphItem if available
        else:
            targetCenter = self.targetPos  # Use QPointF if target is not set yet

        if targetCenter:
            self._line = QLineF(sourceCenter, targetCenter)
            self.setLine(self._line)  # Set the updated line

    def getCenterPos(self, item):
        """Helper method to get the center position of a GraphItem or return the QPointF if provided."""
        if isinstance(item, QtWidgets.QGraphicsItem):
            rect = item.boundingRect()  # Get bounding rectangle of the item
            center_x = item.pos().x() + rect.width() / 2  # X-coordinate of the center
            center_y = item.pos().y() + rect.height() / 2  # Y-coordinate of the center
            return QPointF(center_x, center_y)
        elif isinstance(item, QPointF):
            return item  # If it's already a QPointF, return it
        return None

    def setEnd(self, end):
        """Set the target GraphItem and update the line."""
        self.end = end
        self.targetPos = None  # Reset target position once the end GraphItem is set
        self.updatePosition()  # Update the line position accordingly


    def setStart(self, start):
        self.start = start
        self.updateLine()

    def setP2(self, point):
        self._line.setP2(point)
        self.setLine(self._line)

    def controlPoints(self):
        return self.start, self.end

    def updateLine(self):
        if self.start:
            self._line.setP1(self.getCenterPos(self.start))
        if self.end:
            self._line.setP2(self.getCenterPos(self.end))
        self.setLine(self._line)

    def _get_source(self):
        return self.source

    def _set_source(self, _source):
        self.source = _source

    def _get_target(self):
        return self.target

    def _set_target(self, _target):
        self.target = _target

    def setP2(self, point):
        self._line.setP2(point)
        self.setLine(self._line)
