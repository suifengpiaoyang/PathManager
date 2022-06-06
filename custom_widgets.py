from PySide2.QtCore import Signal
from PySide2.QtWidgets import QListWidget, QTextEdit


class CustomQListWidget(QListWidget):

    dropMessage = Signal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def mimeTypes(self):
        mimetypes = super().mimeTypes()
        mimetypes.append('text/uri-list')
        return mimetypes

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        self.dropMessage.emit(urls)


class CustomQTextEdit(QTextEdit):

    editingFinished = Signal()

    def focusInEvent(self, event):
        self._base_data = self.toPlainText()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if self.toPlainText() != self._base_data:
            self.editingFinished.emit()
        super().focusOutEvent(event)
