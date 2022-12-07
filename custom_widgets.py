from PySide2.QtCore import Signal
from PySide2.QtWidgets import QListWidget, QTextEdit


class CustomQListWidget(QListWidget):

    dropMessage = Signal(list)
    dragDropSignal = Signal(int, int)

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
        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            self.dropMessage.emit(urls)
        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            drop_position = event.pos()
            drop_row = self.row(self.itemAt(drop_position))
            start_row = self.currentRow()
            self.dragDropSignal.emit(start_row, drop_row)
            # event.accept()
        else:
            event.ignore()


class CustomQTextEdit(QTextEdit):

    editingFinished = Signal()

    def focusInEvent(self, event):
        self._base_data = self.toPlainText()
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        if self.toPlainText() != self._base_data:
            self.editingFinished.emit()
        super().focusOutEvent(event)
