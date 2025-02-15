import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个 QLabel 组件
        self.label = QLabel(self)
        self.label.setScaledContents(True)

        # 加载图片
        pixmap = QPixmap("../../Docs/images/planning_system.png")

        # 将图片设置到 QLabel
        self.label.setPixmap(pixmap)

        # 调整窗口大小以适应图片
        self.setCentralWidget(self.label)
        # self.resize(pixmap.width(), pixmap.height())
        self.label.resize(800, 800)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 800)
    window.show()
    sys.exit(app.exec())
