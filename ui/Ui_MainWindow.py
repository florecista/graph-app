import os

from PyQt5.QtCore import QRect, QSize, Qt, QCoreApplication, QMetaObject
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMenuBar, QStatusBar, QDockWidget, QSizePolicy, \
    QTabWidget, QGroupBox, QFormLayout, QLabel, QCheckBox, QComboBox, QPushButton, QSpacerItem, QListView, QFrame, \
    QToolButton, QLineEdit, QGraphicsView

from widgets.GraphView import GraphView
from widgets.GraphScene import GraphScene


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabGraph = QWidget(self.centralwidget)
        self.tabGraph.setObjectName(u"tabGraph")
        self.verticalLayout_4 = QVBoxLayout(self.tabGraph)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.toolbarNorth = QHBoxLayout()
        self.toolbarNorth.setObjectName(u"toolbarNorth")

        self.buttonGraphLayoutCircle = QToolButton(self.tabGraph)
        self.buttonGraphLayoutCircle.setObjectName(u"buttonGraphLayoutCircle")
        self.buttonGraphLayoutCircle.setMinimumSize(QSize(30, 30))
        self.buttonGraphLayoutCircle.setMaximumSize(QSize(30, 30))
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\layout-circular.png"
        icon = QIcon(icon_path)
        self.buttonGraphLayoutCircle.setIcon(icon)
        self.buttonGraphLayoutCircle.setIconSize(QSize(24, 24))

        self.toolbarNorth.addWidget(self.buttonGraphLayoutCircle)

        self.buttonGraphLayoutRadial = QToolButton(self.tabGraph)
        self.buttonGraphLayoutRadial.setObjectName(u"buttonGraphLayoutRadial")
        self.buttonGraphLayoutRadial.setMinimumSize(QSize(30, 30))
        self.buttonGraphLayoutRadial.setMaximumSize(QSize(30, 30))
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\layout-radial.png"
        icon1 = QIcon(icon_path)
        self.buttonGraphLayoutRadial.setIcon(icon1)
        self.buttonGraphLayoutRadial.setIconSize(QSize(24, 24))

        self.toolbarNorth.addWidget(self.buttonGraphLayoutRadial)

        self.buttonGraphLayoutTree = QToolButton(self.tabGraph)
        self.buttonGraphLayoutTree.setObjectName(u"buttonGraphLayoutTree")
        self.buttonGraphLayoutTree.setMinimumSize(QSize(30, 30))
        self.buttonGraphLayoutTree.setMaximumSize(QSize(30, 30))
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\layout-tree.png"
        icon2 = QIcon(icon_path)
        self.buttonGraphLayoutTree.setIcon(icon2)
        self.buttonGraphLayoutTree.setIconSize(QSize(24, 24))

        self.toolbarNorth.addWidget(self.buttonGraphLayoutTree)

        self.buttonGraphLayoutSubGraph = QToolButton(self.tabGraph)
        self.buttonGraphLayoutSubGraph.setObjectName(u"buttonGraphLayoutSubGraph")
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\layout-grid.png"
        icon3 = QIcon(icon_path)
        icon3.addFile(u":/images/layout-grid.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonGraphLayoutSubGraph.setIcon(icon3)
        self.buttonGraphLayoutSubGraph.setIconSize(QSize(24, 24))

        self.toolbarNorth.addWidget(self.buttonGraphLayoutSubGraph)

        self.lineEditGraphFilter = QLineEdit(self.tabGraph)
        self.lineEditGraphFilter.setObjectName(u"lineEditGraphFilter")
        self.lineEditGraphFilter.setMaximumSize(QSize(150, 16777215))

        self.toolbarNorth.addWidget(self.lineEditGraphFilter)

        self.buttonGraphFit = QToolButton(self.tabGraph)
        self.buttonGraphFit.setObjectName(u"buttonGraphFit")
        self.buttonGraphFit.setMinimumSize(QSize(30, 30))
        self.buttonGraphFit.setMaximumSize(QSize(30, 30))
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\layout-fit.png"
        icon4 = QIcon(icon_path)
        self.buttonGraphFit.setIcon(icon4)
        self.buttonGraphFit.setIconSize(QSize(24, 24))

        self.toolbarNorth.addWidget(self.buttonGraphFit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.toolbarNorth.addItem(self.horizontalSpacer)

        self.verticalLayout_4.addLayout(self.toolbarNorth)

        self.canvasGraph = QVBoxLayout()
        self.canvasGraph.setObjectName(u"canvasGraph")

        self.graphScene = GraphScene(self.tabGraph)
        self.graphScene.setObjectName(u"graphView")
        self.graphView = GraphView()
        self.graphView.setScene(self.graphScene)

        self.canvasGraph.addWidget(self.graphView)

        # This is connected here because it needs the PlotWidget to be instantiated before it can be passed as a parameter
        # self.lineEditGraphFilter.textEdited.connect(self.graphView.eventFilterGraph)

        self.verticalLayout_4.addLayout(self.canvasGraph)

        self.verticalLayout_2.addWidget(self.tabGraph)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1257, 29))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        ## START OF CONFIGURATION PANEL
        self.dockWidgetFormatPanel = QDockWidget(MainWindow)
        self.dockWidgetFormatPanel.setObjectName(u"dockWidgetFormatPanel")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetFormatPanel.sizePolicy().hasHeightForWidth())
        self.dockWidgetFormatPanel.setSizePolicy(sizePolicy)
        self.dockWidgetFormatPanel.setMinimumSize(QSize(307, 540))
        self.dockWidgetFormatPanel.setMaximumSize(QSize(400, 524287))
        self.dockWidgetFormatPanel.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dockWidgetFormatPanel.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_12 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.settingTabWidget = QTabWidget(self.dockWidgetContents)
        self.settingTabWidget.setObjectName(u"settingTabWidget")
        self.tabSettingStyle = QWidget()
        self.tabSettingStyle.setObjectName(u"tabSettingStyle")
        self.verticalLayout = QVBoxLayout(self.tabSettingStyle)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.styleNodeGroupBox = QGroupBox(self.tabSettingStyle)
        self.styleNodeGroupBox.setObjectName(u"styleNodeGroupBox")
        self.formLayout = QFormLayout(self.styleNodeGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(10)
        self.lblStyleUseImage = QLabel(self.styleNodeGroupBox)
        self.lblStyleUseImage.setObjectName(u"lblStyleUseImage")
        self.lblStyleUseImage.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblStyleUseImage)

        self.chkStyleNodeUseImage = QCheckBox(self.styleNodeGroupBox)
        self.chkStyleNodeUseImage.setObjectName(u"chkStyleNodeUseImage")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.chkStyleNodeUseImage)

        self.lblStyleNodeShowIcon = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShowIcon.setObjectName(u"lblStyleNodeShowIcon")
        self.lblStyleNodeShowIcon.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblStyleNodeShowIcon)

        self.chkStyleNodeShowIcon = QCheckBox(self.styleNodeGroupBox)
        self.chkStyleNodeShowIcon.setObjectName(u"chkStyleNodeShowIcon")
        self.chkStyleNodeShowIcon.setChecked(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.chkStyleNodeShowIcon)

        self.lblStyleNodeShowLabel = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShowLabel.setObjectName(u"lblStyleNodeShowLabel")
        self.lblStyleNodeShowLabel.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblStyleNodeShowLabel)

        self.chkStyleNodeShowLabel = QCheckBox(self.styleNodeGroupBox)
        self.chkStyleNodeShowLabel.setObjectName(u"chkStyleNodeShowLabel")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.chkStyleNodeShowLabel)

        self.lblStyleNodeSize = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeSize.setObjectName(u"lblStyleNodeSize")
        self.lblStyleNodeSize.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblStyleNodeSize)

        self.cboNodeSize = QComboBox(self.styleNodeGroupBox)
        self.cboNodeSize.setObjectName(u"cboNodeSize")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cboNodeSize)

        self.lblStyleNodeLabelPosition = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeLabelPosition.setObjectName(u"lblStyleNodeLabelPosition")
        self.lblStyleNodeLabelPosition.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblStyleNodeLabelPosition)

        self.cboStyleNodeLabelPosition = QComboBox(self.styleNodeGroupBox)
        self.cboStyleNodeLabelPosition.setObjectName(u"cboStyleNodeLabelPosition")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.cboStyleNodeLabelPosition)

        self.lblStyleNodeLabelSize = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeLabelSize.setObjectName(u"lblStyleNodeLabelSize")
        self.lblStyleNodeLabelSize.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.lblStyleNodeLabelSize)

        self.cboStyleNodeLabelSize = QComboBox(self.styleNodeGroupBox)
        self.cboStyleNodeLabelSize.setObjectName(u"cboStyleNodeLabelSize")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.cboStyleNodeLabelSize)

        self.lblStyleNodeShape = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShape.setObjectName(u"lblStyleNodeShape")
        self.lblStyleNodeShape.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.lblStyleNodeShape)

        self.cboStyleNodeShape = QComboBox(self.styleNodeGroupBox)
        self.cboStyleNodeShape.setObjectName(u"cboStyleNodeShape")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.cboStyleNodeShape)

        self.lblStyleNodeShapeForegroundColor = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShapeForegroundColor.setObjectName(u"lblStyleNodeShapeForegroundColor")
        self.lblStyleNodeShapeForegroundColor.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.lblStyleNodeShapeForegroundColor)

        self.buttonStyleNodeShapeForegroundColor = QPushButton(self.styleNodeGroupBox)
        self.buttonStyleNodeShapeForegroundColor.setObjectName(u"buttonStyleNodeShapeForegroundColor")
        self.buttonStyleNodeShapeForegroundColor.setMaximumSize(QSize(25, 25))
        self.buttonStyleNodeShapeForegroundColor.setAutoFillBackground(False)
        self.buttonStyleNodeShapeForegroundColor.setStyleSheet(u"background: rgb(255, 0, 0)")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.buttonStyleNodeShapeForegroundColor)

        self.lblStyleNodeShapeBackgroundColor = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShapeBackgroundColor.setObjectName(u"lblStyleNodeShapeBackgroundColor")
        self.lblStyleNodeShapeBackgroundColor.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.lblStyleNodeShapeBackgroundColor)

        self.buttonStyleNodeShapeBackgroundColor = QPushButton(self.styleNodeGroupBox)
        self.buttonStyleNodeShapeBackgroundColor.setObjectName(u"buttonStyleNodeShapeBackgroundColor")
        self.buttonStyleNodeShapeBackgroundColor.setMaximumSize(QSize(25, 25))
        self.buttonStyleNodeShapeBackgroundColor.setStyleSheet(u"background: rgb(0, 0, 0)")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.buttonStyleNodeShapeBackgroundColor)

        self.lblStyleNodeShapeHighlightColor = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShapeHighlightColor.setObjectName(u"lblStyleNodeShapeHighlightColor")
        self.lblStyleNodeShapeHighlightColor.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.lblStyleNodeShapeHighlightColor)

        self.buttonStyleNodeShapeHighlightColor = QPushButton(self.styleNodeGroupBox)
        self.buttonStyleNodeShapeHighlightColor.setObjectName(u"buttonStyleNodeShapeHighlightColor")
        self.buttonStyleNodeShapeHighlightColor.setMinimumSize(QSize(0, 0))
        self.buttonStyleNodeShapeHighlightColor.setMaximumSize(QSize(25, 25))
        self.buttonStyleNodeShapeHighlightColor.setStyleSheet(u"background: rgb(0, 0, 255);")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.buttonStyleNodeShapeHighlightColor)

        self.lblStyleNodeShapeLabelFontColor = QLabel(self.styleNodeGroupBox)
        self.lblStyleNodeShapeLabelFontColor.setObjectName(u"lblStyleNodeShapeLabelFontColor")
        self.lblStyleNodeShapeLabelFontColor.setMinimumSize(QSize(0, 20))

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.lblStyleNodeShapeLabelFontColor)

        self.buttonStyleNodeShapeLabelFontColor = QPushButton(self.styleNodeGroupBox)
        self.buttonStyleNodeShapeLabelFontColor.setObjectName(u"buttonStyleNodeShapeLabelFontColor")
        self.buttonStyleNodeShapeLabelFontColor.setMaximumSize(QSize(25, 25))
        self.buttonStyleNodeShapeLabelFontColor.setStyleSheet(u"background: rgb(0, 255, 0)")

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.buttonStyleNodeShapeLabelFontColor)

        self.verticalLayout.addWidget(self.styleNodeGroupBox)

        self.styleEdgeGroupBox = QGroupBox(self.tabSettingStyle)
        self.styleEdgeGroupBox.setObjectName(u"styleEdgeGroupBox")
        self.formLayout_2 = QFormLayout(self.styleEdgeGroupBox)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(10)
        self.lblStyleEdgeShowLabel = QLabel(self.styleEdgeGroupBox)
        self.lblStyleEdgeShowLabel.setObjectName(u"lblStyleEdgeShowLabel")
        self.lblStyleEdgeShowLabel.setMinimumSize(QSize(117, 0))

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.lblStyleEdgeShowLabel)

        self.chkStyleEdgeShowLabel = QCheckBox(self.styleEdgeGroupBox)
        self.chkStyleEdgeShowLabel.setObjectName(u"chkStyleEdgeShowLabel")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.chkStyleEdgeShowLabel)

        self.lblStyleEdgeDirectionArrow = QLabel(self.styleEdgeGroupBox)
        self.lblStyleEdgeDirectionArrow.setObjectName(u"lblStyleEdgeDirectionArrow")
        self.lblStyleEdgeDirectionArrow.setMinimumSize(QSize(117, 0))

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.lblStyleEdgeDirectionArrow)

        self.chkStyleEdgeDirectionArrow = QCheckBox(self.styleEdgeGroupBox)
        self.chkStyleEdgeDirectionArrow.setObjectName(u"chkStyleEdgeDirectionArrow")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.chkStyleEdgeDirectionArrow)

        self.verticalLayout.addWidget(self.styleEdgeGroupBox)

        self.verticalSpacer_6 = QSpacerItem(20, 161, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.settingTabWidget.addTab(self.tabSettingStyle, "")
        self.tabSettingAdvanced = QWidget()
        self.tabSettingAdvanced.setObjectName(u"tabSettingAdvanced")
        self.verticalLayout_tabSettingsAdvanced = QVBoxLayout(self.tabSettingAdvanced)
        self.verticalLayout_tabSettingsAdvanced.setObjectName(u"verticalLayout_tabSettingsAdvanced")

        self.groupingConfigurationGroupBox = QGroupBox(self.tabSettingAdvanced)
        self.groupingConfigurationGroupBox.setObjectName(u"groupingConfigurationGroupBox")

        self.formLayout_3 = QFormLayout(self.groupingConfigurationGroupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setHorizontalSpacing(10)

        self.lblGroupAttributes = QLabel(self.groupingConfigurationGroupBox)
        self.lblGroupAttributes.setObjectName(u"lblGroupAttributes")
        self.lblGroupAttributes.setMinimumSize(QSize(90, 20))

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.lblGroupAttributes)

        self.cboGroupAttributes = QComboBox(self.groupingConfigurationGroupBox)
        self.cboGroupAttributes.setObjectName(u"cboGroupAttributes")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.cboGroupAttributes)

        self.lblGroupValues = QLabel(self.groupingConfigurationGroupBox)
        self.lblGroupValues.setObjectName(u"lblGroupValues")
        self.lblGroupValues.setMinimumSize(QSize(0, 20))

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.lblGroupValues)

        self.listGroupValues = QListView(self.groupingConfigurationGroupBox)
        self.listGroupValues.setObjectName(u"listGroupValues")

        self.verticalLayout_tabSettingsAdvanced.addWidget(self.groupingConfigurationGroupBox)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.listGroupValues)

        self.centralityGroupingConfigurationGroupBox = QGroupBox(self.tabSettingAdvanced)
        self.centralityGroupingConfigurationGroupBox.setObjectName(u"centralityGroupingConfigurationGroupBox")

        self.formLayout_4 = QFormLayout(self.centralityGroupingConfigurationGroupBox)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setHorizontalSpacing(10)
        self.lblCentralityType = QLabel(self.centralityGroupingConfigurationGroupBox)
        self.lblCentralityType.setObjectName(u"lblCentralityType")
        self.lblCentralityType.setMinimumSize(QSize(90, 20))
        self.lblCentralityType.setLayoutDirection(Qt.LeftToRight)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.lblCentralityType)

        self.cboCentralityType = QComboBox(self.centralityGroupingConfigurationGroupBox)
        self.cboCentralityType.setObjectName(u"cboCentralityType")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.cboCentralityType)

        self.lblCentralityShowBy = QLabel(self.centralityGroupingConfigurationGroupBox)
        self.lblCentralityShowBy.setObjectName(u"lblCentralityShowBy")
        self.lblCentralityShowBy.setMinimumSize(QSize(0, 20))

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.lblCentralityShowBy)

        self.cboCentralityShowBy = QComboBox(self.centralityGroupingConfigurationGroupBox)
        self.cboCentralityShowBy.setObjectName(u"cboCentralityShowBy")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.cboCentralityShowBy)

        self.lblCentralityGradient = QLabel(self.centralityGroupingConfigurationGroupBox)
        self.lblCentralityGradient.setObjectName(u"lblCentralityGradient")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.lblCentralityGradient)

        self.cboCentralityGradient = QComboBox(self.centralityGroupingConfigurationGroupBox)
        self.cboCentralityGradient.setObjectName(u"cboCentralityGradient")

        self.verticalLayout_tabSettingsAdvanced.addWidget(self.centralityGroupingConfigurationGroupBox)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.cboCentralityGradient)

        self.graphConfigurationGroupBox = QGroupBox(self.tabSettingAdvanced)
        self.graphConfigurationGroupBox.setObjectName(u"graphConfigurationGroupBox")

        self.formLayout_6 = QFormLayout(self.graphConfigurationGroupBox)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setHorizontalSpacing(10)
        self.lblGraphConfiguration = QLabel(self.graphConfigurationGroupBox)
        self.lblGraphConfiguration.setObjectName(u"lblGraphConfiguration")
        self.lblGraphConfiguration.setMinimumSize(QSize(90, 20))

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.lblGraphConfiguration)

        self.cboGraphConfiguration = QComboBox(self.graphConfigurationGroupBox)
        self.cboGraphConfiguration.setObjectName(u"cboGraphConfiguration")

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.cboGraphConfiguration)

        self.lblGraphHideOrphans = QLabel(self.graphConfigurationGroupBox)
        self.lblGraphHideOrphans.setObjectName(u"lblGraphHideOrphans")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.lblGraphHideOrphans)

        self.cboGraphHideOrphans = QComboBox(self.graphConfigurationGroupBox)
        self.cboGraphHideOrphans.setObjectName(u"cboGraphHideOrphans")

        self.verticalLayout_tabSettingsAdvanced.addWidget(self.graphConfigurationGroupBox)

        self.verticalSpacer_tabSettingsAdvanced = QSpacerItem(20, 161, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_tabSettingsAdvanced.addItem(self.verticalSpacer_tabSettingsAdvanced)

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.cboGraphHideOrphans)

        self.settingTabWidget.addTab(self.tabSettingAdvanced, "")

        self.verticalLayout_12.addWidget(self.settingTabWidget)

        self.buttonApplyStyle = QPushButton(self.dockWidgetContents)
        self.buttonApplyStyle.setObjectName(u"buttonApplyStyle")

        self.verticalLayout_12.addWidget(self.buttonApplyStyle)

        self.dockWidgetFormatPanel.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidgetFormatPanel)
        ## END OF CONFIGURATION PANEL

        ## START OF PALETTE PANEL
        self.dockWidgetPalette = QDockWidget(MainWindow)
        self.dockWidgetPalette.setObjectName(u"dockWidgetPalette")
        sizePolicy.setHeightForWidth(self.dockWidgetPalette.sizePolicy().hasHeightForWidth())
        self.dockWidgetPalette.setSizePolicy(sizePolicy)
        self.dockWidgetPalette.setMinimumSize(QSize(350, 314))
        self.dockWidgetPalette.setMaximumSize(QSize(550, 524287))
        self.dockWidgetPalette.setAutoFillBackground(False)
        self.dockWidgetPalette.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dockWidgetPalette.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.verticalLayout_8 = QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lblRelation = QLabel(self.dockWidgetContents_4)
        self.lblRelation.setObjectName(u"lblRelation")
        self.lblRelation.setMinimumSize(QSize(0, 22))
        self.lblRelation.setFrameShape(QFrame.Panel)
        self.lblRelation.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.lblRelation)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.edgeSuspected = QLabel(self.dockWidgetContents_4)
        self.edgeSuspected.setObjectName(u"edgeSuspected")
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\edge-suspected.png"
        # self.edgeSuspected.setPixmap(QPixmap(u":/images/edge-suspected.png"))
        self.edgeSuspected.setPixmap(QPixmap(icon_path))
        self.edgeSuspected.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.edgeSuspected)

        self.edgeConfirmed = QLabel(self.dockWidgetContents_4)
        self.edgeConfirmed.setObjectName(u"edgeConfirmed")
        icon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + r"\images\edge-confirmed.png"
        # self.edgeConfirmed.setPixmap(QPixmap(u":/images/edge-confirmed.png"))
        self.edgeConfirmed.setPixmap(QPixmap(icon_path))
        self.edgeConfirmed.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.edgeConfirmed)

        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.dockWidgetPalette.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetPalette)
        self.dockWidgetProperty = QDockWidget(MainWindow)
        self.dockWidgetProperty.setObjectName(u"dockWidgetProperty")
        self.dockWidgetProperty.setMinimumSize(QSize(80, 80))
        self.dockWidgetProperty.setFeatures(QDockWidget.DockWidgetFloatable)
        self.dockWidgetProperty.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.dockWidgetProperty.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidgetProperty)
        ## END OF PALETTE PANEL

        self.retranslateUi(MainWindow)

        self.settingTabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.buttonGraphLayoutCircle.setText("")
        self.buttonGraphLayoutRadial.setText("")
        self.buttonGraphLayoutTree.setText("")
        self.buttonGraphFit.setText("")
        self.styleNodeGroupBox.setTitle(QCoreApplication.translate("MainWindow", "Node Configuration", None))
        self.lblStyleUseImage.setText(QCoreApplication.translate("MainWindow", "Use Image", None))
        self.chkStyleNodeUseImage.setText("")
        self.lblStyleNodeShowIcon.setText(QCoreApplication.translate("MainWindow", "Show Node Icon", None))
        self.chkStyleNodeShowIcon.setText("")
        self.lblStyleNodeShowLabel.setText(QCoreApplication.translate("MainWindow", "Show Node Label", None))
        self.chkStyleNodeShowLabel.setText("")
        self.lblStyleNodeSize.setText(QCoreApplication.translate("MainWindow", "Node Size", None))
        self.lblStyleNodeLabelPosition.setText(QCoreApplication.translate("MainWindow", "Node Label Position", None))
        self.lblStyleNodeLabelSize.setText(QCoreApplication.translate("MainWindow", "Node Label Size", None))
        self.lblStyleNodeShape.setText(QCoreApplication.translate("MainWindow", "Shape", None))
        self.lblStyleNodeShapeForegroundColor.setText(
            QCoreApplication.translate("MainWindow", "Shape Foreground Color", None))
        self.lblStyleNodeShapeBackgroundColor.setText(
            QCoreApplication.translate("MainWindow", "Shape Background Color", None))
        self.lblStyleNodeShapeHighlightColor.setText(
            QCoreApplication.translate("MainWindow", "Shape Highlight Color", None))
        self.lblStyleNodeShapeLabelFontColor.setText(
            QCoreApplication.translate("MainWindow", "Shape Label Font Color", None))
        self.buttonStyleNodeShapeForegroundColor.setText("")
        self.buttonStyleNodeShapeBackgroundColor.setText("")
        self.buttonStyleNodeShapeHighlightColor.setText("")
        self.buttonStyleNodeShapeLabelFontColor.setText("")
        self.styleEdgeGroupBox.setTitle(QCoreApplication.translate("MainWindow", "Edge Configuration", None))
        self.lblStyleEdgeShowLabel.setText(
            QCoreApplication.translate("MainWindow", "Show Edge Label               ", None))
        self.chkStyleEdgeShowLabel.setText("")
        self.lblStyleEdgeDirectionArrow.setText(QCoreApplication.translate("MainWindow", "Show Edge Arrow", None))
        self.chkStyleEdgeDirectionArrow.setText("")
        self.settingTabWidget.setTabText(self.settingTabWidget.indexOf(self.tabSettingStyle),
                                         QCoreApplication.translate("MainWindow", "Style", None))
        self.groupingConfigurationGroupBox.setTitle(
            QCoreApplication.translate("MainWindow", "Grouping Configuration", None))
        self.lblGroupAttributes.setText(QCoreApplication.translate("MainWindow", "Attributes", None))
        self.lblGroupValues.setText(QCoreApplication.translate("MainWindow", "Values", None))
        self.centralityGroupingConfigurationGroupBox.setTitle(
            QCoreApplication.translate("MainWindow", "Centrality Grouping Configuration", None))
        self.lblCentralityType.setText(QCoreApplication.translate("MainWindow", "Type", None))
        self.lblCentralityShowBy.setText(QCoreApplication.translate("MainWindow", "Show by", None))
        self.lblCentralityGradient.setText(QCoreApplication.translate("MainWindow", "Gradient", None))
        self.graphConfigurationGroupBox.setTitle(QCoreApplication.translate("MainWindow", "Graph Configuration", None))
        self.lblGraphConfiguration.setText(QCoreApplication.translate("MainWindow", "Layout", None))
        self.lblGraphHideOrphans.setText(QCoreApplication.translate("MainWindow", "Hide Orphans", None))
        self.settingTabWidget.setTabText(self.settingTabWidget.indexOf(self.tabSettingAdvanced),
                                         QCoreApplication.translate("MainWindow", "Advanced", None))
        self.buttonApplyStyle.setText(QCoreApplication.translate("MainWindow", "Apply", None))
        self.lblRelation.setText(QCoreApplication.translate("MainWindow", "Relations", None))
        self.edgeSuspected.setText("")
        self.edgeConfirmed.setText("")
        self.lineEditGraphFilter.setText("Filter")
        self.lineEditGraphFilter.setStyleSheet("color: grey;")
    # retranslateUi
