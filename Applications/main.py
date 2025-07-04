import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QStackedWidget, QWidget, QVBoxLayout, QLabel, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("推荐界面示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口小部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建水平布局
        layout = QHBoxLayout(main_widget)

        # 创建QListWidget用于导航
        self.list_widget = QListWidget()
        self.list_widget.addItem("推荐内容 1")
        self.list_widget.addItem("推荐内容 2")
        self.list_widget.addItem("推荐内容 3")
        layout.addWidget(self.list_widget)

        # 创建QStackedWidget用于显示推荐内容
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # 创建推荐内容页面
        page1 = QWidget()
        page1_layout = QVBoxLayout()
        page1_label = QLabel("这是推荐内容 1", self)
        page1_layout.addWidget(page1_label)
        page1.setLayout(page1_layout)

        page2 = QWidget()
        page2_layout = QVBoxLayout()
        page2_label = QLabel("这是推荐内容 2", self)
        page2_layout.addWidget(page2_label)
        page2.setLayout(page2_layout)

        page3 = QWidget()
        page3_layout = QVBoxLayout()
        page3_label = QLabel("这是推荐内容 3", self)
        page3_layout.addWidget(page3_label)
        page3.setLayout(page3_layout)

        # 将推荐内容页面添加到QStackedWidget
        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)
        self.stacked_widget.addWidget(page3)

        # 连接QListWidget的信号与QStackedWidget的槽
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
