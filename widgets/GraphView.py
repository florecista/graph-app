# Third-party imports
import networkx as nx
from matplotlib import pyplot as plt

# PyQt5 imports
from PyQt5.QtCore import pyqtSignal, QRect, QPoint, QSize, Qt, QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsView, QRubberBand

# Local imports
import constants
from constants import NodeShapes
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
    edges_selection_changed = pyqtSignal(dict)
    deselected = pyqtSignal()

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
            if isinstance(child, GraphItem):
                childRect = QRect(
                    int(child.x()), int(child.y()),
                    int(child.boundingRect().width()) + graphEdgePointOffset,
                    int(child.boundingRect().height())
                )
                positionOffset = QPoint(self.origin.x() - 32, self.origin.y())
                if childRect.contains(positionOffset):
                    is_touching_icon = True
                    self.nodes_selection_changed.emit({'selected_node': child})  # Emit only if icon is selected
                    break  # No need to check further if node is selected

            elif isinstance(child, GraphEdge):
                edgeRect = QRectF(child.line().p1(), child.line().p2()).normalized()
                if edgeRect.contains(event.pos()):
                    self.edges_selection_changed.emit({'selected_edge': child})  # Emit only if edge is selected
                    break  # Stop further checks if edge is selected

        if not is_touching_icon:
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rect_changed.emit(self.rubberBand.geometry())
            self.rubberBand.show()
            self.changeRubberBand = True

        super().mousePressEvent(event)

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

                # print(str(len(selected)), 'nodes selected')
        self.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self,event)

    def apply_settings(self, parent_window):
        nodes, edges = self._collect_graph_items()
        layout_object = parent_window.ui.cboGraphConfiguration.currentData()
        self._apply_layout(layout_object, nodes, edges, parent_window)

        # Centrality settings
        centrality_type = constants.CentralityType(parent_window.ui.cboCentralityType.currentData())
        centrality_gradient = constants.CentralityGradient(parent_window.ui.cboCentralityGradient.currentData())
        centrality_showby = constants.CentralityShowBy(parent_window.ui.cboCentralityShowBy.currentData())

        # Apply default settings if centrality is not selected
        if self._should_apply_default_settings(centrality_type, centrality_gradient, centrality_showby):
            self._apply_default_node_settings(parent_window)
            return  # Exit if no centrality analysis is selected

        # Perform centrality analysis and visualization
        G = self._build_networkx_graph(nodes, edges)
        centrality_scores = self._calculate_centrality(G, centrality_type)
        self._apply_centrality_visuals(nodes, centrality_scores, centrality_gradient, centrality_showby)
        self.viewport().update()

    def _collect_graph_items(self):
        nodes, edges = [], []
        for child in self.items():
            if isinstance(child, GraphItem):
                nodes.append(child)
            elif isinstance(child, GraphEdge):
                edges.append(child)
        return nodes, edges

    def _apply_layout(self, layout_object, nodes, edges, parent_window):
        if layout_object and nodes:
            layout_factory = LayoutFactory()
            layout = layout_factory.create_layout(layout_object, nodes, edges, self.height(), self.width())
            if isinstance(layout, HierarchicalTreeLayout):
                root_node = self.find_root_node(nodes)
                layout.layout(root_node)
            else:
                layout.layout()

    def _should_apply_default_settings(self, centrality_type, centrality_gradient, centrality_showby):
        return (
                centrality_type == constants.CentralityType.Select or
                centrality_gradient == constants.CentralityGradient.Select or
                centrality_showby == constants.CentralityShowBy.Select
        )

    def _apply_default_node_settings(self, parent_window):
        for child in self.items():
            if isinstance(child, GraphItem):
                child.show_label = parent_window.ui.chkStyleNodeShowLabel.isChecked()
                child.label_position = constants.LabelPosition(parent_window.ui.cboStyleNodeLabelPosition.currentData())
                # In _apply_default_node_settings
                size = parent_window.ui.cboStyleNodeLabelSize.currentData()
                if isinstance(size, int):
                    child.label_size = size
                else:
                    child.label_size = 8  # Fallback to a default size if there's an issue
                child.node_background_color = self.node_background_color
                child.node_foreground_color = self.node_foreground_color
                child.show_icon = parent_window.ui.chkStyleNodeShowIcon.isChecked()
                child.use_image = parent_window.ui.chkStyleNodeUseImage.isChecked()
                child.node_shape = NodeShapes(parent_window.ui.cboStyleNodeShape.currentData())
                child.prepareGeometryChange()
                child.update()
            elif isinstance(child, GraphEdge):
                child.arrow_enabled = parent_window.ui.chkStyleEdgeDirectionArrow.isChecked()
                child.show_label = parent_window.ui.chkStyleEdgeShowLabel.isChecked()
        self.scene().update()
        self.viewport().repaint()

    def _build_networkx_graph(self, nodes, edges):
        G = nx.Graph()
        for node in nodes:
            G.add_node(node.identifier)
        for edge in edges:
            G.add_edge(edge.start.identifier, edge.end.identifier)
        return G

    def _calculate_centrality(self, G, centrality_type):
        if centrality_type == constants.CentralityType.Degrees:
            return nx.degree_centrality(G)
        elif centrality_type == constants.CentralityType.Eigenvactor:
            return nx.eigenvector_centrality(G, max_iter=500)
        elif centrality_type == constants.CentralityType.Katz:
            return nx.katz_centrality(G)
        elif centrality_type == constants.CentralityType.PageRank:
            return nx.pagerank(G)
        elif centrality_type == constants.CentralityType.Closeness:
            return nx.closeness_centrality(G)
        elif centrality_type == constants.CentralityType.Betweenness:
            return nx.betweenness_centrality(G)
        return {}

    def _apply_centrality_visuals(self, nodes, centrality_scores, centrality_gradient, centrality_showby):
        min_score, max_score = min(centrality_scores.values(), default=0), max(centrality_scores.values(), default=0)
        colormap = plt.get_cmap(
            "viridis") if centrality_gradient == constants.CentralityGradient.Viridis else plt.get_cmap("RdBu")

        min_size, max_size = 10, 50
        for node in nodes:
            score = centrality_scores.get(node.identifier, 0)
            normalized_score = (score - min_score) / (max_score - min_score) if max_score > min_score else 0

            if centrality_showby in (constants.CentralityShowBy.Color, constants.CentralityShowBy.Both):
                color = colormap(normalized_score)
                qcolor = QColor(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
                node.node_foreground_color = qcolor

            if centrality_showby in (constants.CentralityShowBy.Size, constants.CentralityShowBy.Both):
                node.node_size = min_size + normalized_score * (max_size - min_size)

            node.update()

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

    def tree_plot(self):
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

        layout_factory = LayoutFactory()
        layout = layout_factory.create_layout(constants.GraphLayout.HierarchicalTree, nodes, edges, self.height(), self.width())
        root_node = self.find_root_node(nodes)
        layout.layout(root_node)

    def open_graphml(self, scene, filename):
        # Ensure the scene is correctly passed
        if scene is None:
            print("Error: Scene is not initialized!")
        else:
            print(f"Scene: {scene}")

        # Proceed to load the GraphML data and check if nodes have positions
        has_positions = file_utils.load_graphml_to_scene(scene, filename)
        return has_positions

    def open_gexf(self, scene, filename):
        # Ensure the scene is correctly passed
        if scene is None:
            print("Error: Scene is not initialized!")
        else:
            print(f"Scene: {scene}")

        # Proceed to load the GraphML data and check if nodes have positions
        has_positions = file_utils.open_gexf(scene, filename)
        return has_positions

    def save_graphml(self, scene, filename):
        # Ensure the scene is correctly passed
        if scene is None:
            print("Error: Scene is not initialized!")
        else:
            print(f"Scene: {scene}")

        file_utils.save_graphml(scene, filename)


    def save_gexf(self, scene, filename):
        # Ensure the scene is correctly passed
        if scene is None:
            print("Error: Scene is not initialized!")
        else:
            print(f"Scene: {scene}")

        file_utils.save_gexf(scene, filename)

