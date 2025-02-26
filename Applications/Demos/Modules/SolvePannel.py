
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QProcess
import pandas as pd
import pathlib
import glob
import re

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from UI_SolvePannel import Ui_Pannel
sys.path.append(
    os.path.dirname (
        os.path.dirname(os.path.abspath(__file__))
    )
 )
from Widgets.PandasModel import PandasModel

# A regular expression, to extract the % complete.
progress_re = re.compile("Total complete: (\d+)%")


class SolvePannel(QWidget):
    def __init__(self):
        super(SolvePannel, self).__init__()
        self.ui = Ui_Pannel()
        self.ui.setupUi(self)

        self.process = None

        self.read_data()

        self.ui.statusLabel.setText('')
        self.ui.startBtn.setEnabled(True)
        self.ui.stopBtn.setEnabled(False)
        self.ui.workcenters.currentIndexChanged.connect(self.change_result)

        self.ui.startBtn.clicked.connect(self.on_start)
        self.ui.stopBtn.clicked.connect(self.on_stop)
        self.ui.tabWidget.currentChanged.connect(self.on_tab_changed)

    def read_data(self) -> None:
        folder = pathlib.Path(__file__).parent.resolve()
        path = f'{folder.parent.parent}/ProductionPlanning/'
        filename = 'workcenter' + '*.csv'
        files = glob.glob(f'{path}/{filename}')
        self.results = [pd.read_csv(f) for f in files]
        self.ui.workcenters.clear()
        for f in files:
            fn, _ = os.path.splitext(os.path.basename(f))
            self.ui.workcenters.addItem(fn)

        self.ui.workcenters.setMinimumWidth(200)
        self.ui.workcenters.adjustSize()

        self.ui.workcenters.setCurrentIndex(0)
        self.ui.resultView.setModel(PandasModel(self.results[0]))

        df = pd.read_csv(f'{path}/demand.csv')
        self.ui.demandView.setModel(PandasModel(df))

    def change_result(self, index) -> None:
        self.ui.resultView.setModel(PandasModel(self.results[index]))

    def on_tab_changed(self, index):
        if index == 2:
            self.ui.workcenters.show()
        else:
            self.ui.workcenters.hide()

    def on_start(self) -> None:
        if self.process is None:
            self.ui.statusLabel.setText('Executing process')

            self.process = QProcess()
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.stateChanged.connect(self.handle_state)
            self.process.finished.connect(self.on_finished)

            self.ui.startBtn.setEnabled(False)
            self.ui.stopBtn.setEnabled(True)

            folder = pathlib.Path(__file__).parent.resolve()
            excutor = f'{folder.parent.parent}/ProductionPlanning/Workshop.py'
            self.process.start("python3", [excutor])

    def on_stop(self) -> None:
        if self.process is not None:
            self.process.kill()

    def handle_stderr(self) -> None:
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        m = progress_re.search(stderr)
        if m:
            pc_complete = int(m.group(1))
            # Extract progress if it is in the data.
            if pc_complete:
                self.ui.statusLabel.setText(f'complete {pc_complete} percent')

    def handle_stdout(self) -> None:
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)
        # self.message(stdout)

        # df = pd.read_json(StringIO(stdout))
        # print(df)

    def handle_state(self, state) -> None:
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.ui.statusLabel.setText(f"State changed: {state_name}")

    def on_finished(self) -> None:
        self.ui.statusLabel.setText("Process finished.")
        self.process = None
        self.ui.startBtn.setEnabled(True)
        self.ui.stopBtn.setEnabled(False)

        self.read_data()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    window = SolvePannel()
    window.show()

    sys.exit(app.exec())
