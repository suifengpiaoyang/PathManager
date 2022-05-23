import os
import re
import sys
import json
import hashlib
import webbrowser
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QAction,
                               QApplication,
                               QListWidget,
                               QMenu,
                               QMessageBox,
                               QTableWidgetItem)
from PySide2.QtCore import (QFile,
                            QIODevice,
                            Qt,
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


class MainWindow:

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ui_path = os.path.join(self.BASE_DIR, 'ui', 'main_window.ui')
        self.filename = 'data.json'
        self.filepath = os.path.join(self.BASE_DIR, self.filename)
        self.has_edited = False
        self.search_mode = False
        self.ui = self._load_ui_file(self.ui_path)
        icon_path = os.path.join(self.BASE_DIR, 'static', 'folder.ico')
        if os.path.exists(icon_path):
            self.ui.setWindowIcon(QIcon(icon_path))
        self.data_init()
        self.add_context_menu()
        self.handle_slots()
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

    def add_context_menu(self):
        self.ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(
            self._show_context_menu)

    def data_init(self):
        if not os.path.exists(self.filepath):
            self.data = JsonDb({'totalCount': 0, 'dataList': []})
        else:
            self.data = JsonDb.from_json(self.filepath)
            self.data['totalCount'] = len(self.data['dataList'])
            self._load_list_data()

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
        self.open_selected_file()

    def drop_add_item(self, urllist):
        self.has_edited = True
        for QUrl in urllist:
            path = QUrl.toLocalFile()
            row_count = self.ui.listWidget.count()
            basename = os.path.basename(path)
            datalist = {
                'name': basename,
                'path': path
            }
            self.data['dataList'].append(datalist)
            self.data['totalCount'] += 1
        self.fresh(reload=False, show_pop_box=False)
        self.ui.lineEditName.setText(self.data['dataList'][-1]['name'])
        self.ui.textEditPath.append(self.data['dataList'][-1]['path'])
        self.ui.listWidget.setCurrentRow(self.data['totalCount'] - 1)

    def fresh(self, reload=True, show_pop_box=True):
        if self.has_edited and show_pop_box:
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
        if self.search_mode:
            self.search_mode = False
            self.data = self.data_backup
            self._change_button_status(mode='enabled')
        self._load_list_data()

    def handle_slots(self):
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
        self.ui.freshButton.clicked.connect(lambda: self.fresh())
        self.ui.saveButton.clicked.connect(self.save)

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

    def open_console_window(self):
        directory = self._get_selected_directory()
        if directory:
            command = f'start "Console" /D "{directory}"'
            os.system(command)

    def open_path_through_sublime(self):
        SUBLIME_HOME = os.environ.get('SUBLIME_HOME')
        if SUBLIME_HOME is None:
            QMessageBox.about(self.ui,
                              '提示',
                              '请设置环境变量SUBLIME_HOME,值为sublime text软件路径！')
            return
        directory = self._get_selected_directory()
        if directory:
            os.chdir(SUBLIME_HOME)
            command = f'sublime.exe "{directory}"'
            os.system(command)
            os.chdir(self.BASE_DIR)
            # 为什么这种写法不起作用？明明在 Console 里面能正常执行的。
            # 是我考虑少了什么吗？
            # program = os.path.join(SUBLIME_HOME, 'sublime_text.exe')
            # command = f'"{program}" "{directory}"'
            # os.system(command)

    def open_selected_file(self):
        path = self._get_selected_path()
        if not path:
            return
        if path.startswith('http'):
            webbrowser.open(path)
        elif self._check_path_exists(path):
            os.startfile(path)

    def open_selected_directory(self):
        directory = self._get_selected_directory()
        if directory:
            os.startfile(directory)

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
        if not flag:
            self.fresh(reload=False)
            return
        if not self.search_mode:
            self.data_backup = self.data
        self.ui.listWidget.clear()
        search_result = JsonDb({'dataList': [], 'totalCount': 0})
        for index, item in enumerate(self.data_backup['dataList']):
            check_message = ''.join(item.values())
            if re.search(r'{}'.format(flag), check_message, re.I):
                search_result['dataList'].append(item)
        search_result['totalCount'] = len(search_result['dataList'])
        self._change_button_status(mode='disabled')
        self.data = search_result
        self.search_mode = True
        self._load_list_data()

    def _change_button_status(self, *, mode):
        assert mode in ('enabled', 'disabled')
        button_list = [self.ui.addButton, self.ui.deleteButton,
                       self.ui.moveDownButton, self.ui.moveFirstButton,
                       self.ui.moveUpButton, self.ui.moveLastButton,
                       self.ui.saveButton]
        if mode == 'disabled':
            for button in button_list:
                button.setEnabled(False)
        elif mode == 'enabled':
            for button in button_list:
                button.setEnabled(True)

    def _check_path_exists(self, path):
        if not os.path.exists(path):
            QMessageBox.critical(self.ui, '错误', f'找不到目标路径：{path}')
            return False
        else:
            return True

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

    def _get_selected_directory(self):
        path = self._get_selected_path()
        if not path:
            return
        if path.startswith('http'):
            return
        if not self._check_path_exists(path):
            return
        if os.path.isdir(path):
            directory = path
        elif os.path.isfile(path):
            directory = os.path.dirname(path)
        else:
            # not work for url
            return
        return directory

    def _get_selected_path(self):
        """Get selected item path.
        """
        current_row = self.ui.listWidget.currentRow()
        if current_row >= self.data['totalCount']:
            return
        _, path, _ = self._get_row_data(current_row)
        return path

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

    def _show_context_menu(self, position):
        """Show context menu and handle slots.
        """
        # 顺带触发了一次左键选中更新信息，这种处理方式有点偏门，
        # 有点取巧。
        # 本来想通过正常的右键 click 捕捉的，但是实际操作时发现
        # 不知道为何右键选中的下标一直不对，故而放弃了那种做法。
        self.left_click_event()
        open_selected_path = QAction('打开目标路径')
        open_console_window = QAction('打开console窗口')
        open_path_through_sublime = QAction('使用sublime text打开文件夹')
        open_selected_file = QAction('打开目标文件(同双击)')

        open_selected_path.triggered.connect(self.open_selected_directory)
        open_console_window.triggered.connect(self.open_console_window)
        open_path_through_sublime.triggered.connect(
            self.open_path_through_sublime)
        open_selected_file.triggered.connect(self.open_selected_file)

        menu = QMenu(self.ui.listWidget)
        menu.addAction(open_selected_path)
        menu.addAction(open_console_window)
        menu.addAction(open_path_through_sublime)
        menu.addSeparator()
        menu.addAction(open_selected_file)
        menu.exec_(self.ui.listWidget.mapToGlobal(position))

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
