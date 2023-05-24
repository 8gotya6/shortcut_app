import os
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QTableWidget, QTableWidgetItem, QWidget, QAbstractItemView, QMenu, QAction, QMessageBox, QTabBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal
import pandas as pd

from Ui_hyperlink_table import Ui_hyperlink_window
from add_link_window import add_link_window



class CustomTabBar(QTabBar):
    del_tab_signal = pyqtSignal(str)
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            index = self.tabAt(event.pos())
            if index != -1:
                self.setCurrentIndex(index)
        else:
            super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        if self.currentIndex() != -1:
            menu = QMenu(self)
            menu.setStyleSheet(
                        """
                        QMenu {
                            background-color: white;
                        }

                        QMenu::item {
                            padding: 5px 25px 5px 20px;
                            background-color: transparent;
                            color: black;
                        }

                        QMenu::item:selected {
                            background-color: rgb(158, 107, 107);
                            color: rgb(255, 255, 255);
                        }

                        QMenu::item:!selected:hover {
                            background-color: rgb(248, 249, 238);
                        }
                        """
                    )

            delete_action = QAction("刪除此頁", self)
            delete_action.triggered.connect(self.delete_tab)
            menu.addAction(delete_action)
            menu.exec_(event.globalPos())


    def delete_tab(self):
        index = self.currentIndex()
        if index != -1:
            tab_name = self.tabText(index)
            self.parentWidget().removeTab(index)

            self.del_tab_signal.emit(tab_name)


class hyperlink_table_window(QMainWindow, Ui_hyperlink_window):
    update_favorite_signal = pyqtSignal(object)
    update_is_auto_hide_signal = pyqtSignal(bool)
    def __init__(self, icon_path, pos_x, pos_y, config, main_gui):
        super(hyperlink_table_window, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.Tool)
        self.setWindowIcon(QIcon(icon_path))
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

        custom_tabBar = CustomTabBar(self.hyperlink_tabpage)
        custom_tabBar.del_tab_signal.connect(self.drop_df_by_tabname)
        self.hyperlink_tabpage.setTabBar(custom_tabBar)
        self.config = config
        main_gui.update_config_signal.connect(self.update_config)

        self.reload_table_btn.setIcon(QIcon('icon/loop.png'))
        self.reload_table_btn.setIconSize(QSize(30, 30))
        self.save_table_btn.setIcon(QIcon('icon/save.png'))
        self.save_table_btn.setIconSize(QSize(27, 27))
        self.new_data_btn.setIcon(QIcon('icon/add.png'))
        self.new_data_btn.setIconSize(QSize(27, 27))
        self.open_link_setting_btn.setIcon(QIcon('icon/excel.png'))
        self.open_link_setting_btn.setIconSize(QSize(27, 27))

        if pos_x-self.width()//2 > 0 and pos_x+self.width() > (main_gui.x() + main_gui.width()):
            qpoint_x = main_gui.x() + main_gui.width() - self.width()
            qpoint_x = qpoint_x if qpoint_x >= 0 else 0
        elif pos_x-self.width()//2 < 0:
            qpoint_x = 0
        else:
            qpoint_x = pos_x-self.width()//2
        self.move(QPoint(qpoint_x, pos_y))

        self.dfs = pd.read_excel('link_setting.xlsx', sheet_name=None)
        self.load_mylink_setting()
        self.reload_table_btn.clicked['bool'].connect(self.reload_link_setting)
        self.save_table_btn.clicked['bool'].connect(self.save_mylink_data)
        self.new_data_btn.clicked['bool'].connect(lambda: self.open_new_link_win())
        self.open_link_setting_btn.clicked['bool'].connect(self.open_link_setting)


    def update_config(self, config):
        self.config = config

    
    def move_to(self, offset_dict):
        current_pos = self.pos()
        new_pos = current_pos + QPoint(offset_dict['offset_x'], offset_dict['offset_y'])
        self.move(new_pos)


    def reload_link_setting(self):
        dfs = pd.read_excel('link_setting.xlsx', sheet_name=None)
        
        check_diff = False
        for k, v in dfs.items():
            v.fillna('', inplace=True)
            if k not in self.dfs:
                check_diff = True
            else:
                if not v.equals(self.dfs[k]):
                    check_diff = True
        
        if check_diff:
            self.update_is_auto_hide_signal.emit(False)
            msg = QMessageBox.warning(self, 'warning', '現有資料與設定檔不相符，是否重新載入?', QMessageBox.Yes|QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.dfs = dfs
                self.load_mylink_setting()

            self.update_is_auto_hide_signal.emit(True)


    def load_mylink_setting(self):
        i = 0
        self.hyperlink_tabpage.clear()
        self.hyperlink_tabpage.setStyleSheet("background-color: rgb(56, 76, 101);color: rgb(248, 249, 238);margin:0px")
        for sheet_name, df in self.dfs.items():
            tab_page = QWidget()
            self.hyperlink_tabpage.addTab(tab_page, sheet_name)

            layout = QGridLayout(tab_page)
            tb = QTableWidget(len(df), 3)
            tb.horizontalHeader().setStretchLastSection(True)
            tb.setHorizontalHeaderLabels(df.columns)
            tb.setStyleSheet("background-color: rgb(204, 203, 201);color: rgb(30, 30, 30);margin:0px")
            tb.setSelectionMode(QAbstractItemView.SingleSelection)
            tb.setSelectionBehavior(QAbstractItemView.SelectRows)
            tb.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            tb.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
            
            layout.addWidget(tb, 0, 0, 1, 1)

            self.hyperlink_tabpage.setTabText(i, sheet_name)
            df.fillna('', inplace=True)
            for r in range(len(df)):
                tb.setItem(r, 0, QTableWidgetItem(df.iloc[r, 0]))
                tb.setItem(r, 1, QTableWidgetItem(df.iloc[r, 1]))
                tb.setItem(r, 2, QTableWidgetItem(df.iloc[r, 2]))

            tb.resizeColumnsToContents()
            tb.cellClicked.connect(lambda row, col, table_widget=tb: self.link_table_clicked(row, table_widget, ''))
            tb.setContextMenuPolicy(Qt.CustomContextMenu)
            tb.customContextMenuRequested.connect(self.show_context_menu)

            i += 1
        
        self.request_update_favorite_table()


    def show_context_menu(self, pos):
        table = self.hyperlink_tabpage.currentWidget().findChild(QTableWidget)
        sheet_name = self.hyperlink_tabpage.tabText(self.hyperlink_tabpage.currentIndex())

        menu = QMenu(self)
        menu.setStyleSheet(
                        """
                        QMenu {
                            background-color: white;
                        }

                        QMenu::item {
                            padding: 5px 25px 5px 20px;
                            background-color: transparent;
                            color: black;
                        }

                        QMenu::item:selected {
                            background-color: rgb(158, 107, 107);
                            color: rgb(255, 255, 255);
                        }

                        QMenu::item:!selected:hover {
                            background-color: rgb(248, 249, 238);
                        }
                        """
                    )
        open_link_action = QAction("開啟連結", self)
        open_link_action.triggered.connect(lambda: self.link_table_clicked([index.row() for index in table.selectedIndexes()][0], table, 'open'))
        menu.addAction(open_link_action)

        add_favorite_action = QAction("加入我的最愛", self)
        add_favorite_action.triggered.connect(lambda: self.add_to_favorites(table, sheet_name, 'add'))
        menu.addAction(add_favorite_action)

        cancel_favorite_action = QAction("取消我的最愛", self)
        cancel_favorite_action.triggered.connect(lambda: self.add_to_favorites(table, sheet_name, 'cancel'))
        menu.addAction(cancel_favorite_action)

        del_data_action = QAction("刪除此筆", self)
        del_data_action.triggered.connect(lambda: self.delete_selected_row(table, sheet_name))
        menu.addAction(del_data_action)

        menu.exec_(table.viewport().mapToGlobal(pos))


    def link_table_clicked(self, row, table_widget, flag):
        link_item = table_widget.item(row, 2)
        if link_item is not None:
            link_value = link_item.text()

            if self.config['isopenlink_byclicktable'] == 1 or flag == 'open':
                self.open_link(link_value)


    def open_link(self, link_value):
        if 'http' in link_value:
            self.open_url_byedge(link_value)
        elif os.path.exists(link_value) and os.path.isfile(link_value):
            os.startfile(link_value)
        elif os.path.exists(link_value) and os.path.isdir(link_value):
            os.startfile(link_value)
        else:
            print('not found')


    def open_url_byedge(self, url):
        # Edge 瀏覽器的執行檔路徑
        edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        # 使用 os 模組呼叫 Edge 瀏覽器並傳遞網址參數
        os.system(f'"{edge_path}" {url}')


    def request_update_favorite_table(self):
        favorite_list = []
        for sheet_name, df in self.dfs.items():
            filtered_df = df[df['我的最愛'] == 'V']
            favorite_list.append(filtered_df)

        df_favorite = pd.concat(favorite_list)
        self.update_favorite_signal.emit(df_favorite)


    def add_to_favorites(self, tb, sheet_name, flag):
        df = self.dfs[sheet_name]
        selected_rows = set(index.row() for index in tb.selectedIndexes())
        if selected_rows:
            for row in selected_rows:
                link_value = tb.item(row, 2).text()
                df.loc[df['位址'] == link_value, '我的最愛'] = 'V' if flag == 'add' else ''
                tb.setItem(row, 0, QTableWidgetItem('V' if flag == 'add' else ''))
                break

        self.request_update_favorite_table()


    def delete_selected_row(self, tb, sheet_name):
        selected_rows = [index.row() for index in tb.selectedIndexes()]

        for row in selected_rows:
            tb.removeRow(row)
            break

        self.dfs[sheet_name] = self.dfs[sheet_name].drop(self.dfs[sheet_name].index[selected_rows])

    
    def drop_df_by_tabname(self, sheet_name):
        try:
            del self.dfs[sheet_name]
        except KeyError:
            pass

        
    def save_mylink_data(self):
        output_file = 'link_setting.xlsx'
        try:
            writer = pd.ExcelWriter(output_file, engine='xlsxwriter')
            for sheet_name, df in self.dfs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.save()
        except PermissionError:
            msg = QMessageBox.warning(self, 'Error', '檔案已被開啟, 無法寫入!')
        except FileNotFoundError:
            msg = QMessageBox.warning(self, 'Error', '檔案不存在, 請重新確認路徑檔案是否正確!')


    def open_new_link_win(self, link_path=''):
        self.update_is_auto_hide_signal.emit(False)

        tab_names = [self.hyperlink_tabpage.tabText(index) for index in range(self.hyperlink_tabpage.count())]
        self.add_new_link_win = add_link_window(tab_names, link_path)
        self.add_new_link_win.sure_add_signal.connect(self.add_new_link)
        self.add_new_link_win.not_add_signal.connect(self.hide_add_new_link_win)
        self.add_new_link_win.show()

    
    def hide_add_new_link_win(self):
        self.add_new_link_win.hide()
        self.update_is_auto_hide_signal.emit(True)


    def add_new_link(self, new_link_data):
        page_name = new_link_data['link_page']
        #update df
        update_data = {
                    '我的最愛': 'V' if new_link_data['is_add_favorite'] else '',
                    '名稱': new_link_data['link_name'],
                    '位址': new_link_data['link_path']
                }
        if page_name in self.dfs:
            self.dfs[page_name] = self.dfs[page_name].append(
                update_data, ignore_index=True)
        else:
            self.dfs[page_name] = pd.DataFrame(update_data, index=[0])

        #update link table
        self.load_mylink_setting()

        if new_link_data['is_auto_save']:
            self.save_mylink_data()


    def open_link_setting(self):
        try:
            os.startfile(self.config['setting_path'])
        except:
            msg = QMessageBox.warning(self, 'Error', '檔案不存在, 請重新確認路徑檔案是否正確!')