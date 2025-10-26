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
from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

class FilterByDialog(QDialog):

    def __init__(self, parent, fields=None, default_value=''):
        super().__init__(parent)
        self._fields = fields
        self.default_value = default_value
        if fields is None:
            self._fields = []
        self.setWindowTitle('Filter by')
        self.init_ui()

    def init_ui(self):
        # Headers
        self.headers_box = QComboBox(self)
        self.headers_box.addItems(self._fields)

        self.line_ed = QLineEdit(self.default_value, self)
        self.line_ed.setPlaceholderText('Regex expression')

        # Buttons
        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.headers_box)
        layout.addWidget(self.line_ed)
        layout.addLayout(hbox)

        self.setLayout(layout)

    def fields(self):
        return self._fields

    def set_fields(self, fields):
        if not self._fields == fields:
            self._fields = fields
            self.headers_box.clear()
            self.headers_box.addItems(self._fields)

    def data(self):
        field_index = -1
        field_name = self.headers_box.currentText()
        if field_name in self._fields:
            field_index = self._fields.index(field_name)
        field_value = self.line_ed.text()
        return field_index, field_value

class FilterView(QDialog):

    def __init__(self, parent, proxy_model=None):
        super().__init__(parent)
        self.setWindowTitle('Filter')
        self.proxy_model = proxy_model
        self.init_ui()

    def init_ui(self):
        # Headers
        ncols = self.proxy_model.columnCount()
        orientation = Qt.Orientation.Horizontal
        headers = [self.proxy_model.headerData(i, orientation) for i in range(ncols)]

        # Filter form
        self.form = QFormLayout()
        for header_str in headers:
            editor = QLineEdit(self)
            editor.setPlaceholderText('Insert value')
            self.form.addRow(header_str, editor)

        # Buttons
        filter_btn = QPushButton('Filter', self)
        filter_btn.clicked.connect(self.filter_rows)

        reset_btn = QPushButton('Reset', self)

        hbox = QHBoxLayout()
        hbox.addWidget(filter_btn)
        hbox.addWidget(reset_btn)

        # Main Layout
        layout = QVBoxLayout()
        layout.addLayout(self.form)
        layout.addLayout(hbox)
        self.setLayout(layout)

    def filter_rows(self):
        for i in range(self.form.rowCount()):
            editor = self.form.itemAt(i, QFormLayout.FieldRole).widget()
            expression = editor.text()
            if expression:
                self.proxy_model.setFilterRegularExpression(expression)
                self.proxy_model.setFilterKeyColumn(i)
