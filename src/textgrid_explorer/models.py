import json
import re
from pathlib import Path
from importlib import resources
from pprint import pprint

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QDate,
)
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QColor
)
from textgrid_explorer import utils

icons_dir = resources.files('textgrid_explorer.resources') / 'fuge-icons'

class TGTableModel(QAbstractTableModel):

    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = []
        self._data = data
        self._headers = []

    def set_full_dataset(self, headers, new_data):
        self.beginResetModel()
        self._headers = headers
        self._data = new_data
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if not role == Qt.ItemDataRole.DisplayRole:
            return

        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return section+1

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole):
        row, column = index.row(), index.column()
        item = self._data[row][column]

        if item is None:
            return ''

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return item.name
            else:
                return item.text

        if role == Qt.ItemDataRole.EditRole:
            if column > 0:
                return item.text

        if role == Qt.ItemDataRole.UserRole:
            return self._data[row]

        return

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role != Qt.ItemDataRole.EditRole:
            return

        column, row = index.column(), index.row()

        if column > 0: # Text
            item = self._data[row][column]
            if item is None:
                return False
            item.text = value
            item.parent.parent.write(item.parent.parent._path)
            return True
        return False

    def append_data(self, dict_):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(dict_)
        row = len(self._data) - 1
        self.save(row)
        self.endInsertRows()

    def flags(self, index=QModelIndex()):
        myflags = Qt.ItemFlag.ItemIsSelectable|Qt.ItemFlag.ItemIsEnabled 
        if index.column() > 0:
            return myflags|Qt.ItemFlag.ItemIsEditable
        return myflags

    def search_and_replace(self, column, search, replace):
        p = re.compile(search)

        for irow in range(self.rowCount()):
            index = self.index(irow, column)
            old_value = index.data()

            new_value = re.sub(search, replace, old_value)
            self.setData(index, new_value)

    def data_collection(self):
        return self._data
