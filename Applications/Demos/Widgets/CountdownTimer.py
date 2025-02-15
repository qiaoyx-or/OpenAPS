
from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QSlider

class Pomodoro(QWidget):
    def __init__(self):
        super().__init__()

        self.pomodoro_slider = QSlider()
        self.pomodoro_slider.setOrientation(Qt.Orientation.Horizontal)

        self.pomodoro_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.pomodoro_slider.setMinimum(1)
        self.pomodoro_slider.setMaximum(60)
        self.pomodoro_slider.setTickInterval(1)

        ### BREAK TIMER SLIDER ###
        self.pomodoro_break_slider = QSlider()
        self.pomodoro_break_slider.setOrientation(Qt.Orientation.Horizontal)
        self.pomodoro_break_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.pomodoro_break_slider.setMinimum(0)
        self.pomodoro_break_slider.setMaximum(30)
        self.pomodoro_break_slider.setTickInterval(1)

        ### INIT VALUES ###
        self.pomodoro_slider.setValue(20)
        self.pomodoro_break_slider.setValue(5)
        self.minutes = 20
        self.seconds = 60
        self.break_time_minutes = 5

        ### CLOCK STYLE ###
        QFontDatabase.addApplicationFont("Seven Segment.ttf")
        self.timer_font = QFont("Seven Segment", 100)
        self.timer_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 115)
        self.timer_label = QLabel("20:00")

        self.timer_label.setFont(self.timer_font)

        ### TIMER BUTTONS ###
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_timer)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_timer)
        self.stop_btn.setCheckable(True)
        self.stop_btn.setDisabled(True)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_timer)
        self.reset_btn.setDisabled(True)


        ### MAIN LAYOUT ###
        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.timer_label, 0,0,1,3)
        self.grid_layout.addWidget(self.start_btn, 1,0)
        self.grid_layout.addWidget(self.stop_btn, 1,1)
        self.grid_layout.addWidget(self.reset_btn, 1,2)
        self.grid_layout.addWidget(self.pomodoro_slider, 2,0,1,3)
        self.grid_layout.addWidget(self.pomodoro_break_slider, 3,0,1,3)
        self.setLayout(self.grid_layout)

        ### SLIDERS CONNECTIONS ###
        self.pomodoro_slider.valueChanged.connect(self.update_timer_slider)
        self.pomodoro_break_slider.valueChanged.connect(self.update_break_timer_slider)


    ### START TIMER FUNCTION ###
    def start_timer(self):
        self.setMaximumSize(400, 115)
        self.setMinimumSize(400, 115)
        self.stop_btn.setDisabled(False)
        self.reset_btn.setDisabled(False)
        self.start_btn.setDisabled(True)
        self.pomodoro_slider.setHidden(True)
        self.pomodoro_break_slider.setHidden(True)
        self.timer = QTimer(self)
        self.minutes = self.pomodoro_slider.value() - 1
        self.seconds = 60
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.update_gui()

    ### STOP TIMER FUNCTION ###
    def stop_timer(self):
        # click_sound.play()
        if self.stop_btn.isChecked():
            self.timer.stop()
            self.stop_btn.setText("Resume")
        if not self.stop_btn.isChecked():
            self.stop_btn.setText("Stop")
            self.timer.start(1000)
    ############################
    ### RESET TIMER FUNCTION ###
    def reset_timer(self):
        # click_sound.play()
        self.setMaximumSize(400, 300)
        self.setMinimumSize(400, 300)
        self.resize(400, 300)
        # self.timer_label.setStyleSheet("font-size: 100px; ")
        self.stop_btn.setDisabled(True)
        self.stop_btn.setText("Stop")
        self.stop_btn.setChecked(False)
        self.reset_btn.setDisabled(True)
        self.start_btn.setDisabled(False)
        self.pomodoro_slider.setHidden(False)
        self.pomodoro_break_slider.setHidden(False)
        self.minutes = self.pomodoro_slider.value()
        self.timer.stop()
        self.update_timer_slider()

    ### UPDATE TIMER FUNCTION ###
    def update_timer(self):
        if self.pomodoro_slider.value == 1:
            self.minutes == 0
        self.seconds = (self.seconds - 1) % 60

        if (self.seconds == 0 or self.seconds == 60) and self.minutes != 0:
            self.minutes -=1

        elif self.minutes == 0:
            if self.minutes == 0 and (self.seconds == 0 or self.seconds == 60):

                self.timer.stop()
                valor = self.pomodoro_break_slider.value()
                if valor > 0:
                    self.start_break_time()
                else:
                    self.start_timer()
        self.update_gui()

    ### UPDATE BREAK TIMER FUNCTION
    def update_break_timer(self):
        self.seconds = (self.seconds - 1) % 60
        if (self.seconds == 0 or self.seconds == 60) and self.minutes != 0:
            self.minutes -=1

        elif self.minutes == 0:
            if self.minutes == 0 and (self.seconds == 0 or self.seconds == 60):
                self.timer.stop()
                self.start_timer()
        self.update_gui()

    ### UPDATE TIMER WITH SLIDER FUNCTION ###
    def update_timer_slider(self):
        self.minutes = self.pomodoro_slider.value()
        self.timer_label.setText("{0:02d}:00".format(self.minutes))

    ### UPDATE BREAK TIMER WITH SLIDER FUNCTION ###
    def update_break_timer_slider(self):
        self.break_time_minutes = self.pomodoro_break_slider.value()
        self.timer_label.setText("{0:02d}:00".format(self.break_time_minutes))

    ### START THE BREAK TIME ###
    def start_break_time(self):
        self.timer = QTimer(self)
        self.minutes = self.pomodoro_break_slider.value()  - 1
        self.seconds = 60
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_break_timer)
        self.update_gui()

    ### UPDATE TIMER LABEL ON GUI ###
    def update_gui(self):
        if self.seconds == 60:
            self.timer_label.setText("{0:02d}:00".format(self.minutes))
        else:
            self.timer_label.setText("{0:02d}:{1:02d}".format(self.minutes, self.seconds))
