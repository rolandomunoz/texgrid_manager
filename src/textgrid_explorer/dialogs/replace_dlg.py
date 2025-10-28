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
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout
)

class FindAndReplaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Search and replace')
        self._fields = []
        self.init_ui()

    def init_ui(self):
        self.fields_box = QComboBox(self)
        self.fields_box.addItems(self._fields)

        self.search_ed = QLineEdit(self)
        self.replace_ed = QLineEdit(self)

        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        btn_box = QHBoxLayout()
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)

        main_box = QVBoxLayout()
        main_box.addWidget(QLabel('Column name:'))
        main_box.addWidget(self.fields_box)

        main_box.addWidget(QLabel('Find what:'))
        main_box.addWidget(self.search_ed)

        main_box.addWidget(QLabel('Replace with:'))
        main_box.addWidget(self.replace_ed)
        main_box.addLayout(btn_box)

        self.setLayout(main_box)

    def set_fields(self, fields):
        if not self._fields == fields:
            self._fields = fields
            self.fields_box.clear()
            self.fields_box.addItems(fields)

    def data(self):
        Result = namedtuple(
            'Results', ['field_index', 'field', 'search', 'replace']
        )
        r = Result(
            self.fields_box.currentIndex(),
            self.fields_box.currentText(),
            self.search_ed.text(),
            self.replace_ed.text()
        )
        return r

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

        self.search_ed = QLineEdit(self)
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
        form.addRow('Find what:', self.search_ed)
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
            'Results', ['src_column', 'src_column_index', 'dst_column', 'dst_column_index', 'search', 'replace']
        )
        src_column = self.src_tier_box.currentText()
        dst_column = self.dst_tier_box.currentText()
        
        r = Results(
            src_column,
            self._fields.index(src_column),
            dst_column,
            self._fields.index(dst_column),
            self.search_ed.text(),
            self.replace_ed.text(),
        )
        return r
