import os
import sys
from datetime import datetime

from PyQt5.QtCore import QTranslator, QDir, QPoint, QMimeData, QRect, QFileInfo
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QMenuBar, QActionGroup, QDialog, QLabel, \
    QTableView, QAbstractItemView, QHeaderView, QVBoxLayout, QPushButton, QColorDialog, QFileDialog

import constants
from delegates.EdgePropertyDelegate import EdgePropertyDelegate
from delegates.NodePropertyDelegate import NodePropertyDelegate
from managers import js_manager
from models.EdgePropertyModel import EdgePropertyModel
from models.NodePropertyModel import NodePropertyModel
from ui.Ui_DlgEdge import Ui_DlgEdge
from ui.Ui_MainWindow import Ui_MainWindow
from utils import file_utils
from utils.utils import populate_listwidget_enum


class EdgeDialog(QDialog):
    graphView = None

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_DlgEdge()
        self.ui.setupUi(self)

        self.ui.cboRelationType.addItem("Confirmed")
        self.ui.cboRelationType.addItem("Suspeted")

    def showEvent(self, arg1):
        self.ui.cboSource.clear()
        self.ui.txtLabel.setText("")
        self.ui.txtWeight.setText("0")
        # self.ui.cboSource.addItems(graphm.G.nodes())
        self.ui.cboTarget.clear()
        # self.ui.cboTarget.addItems(graphm.G.nodes())

    def accept(self):
        source = self.ui.cboSource.currentText()
        target = self.ui.cboTarget.currentText()
        label = self.ui.txtLabel.text()
        weight = float(self.ui.txtWeight.text())
        self.graphView.add_edge(source, target, label, weight)

        super().accept()


class GraphTab(QMainWindow):
    selectedPoints = []

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # js_manager.node_updated.connect(self.ui.graphView.apply_settings)

        self.dlgedge = EdgeDialog(self)
        self.dlgedge.graphView = self.ui.graphScene

        self.setAcceptDrops(True)
        self.dragStartPosition = QPoint()

        self.icon_size = self.ui.graphScene.graphSceneProperties.application_icon_size

        # self._load_state()
        self._read_json()
        self.__init_gui()
        self.__init_property_view()

        self.ui.graphView.nodes_selection_changed.connect(self.__node_selection_changed)
        self.ui.graphView.edges_selection_changed.connect(self.__edge_selection_changed)

        self.import_path = ""

        self.graph_layout_has_changed = False

    def __node_selection_changed(self, node):
        self.tableView.setModel(self.node_property_model)
        self.tableView.setItemDelegate(NodePropertyDelegate(self.tableView))
        self.node_property_model.reset(node)
        self.remove_button.setEnabled(len(node) > 0)

    def __edge_selection_changed(self, edge):
        selected_edge = edge.get('selected_edge')
        if selected_edge:
            self.tableView.setModel(self.edge_property_model)
            self.tableView.setItemDelegate(EdgePropertyDelegate(self.tableView))
            self.edge_property_model.set_edge(selected_edge)  # Pass the edge to the model
            self.remove_button.setEnabled(True)
        else:
            self.tableView.setModel(None)
            self.remove_button.setEnabled(False)

    #
    # def mousePressEvent(self, event):
    #     if event.type() == Qt.MouseButton.LeftButton:
    #         self.dragStartPosition = event.pos()

    def mouseMoveEvent(self, event):
        if (
            event.pos() - self.dragStartPosition
        ).manhattanLength() < QApplication.startDragDistance():
            return

        label = self.childAt(event.pos())
        if label is None or not isinstance(label, QLabel):
            return

        self.draggingLabel = label
        pxm = label.pixmap()
        if pxm is None:
            return

        drag = QDrag(label)
        mime = QMimeData()
        drag.setMimeData(mime)
        # mime.setImageData(pxm.toImage())
        drag.setPixmap(pxm)

        drag.exec_()

    # def mouseReleaseEvent(self, event):
    #     super(GraphTab, self).mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        event.setAccepted(True)

    def dropEvent(self, event):

        window_pos_x = event.pos().x()
        window_pos_y = event.pos().y()

        configuration_panel_left_width = self.ui.dockWidgetFormatPanel.width()
        x = window_pos_x - configuration_panel_left_width
        # TODO - this is wrong
        y = window_pos_y

        position = QPoint(x, y)

        self.ui.statusbar.showMessage("Dropped at x:% s, y:% s" % (x, y))
        w = self.ui.graphView.width()
        h = self.ui.graphView.height()

        viewRect = QRect(x, y, w, h)
        if not viewRect.contains(position):
            print('Position not inside View Rectangle width:% s and x:% s' % (w, x))
            return

        labelObjName = self.draggingLabel.objectName()
        if labelObjName == "edgeSuspected" or labelObjName == "edgeConfirmed":
            print('dropping edge')
            # nodes = graphm.G.nodes()
            # if len(nodes) > 1:
            #     self.dlgedge.exec()
        else:
            attributes: dict = {
                "Group": self.draggingLabel.property("Group"),
                "Type": self.draggingLabel.property("Type"),
            }
            attr_property = self.draggingLabel.property("Attributes")
            if attr_property is not None:
                attributes["Attributes"] = attr_property
            else:
                attributes["Attributes"] = []

            attributes['Image'] = self.draggingLabel.property('image')
            self.ui.graphScene.add_node(position, attributes)

    def _read_json(self):
        js_manager.init(file_name="type.json", icon_size=self.icon_size)
        self.toolbox = js_manager.tool_box_widget(parent=self.ui.dockWidgetContents_4)
        self.ui.verticalLayout_8.addWidget(self.toolbox)

    def __init_gui(self):
        # Style Tab
        # self.ui.chkStyleNodeUseImage.clicked.connect(
        #     self.__gui_style_node_use_image_changed
        # )
        # self.ui.chkStyleNodeShowIcon.clicked.connect(
        #     self.__gui_style_node_show_icon_changed
        # )
        # self.ui.chkStyleNodeShowLabel.clicked.connect(
        #     self.__gui_style_node_show_label_changed
        # )

        self.ui.cboNodeSize.addItem("30x30", 30)
        self.ui.cboNodeSize.addItem("50x50", 50)
        self.ui.cboNodeSize.addItem("100x100", 100)
        self.ui.cboNodeSize.addItem("200x200", 200)
        self.ui.cboNodeSize.addItem("300x300", 300)
        #self.ui.cboNodeSize.activated.connect(self.__gui_node_size_changed)

        populate_listwidget_enum(
            self.ui.cboStyleNodeLabelPosition, constants.LabelPosition
        )
        # self.ui.cboStyleNodeLabelPosition.activated.connect(
        #     self.__gui_node_label_position_changed
        # )

        self.ui.cboStyleNodeLabelSize.addItem("8", 8)
        self.ui.cboStyleNodeLabelSize.addItem("16", 16)
        self.ui.cboStyleNodeLabelSize.addItem("24", 24)
        self.ui.cboStyleNodeLabelSize.addItem("32", 32)
        # self.ui.cboStyleNodeLabelSize.activated.connect(
        #     self.__gui_node_label_size_changed
        # )

        populate_listwidget_enum(self.ui.cboStyleNodeShape, constants.NodeShapes)
        # self.ui.cboStyleNodeShape.activated.connect(self.__gui_style_node_shape_changed)

        self.ui.buttonStyleNodeShapeForegroundColor.clicked.connect(
            self.__gui_node_foreground_color
        )
        self.ui.buttonStyleNodeShapeBackgroundColor.clicked.connect(
            self.__gui_node_background_color
        )
        # self.ui.buttonStyleNodeShapeHighlightColor.clicked.connect(
        #     self.__gui_node_highlight_color
        # )
        # self.ui.buttonStyleNodeShapeLabelFontColor.clicked.connect(
        #     self.__gui_node_label_text_color
        # )
        #
        # self.ui.chkStyleEdgeShowLabel.clicked.connect(
        #     self.__gui_style_edge_show_label_changed
        # )
        #
        # self.ui.chkStyleEdgeDirectionArrow.clicked.connect(
        #     self.__gui_style_edge_show_arrow_changed
        # )

        # Advanced Tab
        populate_listwidget_enum(self.ui.cboCentralityType, constants.CentralityType)
        # self.ui.cboCentralityType.activated.connect(self.__gui_centrality_type_changed)
        #
        populate_listwidget_enum(
            self.ui.cboCentralityShowBy, constants.CentralityShowBy
        )
        # self.ui.cboCentralityShowBy.activated.connect(
        #     self.__gui_centrality_show_by_changed
        # )

        populate_listwidget_enum(
            self.ui.cboCentralityGradient, constants.CentralityGradient
        )
        # self.ui.cboCentralityGradient.activated.connect(
        #     self.__gui_centrality_gradient_changed
        # )

        populate_listwidget_enum(self.ui.cboGraphConfiguration, constants.GraphLayout)
        # self.ui.cboGraphConfiguration.activated.connect(self.__gui_graph_layout_changed)

        populate_listwidget_enum(
            self.ui.cboGraphHideOrphans, constants.GraphHideOrphans
        )
        # self.ui.cboGraphHideOrphans.activated.connect(
        #     self.__gui_graph_hide_orphans_changed
        # )

        # General
        self.ui.buttonApplyStyle.clicked.connect(self.apply_settings)

        # self.ui.buttonGraphLayoutCircle.clicked.connect(self.graphLayoutCircleClicked)
        # self.ui.buttonGraphLayoutRadial.clicked.connect(self.graphLayoutRadialClicked)
        self.ui.buttonGraphLayoutTree.clicked.connect(self.graphLayoutTreeClicked)
        # self.ui.buttonGraphLayoutSubGraph.clicked.connect(
        #     self.graphLayoutSubGraphClicked
        # )

    def __gui_node_foreground_color(self):
        self.ui.graphView.node_foreground_color = QColorDialog.getColor()

    def __gui_node_background_color(self):
        self.ui.graphView.node_background_color = QColorDialog.getColor()

    def __init_property_view(self):
        self.tableView = QTableView(self.ui.dockWidgetContents_2)
        self.tableView.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableView.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.node_property_model = NodePropertyModel(self.tableView)
        self.node_property_model.dataChanged.connect(self.__node_property_changed)
        js_manager.node_updated.connect(self.node_property_model.reset)

        self.edge_property_model = EdgePropertyModel(self.tableView)
        self.edge_property_model.dataChanged.connect(self.__edge_property_changed)

        v_layout = QVBoxLayout(self.ui.dockWidgetContents_2)
        v_layout.addWidget(self.tableView)

        self.remove_button = QPushButton("", self.ui.dockWidgetContents_2)
        self.remove_button.setText(self.tr("Delete"))
        self.remove_button.setEnabled(False)
        self.remove_button.clicked.connect(self.__remove_selected)
        v_layout.addWidget(self.remove_button)

    def __node_property_changed(self):
        self.ui.graphView.apply_settings(self)

    def __edge_property_changed(self):
        self.ui.graphView.apply_settings(self)

    def __remove_selected(self):
        # nodes = list(graphm.cur_G.nodes.data(False))
        # for i in self.ui.graphView.selected_node_indexes:
        #     graphm.G.remove_node(nodes[i])
        #
        # edges = list(graphm.cur_G.edges.data(False))
        # for i in self.ui.graphView.edge_selected_indexes:
        #     graphm.G.remove_edge(edges[i][0], edges[i][1])
        #
        # self.ui.graphView.selected_node_indexes = []
        # self.ui.graphView.edge_selected_indexes = []
        #
        # self.ui.graphView.selected_node_names = None
        # self.ui.graphView.selected_node_pressed_positions = None

        self.__deselected()
        self.apply_settings()

    def graphLayoutTreeClicked(self):
        self.ui.graphView.tree_plot()

    def open_graph(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open", self.import_path, "GraphML (*.graphml);;GEXF (*.gexf)"
        )
        if file_name:
            self.import_path = str(QFileInfo(file_name).absolutePath())
            self.ui.statusbar.showMessage("Importing data...")
            self.ui.statusbar.repaint()

            # Clear the current graphScene before importing new data
            self.ui.graphScene.clear()

            # Determine which function to call based on file extension
            if file_name.endswith(".graphml"):
                has_positions = self.ui.graphView.open_graphml(self.ui.graphScene, file_name)
            elif file_name.endswith(".gexf"):
                has_positions = self.ui.graphView.open_gexf(self.ui.graphScene, file_name)

            # If nodes do not have saved positions, use default layout
            if not has_positions:
                self.ui.cboGraphConfiguration.setCurrentIndex(constants.GraphLayout.FruchtermanReingold)

            self.apply_settings()
            self.ui.statusbar.clearMessage()

    def save_graph(self) -> None:
        file_name = datetime.today().strftime("%Y-%m-%d") + "_Graph"
        default_filename = os.path.join(self.import_path, file_name)
        file_name, file_filter = QFileDialog.getSaveFileName(
            self,
            "Save",
            default_filename,
            "GraphML (*.graphml);;GEXF (*.gexf)"
        )
        if file_name:
            if file_filter == "GraphML (*.graphml)":
                self.ui.graphView.save_graphml(self.ui.graphScene, file_name)
            elif file_filter == "GEXF (*.gexf)":
                self.ui.graphView.save_gexf(self.ui.graphScene, file_name)

    def apply_settings(self):
        self.ui.graphScene.style_updated = True
        #if self.graph_layout_has_changed:
        #    self.ui.graphView.apply_settings()
        #    self.graph_layout_has_changed = False
        #else:
        #self.ui.graphScene.apply_settings()
        self.ui.graphView.apply_settings(self)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.license_file = ""
        self.translator = None

        self.tabWidget = QTabWidget()
        self.graph_view = GraphTab() # Graph Tab
        self.tabWidget.addTab(self.graph_view, self.tr("Graph")) # Add Graph Tab
        self.tabWidget.addTab(QWidget(), self.tr("Timeline")) # Add Timeline Tab
        self.setCentralWidget(self.tabWidget)

        self.menubar = QMenuBar()
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.menu_file_items = self.menubar.addMenu("&File")
        self.menu_file_items.aboutToShow.connect(self.on_menu_file_about_to_show)

        self.menu_language_items = self.menubar.addMenu("&Language")
        self.menu_language_items.aboutToShow.connect(
            self.on_menu_language_about_to_show
        )
        self.menu_language_items_group = QActionGroup(self)
        self.menu_language_items_group.setExclusive(True)

        self.menu_help_items = self.menubar.addMenu("&Help")
        self.menu_help_items.aboutToShow.connect(self.on_menu_help_about_to_show)

        self.showMaximized()

    def on_menu_file_about_to_show(self):
        self.menu_file_items.clear()
        action = self.menu_file_items.addAction("")
        action.setText(self.tr("&New"))
        # action.triggered.connect(self.graph_view.clear_graph)
        action = self.menu_file_items.addAction("")
        action.setText(self.tr("&Open..."))
        action.triggered.connect(self.graph_view.open_graph)
        action = self.menu_file_items.addAction("&Import...")
        action.setText(self.tr("&Import..."))
        action.setDisabled(True)
        action = self.menu_file_items.addAction("&Close")
        action.setText(self.tr("&Close"))
        action.setDisabled(True)
        action = self.menu_file_items.addAction("&Save...")
        action.setText(self.tr("&Save..."))
        action.triggered.connect(self.graph_view.save_graph)
        action = self.menu_file_items.addAction("&Export Image...")
        action.setText(self.tr("&Export Image..."))
        # action.triggered.connect(self.graph_view.export_image)

        action = self.menu_file_items.addAction("&Exit")
        action.setText(self.tr("&Exit"))
        action.triggered.connect(self.exit)

    def on_menu_language_about_to_show(self):
        self.menu_language_items.clear()

        actions = self.menu_language_items_group.actions()
        for action in actions:
            self.menu_language_items_group.removeAction(action)

        action = self.menu_language_items.addAction("")
        action.setText(self.tr("&English"))
        self.menu_language_items_group.addAction(action)
        action.setCheckable(True)
        action.setChecked(self.translator is None)
        action.triggered.connect(lambda: self.on_language_changed(""))

        action = self.menu_language_items.addAction("")
        action.setText(self.tr("&Russian"))
        self.menu_language_items_group.addAction(action)
        action.setCheckable(True)
        action.setChecked(self.translator is not None and self.translator.language() == "ru_RU")
        action.triggered.connect(lambda: self.on_language_changed("RU"))

    def on_language_changed(self, language: str):
        QDir.addSearchPath("translations", "translations")
        if language == "RU":
            self.translator = QTranslator(self)
            if self.translator.load(u"RU.qm", ":/translations"):
                QApplication.installTranslator(self.translator)
        else:
            if self.translator:
                QApplication.removeTranslator(self.translator)
            self.translator = None

        self.graph_view.ui.retranslateUi(self.graph_view)

        self.menu_file_items.setTitle(self.tr("&File"))
        self.menu_language_items.setTitle(self.tr("&Language"))
        self.menu_help_items.setTitle(self.tr("&Help"))

        self.tabWidget.setTabText(0, self.tr("Graph"))
        self.tabWidget.setTabText(1, self.tr("Timeline"))

        self.graph_view.dlgedge.ui.retranslateUi(self.graph_view.dlgedge)
        for ind in range(self.graph_view.toolbox.count()):
            self.graph_view.toolbox.setItemText(ind, self.tr(self.graph_view.toolbox.itemText(ind)))

        self.graph_view.remove_button.setText(self.tr('Delete'))

    def on_menu_help_about_to_show(self):
        self.menu_help_items.clear()
        action = self.menu_help_items.addAction("")
        action.setText(self.tr("&About"))
        # action.triggered.connect(self.show_about_dialog)

    def exit(self):
        QApplication.closeAllWindows()

    # def show_about_dialog(self) -> None:
    #     ShowLicenseWindow = Ui_Registration()
    #     ShowLicenseWindow.aboutLicense(self.license_file)
    #     ShowLicenseWindow.exec_()



app = QApplication([])
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec_())
# END: bypass license check


if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    app.setOrganizationName("Graph")
    app.setApplicationName("Graph")

    # check license file
    licenseFlag = False

    for licenseFile in glob.glob("*.license"):
        if check_license_file(licenseFile):
            licenseFlag = True
            file = licenseFile

    if licenseFlag:
        mainwindow = MainView()
        mainwindow.license_file = file
        mainwindow.show()
    else:
        print("License is expired or not found.")
        addLicenseWindow = Ui_Registration()
        result = addLicenseWindow.exec_()
        if result == 0:
            sys.exit(0)

        if len(addLicenseWindow.licenseFile) > 0:
            print(
                'License file: "'
                + addLicenseWindow.licenseFile
                + '" is copied to current folder.'
            )

            old_path, base = os.path.split(addLicenseWindow.licenseFile)
            new_path = os.path.join(os.getcwd(), base)
            dest = shutil.copyfile(addLicenseWindow.licenseFile, new_path)

            if check_license_file(dest):
                mainwindow = MainView()
                mainwindow.license_file = base
                mainwindow.show()

    sys.exit(app.exec_())
