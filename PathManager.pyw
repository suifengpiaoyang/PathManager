import os
import re
import sys
import hashlib
import subprocess
import webbrowser
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QAction,
                               QApplication,
                               QFileDialog,
                               QWidget,
                               QListWidget,
                               QMainWindow,
                               QMenu,
                               QMessageBox,
                               QTableWidgetItem)
from PySide2.QtCore import Qt, Signal

from ui.main_window import Ui_MainWindow
from ui.config_form import Ui_ConfigForm
from data_storage import ConfigStorage, DataStorage


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILEPATH = os.path.join(BASE_DIR, 'data.json')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')


class ConfigForm(QWidget):

    update_config = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_ConfigForm()
        self.ui.setupUi(self)

        self.has_edited = False

        # set gui icon
        icon_path = os.path.join(BASE_DIR, 'static', 'folder.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # load config file
        self.config = ConfigStorage.from_json(CONFIG_FILE)
        sublime_text_path = self.config.get('sublime_text_path')
        if sublime_text_path:
            self.ui.lineEdit.setText(sublime_text_path)

        # connect slots
        self.ui.pushButton.clicked.connect(self.choose_sublime_text)
        self.ui.pushButtonConfirm.clicked.connect(self.confirm)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)

    def choose_sublime_text(self):
        path, _ = QFileDialog.getOpenFileName(self,
                                              '选择Sublime Text.exe程序',
                                              None,
                                              'Program (*.exe)')
        if not path:
            return
        self.ui.lineEdit.setText(path)
        self.config['sublime_text_path'] = path
        self.has_edited = True

    def cancel(self):
        del self.config
        self.has_edited = False
        self.close()

    def confirm(self):
        self.config.save(CONFIG_FILE)
        self.has_edited = False
        self.update_config.emit()
        self.close()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 有关菜单栏 "关于" 的功能还没想好，暂时
        # 将其隐藏
        self.ui.menuAbout.setTitle('')

        self.BASE_WINDOW_TITLE = self.windowTitle()

        # set gui icon
        icon_path = os.path.join(BASE_DIR, 'static', 'folder.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # set base data
        self.data = DataStorage.from_json(FILEPATH)
        self.config = ConfigStorage.from_json(CONFIG_FILE)
        self._load_list_data()

        # set gui size
        width = self.config.get('width')
        height = self.config.get('height')
        if width and height:
            self.resize(width, height)

        self.has_edited = False
        self.search_mode = False

        self.add_context_menu()
        self.handle_slots()

    def add_empty_item(self):

        row_count = self.ui.listWidget.count()
        self.ui.listWidget.addItem('未命名')
        self._clear_input_widgets()
        self.data.add_empty_item()
        self.set_has_edited(True)
        self.ui.lineEditName.setFocus()
        self.ui.listWidget.setCurrentRow(row_count)

    def add_context_menu(self):
        self.ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(
            self._show_context_menu)

    def closeEvent(self, event):
        # save the gui size when the gui closed
        self.config['width'] = self.width()
        self.config['height'] = self.height()
        self.config.save(CONFIG_FILE)

        if self.has_edited:
            flag = QMessageBox.warning(self,
                                       '警告',
                                       '当前数据善未保存，是否要保存数据？',
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if flag == QMessageBox.StandardButton.Yes:
                # 保存关闭
                # save data and close window
                self.save(flash_flag=False)
                # self.set_has_edited(False)
                event.accept()
            elif flag == QMessageBox.StandardButton.No:
                # 不保存数据，强制关闭
                # not save data and close window
                event.accept()
            elif flag == QMessageBox.StandardButton.Cancel:
                # 取消关闭操作
                event.ignore()
        else:
            event.accept()

    def delete_item(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0:
            return
        self.set_has_edited(True)
        self.ui.listWidget.takeItem(current_row)
        self.data.delete_item(current_row)
        self._clear_input_widgets()
        current_row = self.ui.listWidget.currentRow()
        self._show_row_data(current_row)

    def double_click_event(self):
        self.open_selected_file()

    def handle_drop_items(self, urlist):
        if self.search_mode:
            QMessageBox.about(self, '提示', '搜索状态下不支持拖动。')
            return
        self.set_has_edited(True)
        self.data.handle_drop_items(urlist)
        self.fresh(reload=False, show_pop_box=False)
        last_item = self.data.get_data_from_index(-1)
        self.ui.lineEditName.setText(last_item['name'])
        self.ui.textEditPath.append(last_item['path'])
        self.ui.listWidget.setCurrentRow(self.data.total_count - 1)

    def finished_edit_name(self):
        # 目前的搜索模式不支持修改数据
        # 因为里面的数据映射逻辑善未完成
        if self.search_mode:
            return
        current_row = self.ui.listWidget.currentRow()
        if current_row == -1:
            return
        list_counts = self.ui.listWidget.count()
        name = self.ui.lineEditName.text()
        self.data['dataList'][current_row]['name'] = name
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(current_row)
        self.set_has_edited(True)

    def finished_edit_path(self):
        if self.search_mode:
            return
        current_row = self.ui.listWidget.currentRow()
        if current_row == -1:
            return
        list_counts = self.ui.listWidget.count()
        path = self.ui.textEditPath.toPlainText()
        self.data['dataList'][current_row]['path'] = path
        self.set_has_edited(True)

    def finished_edit_comment(self):
        if self.search_mode:
            return
        current_row = self.ui.listWidget.currentRow()
        if current_row == -1:
            return
        list_counts = self.ui.listWidget.count()
        comment = self.ui.textEditComment.toPlainText()
        self.data['dataList'][current_row]['comment'] = comment
        self.set_has_edited(True)

    def fresh(self, reload=True, show_pop_box=True):
        if self.has_edited and show_pop_box:
            flag = QMessageBox.question(self,
                                        '警告',
                                        '当前数据善未保存，是否确定要刷新？')
            if flag == QMessageBox.Yes:
                self.set_has_edited(False)
            else:
                return
        self._clear_all_widgets()
        self.ui.lineEditSearch.setFocus()
        if reload:
            self.data = DataStorage.from_json(FILEPATH)
        if self.search_mode:
            self.search_mode = False
            self.data = self.data_backup
            self._change_button_status(mode='enabled')
        self._load_list_data()

    def handle_slots(self):
        self.ui.addButton.clicked.connect(self.add_empty_item)
        self.ui.deleteButton.clicked.connect(self.delete_item)
        self.ui.listWidget.clicked.connect(self.left_click_event)
        self.ui.listWidget.itemDoubleClicked.connect(self.double_click_event)
        self.ui.listWidget.dropMessage.connect(self.handle_drop_items)
        self.ui.listWidget.dragDropSignal.connect(self.move_row)
        self.ui.lineEditName.editingFinished.connect(self.finished_edit_name)
        self.ui.textEditPath.editingFinished.connect(self.finished_edit_path)
        self.ui.textEditComment.editingFinished.connect(
            self.finished_edit_comment)
        self.ui.lineEditSearch.returnPressed.connect(self.search)
        self.ui.moveFirstButton.clicked.connect(self.move_first)
        self.ui.moveLastButton.clicked.connect(self.move_last)
        self.ui.freshButton.clicked.connect(lambda: self.fresh())
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.configAction.triggered.connect(self.open_config_form)

    def left_click_event(self):
        current_row = self.ui.listWidget.currentRow()
        self._show_row_data(current_row)

    def move_first(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0 or current_row >= self.data.total_count:
            return
        self.data.move_first(current_row)
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(0)
        self.set_has_edited(True)

    def move_last(self):
        current_row = self.ui.listWidget.currentRow()
        if current_row < 0 or current_row >= self.data.total_count:
            return
        self.data.move_last(current_row)
        self.ui.listWidget.clear()
        self._load_list_data()
        self.ui.listWidget.setCurrentRow(self.data.total_count - 1)
        self.set_has_edited(True)

    def move_row(self, startrow, endrow):
        if self.search_mode:
            QMessageBox.about(self, '提示', '搜索状态下不支持拖动。')
            return
        self.set_has_edited(True)
        current_data = self.data.get_data_from_index(startrow)
        self.data.move_row(startrow, endrow)
        self.fresh(reload=False, show_pop_box=False)
        self.ui.lineEditName.setText(current_data['name'])
        self.ui.textEditPath.append(current_data['path'])
        self.ui.listWidget.setCurrentRow(endrow)

    def open_config_form(self):
        self.config_form = ConfigForm()
        self.config_form.update_config.connect(self.update_config)
        self.config_form.show()

    def open_console_window(self):
        directory = self._get_selected_directory()
        if directory:
            command = f'start /D "{directory}"'
            os.system(command)

    def open_with_sublime(self, flag):
        assert flag in ('file', 'path'), 'flag 必须为 file 或者 path'
        if flag not in ('file', 'path'):
            return
        sublime_text_path = self.config.get('sublime_text_path')
        if sublime_text_path is None:
            QMessageBox.about(self,
                              '提示',
                              '请先在[首选项]里面配置sublime text路径。')
            return
        if not os.path.exists(sublime_text_path):
            QMessageBox.critical(self, '错误', f'[{sublime_text_path}]不存在！')
            return
        SUBLIME_HOME = os.path.dirname(sublime_text_path)
        program_name = os.path.basename(sublime_text_path)
        path = self._get_selected_path()
        if not path:
            QMessageBox.critical(self, '错误', '路径不能为空值！')
            return
        if not self._check_path_exists(path):
            return
        if flag == 'file':
            if os.path.isfile(path):
                target = path
            else:
                QMessageBox.critical(self, '错误', '目标是一个文件夹！')
                return
        elif flag == 'path':
            target = self._get_selected_directory()
            if not target:
                return
        subprocess.Popen([sublime_text_path, target])

    def open_selected_file(self):
        path = self._get_selected_path()
        if not path:
            return
        if path.startswith('http'):
            webbrowser.open(path)
        elif path.startswith(('ftp', r'\\')):
            subprocess.Popen(['explorer.exe', path])
        elif self._check_path_exists(path):
            # 运行时切换到目标路径下。
            # 曾经出现过目标程序读取配置文件时使用 config.json
            # 的配置文件，但是却错误地读取到该程序下的配置文件导致
            # 程序崩溃。添加部分代码来规避这种情况的出现。
            directory_path = os.path.dirname(path)
            os.chdir(directory_path)
            os.startfile(path)
            os.chdir(BASE_DIR)

    def open_selected_directory(self):
        """
        可通过 Windows 特有的方式，除了打开文件夹之外，
        直接定位到目标文件。
        """
        path = self._get_selected_path()
        if not path:
            return
        if os.path.isdir(path):
            os.startfile(path)
        elif os.path.isfile(path):
            path = path.replace('/', '\\')
            directory = os.path.dirname(path)
            subprocess.Popen(rf'explorer /select,"{path}"')
        else:
            QMessageBox.about(self,
                              '提示',
                              '该路径不是文件或者文件夹，无法使用此方式打开。')

    def save(self, flash_flag=True):
        """
        保存是对内存中的 self.data 进行保存。
        """
        self.data.save(FILEPATH)
        self.set_has_edited(False)
        QMessageBox.about(self, '提示', '\n   保存成功\t\n')
        # 保存成功后需要重载
        if flash_flag:
            self.fresh()

    def search(self):
        flag = self.ui.lineEditSearch.text()
        if not flag:
            self.fresh(reload=False)
            return
        if not self.search_mode:
            self.data_backup = self.data
        self.ui.listWidget.clear()
        search_result = DataStorage({'dataList': [], 'totalCount': 0})
        for index, item in enumerate(self.data_backup['dataList']):
            check_message = ''.join(item.values())
            if re.search(r'{}'.format(flag), check_message, re.I):
                search_result['dataList'].append(item)
        search_result['totalCount'] = len(search_result['dataList'])
        self._change_button_status(mode='disabled')
        self.data = search_result
        self.search_mode = True
        self._load_list_data()

    def set_has_edited(self, state=True):
        self.has_edited = state
        if state:
            self.setWindowTitle(self.BASE_WINDOW_TITLE + ' *')
        else:
            self.setWindowTitle(self.BASE_WINDOW_TITLE)

    def update_config(self):
        self.config = ConfigStorage.from_json(CONFIG_FILE)
        self.config.pretty_print()

    def _change_button_status(self, *, mode):
        assert mode in ('enabled', 'disabled')
        button_list = [self.ui.addButton, self.ui.deleteButton,
                       self.ui.moveFirstButton, self.ui.moveLastButton,
                       self.ui.saveButton]
        if mode == 'disabled':
            for button in button_list:
                button.setEnabled(False)
        elif mode == 'enabled':
            for button in button_list:
                button.setEnabled(True)

    def _check_path_exists(self, path):
        if not os.path.exists(path):
            QMessageBox.critical(self, '错误', f'找不到目标路径：{path}')
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
        if row >= 0 and row < self.data.total_count:
            current_data = self.data.get_data_from_index(row)
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
        if path.startswith(('http', 'ftp')):
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
        while row < self.data.total_count:
            for item in self.data['dataList']:
                self.ui.listWidget.addItem(item['name'])
                row += 1

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
        open_file_with_sublime = QAction('使用sublime text打开文件')
        open_path_with_sublime = QAction('使用sublime text打开文件夹')
        open_selected_file = QAction('打开目标文件(同双击)')

        open_selected_path.triggered.connect(self.open_selected_directory)
        open_console_window.triggered.connect(self.open_console_window)
        open_file_with_sublime.triggered.connect(
            lambda: self.open_with_sublime(flag='file'))
        open_path_with_sublime.triggered.connect(
            lambda: self.open_with_sublime(flag='path'))
        open_selected_file.triggered.connect(self.open_selected_file)

        menu = QMenu(self.ui.listWidget)
        menu.addAction(open_selected_path)
        menu.addAction(open_console_window)
        menu.addSeparator()
        menu.addAction(open_file_with_sublime)
        menu.addAction(open_path_with_sublime)
        menu.addSeparator()
        menu.addAction(open_selected_file)
        menu.exec_(self.ui.listWidget.mapToGlobal(position))

    def _show_row_data(self, row):
        """Show one row data to input widgets.
        """
        self._clear_input_widgets()
        name, path, comment = self._get_row_data(row)
        self.ui.lineEditName.setText(name)
        self.ui.textEditPath.insertPlainText(path)
        self.ui.textEditComment.insertPlainText(comment)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
