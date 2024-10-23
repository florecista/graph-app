from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QRubberBand

from constants import NodeShapes, GraphLayout
from graph.HierarchicalTreeLayout import HierarchicalTreeLayout
from graph.LayoutFactory import LayoutFactory
from utils import file_utils
from widgets.GraphEdge import GraphEdge
from widgets.GraphItem import GraphItem


## Reference - https://stackoverflow.com/questions/10770255/resize-qgraphicsview-doesnt-move-the-widgets
##
## Reference - https://stackoverflow.com/questions/47102224/pyqt-draw-selection-rectangle-over-picture
##
class GraphView(QGraphicsView):
    rect_changed = pyqtSignal(QRect)
    nodes_selection_changed = pyqtSignal(dict)

    node_foreground_color = QColor(255, 0, 0)
    node_background_color = QColor(0, 0, 0)
    node_highlight_color = QColor(0, 0, 255)
    node_label_text_color = QColor(0, 255, 0)

    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self._center = None

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

    def mousePressEvent(self, event):
        self.origin = event.pos()

        is_touching_icon = False

        graphEdgePointOffset = 50

        for child in self.items():
            if (isinstance(child, GraphItem)):
                childRect = QRect(int(child.x()), int(child.y()), int(child.boundingRect().width())+graphEdgePointOffset,
                                  int(child.boundingRect().height()))
                positionOffset = QPoint(self.origin.x()-32, self.origin.y())
                if childRect.contains(positionOffset):
                    is_touching_icon = True
                # for line in child.lines:
                #     line.updateLine(child)
            self.nodes_selection_changed.emit({})

        if not is_touching_icon:
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rect_changed.emit(self.rubberBand.geometry())
            self.rubberBand.show()
            self.changeRubberBand = True

        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rect_changed.emit(self.rubberBand.geometry())
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.changeRubberBand = False
            if self.rubberBand.isVisible():
                self.rubberBand.hide()
                selected = []
                rect = self.rubberBand.geometry()
                for child in self.items():
                    if (isinstance(child, GraphItem)):
                        childRect = QRect(int(child.x()), int(child.y()), int(child.boundingRect().width()), int(child.boundingRect().height()))
                        if rect.intersects(childRect):
                            child.setSelected(True)
                            selected.append(child)

                print(str(len(selected)), 'nodes selected')
        self.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self,event)

    def apply_settings(self, parent_window):

        nodes = []
        node_index = 1
        node_str = "node_"
        edges = []
        edge_index = 1
        edge_str = "edge_"
        for child in self.items():
            if (isinstance(child, GraphItem)):
                key = node_str + str(node_index)
                nodes.append(child)
                node_index = node_index + 1
            elif (isinstance(child, GraphEdge)):
                key = edge_str + str(edge_index)
                edges.append(child)
                edge_index = edge_index + 1

        # Get the selected layout object directly from the ComboBox
        layout_object = parent_window.ui.cboGraphConfiguration.currentData()

        if layout_object and len(nodes) > 0:
            layout_factory = LayoutFactory()
            layout = layout_factory.create_layout(layout_object, nodes, edges, self.height(), self.width())

            # Check for HierarchicalTreeLayout and pass the root_node
            if isinstance(layout, HierarchicalTreeLayout):
                root_node = self.find_root_node(nodes)
                layout.layout(root_node)
            else:
                layout.layout()

            # for node in nodes:
            #     print("After:", node.pos())

        count = 0
        for child in self.items():
            if (isinstance(child, GraphItem)):

                child.show_icon = parent_window.ui.chkStyleNodeShowIcon.isChecked()
                child.use_image = parent_window.ui.chkStyleNodeUseImage.isChecked()

                child.node_foreground_color = self.node_foreground_color
                child.node_background_color = self.node_background_color

                node_size = parent_window.ui.cboNodeSize.currentData()
                child.node_size = node_size

                node_shape = NodeShapes(parent_window.ui.cboStyleNodeShape.currentData())
                child.node_shape = node_shape

                # print(child.identifier)
                if child.isSelected():
                    print(child.identifier, 'selected')
                count = count + 1
            if (isinstance(child, GraphEdge)):
                child.arrow_enabled = parent_window.ui.chkStyleEdgeDirectionArrow.isChecked()
                child.show_label = parent_window.ui.chkStyleEdgeShowLabel.isChecked()

        ## Reference - https://stackoverflow.com/questions/12439082/qgraphicssceneclear-clearing-scene-but-not-the-view
        self.viewport().update()

    def resizeEvent(self, event):
        super(GraphView, self).resizeEvent(event)
        if self._center:
            self.centerOn(self._center)

    def updateCenter(self):
        center = self.geometry().center()
        self._center = self.mapToScene(center)

    def find_root_node(self, nodes):
        for node in nodes:
            if not node.has_parent():  # Assuming a method to check for the parent
                return node
        return None  # Or raise an exception if there's no root

    def open_graphml(self, scene, filename):
        # Ensure the scene is correctly passed
        if scene is None:
            print("Error: Scene is not initialized!")
        else:
            print(f"Scene: {scene}")

        # Proceed to load the GraphML data and check if nodes have positions
        has_positions = file_utils.load_graphml_to_scene(scene, filename)
        return has_positions


