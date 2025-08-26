import json
from pathlib import Path
from importlib import resources

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
from textgrid_manager import utils

icons_dir = resources.files('textgrid_manager.resources') / 'fuge-icons'

class TGTableModel(QAbstractTableModel):

    def __init__(self, data=None):
        super().__init__()
        if data is None:
            data = []
        self._data = data
        self._headers = ['Filename', 'Tier', 'Text']
        self.update_data(self._data)

    def update_data(self, data):
        list_ = []
        for tg in data:
            for tier in tg:
                tier.parent = tg
                for item in tier:
                    if item.text == '':
                        continue
                    list_.append(item)
        self.beginResetModel()
        self._data = list_
        self.endResetModel()

    def rowCount(self, index=QModelIndex()):
        return len(self._data)

    def columnCount(self, index=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return

        if orientation == Qt.Orientation.Horizontal:
            return self._headers[section]
        return section+1

    def data(self, index=QModelIndex(), role=Qt.ItemDataRole.DisplayRole):
        row, column = index.row(), index.column()
        item = self._data[row]

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if column == 0: # File
                return item.parent.parent.path.name

            elif column == 1: # tier
                return item.parent.name

            elif column == 2: # Text
                return item.text

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role != Qt.ItemDataRole.EditRole:
            return

        column, row = index.column(), index.row()
        if column == 2: # Text
            item = self._data[row]
            item.text = value
            item.parent.parent.write(item.parent.parent.path)
            print(item.parent.parent.path)
            return True

    def append_data(self, dict_):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(dict_)
        row = len(self._data) - 1
        self.save(row)
        self.endInsertRows()

    def flags(self, index=QModelIndex()):
        myflags = Qt.ItemFlag.ItemIsSelectable|Qt.ItemFlag.ItemIsEnabled 
        if index.column() == 2:
            return myflags|Qt.ItemFlag.ItemIsEditable
        return myflags

    def data_collection(self):
        return self._data

