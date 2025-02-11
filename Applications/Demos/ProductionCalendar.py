from __future__ import annotations

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPoint, QRect, QSize,
    QObject, Signal, Slot,
    Qt, QEvent
)

from PySide6.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QTableView,
    QApplication,
    QHeaderView,
    QToolTip,
    QMenu
)

from PySide6.QtGui import (
    QMouseEvent, QColor, QPainter, QCursor, QAction
)

from qt_material import apply_stylesheet, list_themes

import sys, os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)
from Interface.Interface import TimeLineUnit


class MultiHeaderView(QHeaderView):
    def __init__(
            self,
            orientation: Qt.Orientation,
            rows: int,
            columns: int,
            parent: QWidget=None
    ) -> None:
        QHeaderView.__init__(self, orientation, parent)
        pass

    def setRowHeight(
            self, row: int, rowHeight: int
    ) -> None:
        pass

    def setColumnsWidth(
            self, col: int, colWidth: int
    ) -> None:
        pass

    def setSpan(
            self,
            row: int,
            column: int,
            rowSpanCount: int,
            columnSpanCount: int
    ) -> None:
        pass

    def setCellBackgroundColor(
            self, index: QModelIndex, color: QColor
    ) -> None:
        pass

    def setCellForegroundColor(
            self, index: QModelIndex, color: QColor
    ) -> None:
        pass

    def mousePressEvent(
            self, event: QMouseEvent
    ) -> None:
        pass

    def indexAt(self, point: QPoint) -> QModelIndex:
        pass

    def paintSection(
            self,
            painter: QPainter,
            rect: QRect,
            logicalIndex: int
    ) -> None:
        pass

    def sectionSizeFromContents(
            self, logicalIndex: int
    ) -> QSize:
        pass

    def columnSpanIndex(
            self, currentIndex: QModelIndex
    ) -> QModelIndex:
        pass

    def rowSpanIndex(
            self, currentIndex: QModelIndex
    ) -> QModelIndex:
        pass

    def columnSpanSize(
            self, row: int, From: int, spanCount: int
    ) -> int:
        pass

    def rowSpanSize(
            self, column: int, From: int, spanCount: int
    ) -> int:
        pass

    def getSectionRange(
            self,
            index: QModelIndex,
            beginSection: int,
            endSection: int
    ) -> int:
        pass

    # slots:
    def onSectionResized(
            self, logicalIndex: int, oldSize: int, newSize: int
    ) -> None:
        pass

    # signals:
    def sectionRressed(
            self, From: int, To: int
    ) -> None:
        pass


class CalendarModel(QAbstractTableModel):

    def __init__(
            self, *, days: int=1, hours: int=24, parent=None
    ) -> None:
        QAbstractTableModel.__init__(self, parent)
        self._days = days
        self._hours = hours

    def data(
            self,
            index: QModelIndex,
            role: Qt.ItemDataRole
    ) -> None:
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            pass

        return None

    def rowCount(self, parent=QModelIndex()) -> int:
        return self._days

    def columnCount(self, parent=QModelIndex()) -> int:
        return self._hours

    def headerData(
            self,
            section: int,
            orientation: Qt.Orientation,
            role: Qt.ItemDataRole
    ):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(section)

            if orientation == Qt.Orientation.Vertical:
                return str(section + 1)

        return None


class CalendarView(QTableView):
    def __init__(self, parent=None):
        """ Multi-header_view & column selector
            每一行对应一个班次
        """

        QTableView.__init__(self, parent)
        self.installEventFilter(self)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableView.SelectItems)
        # self.horizontalHeader().setStretchLastSection(True)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setMinimumSectionSize(24)
        self.horizontalHeader().setDefaultSectionSize(24)

        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setMinimumSectionSize(24)
        self.verticalHeader().setDefaultSectionSize(24)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # self.setAcceptHoverEvents(True)
        self.setAttribute(Qt.WA_Hover, True)
        # self.setMouseTracking(True)
        # self.entered.connect(self.showTooltip)

    @Slot(QModelIndex)
    def showTooltip(obj: QWidget) -> None:
        pos = QCursor.pos()
        QToolTip.showText(
            pos,
            f"row: {obj.rowAt(pos.y())}, column: {obj.columnAt(pos.x())}"
        )

    def on_context_menu(self, pos):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))

        context.exec(self.mapToGlobal(pos))

    # def hoverEnterEvent(self, e):
    #     pirnt('inside')

    # def hoverLeaverEvent(self, e):
    #     print('outside')

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        if o == self:
            if e.type() == QEvent.Enter:
                print(f'*************** {e.type()}')
                return True
            elif e.type() == QEvent.HoverLeave:
                print(f'^^^^^^^^^^^^^^^ {e.type()}')
                return True
            else:
                print(f'############### {e.type()}')
        else:
            print('.................')

        return super().eventFilter(o, e)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("OpenAPS")
    # window.setToolTip('Tip Info 这是按钮的提示信息')
    layout = QVBoxLayout()

    window.resize(800, 600)

    # setup stylesheet
    apply_stylesheet(app, theme='dark_teal.xml')
    # apply_stylesheet(app, theme='dark_cyan.xml')
    # print(list_themes())

    days = 10
    model = CalendarModel(days=days)
    view = CalendarView(window)
    view.setModel(model)
    layout.addWidget(view)
    # view.resizeColumnsToContents()
    # view.resizeRowsToContents()
    # view.resize(800, 600)
    view.clearSpans()

    # hheader = view.horizontalHeader()
    # for i in range(hheader.count()):
    #     key = hheader.model().headerData(
    #         i, Qt.Horizontal, Qt.ItemDataRole.DisplayRole
    #     )
    #     toolTip = str(key)
    #     view.horizontalHeaderItem(i).setToolTip(toolTip)

    # selected_indexes = view.selectionModel().selectedIndexes()
    # selected_rows = set(index.row() for index in selected_indexes)
    # for row_index in selected_rows:
    #     print('Row:', row_index + 1)
    #     for column_index in range(model.columnCount()):
    #         item = model.item(row_index, column_index)
    #         print('Column:', column_index + 1, 'Value:', item.text())
    # print('----------------------')

    window.setLayout(layout)
    window.setCentralWidget(view)
    window.show()

    sys.exit(app.exec())
