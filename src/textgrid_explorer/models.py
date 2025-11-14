#!/usr/bin/env python
#   textgrid_explorer - A TextGrid editing tool with a spreadsheet interface
#   Copyright (C) 2025 Rolando Muñoz <rolando.muar@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License version 3, as published
#   by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranties of
#   MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.
import re

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    QDate,
)
from PySide6.QtGui import (
    QPixmap,
    QIcon,
    QColor,
    QBrush
)

class TGTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._data = []
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
        """
        Underlying data structure is a list.
        [
            `pathlib.Path`, # Item from TextGrid property
            `mytextgrid.Interval`, # Item from primary tier
            `mytextgrid.Interval` or None, # Items from secondary tiers
            ...
            `mytextgrid.Interval` or None, # Items from secondary tiers
        ]
        """
        row, column = index.row(), index.column()
        item = self._data[row][column]

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0: # first column is `pathlib.Path` object
                return item.name

            if item is None: # Item is None
                return ''

            return item.text # `Interval` object

        elif role == Qt.ItemDataRole.BackgroundRole:
            if item is None:
                return QBrush(QColor('lightGray'))
            return QBrush(QColor('white'))

        elif role == Qt.ForegroundRole.ForegroundRole:
            if column > 0 and item is not None:
                if item.modified:
                    return QBrush(QColor('blue'))
            return QBrush(QColor('black'))

        elif role == Qt.ItemDataRole.EditRole:
            if column == 0:
                return item.name

            if item is None:
                return ''

            return item.text

        elif role == Qt.ItemDataRole.UserRole:
            return item

        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False

        if role == Qt.ItemDataRole.EditRole:
            if index.column() == 0: # pathlib.Path
                return False

            column, row = index.column(), index.row()
            item = self._data[row][column]

            if item is None:
                return False

            if item.text == value:
                return False

            item.text = value
            item.modified = True
            self._data[row][column] = item

            self.dataChanged.emit(index, index)
            return True

        elif role == Qt.ForegroundRole.ForegroundRole:
            row, col = index.row(), index.column()
            self._data[row][col].modified = value
            self.dataChanged.emit(index, index)
            return True

        elif role == Qt.ItemDataRole.UserRole:
            row, col = index.row(), index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index)
            return True

        return False

    def append_data(self, dict_):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(dict_)
        row = len(self._data) - 1
        self.save(row)
        self.endInsertRows()

    def flags(self, index=None):
        if index is None:
            index = QModelIndex()

        my_flags = super().flags(index)

        if index.column() == 0:
            return my_flags

        column, row = index.column(), index.row()
        item = self._data[row][column]
        if item is None:
            return my_flags
        return my_flags|Qt.ItemFlag.ItemIsEditable

    def replace(self, indexes, pattern, repl):
        p = re.compile(pattern)
        for index in indexes:
            item_str = index.data()
            if not p.search(item_str):
                continue
            new_str = p.sub(repl, item_str)
            self.setData(index, new_str)

    def replace_all(self, pattern, repl, src_column, dst_column=-1):
        '''
        Searches for a regex pattern in one column and replaces the matching
        substrings in another column with a specified replacement string.

        Parameters
        ----------
        pattern : str
            The regular expression (regex) pattern to search for in the source column's strings.
        repl : str
            The replacement string. This is substituted for all non-overlapping
            occurrences of the pattern in the source string.
        src_column : int
            The zero-based index of the column whose cell data is used to
            perform the search.
        dst_column : int, default -1
            The zero-based index of the column where the new, potentially
            modified, string value will be written. If -1, the the value is
            equal to src_column
        '''
        p = re.compile(pattern)

        if dst_column == -1:
            dst_column = src_column

        for irow in range(self.rowCount()):
            src_index = self.index(irow, src_column)
            dst_index = self.index(irow, dst_column)

            src_str = src_index.data()
            if p.search(src_str):
                new_str = p.sub(repl, src_str)
                self.setData(dst_index, new_str)
        p = re.compile(pattern)

        for irow in range(self.rowCount()):
            src_index = self.index(irow, src_column)
            dst_index = self.index(irow, dst_column)

            src_str = src_index.data()
            if p.search(src_str):
                new_str = p.sub(repl, src_str)
                self.setData(dst_index, new_str)

    def data_collection(self):
        return self._data
