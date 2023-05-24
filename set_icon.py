from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSignal

from Ui_Shortcut_App import Ui_icon_window


class button_icon(QMainWindow, Ui_icon_window):
    update_config_signal = pyqtSignal(dict)
    drag_drop_signal = pyqtSignal(str)
    exit_signal = pyqtSignal(object)
    def __init__(self, size, icon_path, pos_x, pos_y, tooltip, show_exit_menu=False):
        super(button_icon, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.Tool)
        self.setWindowIcon(QIcon(icon_path))
        self.setAcceptDrops(True)

        self.setMinimumSize(QSize(size, size))
        self.setMaximumSize(QSize(size, size))

        self.setAttribute(Qt.WA_TranslucentBackground)
        radius = size // 2 - 10
        self.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-top-left-radius:{0}px;
            border-bottom-left-radius:{0}px;
            border-top-right-radius:{0}px;
            border-bottom-right-radius:{0}px;
            margin: 10px;
            """.format(radius)
        )

        self.move(QPoint(pos_x if pos_x > 0 else 0, pos_y))

        self.menu_btn.setIcon(QIcon(icon_path))
        self.menu_btn.setIconSize(QSize(size, size))
        self.menu_btn.setToolTip(tooltip)

        self.tooltip = tooltip
        self.menu_btn.enterEvent = self.show_tooltip
        self.menu_btn.leaveEvent = self.hide_tooltip

        if show_exit_menu:
            self.menu_btn.setContextMenuPolicy(Qt.CustomContextMenu)
            self.menu_btn.customContextMenuRequested.connect(self.show_context_menu)


    def move_to(self, offset_value):
        current_pos = self.pos()
        new_pos = current_pos + QPoint(offset_value.x(), offset_value.y())
        self.move(new_pos)


    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()


    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            file_path = text.replace('file:///', '')
            self.drag_drop_signal.emit(file_path)

    
    def show_tooltip(self, event):
        tooltip_text = self.menu_btn.toolTip()
        tooltip_pos = self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft())
        QToolTip.showText(tooltip_pos, tooltip_text, self.menu_btn)

    def hide_tooltip(self, event):
        QToolTip.hideText()


    def show_context_menu(self, position):
        menu = QMenu(self)
        menu.setStyleSheet(
                        """
                        QMenu {
                            background-color: white;
                            padding: 3px 5px 3px 5px;
                            margin: 3px
                        }

                        QMenu::item {
                            padding: 3px;
                            margin: 0px;
                            background-color: transparent;
                            color: black;
                        }

                        QMenu::item:selected {
                            background-color: rgb(158, 107, 107);
                            padding: 3px;
                            color: rgb(255, 255, 255);
                        }

                        QMenu::item:!selected:hover {
                            background-color: rgb(248, 249, 238);
                        }
                        """
                    )

        exit_action = QAction("關閉程式", self)
        exit_action.triggered.connect(self.exit_signal.emit)

        menu.addAction(exit_action)

        menu.exec_(self.menu_btn.mapToGlobal(position))
