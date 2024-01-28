from PyQt5 import QtWidgets, QtCore


class GraphEdge(QtWidgets.QGraphicsLineItem):
    def __init__(self, source, target):
        super().__init__()
        self.start = source
        self.end = None
        self._line = QtCore.QLineF(source.scenePos(), target)
        self.setLine(self._line)

    def _get_source(self):
        return self.source

    def _set_source(self, _source):
        self.source = _source

    def _get_target(self):
        return self.target

    def _set_target(self, _target):
        self.target = _target

    def controlPoints(self):
        return self.start, self.end

    def setP2(self, p2):
        self._line.setP2(p2)
        self.setLine(self._line)

    def setStart(self, start):
        self.start = start
        self.updateLine()

    def setEnd(self, end):
        self.end = end
        self.updateLine(end)

    def updateLine(self, source):
        if source == self.start:
            self._line.setP1(source.scenePos())
        else:
            self._line.setP2(source.scenePos())
        self.setLine(self._line)