from PyQt5.QtCore import QStandardPaths, QDir, QMimeDatabase, QMimeType, QFileInfo, QByteArray, QBuffer, QIODevice, \
    pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QImageReader, QImageWriter
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QToolButton, QLabel, QSizePolicy, QFileDialog


class ImagePropertyWidget(QWidget):
    image_changed = pyqtSignal()
    import_path: str = ''

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.name: str = ''
        self.image: QImage = QImage()
        self.__init_ui()

    def __init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(self)
        label.setWordWrap(False)
        layout.addWidget(label)

        button = QToolButton(self)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
        button.setText('...')
        layout.addWidget(button)

        self.setFocusProxy(button)
        self.setFocusPolicy(button.focusPolicy())

        button.clicked.connect(self.__open)

    @staticmethod
    def __initialize_image_file_dialog(dialog: QFileDialog, accept_mode: QFileDialog.AcceptMode) -> None:
        if not ImagePropertyWidget.import_path:
            pictures_locations: list = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            if len(pictures_locations) == 0:
                ImagePropertyWidget.import_path = QDir.currentPath()
            else:
                ImagePropertyWidget.import_path = pictures_locations[-1]

        dialog.setDirectory(ImagePropertyWidget.import_path)
        if accept_mode == QFileDialog.AcceptOpen:
            supported_mime_types: list = QImageReader.supportedMimeTypes()
        else:
            supported_mime_types: list = QImageWriter.supportedMimeTypes()

        supported_types = [item.data().decode() for item in supported_mime_types]
        supported_types.sort()

        # compose filter for all supported types
        mime_db = QMimeDatabase()
        all_supported_formats: list = []
        for supported_type in supported_types:
            mime_type: QMimeType = mime_db.mimeTypeForName(supported_type)
            if mime_type.isValid():
                all_supported_formats.extend(mime_type.globPatterns())

        dialog.setMimeTypeFilters(supported_types)
        dialog.selectMimeTypeFilter("image/jpeg")

        all_supported_formats_filter = 'All supported formats ({})'.format(' '.join(all_supported_formats))
        name_filters: list = dialog.nameFilters()
        name_filters.append(all_supported_formats_filter)
        dialog.setNameFilters(name_filters)
        dialog.selectNameFilter(all_supported_formats_filter)

        dialog.setAcceptMode(accept_mode)
        if accept_mode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    @pyqtSlot()
    def __open(self) -> None:
        dialog = QFileDialog(self, 'Open File')
        self.__initialize_image_file_dialog(dialog, QFileDialog.AcceptOpen)
        if dialog.exec() == QFileDialog.Accepted:
            files = dialog.selectedFiles()
            if len(files) > 0:
                self.__load_image(files[0])

    def __load_image(self, file_name: str) -> None:
        reader = QImageReader(file_name)
        if reader.canRead():
            ImagePropertyWidget.import_path = QFileInfo(file_name).absolutePath()
            self.name = QFileInfo(file_name).fileName()
            self.image = reader.read()
            if self.image.isNull():
                print(reader.errorString())
        else:
            print('{}: image data is invalid'.format(file_name))
        self.image_changed.emit()

    def get_data(self) -> dict:
        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QIODevice.WriteOnly)
        if self.image.save(buffer, 'PNG'):
            buffer.close()
            return {'name': self.name, 'image': bytes(data.toBase64()).decode()}
        else:
            buffer.close()
            return {'name': '', 'image': ''}

    def set_data(self, data: dict) -> None:
        assert 'name' in data.keys()
        assert 'image' in data.keys()
        self.name = data['name']
        self.image = QImage.fromData(self.__str_to_q_byte_array(data['image']))

    @staticmethod
    def __str_to_q_byte_array(val: str) -> QByteArray:
        q_byte_array = QByteArray(val.encode())
        q_byte_array = QByteArray.fromBase64(q_byte_array)
        return q_byte_array
