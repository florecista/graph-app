from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGraphicsItem


from PyQt5 import QtWidgets, QtCore

class GraphEdge(QtWidgets.QGraphicsLineItem):
    def __init__(self, source, target):
        super().__init__()
        self.start = source  # Using 'start' instead of 'source'
        self.end = None  # Using 'end' instead of 'target'
        sourceCenter = self.getCenterPos(self.start)
        self._line = QtCore.QLineF(sourceCenter, target)
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
        rect = item.boundingRect()
        return item.scenePos() + QtCore.QPointF(rect.width() / 2, rect.height() / 2)

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
