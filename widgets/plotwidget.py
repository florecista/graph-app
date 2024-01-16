from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView


class PlotWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.initUI()

    def initUI(self):
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.view)
