
from __future__ import annotations
from PySide6.QtCore import (
    QObject, QThread,
    Signal,
    Slot
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    # QStackedLayout,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QTabWidget,
    # QButtonGroup,
    QPushButton,
    # QToolButton,
    QSpacerItem,
    QSizePolicy
)

import pandas as pd
import sys, os
sys.path.append(
    os.path.dirname (
        os.path.dirname(os.path.abspath(__file__))
    )
 )
from Widgets.PandasModel import PandasModel
sys.path.append(
    os.path.dirname(
        os.path.dirname (
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)
from ProductionPlanning.Workshop import WorkshopSolver, create_solver


class SolveWorker(QObject):
    update_signal = Signal()
    finish_signal = Signal()

    def __init__(self, obj: WorkshopSolver) -> None:
        super().__init__()

        self.obj = obj
        self.isRunning = False

    def run(self) -> None:
        if self.isRunning:
            return

        self.isRunning = True
        self.obj.run()

        self.update_signal.emit()
        self.finish_signal.emit()
        self.isRunning = False

    def stop(self) -> None:
        self.isRunning = False


class WorkshopPlanning(QWidget):
    """ 包括: 输入、输出、配置、分析相关数据的展示
    """

    def __init__(self, worker, parent=None) -> None:
        super().__init__(parent)

        self.worker = worker
        self.thread = QThread()

        self.input_view = QTableView()
        self.config_view = QTableView()  # tableview 占位
        self.result_view = QTableView()
        self.analysis_view = QTableView()  # tableview 占位

        self.solve_btn = QPushButton('开始求解')
        self.stop_btn = QPushButton('中止求解')

        self.worker.update_signal.connect(self.on_update)
        self.worker.finish_signal.connect(self.on_finish)
        self.thread.started.connect(self.worker.run)

        self.init_ui()

    def init_ui(self) -> None:
        self.solve_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        main_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()
        pannal = QVBoxLayout()

        btn_frame = QFrame()
        btn_layout.addWidget(self.solve_btn)
        btn_layout.addItem(QSpacerItem(
            800, 10, QSizePolicy.Expanding, QSizePolicy.Minimum
        ))
        btn_layout.addWidget(self.stop_btn)
        btn_frame.setLayout(btn_layout)

        self.stacked = QTabWidget()
        self.stacked.setTabPosition(QTabWidget.West)
        self.stacked.setTabShape(QTabWidget.Rounded)
        self.stacked.addTab(self.input_view, '订单')
        self.stacked.addTab(self.config_view, '产能')
        self.stacked.addTab(self.result_view, '结果')
        self.stacked.addTab(self.analysis_view, '分析')

        pannal.addWidget(self.stacked)
        pannal.addWidget(btn_frame)

        main_layout.addLayout(pannal)
        self.setLayout(main_layout)

        df = self.worker.obj.engine.demand.data[
            ['id', 'code', 'name', 'number', 'delivery_time', 'description']
        ]
        model = PandasModel(df)
        self.input_view.setModel(model)

        self.solve_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)

    @staticmethod
    def create():
        solver = create_solver()
        worker = SolveWorker(solver)
        return WorkshopPlanning(worker)

    @Slot(pd.DataFrame)
    def on_update(self) -> None:
        import glob
        filename = 'workcenter' + '*.csv'
        for file in glob.glob(f'./{filename}'):
            print(file)
            df = pd.read_csv(file)
            model = PandasModel(df)
            self.result_view.setModel(model)

    @Slot()
    def on_finish(self) -> None:
        self.stop()

    def start(self):
        if not self.thread.isRunning():
            self.worker.moveToThread(self.thread)
            self.thread.start()

        self.solve_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop(self):
        if self.thread.isRunning():
            self.worker.stop()
            self.thread.quit()
            self.thread.wait()

        self.solve_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)


if __name__ == "__main__":
    from qt_material import apply_stylesheet
    from PySide6.QtWidgets import QApplication, QMainWindow
    # from qt_material import list_themes
    # print(list_themes())

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')

    solver = create_solver()
    worker = SolveWorker(solver)
    page = WorkshopPlanning(worker)
    window = QMainWindow()
    window.setCentralWidget(page)
    window.setMinimumSize(800, 600)
    window.setMaximumSize(2560, 1440)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
