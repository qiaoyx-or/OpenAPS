from __future__ import annotations

import pandas as pd
# from numpy import isnumeric
from pandas.api.types import is_numeric_dtype

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex


class PandasModel(QAbstractTableModel):
    def __init__(
            self, df: pd.DataFrame, parent: QWidget=None
    ) -> None:
        """A model to interface a Qt view with pandas dataframe """

        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """

        if parent == QModelIndex():
            return self._df.shape[0]
        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """

        if parent == QModelIndex():
            return self._df.shape[1]
        return 0

    def data(
            self,
            index: QModelIndex,
            role: Qt.ItemDataRole=Qt.DisplayRole
    ):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """

        if not index.isValid():
            return None

        value = self._df.iloc[index.row(), index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if is_numeric_dtype(value):
                return Qt.AlignmentFlag.AlignRight
            else:
                return Qt.AlignmentFlag.AlignCenter

        return None

    def headerData(
            self,
            section: int,
            orientation: Qt.Orientation,
            role: Qt.ItemDataRole=Qt.DisplayRole
    ):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as
        horizontal header data.
        """

        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._df.columns[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(self._df.index[section])

        return None
