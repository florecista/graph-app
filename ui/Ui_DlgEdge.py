from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt
from PyQt5.QtWidgets import QFormLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox


class Ui_DlgEdge(object):
    def setupUi(self, DlgEdge):
        if not DlgEdge.objectName():
            DlgEdge.setObjectName(u"DlgEdge")
        DlgEdge.resize(400, 230)
        self.formLayout = QFormLayout(DlgEdge)
        self.formLayout.setObjectName(u"formLayout")
        self.lblLabel = QLabel(DlgEdge)
        self.lblLabel.setObjectName(u"lblLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblLabel)

        self.txtLabel = QLineEdit(DlgEdge)
        self.txtLabel.setObjectName(u"txtLabel")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtLabel)

        self.lblRelationType = QLabel(DlgEdge)
        self.lblRelationType.setObjectName(u"lblRelationType")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblRelationType)

        self.cboRelationType = QComboBox(DlgEdge)
        self.cboRelationType.setObjectName(u"cboRelationType")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.cboRelationType)

        self.lblSource = QLabel(DlgEdge)
        self.lblSource.setObjectName(u"lblSource")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblSource)

        self.cboSource = QComboBox(DlgEdge)
        self.cboSource.setObjectName(u"cboSource")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cboSource)

        self.lblTarget = QLabel(DlgEdge)
        self.lblTarget.setObjectName(u"lblTarget")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblTarget)

        self.cboTarget = QComboBox(DlgEdge)
        self.cboTarget.setObjectName(u"cboTarget")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.cboTarget)

        self.buttonBox = QDialogButtonBox(DlgEdge)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.buttonBox)

        self.txtWeight = QLineEdit(DlgEdge)
        self.txtWeight.setObjectName(u"txtWeight")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.txtWeight)

        self.lblWeight = QLabel(DlgEdge)
        self.lblWeight.setObjectName(u"lblWeight")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblWeight)


        self.retranslateUi(DlgEdge)
        self.buttonBox.accepted.connect(DlgEdge.accept)
        self.buttonBox.rejected.connect(DlgEdge.reject)

        QMetaObject.connectSlotsByName(DlgEdge)
    # setupUi

    def retranslateUi(self, DlgEdge):
        DlgEdge.setWindowTitle(QCoreApplication.translate("DlgEdge", "Relation", None))
        self.lblLabel.setText(QCoreApplication.translate("DlgEdge", "Label", None))
        self.lblRelationType.setText(QCoreApplication.translate("DlgEdge", "Relation Type", None))
        self.lblSource.setText(QCoreApplication.translate("DlgEdge", "Source", None))
        self.lblTarget.setText(QCoreApplication.translate("DlgEdge", "Target", None))
        self.lblWeight.setText(QCoreApplication.translate("DlgEdge", "Weight", None))
    # retranslateUi

