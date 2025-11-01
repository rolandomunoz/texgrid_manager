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
from PySide6.QtCore import (
    Qt,
    Signal,
    Slot,
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
        form.addRow('In c&olumn:', self.column_box)
        form.addRow('Fi&nd what:', self.find_ed)
        form.addRow('Re&place with:', self.replace_ed)

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
        form.addRow('In c&olumn:', self.column_box)
        form.addRow('Fi&nd what:', self.find_ed)

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
    my_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Find and replace')
        self.setMinimumWidth(500)
        self._fields = []
        self.init_ui()

    def init_ui(self):
        self.replace_tab = ReplaceTab(self)
        self.find_tab = FindTab(self)

        # Connect through signal and slots widgets of the find and replace tabs
        self.find_tab.column_box.currentIndexChanged.connect(self.replace_tab.column_box.setCurrentIndex)
        self.replace_tab.column_box.currentIndexChanged.connect(self.find_tab.column_box.setCurrentIndex)

        self.find_tab.find_ed.textChanged.connect(self.replace_tab.find_ed.setText)
        self.replace_tab.find_ed.textChanged.connect(self.find_tab.find_ed.setText)

        # Add tabs
        self.tabs = QTabWidget(self)
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.addTab(self.find_tab, '&Find')
        self.tabs.addTab(self.replace_tab, 'R&eplace')
        self.tabs.currentChanged.connect(self.display_tab)

        # Control panel
        self.replace_all_btn = QPushButton('Replace &all')
        self.replace_all_btn.clicked.connect(lambda: self.done(2))
        self.replace_all_btn.hide()

        self.replace_btn = QPushButton('&Replace')
        self.replace_btn.clicked.connect(lambda: self.done(3))
        self.replace_btn.hide()

        self.find_all_btn = QPushButton('F&ind all')
        self.find_all_btn.clicked.connect(lambda: self.done(4))

        self.find_next_btn = QPushButton('Find &next')
        self.find_next_btn.setDefault(True)
        self.find_next_btn.clicked.connect(lambda: self.done(5))

        close_btn = QPushButton('&Close')
        close_btn.clicked.connect(self.reject)

        # Layout
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.replace_all_btn)
        hbox.addWidget(self.replace_btn)
        hbox.addSpacing(10)
        hbox.addWidget(self.find_all_btn)
        hbox.addWidget(self.find_next_btn)
        hbox.addSpacing(10)
        hbox.addWidget(close_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addLayout(hbox)

        self.setLayout(layout)

    @Slot(int)
    def display_tab(self, index):
        self.tabs.setCurrentIndex(index)
        if index == 0:
            self.replace_btn.hide()
            self.replace_all_btn.hide()
        elif index == 1:
            self.replace_btn.show()
            self.replace_all_btn.show()

    def set_find_field(self, value):
        self.find_tab.set_find_field(value)
        self.replace_tab.set_find_field(value)

    def set_column_field(self, column_names, index=-1):
        self.find_tab.set_column_field(column_names, index)
        self.replace_tab.set_column_field(column_names, index)

    def data(self):
        return self.replace_tab.data()

    def done(self, r):
        """
        Customize to emit multiple choices depending on the clicked button.
        Aditionally, close the Dialog only if `0` or `1` (traditionally
        reject and accept) values are passed.

        Parameters
        ----------
        r : int
            The clicked button value.
        """
        self.my_clicked.emit(r)

        if r in (0, 1):
            super().done(r)

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
