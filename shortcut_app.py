import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QPoint, pyqtSlot, QParallelAnimationGroup, \
    QPropertyAnimation, QEasingCurve, QRect, QSize

from set_icon import button_icon
from hyperlink_table import hyperlink_table_window
from favorite_table import favorite_table_window
from setting_table import App_Setting_Window


class main():
    def __init__(self):
        app = QApplication([])
        app.setStyle('Fusion')
        app.setQuitOnLastWindowClosed(False)
        app.focusChanged.connect(self.on_focus_changed)

        self.maximum_width = QDesktopWidget().screenGeometry(0).width()

        self.initial_pos()

        # 第一層
        self.main_icon = button_icon(
            self.config['main_icon_size'], 
            self.config['main_icon_path'], 
            self.config['pos_x'], 
            self.config['pos_y'],
            '功能表',
            True
            )
        self.main_icon.drag_drop_signal.connect(self.add_newdata_by_drag)
        self.main_icon.exit_signal.connect(sys.exit)
        # 子層
        self.initial_sub_gui()
        
        # function
        self.main_icon.menu_btn.clicked['bool'].connect(lambda: self.icon_visible(self.main_icon, self.sub_dict, self.sub_tables))
        self.initital_sub_function()

        self.main_icon.show()

        sys.exit(app.exec_())



    def initial_config(self):
        self.config = App_Setting_Window.load_config()
        self.auto_hide_flag = True if self.config['is_auto_hide'] == 1 else False
        try:
            self.main_icon.update_config_signal.emit(self.config)
        except:
            pass


    def initial_pos(self):
        self.initial_config()


        pos_check = 1 if self.config['pos_x'] > self.maximum_width // 2 else -1

        self.sub1_pos = (self.config['pos_x'] - self.config['main_distance']*pos_check, self.config['pos_y'])
        self.sub2_pos = (self.config['pos_x'] - self.config['main_distance']*2*pos_check, self.config['pos_y'])
        self.sub3_pos = (self.config['pos_x'] - self.config['main_distance']*3*pos_check, self.config['pos_y'])

        
    def update_pos(self):
        self.initial_pos()
        self.sub_dict = dict(zip([self.sub1_icon, self.sub2_icon, self.sub3_icon], [self.sub1_pos, self.sub2_pos, self.sub3_pos]))


    def initial_sub_gui(self):
        # 第二層
        self.sub1_icon = button_icon(self.config['sub_icon_size'], self.config['favorite_icon_path'], self.sub1_pos[0], self.sub1_pos[1], '我的最愛')
        self.sub2_icon = button_icon(self.config['sub_icon_size'], self.config['link_icon_path'], self.sub2_pos[0], self.sub2_pos[1], '超連結清單')
        self.sub3_icon = button_icon(self.config['sub_icon_size'], self.config['setting_icon_path'], self.sub3_pos[0], self.sub3_pos[1], '設定')

        # 第三層
        self.favorite_table = favorite_table_window('', self.sub1_pos[0], self.sub1_pos[1]+self.config['sub_distance'], self.main_icon)
        self.hyperlink_table = hyperlink_table_window('', self.sub2_pos[0], self.sub2_pos[1]+self.config['sub_distance'], self.config, self.main_icon)
        self.hyperlink_table.update_favorite_signal.connect(self.favorite_table.import_favorite_link)
        self.hyperlink_table.update_is_auto_hide_signal.connect(self.update_auto_hide_flag)
        self.hyperlink_table.request_update_favorite_table()
        self.favorite_table.reload_favorite_signal.connect(self.hyperlink_table.load_mylink_setting)
        self.setting_table = App_Setting_Window('', self.sub3_pos[0], self.sub3_pos[1]+self.config['sub_distance'], self.main_icon)
        self.setting_table.save_and_move_signal.connect(self.move_gui)
        self.setting_table.save_signal.connect(self.initial_config)
        self.setting_table.update_is_auto_hide_signal.connect(self.update_auto_hide_flag)

        #variable
        self.sub_tables = [self.favorite_table, self.hyperlink_table, self.setting_table]
        self.sub_dict = dict(zip([self.sub1_icon, self.sub2_icon, self.sub3_icon], [self.sub1_pos, self.sub2_pos, self.sub3_pos]))
    

    def initital_sub_function(self):
        self.sub1_icon.menu_btn.clicked['bool'].connect(lambda: self.table_visible(self.favorite_table, self.sub_tables))
        self.sub2_icon.menu_btn.clicked['bool'].connect(lambda: self.table_visible(self.hyperlink_table, self.sub_tables))
        self.sub3_icon.menu_btn.clicked['bool'].connect(lambda: self.table_visible(self.setting_table, self.sub_tables))


    def move_gui(self, offset_dict):
        self.icon_visible(self.main_icon, self.sub_dict, self.sub_tables, 'hide')

        self.main_icon.animation_group = QParallelAnimationGroup()
        easing_curve = QEasingCurve.InOutCubic

        self.main_icon.animation_btnsize = QPropertyAnimation(self.main_icon.menu_btn, b"iconSize")
        self.main_icon.animation_mainminsize = QPropertyAnimation(self.main_icon, b"minimumSize")
        self.main_icon.animation_mainmaxsize = QPropertyAnimation(self.main_icon, b"maximumSize")
        self.main_icon.animation_pos = QPropertyAnimation(self.main_icon, b"pos")

        self.main_icon.animation_group.addAnimation(self.main_icon.animation_btnsize)
        self.main_icon.animation_group.addAnimation(self.main_icon.animation_mainminsize)
        self.main_icon.animation_group.addAnimation(self.main_icon.animation_mainmaxsize)
        self.main_icon.animation_group.addAnimation(self.main_icon.animation_pos)

        start_size = self.main_icon.menu_btn.iconSize()
        end_size = QSize(offset_dict['main_icon_size'], offset_dict['main_icon_size'])
        self.main_icon.animation_btnsize.setDuration(50)
        self.main_icon.animation_btnsize.setStartValue(start_size)
        self.main_icon.animation_btnsize.setEndValue(end_size)
        self.main_icon.animation_btnsize.setEasingCurve(QEasingCurve.OutInCubic)

        self.main_icon.animation_mainminsize.setDuration(50)
        self.main_icon.animation_mainminsize.setStartValue(QSize(self.main_icon.x(), self.main_icon.y()))
        self.main_icon.animation_mainminsize.setEndValue(QSize(offset_dict['main_icon_size'], offset_dict['main_icon_size']))
        self.main_icon.animation_mainminsize.setEasingCurve(QEasingCurve.Linear)

        self.main_icon.animation_mainmaxsize.setDuration(50)
        self.main_icon.animation_mainmaxsize.setStartValue(QSize(self.main_icon.x(), self.main_icon.y()))
        self.main_icon.animation_mainmaxsize.setEndValue(QSize(offset_dict['main_icon_size'], offset_dict['main_icon_size']))
        self.main_icon.animation_mainmaxsize.setEasingCurve(QEasingCurve.Linear)

        self.main_icon.animation_pos.setDuration(150)
        self.main_icon.animation_pos.setStartValue(self.main_icon.pos())
        self.main_icon.animation_pos.setEndValue(QPoint(self.main_icon.x() + offset_dict['offset_x'], self.main_icon.y() + offset_dict['offset_y']))
        self.main_icon.animation_pos.valueChanged.connect(lambda x: self.main_icon.move_to)
        self.main_icon.animation_pos.setEasingCurve(easing_curve)

        self.main_icon.animation_group.finished.connect(self.move_gui_II)

        self.main_icon.animation_group.start()


    def move_gui_II(self):
        self.update_pos()
        self.initial_sub_gui()
        self.initital_sub_function()

    
    def add_newdata_by_drag(self, link_path):
        self.hyperlink_table.open_new_link_win(link_path)

    
    def update_auto_hide_flag(self, flag):
        self.auto_hide_flag = flag


    def on_focus_changed(self, old, new):
        if not new and self.config['is_auto_hide'] and self.auto_hide_flag:
            self.icon_visible(self.main_icon, self.sub_dict, self.sub_tables, 'hide')


    def icon_visible(self, parent, childs_info:dict, sub_tables, flag=''):
        for ch, pos in childs_info.items():
            if ch.isVisible() or flag == 'hide':
                for tb in sub_tables:
                    self.show_with_animation(tb, tb, [tb.x(), tb.y()], 'hide', self.config['sub_ani_period'])
                self.show_with_animation(parent, ch, pos, 'hide', self.config['main_ani_period'])
            else:
                self.show_with_animation(parent, ch, pos, 'show', self.config['main_ani_period'])

    
    def table_visible(self, tb, sub_tables):
        if tb.isVisible():
            self.show_with_animation(tb, tb, [tb.x(), tb.y()], 'hide', self.config['sub_ani_period'])
        else:
            for other_tb in [v for v in sub_tables if v != tb]:
                self.show_with_animation(other_tb, other_tb, [other_tb.x(), other_tb.y()], 'hide', self.config['sub_ani_period'])
            self.show_with_animation(tb, tb, [tb.x(), tb.y()], 'show', self.config['sub_ani_period'])


    def show_with_animation(self, parent, ch, pos, flag, ani_period):
        ch.animation_group = QParallelAnimationGroup()

        ch.animation_opacity = QPropertyAnimation(ch, b"windowOpacity")
        ch.animation_opacity.setDuration(ani_period)

        ch.animation_pos = QPropertyAnimation(ch, b"pos")
        ch.animation_pos.setDuration(ani_period)

        ch.animation_group.addAnimation(ch.animation_opacity)
        ch.animation_group.addAnimation(ch.animation_pos)
        
        if flag == 'show':
            start_pos, end_pos = parent.pos(), QPoint(pos[0], pos[1])
            start_opacity, end_opacity = 0.0, 1.0
            ch.show()
        else:
            start_pos, end_pos = QPoint(pos[0], pos[1]), parent.pos()
            start_opacity, end_opacity = 1.0, 0.0

        ch.animation_opacity.setStartValue(start_opacity)
        ch.animation_opacity.setEndValue(end_opacity)
        ch.animation_opacity.setEasingCurve(QEasingCurve.InQuad)

        ch.animation_pos.setStartValue(start_pos)
        ch.animation_pos.setEndValue(end_pos)

        if flag == 'hide':
            ch.animation_group.finished.connect(ch.hide)

        ch.animation_group.start()


if __name__ =='__main__':
    # # Create the tray
    # tray = QSystemTrayIcon()
    # tray.setIcon(QIcon('icon/icon.png'))
    # tray.setVisible(True)

    app = main()
    # tray.setToolTip(tooltip)

    # # Create the menu
    # menu = QMenu()
    # action1 = QAction("關閉程式")
    # action1.triggered.connect(app.exit)
    # menu.addAction(action1)

    # # Add the menu to the tray
    # tray.setContextMenu(menu)
    
    # myWin = MainWindow(int(main_size))
    # myWin.show()
    