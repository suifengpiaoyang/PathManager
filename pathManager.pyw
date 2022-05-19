import os
import sys
import json
import hashlib
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QApplication,
                               QListWidget,
                               QTableWidgetItem,
                               QMessageBox)
from PySide2.QtCore import (QFile,
                            QIODevice,
                            Signal)


class JsonDb(dict):

    @classmethod
    def from_json(cls, file):
        with open(file, 'r', encoding='utf-8')as fl:
            data = json.load(fl)
        return cls(data)

    def pretty_print(self):
        print(json.dumps(self, indent=4, ensure_ascii=False))

    def save(self, file):
        with open(file, 'w', encoding='utf-8')as fl:
            json.dump(self, fl, indent=4, ensure_ascii=False)


class CustomQListWidget(QListWidget):

    dropMessage = Signal(str)

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
        self.dropMessage.emit(urls[0].toLocalFile())
        # self.addItem(urls[0].toLocalFile())


class MainWindow:

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ui_path = os.path.join(self.BASE_DIR, 'ui', 'main_window.ui')
        self.filename = 'data.json'
        self.filepath = os.path.join(self.BASE_DIR, self.filename)
        self.has_edited = False
        self.ui = self._load_ui_file(self.ui_path)
        self.ui.addButton.clicked.connect(self.add_item)
        self.ui.deleteButton.clicked.connect(self.delete_item)
        self.ui.listWidget.clicked.connect(self.left_click_event)
        self.ui.listWidget.itemDoubleClicked.connect(self.double_click_event)
        self.ui.listWidget.dropMessage.connect(self.drop_add_item)
        self.ui.lineEditSearch.returnPressed.connect(self.search)
        self.ui.moveFirstButton.clicked.connect(self.move_first)
        self.ui.moveLastButton.clicked.connect(self.move_last)
        self.ui.moveUpButton.clicked.connect(self.move_up)
        self.ui.moveDownButton.clicked.connect(self.move_down)
        self.ui.freshButton.clicked.connect(lambda:self.fresh())
        self.ui.saveButton.clicked.connect(self.save)
        self._data_init()
        self.current_row = self.ui.listWidget.currentRow()

    def add_item(self):

        self.has_edited = True
        # 点击两次添加就将前面一次存进内存
        row_count = self.ui.listWidget.count()

        if row_count - self.data['totalCount'] == 1:
            name, path, comment = self._get_input_datas()
            if not name:
                QMessageBox.critical(self.ui, '错误', '名称部分不能为空！')
                self.ui.lineEditName.setFocus()
                return
            previous_data = {
                'name': name,
                'path': path,
                'comment': comment
            }
            self.data['dataList'].append(previous_data)
            self.ui.listWidget.insertItem(row_count - 1, name)
            self._clear_input_widgets()
            self.data['totalCount'] += 1
            self.has_edited = True
        else:
            self.ui.listWidget.addItem('未命名')
            self._clear_input_widgets()
        self.ui.lineEditName.setFocus()
        self.ui.listWidget.setCurrentRow(row_count)

    def delete_item(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0:
            return
        self.has_edited = True
        self.ui.listWidget.takeItem(current_row)
        self.data['dataList'].pop(current_row)
        self.data['totalCount'] -= 1
        # totalCount 是否还需要，这个函数里其实是不需要
        # 这个参数的。
        self._clear_input_widgets()
        current_row = self.ui.listWidget.currentRow()
        self._show_row_data(current_row)

    def double_click_event(self):
        current_index = self.ui.listWidget.currentRow()
        if current_index >= self.data['totalCount']:
            return
        current_data = self.data['dataList'][current_index]
        path = current_data.get('path')
        if not path:
            return
        try:
            os.startfile(path)
        except FileNotFoundError:
            QMessageBox.critical(self.ui, '错误', f'找不到目标路径：{path}')

    def drop_add_item(self, message):
        self.has_edited = True
        row_count = self.ui.listWidget.count()
        abs_path = message
        basename = os.path.basename(abs_path)
        datalist = {
            'name': basename,
            'path': abs_path
        }
        self.data['dataList'].append(datalist)
        self.data['totalCount'] += 1
        self._clear_input_widgets()
        self.ui.listWidget.addItem(basename)
        self.ui.lineEditName.setText(basename)
        self.ui.textEditPath.append(abs_path)
        self.ui.listWidget.setCurrentRow(row_count)

    def fresh(self, reload=True):
        if self.has_edited:
            flag = QMessageBox.question(self.ui,
                                        '警告',
                                        '当前数据善未保存，是否确定要刷新？')
            if flag == QMessageBox.Yes:
                self.has_edited = False
            else:
                return
        self._clear_all_widgets()
        self.ui.lineEditSearch.setFocus()
        if reload:
            self.data = JsonDb.from_json(self.filepath)
        self._load_list_data()

    def left_click_event(self):
        current_row = self.ui.listWidget.currentRow()

        # 检测有没有数据发生更改

        # 当前数据显示
        self._show_row_data(current_row)

    def move_first(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0 or current_row >= self.data['totalCount']:
            return
        data = self.data['dataList'].pop(current_row)
        self.data['dataList'].insert(0, data)
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(0)
        self.has_edited = True

    def move_up(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row <= 0 or current_row >= self.data['totalCount']:
            return
        data = self.data['dataList'].pop(current_row)
        self.data['dataList'].insert(current_row - 1, data)
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(current_row - 1)
        self.has_edited = True

    def move_down(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0 or current_row >= self.data['totalCount']:
            return
        if current_row == self.data['totalCount'] - 1:
            return
        data = self.data['dataList'].pop(current_row)
        self.data['dataList'].insert(current_row + 1, data)
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(current_row + 1)
        self.has_edited = True

    def move_last(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0 or current_row >= self.data['totalCount']:
            return
        data = self.data['dataList'].pop(current_row)
        self.data['dataList'].append(data)
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(self.data['totalCount'] - 1)
        self.has_edited = True

    def save(self):
        """
        保存是对内存中的 self.data 进行保存。
        """

        # 点击添加按钮的最后一项
        # current_row 的下标是从0开始的
        current_row = self.ui.listWidget.currentRow()
        # 处理添加最后一行的部分
        if self.data['totalCount'] == current_row:
            name, path, comment = self._get_input_datas()
            if name:
                data = {
                    'name': name,
                    'path': path,
                    'comment': comment
                }
                self.data['dataList'].append(data)
                self.data['totalCount'] += 1
                self.has_edited = True
        # 编辑过的保存
        # 先只考虑最简单的一种情况，只保存当前选择的那一行
        # 将一下这种情况定义为编辑过
        if current_row < self.data['totalCount'] and not self.has_edited:
            name, path, comment = self._get_input_datas()
            if name:
                self.data['dataList'][current_row]['name'] = name
                self.data['dataList'][current_row]['path'] = path
                self.data['dataList'][current_row]['comment'] = comment
            else:
                QMessageBox.warning(self.ui, '警告', '名称部分不能为空！')

        # 删除的保存不用特别处理
        self.data.save(self.filepath)
        self.has_edited = False
        QMessageBox.about(self.ui, '提示', '\n   保存成功\t\n')
        # 保存成功后需要重载
        self.fresh()

    def search(self):
        flag = self.ui.lineEditSearch.text()
        # self.ui.listWidget.clear()

    def _clear_all_widgets(self):
        self._clear_input_widgets()
        self.ui.lineEditSearch.clear()
        self.ui.listWidget.clear()

    def _clear_input_widgets(self):
        """Clear all input widgets.
        """
        self.ui.lineEditName.clear()
        self.ui.textEditPath.clear()
        self.ui.textEditComment.clear()

    def _data_init(self):
        if not os.path.exists(self.filepath):
            self.data = JsonDb({'totalCount': 0, 'dataList': []})
        else:
            self.data = JsonDb.from_json(self.filepath)
            self.data['totalCount'] = len(self.data['dataList'])
            self._load_list_data()

    def _get_input_datas(self):
        name = self.ui.lineEditName.text()
        path = self.ui.textEditPath.toPlainText()
        comment = self.ui.textEditComment.toPlainText()
        return (name, path, comment)

    def _get_row_data(self, row):
        """Get one row data from self.data.
        """
        if row >= 0 and row < self.data['totalCount']:
            current_data = self.data['dataList'][row]
        else:
            current_data = {}
        name = current_data.get('name')
        path = current_data.get('path')
        comment = current_data.get('comment')
        return (name, path, comment)

    def _load_list_data(self):
        row = 0
        while row < self.data['totalCount']:
            for item in self.data['dataList']:
                self.ui.listWidget.addItem(item['name'])
                row += 1

    def _load_ui_file(self, ui_path):
        """Load ui file return a pyside object.
        """
        ui_file = QFile(ui_path)
        loader = QUiLoader()
        loader.registerCustomWidget(CustomQListWidget)
        window = loader.load(ui_file)
        ui_file.close()
        return window

    def _show_row_data(self, row):
        """Show one row data on input widgets.
        """
        self._clear_input_widgets()
        name, path, comment = self._get_row_data(row)
        self.ui.lineEditName.setText(name)
        self.ui.textEditPath.insertPlainText(path)
        self.ui.textEditComment.insertPlainText(comment)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec_())
