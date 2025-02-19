# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SolvePannel.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

class Ui_Pannel(object):
    def setupUi(self, Pannel):
        if not Pannel.objectName():
            Pannel.setObjectName(u"Pannel")
        Pannel.resize(815, 617)
        self.verticalLayout_2 = QVBoxLayout(Pannel)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Pannel)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.West)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.demandTab = QWidget()
        self.demandTab.setObjectName(u"demandTab")
        self.horizontalLayout = QHBoxLayout(self.demandTab)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.demandView = QTableView(self.demandTab)
        self.demandView.setObjectName(u"demandView")

        self.horizontalLayout.addWidget(self.demandView)

        self.tabWidget.addTab(self.demandTab, "")
        self.capacityTab = QWidget()
        self.capacityTab.setObjectName(u"capacityTab")
        self.tabWidget.addTab(self.capacityTab, "")
        self.resultTab = QWidget()
        self.resultTab.setObjectName(u"resultTab")
        self.horizontalLayout_2 = QHBoxLayout(self.resultTab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.resultView = QTableView(self.resultTab)
        self.resultView.setObjectName(u"resultView")

        self.horizontalLayout_2.addWidget(self.resultView)

        self.tabWidget.addTab(self.resultTab, "")
        self.analysisTab = QWidget()
        self.analysisTab.setObjectName(u"analysisTab")
        self.tabWidget.addTab(self.analysisTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.workcenters = QComboBox(Pannel)
        self.workcenters.setObjectName(u"workcenters")

        self.horizontalLayout_3.addWidget(self.workcenters)

        self.horizontalSpacer = QSpacerItem(21, 22, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.statusLabel = QLabel(Pannel)
        self.statusLabel.setObjectName(u"statusLabel")

        self.horizontalLayout_3.addWidget(self.statusLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.startBtn = QPushButton(Pannel)
        self.startBtn.setObjectName(u"startBtn")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.CallStart))
        self.startBtn.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.startBtn)

        self.stopBtn = QPushButton(Pannel)
        self.stopBtn.setObjectName(u"stopBtn")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.CallStop))
        self.stopBtn.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.stopBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Pannel)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Pannel)
    # setupUi

    def retranslateUi(self, Pannel):
        Pannel.setWindowTitle(QCoreApplication.translate("Pannel", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.demandTab), QCoreApplication.translate("Pannel", u"Demand", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.capacityTab), QCoreApplication.translate("Pannel", u"Capacity", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.resultTab), QCoreApplication.translate("Pannel", u"Result", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analysisTab), QCoreApplication.translate("Pannel", u"Analysis", None))
        self.statusLabel.setText(QCoreApplication.translate("Pannel", u"TextLabel", None))
        self.startBtn.setText(QCoreApplication.translate("Pannel", u"start", None))
        self.stopBtn.setText(QCoreApplication.translate("Pannel", u"stop", None))
    # retranslateUi

