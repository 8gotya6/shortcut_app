import os
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal

from Ui_favorite_table import Ui_favorite_window


class favorite_table_window(QMainWindow, Ui_favorite_window):
    reload_favorite_signal = pyqtSignal()
    def __init__(self, icon_path, pos_x, pos_y, main_gui):
        super(favorite_table_window, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.Tool)
        self.setWindowIcon(QIcon(icon_path))
        self.setAcceptDrops(True)

        self.setAttribute(Qt.WA_TranslucentBackground)
        radius = 5
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

        self.reload_table_btn.setIcon(QIcon('icon/loop.png'))
        self.reload_table_btn.setIconSize(QSize(30, 30))

        if pos_x-self.width()//2 > 0 and pos_x+self.width() > (main_gui.x() + main_gui.width()):
            qpoint_x = main_gui.x() + main_gui.width() - self.width()
            qpoint_x = qpoint_x if qpoint_x >= 0 else 0
        elif pos_x-self.width()//2 < 0:
            qpoint_x = 0
        else:
            qpoint_x = pos_x-self.width()//2
        self.move(QPoint(qpoint_x, pos_y))

        header = self.favorite_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)

        header.setDefaultSectionSize(40)

        self.favorite_table.cellClicked.connect(lambda row, col: self.favorite_table_clicked(row, col))
        self.reload_table_btn.clicked['bool'].connect(self.reload_favorite_table)
        self.keyword_filter.textChanged.connect(self.filter_favorite_table)
        self.linktype_filter.currentIndexChanged.connect(self.filter_favorite_table)

        self.favorite_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.favorite_table.customContextMenuRequested.connect(self.show_context_menu)



    def move_to(self, offset_dict):
        current_pos = self.pos()
        new_pos = current_pos + QPoint(offset_dict['offset_x'], offset_dict['offset_y'])
        self.move(new_pos)


    def check_link_type(self, link_value):
        if 'http' in link_value:
            return '網頁'
        elif os.path.exists(link_value) and os.path.isfile(link_value):
            return '檔案'
        elif os.path.exists(link_value) and os.path.isdir(link_value):
            return '資料夾'
        else:
            return ''


    def import_favorite_link(self, df):
        self.favorite_table.setRowCount(len(df))
        for r in range(len(df)):
            self.favorite_table.setItem(r, 0, QTableWidgetItem(df.iloc[r, 1]))
            self.favorite_table.setItem(r, 1, QTableWidgetItem(self.check_link_type(df.iloc[r, 2])))
            self.favorite_table.setItem(r, 2, QTableWidgetItem(df.iloc[r, 2]))

        self.favorite_table.resizeColumnsToContents()


    def favorite_table_clicked(self, row, col):
        link_item = self.favorite_table.item(row, 2)
        if link_item is not None:
            link_value = link_item.text()

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


    def reload_favorite_table(self):
        self.reload_favorite_signal.emit()


    def filter_favorite_table(self):
        keyword = self.keyword_filter.text()
        linktype = self.linktype_filter.currentText()
        for r in range(self.favorite_table.rowCount()):
            all_text = [self.favorite_table.item(r, 0).text(), self.favorite_table.item(r, 1).text(), self.favorite_table.item(r, 2).text()]
            if len(keyword) == 0 or (len(keyword) > 0 and any(keyword in v for v in all_text)):
                if linktype in [self.favorite_table.item(r, 1).text(), '全部']:
                    self.favorite_table.setRowHidden(r, False)
                    continue
                
            self.favorite_table.setRowHidden(r, True)


    def show_context_menu(self, pos):
        table = self.favorite_table

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
        open_link_action.triggered.connect(lambda: self.favorite_table_clicked([index.row() for index in table.selectedIndexes()][0], 2))
        menu.addAction(open_link_action)

        # cancel_favorite_action = QAction("取消我的最愛", self)
        # cancel_favorite_action.triggered.connect(lambda: self.add_to_favorites(table, sheet_name, 'cancel'))
        # menu.addAction(cancel_favorite_action)

        menu.exec_(table.viewport().mapToGlobal(pos))