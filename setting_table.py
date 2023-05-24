from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

from Ui_setting_table import Ui_App_Setting_Window


class App_Setting_Window(QMainWindow, Ui_App_Setting_Window):
    save_and_move_signal = pyqtSignal(dict)
    save_signal = pyqtSignal()
    update_is_auto_hide_signal = pyqtSignal(bool)
    def __init__(self, icon_path, pos_x, pos_y, main_gui):
        super(App_Setting_Window, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.Tool)
        self.setWindowIcon(QIcon(icon_path))
        self.setAcceptDrops(True)

        

        self.setAttribute(Qt.WA_TranslucentBackground)
        radius = 30 // 2 - 10
        self.setStyleSheet(
            f"""
            #centralwidget {"{"}
            background-color: rgb(56, 76, 101);
            border-top-left-radius:{radius}px;
            border-bottom-left-radius:{radius}px;
            border-top-right-radius:{radius}px;
            border-bottom-right-radius:{radius}px;
            {"}"}"""
        )

        if pos_x-self.width()//2 > 0 and pos_x+self.width() > (main_gui.x() + main_gui.width()):
            qpoint_x = main_gui.x() + main_gui.width() - self.width()
            qpoint_x = qpoint_x if qpoint_x >= 0 else 0
        elif pos_x-self.width()//2 < 0:
            qpoint_x = 0
        else:
            qpoint_x = pos_x-self.width()//2
        self.move(QPoint(qpoint_x, pos_y))

        self.config = self.load_config()
        self.import_config_to_UI()

        self.setting_link_path_btn.clicked['bool'].connect(self.set_linksetting_path)
        self.save_btn.clicked['bool'].connect(self.save_config)
        self.reset_btn.clicked['bool'].connect(self.import_config_to_UI)

        self.main_icon_select_btn.clicked['bool'].connect(lambda: self.set_icon_pic(self.main_icon_label, self.main_icon_path))
        self.favorite_icon_select_btn.clicked['bool'].connect(lambda: self.set_icon_pic(self.favorite_icon_label, self.favorite_icon_path))
        self.link_icon_select_btn.clicked['bool'].connect(lambda: self.set_icon_pic(self.link_icon_label, self.link_icon_path))
        self.setting_icon_select_btn.clicked['bool'].connect(lambda: self.set_icon_pic(self.setting_icon_label, self.setting_icon_path))


    def move_to(self, offset_dict):
        current_pos = self.pos()
        new_pos = current_pos + QPoint(offset_dict['offset_x'], offset_dict['offset_y'])
        self.move(new_pos)


    @staticmethod
    def load_config():
        config_content = {}
        for v in open('config.ini', 'r').read().split('\n'):
            try:
                k, v = v.split('=')
            except:
                continue

            config_content[k] = int(v) if v.isdigit() else v

        return config_content


    def save_config(self):
        self.config['setting_path'] = self.link_path.text()

        main_size_diff = self.main_icon_size.value() - self.config['main_icon_size']
        self.config['main_icon_size'] = self.main_icon_size.value()
        sub_size_diff = self.sub_icon_size.value() - self.config['sub_icon_size']
        self.config['sub_icon_size'] = self.sub_icon_size.value()

        offset_x = self.pos_x.value() - self.config['pos_x']
        self.config['pos_x'] = self.pos_x.value()
        offset_y = self.pos_y.value() - self.config['pos_y']
        self.config['pos_y'] = self.pos_y.value()
        offset_main_distance = self.config['main_distance'] - self.main_distance.value()
        self.config['main_distance'] = self.main_distance.value()
        offset_sub_distance = self.config['sub_distance'] - self.sub_distance.value()
        self.config['sub_distance'] = self.sub_distance.value()

        self.config['main_ani_period'] = self.main_ani_period.value()
        self.config['sub_ani_period'] = self.sub_ani_period.value()
        self.config['is_auto_hide'] = 1 if self.is_auto_hide.isChecked() else 0
        self.config['isopenlink_byclicktable'] = 1 if self.isopenlink_byclicktable.isChecked() else 0

        is_icon_change = False
        for lineedit, k in zip(
            [self.main_icon_path, self.favorite_icon_path, self.link_icon_path, self.setting_icon_path],
            ['main_icon_path', 'favorite_icon_path', 'link_icon_path', 'setting_icon_path']):

            if self.config[k] != lineedit.text() and not is_icon_change:
                is_icon_change = True
            
            self.config[k] = lineedit.text()

        # self.config['main_icon_path'] = self.main_icon_path.text()
        # self.config['favorite_icon_path'] = self.favorite_icon_path.text()
        # self.config['link_icon_path'] = self.link_icon_path.text()
        # self.config['setting_icon_path'] = self.setting_icon_path.text()


        with open('config.ini', 'w') as f:
            text = ''
            for k, v in self.config.items():
                text += f'{k}={v}\n'

            f.write(text)

        if any(v != 0 for v in [main_size_diff, sub_size_diff, offset_x, offset_y, offset_main_distance, offset_sub_distance]) or is_icon_change:
            self.save_and_move_signal.emit({'offset_x': offset_x, 'offset_y': offset_y, 'main_icon_size': self.config['main_icon_size']})
        else:
            self.save_signal.emit()


    def import_config_to_UI(self):
        self.link_path.setText(self.config['setting_path'])
        self.main_icon_size.setValue(int(self.config['main_icon_size']))
        self.sub_icon_size.setValue(int(self.config['sub_icon_size']))
        self.pos_x.setValue(int(self.config['pos_x']))
        self.pos_y.setValue(int(self.config['pos_y']))
        self.main_distance.setValue(int(self.config['main_distance']))
        self.sub_distance.setValue(int(self.config['sub_distance']))
        self.main_ani_period.setValue(int(self.config['main_ani_period']))
        self.sub_ani_period.setValue(int(self.config['sub_ani_period']))
        self.is_auto_hide.setChecked(True if self.config['is_auto_hide'] == 1 else False)
        self.isopenlink_byclicktable.setChecked(True if self.config['isopenlink_byclicktable'] == 1 else False)

        for lb, lineedit, k in zip(
            [self.main_icon_label, self.favorite_icon_label, self.link_icon_label, self.setting_icon_label],
            [self.main_icon_path, self.favorite_icon_path, self.link_icon_path, self.setting_icon_path],
            ['main_icon_path', 'favorite_icon_path', 'link_icon_path', 'setting_icon_path']
            ):
            lb.setPixmap(QPixmap(self.config[k]).scaled(30, 30))
            lineedit.setText(self.config[k])


    def set_linksetting_path(self):
        self.update_is_auto_hide_signal.emit(False)
        fd = QFileDialog.getOpenFileName(self, '請選擇檔案', '', 'Excel File (*.xlsx)')
        if len(fd[0]) > 0:
            self.link_path.setText(fd[0])

        self.update_is_auto_hide_signal.emit(True)


    def set_icon_pic(self, lb, lineedit):
        self.update_is_auto_hide_signal.emit(False)
        fd = QFileDialog.getOpenFileName(self, '請選擇icon檔案', '', 'PNG (*.png);;JPEG (*.jpg);;All (*.*)')
        if len(fd[0]) > 0:
            lb.setPixmap(QPixmap(fd[0]).scaled(30, 30))
            lineedit.setText(fd[0])

        self.update_is_auto_hide_signal.emit(True)