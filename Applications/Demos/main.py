
from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QComboBox,
    # QStatusBar,
    # QMenu,
    # QMenuBar,
    # QToolBar,
)

from PySide6.QtGui import QAction, QIcon
from qt_material import apply_stylesheet, list_themes

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Modules.SolvePannel import SolvePannel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Planning Demos")

        styles = map(
            lambda f: f.removesuffix(".xml"),
            list_themes()
        )
        self.style_combo = QComboBox()
        self.style_combo.addItems(styles)

        # 创建菜单栏
        menubar = self.menuBar()

        # 创建菜单
        # file_menu = menubar.addMenu("文件")
        # edit_menu = menubar.addMenu("编辑")
        # style_menu = menubar.addMenu("样式")

        # 创建菜单项
        # new_action = QAction("新建", self)
        # open_action = QAction("打开", self)
        # save_action = QAction("保存", self)

        # 将菜单项添加到菜单
        # file_menu.addAction(new_action)
        # file_menu.addAction(open_action)
        # file_menu.addAction(save_action)

        # 创建工具栏
        toolbar = self.addToolBar("工具栏")
        # toolbar.addAction(new_action)
        # toolbar.addAction(open_action)
        # toolbar.addAction(save_action)
        toolbar.addWidget(self.style_combo)

        # 创建状态栏
        self.statusBar().showMessage("准备就绪")

        # 创建中心小部件
        planning = SolvePannel()
        self.setCentralWidget(planning)

        self.setMinimumSize(800, 600)
        self.setMaximumSize(2560, 1440)
        self.resize(800, 600)

        self.apply_style()
        self.style_combo.currentIndexChanged.connect(self.apply_style)

    def apply_style(self):
        app = QApplication.instance()
        style_name = self.style_combo.currentText()
        apply_stylesheet(app, theme=style_name + '.xml')


if __name__ == "__main__":
    import pathlib

    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_teal.xml')

    folder = pathlib.Path(__file__).parent.resolve()
    app.setWindowIcon(QIcon(f"{folder}/resource/main_logo.png"))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
