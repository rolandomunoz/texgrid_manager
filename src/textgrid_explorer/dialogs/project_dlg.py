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
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QPushButton,
    QListWidgetItem,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from textgrid_explorer import utils

class NewProjectDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('New Project settings')
        self._tiers = []

    def init_ui(self):
        self.textgrid_dir = QLineEdit(r'', self)
        update_btn = QPushButton('&Scan TextGrid files', self)
        update_btn.clicked.connect(self.on_scan_tiers)

        self.primary_tier = QComboBox(self)
        self.primary_tier.currentTextChanged.connect(self.on_primary_tier)
        self.secondary_tiers = QListWidget(self)

        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        btn_box = QHBoxLayout()
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)

        main_box = QVBoxLayout()
        main_box.addWidget(QLabel('TextGrid directory:'))
        main_box.addWidget(self.textgrid_dir)
        main_box.addWidget(update_btn)

        main_box.addWidget(QLabel('Build Table:'))
        main_box.addWidget(QLabel('Primary tier'))
        main_box.addWidget(self.primary_tier)
        main_box.addWidget(QLabel('Secondary tiers'))
        main_box.addWidget(self.secondary_tiers)
        main_box.addLayout(btn_box)

        self.setLayout(main_box)

    def on_scan_tiers(self):
        self._tiers = utils.get_tier_names(self.textgrid_dir.text())

        self.primary_tier.clear()
        self.primary_tier.addItems(self._tiers)

    def on_primary_tier(self, text):
        self.secondary_tiers.clear()
        for t in self._tiers:
            if t == text:
                continue
            item = QListWidgetItem(t)
            item.setFlags(item.flags()|Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.secondary_tiers.addItem(item)

    def accept(self):
        # Check inserted values
        src_dir = Path(self.textgrid_dir.text())
        if not src_dir.is_absolute() or not src_dir.is_dir():
            QMessageBox.warning(self, 'Ups!', 'The TextGrid directory does not exist!')
            return

        if self.primary_tier.currentText() == '':
            QMessageBox.warning(self, 'Ups!', 'Select a primary tier!')
            return
        super().accept()

    def data(self):
        tiers = []
        for i in range(self.secondary_tiers.count()):
            item = self.secondary_tiers.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                tiers.append(item.text())

        dict_ = {
            'src_dir': self.textgrid_dir.text(),
            'primary_tier': self.primary_tier.currentText(),
            'secondary_tiers': tiers
        }
        return dict_

class OpenProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

class ProjectSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
