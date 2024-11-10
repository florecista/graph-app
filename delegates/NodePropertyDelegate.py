import datetime
from PyQt5.QtCore import QModelIndex, Qt, QDate, QAbstractItemModel, pyqtSlot
from PyQt5.QtWidgets import QItemDelegate, QWidget, QComboBox, QDateEdit, QCheckBox, QLineEdit

from widgets.GraphItem import GraphItem
from widgets.ImagePropertyWidget import ImagePropertyWidget
from managers import js_manager


class NodePropertyDelegate(QItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        model = index.model()

        # Determine the key based on row to identify the editor type
        if index.row() < len(model.node_valid_keys):
            key = model.node_valid_keys[index.row()]
        else:
            # Extract key from 'Attributes' based on the adjusted row index
            attr_index = index.row() - len(model.node_valid_keys)
            attributes = model.node.attributes.get("Attributes", [])
            key = attributes[attr_index].get("name", "") if attr_index < len(attributes) else ""

        # Handle QDateEdit for Date fields
        if key == "Date of Birth":
            editor = QDateEdit(parent)
            editor.setDisplayFormat("dd/MM/yyyy")
            editor.setMinimumDate(QDate(1, 1, 1))
            return editor

        # Handle QComboBox for Group and Type
        if key == "Group":
            editor = QComboBox(parent)
            editor.addItems(js_manager.groups())
            return editor
        elif key == "Type":
            editor = QComboBox(parent)
            group = model.node.attributes.get("Group", "") if isinstance(model.node, GraphItem) else model.node.get(
                "Group", "")
            editor.addItems(js_manager.types(group))
            return editor

        # Handle QComboBox for Label (new addition)
        if key == "Label":
            editor = QComboBox(parent)
            editor.addItems(model.label_types)  # Populate with label_types
            editor.setProperty('index', index)  # Store the index in the editor
            editor.currentIndexChanged.connect(self.on_label_changed)  # Connect to the slot
            return editor

        # Handle QComboBox for Country of Birth
        if key == "Country of Birth":
            editor = QComboBox(parent)
            countries = [
                "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
                "Australia",
                "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize",
                "Benin",
                "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
                "Burkina Faso", "Burundi",
                "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China",
                "Colombia",
                "Comoros", "Congo (Congo-Brazzaville)", "Congo (Congo-Kinshasa)", "Costa Rica", "Croatia", "Cuba",
                "Cyprus", "Czechia",
                "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
                "Equatorial Guinea", "Eritrea",
                "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany",
                "Ghana", "Greece",
                "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland",
                "India", "Indonesia",
                "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
                "Kiribati", "Korea (North)",
                "Korea (South)", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
                "Liechtenstein", "Lithuania",
                "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
                "Mauritania", "Mauritius",
                "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
                "Myanmar", "Namibia", "Nauru",
                "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway",
                "Oman", "Pakistan", "Palau",
                "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
                "Romania", "Russia", "Rwanda",
                "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
                "Sao Tome and Principe",
                "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
                "Solomon Islands",
                "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
                "Switzerland", "Syria", "Taiwan",
                "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
                "Turkey", "Turkmenistan",
                "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
                "Uzbekistan", "Vanuatu",
                "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
            ]
            editor.addItems(countries)
            return editor

        # QLineEdit for string attributes
        attribute = next((attr for attr in model.node.attributes.get("Attributes", []) if attr.get("name") == key),
                         None)
        if attribute and attribute.get("type") == "string":
            editor = QLineEdit(parent)
            return editor

        # Default editor handling
        data = index.data(Qt.UserRole)
        if isinstance(data, dict) and 'image' in data.keys():
            editor = ImagePropertyWidget(parent)
        elif isinstance(data, bool):
            editor = QCheckBox(parent)
        elif isinstance(data, str):
            editor = QLineEdit(parent)
        else:
            return None

        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        data = index.data(Qt.UserRole)
        if isinstance(editor, QLineEdit):
            editor.setText(data)
            editor.editingFinished.connect(self.__editing_finished)
        elif isinstance(editor, QDateEdit) and isinstance(data, datetime.date):
            editor.setDate(QDate(data.year, data.month, data.day))
        elif isinstance(editor, QCheckBox):
            editor.setChecked(data)
            editor.clicked.connect(self.__editing_finished)
        elif isinstance(editor, QComboBox):
            editor.setCurrentText(data)
            editor.currentIndexChanged.connect(self.__editing_finished)
        elif isinstance(editor, ImagePropertyWidget):
            editor.set_data(data)
            editor.image_changed.connect(self.__editing_finished)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        key = model.node_valid_keys[index.row()] if index.row() < len(model.node_valid_keys) else ""

        # Handle QDateEdit
        if isinstance(editor, QDateEdit):
            date = editor.date()
            date_str = date.toString("dd/MM/yyyy")
            model.setData(index, date_str, Qt.EditRole)

        # Handle QLineEdit
        elif isinstance(editor, QLineEdit):
            model.setData(index, editor.text(), Qt.EditRole)

        # Handle QComboBox
        elif isinstance(editor, QComboBox):
            selected_value = editor.currentText()
            model.setData(index, selected_value, Qt.EditRole)
            # Update GraphItem.label when the selection changes
            if key == "Label":
                model.node.set_label(selected_value)  # Update the label of the GraphItem

        # Handle QCheckBox
        elif isinstance(editor, QCheckBox):
            model.setData(index, editor.isChecked(), Qt.EditRole)

        # Handle ImagePropertyWidget
        elif isinstance(editor, ImagePropertyWidget):
            data = editor.get_data()
            if data['image']:
                model.setData(index, data, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    @pyqtSlot()
    def __editing_finished(self) -> None:
        self.commitData.emit(self.sender())
        self.closeEditor.emit(self.sender())

    @pyqtSlot()
    def on_label_changed(self):
        editor = self.sender()  # Get the sender (QComboBox)
        if isinstance(editor, QComboBox):
            selected_value = editor.currentText()  # Get the selected value from the combobox

            # Get the index from the editor
            index = editor.property('index')  # Retrieve the index stored in the editor's property

            if index.isValid():
                model = index.model()  # Get the model from the index
                if isinstance(model.node, GraphItem):  # Check if the node is an instance of GraphItem
                    model.node.set_label(selected_value)  # Update the label of the GraphItem
                    self.commitData.emit(editor)  # Commit the data to the model
