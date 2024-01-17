import io

from PIL import Image
from PyQt5.QtCore import Qt, QBuffer, QByteArray
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsPixmapItem, \
    QGraphicsItem


class PlotWidget(QGraphicsScene):

    def __init__(self, parent):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        print('dragEnterEvent2')

    def add_node(self, in_point, type, attributes):
        attributes["Label"] = "Node Name"
        attributes["Position"] = self.__pos_to_str([in_point.x(), in_point.y()])
        attributes["Image"] = {"name": "", "image": ""}
        attributes["Image Scale"] = True

        print('adding ' + attributes['Type'] + ' to ' + str(in_point.x()) + ", " + str(in_point.y()))
        print(attributes["Position"])

        # actually add to scene
        x = in_point.x()
        y = in_point.y()
        rectItem = QGraphicsRectItem(x, y, 20, 20)
        #rectItem.setPos(in_point)
        self.addItem(rectItem)

    @staticmethod
    def __pos_to_str(position):
        return ";".join(map(str, position))

    @staticmethod
    def __str_to_pos(text):
        return list(map(float, text.split(";")))

    @staticmethod
    def __str_to_image(val: str) -> Image:
        img = QImage.fromData(PlotWidget.__str_to_q_byte_array(val))
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        img.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        buffer.close()
        # pil_im.thumbnail(size, Image.ANTIALIAS) # keeping aspect ratio
        # pil_im = pil_im.resize((20, 20), Image.Resampling.LANCZOS)
        return pil_im

    @staticmethod
    def __str_to_q_byte_array(val: str) -> QByteArray:
        q_byte_array = QByteArray(val.encode())
        q_byte_array = QByteArray.fromBase64(q_byte_array)
        return q_byte_array

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        pos = event.pos()
        mimeData = event.mimeData()
        pixMap = QPixmap(mimeData)
        print('dropEvent2')
        # rectItem = QGraphicsRectItem(0, 0, 20, 20)
        # rectItem.setPos(event.pos())
        # self.addItem(rectItem)

        #item = QGraphicsItem()
        newPix = QGraphicsPixmapItem(pixMap)
        # newPix.setPos(event.pos().x(), event.pos().y())

        event.setDropAction(Qt.DropActions.MoveAction)
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage():
            event.accept()
        else:
            event.ignore()