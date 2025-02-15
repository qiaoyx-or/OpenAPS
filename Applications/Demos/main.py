
from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar,
    QMenu,
    # QMenuBar,
    QToolBar,
)

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Modules.WorkshopPlanning import WorkshopPlanning

if __name__ == "__main__":
    from qt_material import apply_stylesheet

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')

    planning = WorkshopPlanning.create()
    window = QMainWindow()
    window.setCentralWidget(planning)
    window.setMinimumSize(800, 600)
    window.setMaximumSize(2560, 1440)
    window.resize(800, 600)
    window.show()

    tool_bar = QToolBar()
    window.addToolBar(tool_bar)
    # window.setMenuBar(menu_bar)
    menu = QMenu()
    menu_bar = window.menuBar()
    menu_bar.addMenu(menu)

    status_bar = QStatusBar()

    window.setStatusBar(status_bar)
    window.setCentralWidget(planning)
    window.setMinimumSize(800, 600)
    window.setMaximumSize(2560, 1440)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
