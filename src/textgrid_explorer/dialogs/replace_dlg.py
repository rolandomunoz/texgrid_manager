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
from collections import namedtuple

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout
)

class ReplaceTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._columns = []
        self.init_ui()

    def init_ui(self):
        self.column_box = QComboBox(self)
        self.find_ed = QLineEdit(self)
        self.replace_ed = QLineEdit(self)

        form = QFormLayout()
        form.addRow('Fi&nd what', self.find_ed)
        form.addRow('Re&place with', self.replace_ed)
        form.addRow('In c&olumn', self.column_box)

        self.setLayout(form)

    def set_find_field(self, value):
        self.find_ed.setText(value)

    def set_replace_field(self, value):
        self.replace_ed.setText(value)

    def set_column_field(self, column_names, index=-1):
        if not self._columns == column_names:
            self._columns = column_names
            self.column_box.clear()
            self.column_box.addItems(column_names)
        self.column_box.setCurrentIndex(index)

    def find_field(self):
        return self.find_ed.text()

    def replace_field(self):
        return self.replace_ed.text()

    def current_column_field(self):
        return self.column_box.currentText()

    def data(self):
        # Deprecated
        Result = namedtuple(
            'Results', ['field_index', 'field', 'find', 'replace']
        )
        r = Result(
            self.column_box.currentIndex(),
            self.column_box.currentText(),
            self.find_ed.text(),
            self.replace_ed.text()
        )
        return r

class FindTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self._columns = []

    def init_ui(self):
        self.column_box = QComboBox(self)
        self.find_ed = QLineEdit(self)

        form = QFormLayout()
        form.addRow('Fi&nd what', self.find_ed)
        form.addRow('In c&olumn', self.column_box)

        self.setLayout(form)

    def set_find_field(self, value):
        self.find_ed.setText(value)

    def set_column_field(self, column_names, index=-1):
        if not self._columns == column_names:
            self._columns = column_names
            self.column_box.clear()
            self.column_box.addItems(column_names)
        self.column_box.setCurrentIndex(index)

    def find_field(self):
        return self.find_ed.text()

    def current_column_field(self):
        return self.column_box.currentText()

class FindAndReplaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Find and replace')
        self.setMinimumWidth(500)
        self._fields = []
        self.init_ui()

    def init_ui(self):
        self.replace_tab = ReplaceTab(self)
        self.find_tab = FindTab(self)

        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.addTab(self.find_tab, '&Find')
        self.tabs.addTab(self.replace_tab, '&Replace')

        ok_btn = QPushButton('&Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('&Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(hbox)

        self.setLayout(layout)

    def set_find_field(self, value):
        self.find_tab.set_find_field(value)
        self.replace_tab.set_find_field(value)

    def set_column_field(self, column_names, index=-1):
        self.find_tab.set_column_field(column_names, index)
        self.replace_tab.set_column_field(column_names, index)

    def set_fields(self, fields):
        self.replace_tab.set_fields(fields)

    def set_current_tab(self, index):
        self.tabs.setCurrentIndex(index)

    def data(self):
        return self.replace_tab.data()

class MapAnnotationDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Map Annotation')
        self._fields = []
        self.init_ui()

    def init_ui(self):
        self.src_tier_box = QComboBox(self)
        self.src_tier_box.addItems(self._fields)
        self.src_tier_box.currentTextChanged.connect(self.on_dst_tier)

        self.dst_tier_box = QComboBox(self)
        #self.dst_tier_box.addItems(self._fields)

        self.find_ed = QLineEdit(self)
        self.replace_ed = QLineEdit(self)

        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        btn_box = QHBoxLayout()
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)

        form = QFormLayout()
        form.addRow('From:', self.src_tier_box)
        form.addRow('To:', self.dst_tier_box)
        form.addRow('Find what:', self.find_ed)
        form.addRow('Replace with:', self.replace_ed)

        main_box = QVBoxLayout()
        main_box.addLayout(form)
        main_box.addLayout(btn_box)

        self.setLayout(main_box)

    def set_fields(self, fields):
        if not self._fields == fields:
            self._fields = fields
            self.src_tier_box.clear()
            self.src_tier_box.addItems(fields)

    def on_dst_tier(self):
        selected_text = self.src_tier_box.currentText()
        dst_fields = [f for f in self._fields if f != selected_text]
        self.dst_tier_box.clear()
        self.dst_tier_box.addItems(dst_fields)

    def data(self):
        Results = namedtuple(
            'Results', ['src_column', 'src_column_index', 'dst_column', 'dst_column_index', 'find', 'replace']
        )
        src_column = self.src_tier_box.currentText()
        dst_column = self.dst_tier_box.currentText()
        
        r = Results(
            src_column,
            self._fields.index(src_column),
            dst_column,
            self._fields.index(dst_column),
            self.find_ed.text(),
            self.replace_ed.text(),
        )
        return r
