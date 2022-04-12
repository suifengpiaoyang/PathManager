import os
import sys
import json
import hashlib
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QApplication,
                               QTableWidgetItem,
                               QMessageBox)
from PySide2.QtCore import QFile, QIODevice


def md5text(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()


class JsonDb(dict):

    @classmethod
    def from_json(cls, file):
        with open(file, 'r', encoding='utf-8')as fl:
            data = json.load(fl)
        return cls(data)

    def save(self, file):
        with open(file, 'w', encoding='utf-8')as fl:
            json.dump(self, fl, indent=4, ensure_ascii=False)


class MainWindow:

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ui_path = os.path.join(self.BASE_DIR, 'ui', 'main_window.ui')
        self.filename = 'data.json'
        self.filepath = os.path.join(self.BASE_DIR, self.filename)
        self.ui = self._load_ui_file(self.ui_path)
        self.ui.addButton.clicked.connect(self.add_item)
        self.ui.deleteButton.clicked.connect(self.delete_item)
        self.ui.listWidget.clicked.connect(self.left_click_event)
        self.ui.listWidget.itemDoubleClicked.connect(self.double_click_event)
        self.ui.lineEditSearch.returnPressed.connect(self.search)
        self.ui.saveButton.clicked.connect(self.save)
        if not os.path.exists(self.filepath):
            self.data = {}
        else:
            self.data = JsonDb.from_json(self.filepath)
            self.widgets_init()
        self.need_save = False
        self.current_row = self.ui.listWidget.currentRow()

    def widgets_init(self):
        row = 0
        while row < self.data['totalCount']:
            for item in self.data['dataList']:
                self.ui.listWidget.addItem(item['name'])
                row += 1

    def add_item(self):
        """功能善未完成。
        add item 有很多需要考虑的情况。
        """
        row_count = self.ui.listWidget.count()
        self.ui.listWidget.addItem('未命名')
        self.ui.lineEditName.setFocus()
        self.ui.listWidget.setCurrentRow(row_count)
        self.ui.lineEditName.clear()
        self.ui.textEditPath.clear()
        self.ui.textEditComment.clear()

    def delete_item(self):
        row_index = self.ui.listWidget.currentRow()
        self.ui.listWidget.takeItem(row_index)
        self.data['dataList'].pop(row_index)
        self.data['totalCount'] = len(self.data['dataList'])

    def double_click_event(self):
        current_index = self.ui.listWidget.currentRow()
        current_data = self.data['dataList'][current_index]
        path = current_data.get('path')
        try:
            os.startfile(path)
        except FileNotFoundError:
            QMessageBox.critical(self.ui, '错误', f'找不到目标路径：{path}')

    def save(self):
        """
        保存是对内存中的 self.data 进行保存。
        """

        # 编辑过的保存
        # 第一种情况，保存当前选中的选项信息
        row_index = self.ui.listWidget.currentRow()
        name = self.ui.lineEditName.text()
        path = self.ui.textEditPath.toPlainText()
        comment = self.ui.textEditComment.toPlainText()
        self.data['dataList'][row_index]['name'] = name
        self.data['dataList'][row_index]['path'] = path
        self.data['dataList'][row_index]['comment'] = comment
        # from pprint import pprint
        # pprint(self.data)
        # 第二种情况，修改很多项信息
        # 需要捕捉按键在不同项之间的移动

        # 删除的保存不用特别处理
        self.data.save(self.filepath)
        QMessageBox.about(self.ui, '提示', '\n   保存成功\t\n')
        # 保存成功后需要重载

    def search(self):
        flag = self.ui.lineEditSearch.text()
        # self.ui.listWidget.clear()

    def left_click_event(self):

        current_index = self.ui.listWidget.currentRow()

        # 检测有没有数据发生更改


        # 当前数据显示
        if current_index >= self.data['totalCount']:
            current_data = {}
        else:
            current_data = self.data['dataList'][current_index]
        name = current_data.get('name')
        path = current_data.get('path')
        comment = current_data.get('comment')
        self.ui.lineEditName.setText(name)
        self.ui.textEditPath.clear()
        self.ui.textEditPath.insertPlainText(path)
        self.ui.textEditComment.clear()
        self.ui.textEditComment.insertPlainText(comment)

    def _load_ui_file(self, ui_path):
        """Load ui file return a pyside object.
        """
        ui_file = QFile(ui_path)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        return window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec_())
