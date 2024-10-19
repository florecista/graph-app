from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtWidgets import QGraphicsItem


from PyQt5 import QtWidgets, QtCore

class GraphEdge(QtWidgets.QGraphicsLineItem):
    def __init__(self, source, target, parent=None):
        super().__init__(parent)

        self.start = source
        self.end = target

        # Get the center positions of source and target GraphItems
        sourceCenter = self.getCenterPos(self.start)
        targetCenter = self.getCenterPos(self.end)

        # Create a line between the two center positions
        self._line = QLineF(sourceCenter, targetCenter)
        self.setLine(self._line)

    def setStart(self, start):
        self.start = start
        self.updateLine()

    def setEnd(self, end):
        self.end = end
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

    def getCenterPos(self, item):
        """Helper method to get the center position of a GraphItem."""
        rect = item.boundingRect()  # Get the bounding rectangle of the item
        center_x = item.pos().x() + rect.width() / 2  # X-coordinate of the center
        center_y = item.pos().y() + rect.height() / 2  # Y-coordinate of the center
        return QPointF(center_x, center_y)

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
