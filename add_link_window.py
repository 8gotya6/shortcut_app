from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

from Ui_add_link_window import Ui_add_link_window

class add_link_window(QMainWindow, Ui_add_link_window):
    sure_add_signal = pyqtSignal(dict)
    not_add_signal = pyqtSignal()
    def __init__(self, tab_names, link_path=''):
        super(add_link_window, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.Tool)
        self.setAcceptDrops(True)

        self.setAttribute(Qt.WA_TranslucentBackground)
        radius = 30 // 2 - 10
        self.setStyleSheet(
            f"""
            #centralwidget {"{"}
            background-color: rgb(255, 255, 255);
            border-top-left-radius:{radius}px;
            border-bottom-left-radius:{radius}px;
            border-top-right-radius:{radius}px;
            border-bottom-right-radius:{radius}px;
            {"}"}"""
        )

        self.link_path.setText(link_path)
        self.page_combobox.addItems(tab_names)

        self.select_path_btn.clicked['bool'].connect(self.select_path)
        self.sure_add.clicked['bool'].connect(self.sure_add_event)
        self.cancel_add.clicked['bool'].connect(self.cancel_add_event)


    def sure_add_event(self):
        add_link_info = {
            'link_name': self.link_name.text(),
            'link_page': self.page_combobox.currentText(),
            'link_path': self.link_path.text(),
            'is_add_favorite': self.is_add_favorite.isChecked(),
            'is_auto_save': self.autosave_after_sureadd.isChecked()
        }
        empty_value = []
        for k, v in add_link_info.items():
            if v == '':
                empty_value.append(k)
        if len(empty_value) > 0:
            msg = QMessageBox.warning(self, 'Error', f'欄位不得為空值:\n{",".join(empty_value)}')
            return
        self.sure_add_signal.emit(add_link_info)
        if self.hide_after_sureadd.isChecked():
            self.not_add_signal.emit()


    def cancel_add_event(self):
        self.not_add_signal.emit()


    def select_path(self):
        fd = QFileDialog.getOpenFileName(self, '請選擇檔案', '', 'All (*.*)')
        if len(fd[0]) > 0:
            self.link_path.setText(fd[0])
    