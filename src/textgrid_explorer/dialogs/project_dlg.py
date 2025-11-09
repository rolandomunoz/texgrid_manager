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
    QFileDialog,
    QListWidgetItem,
    QListWidget,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from textgrid_explorer import utils

class NewProjectDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('New Project Settings')
        self.setMinimumWidth(500)
        self._tiers = []

    def init_ui(self):
        self.textgrid_dir_ed = QLineEdit('')
        textgrid_dir_btn = QPushButton('...')
        textgrid_dir_btn.clicked.connect(self._on_textgrid_dir_btn)

        update_btn = QPushButton('&Scan TextGrid files', self)
        update_btn.clicked.connect(self.on_scan_tiers)

        self.primary_tier = QComboBox(self)
        self.primary_tier.currentTextChanged.connect(self._on_primary_tier)
        self.secondary_tiers = QListWidget(self)

        self.ok_btn = QPushButton('&Ok', self)
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setEnabled(False)

        cancel_btn = QPushButton('&Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        # Layout
        ## Source directory panel
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.textgrid_dir_ed)
        dir_layout.addWidget(textgrid_dir_btn)

        source_layout = QVBoxLayout()
        source_layout.addLayout(dir_layout)
        source_layout.addWidget(update_btn)
        source_groupbox = QGroupBox('TextGrid directory:')
        source_groupbox.setLayout(source_layout)

        ## Table panel
        table_layout = QVBoxLayout()
        table_layout.addWidget(QLabel('Primary tier'))
        table_layout.addWidget(self.primary_tier)
        table_layout.addWidget(QLabel('Secondary tiers'))
        table_layout.addWidget(self.secondary_tiers)
        self.table_groupbox = QGroupBox('Build Table:')
        self.table_groupbox.setLayout(table_layout)
        self.table_groupbox.setEnabled(False)

        ## Control panel
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addStretch()
        ctrl_layout.addWidget(self.ok_btn)
        ctrl_layout.addWidget(cancel_btn)

        # Main Layout
        main_box = QVBoxLayout()
        main_box.addWidget(source_groupbox)
        main_box.addWidget(self.table_groupbox)
        main_box.addLayout(ctrl_layout)
        self.setLayout(main_box)

    def on_scan_tiers(self):
        src_dir_str = self.textgrid_dir_ed.text()
        src_dir = Path(src_dir_str)

        if not src_dir.is_absolute() or not src_dir.is_dir():
            self.table_groupbox.setEnabled(False)
            self.ok_btn.setEnabled(False)
            QMessageBox.information(
                self,
                'Oops',
                'The <b>TextGrid directory</b> does not exist'
            )
            return
        self.table_groupbox.setEnabled(True)
        self.ok_btn.setEnabled(True)
        self._tiers = utils.get_tier_names(src_dir)

        self.primary_tier.clear()
        self.primary_tier.addItems(self._tiers)

    def _on_primary_tier(self, text):
        self.secondary_tiers.clear()
        for t in self._tiers:
            if t == text:
                continue
            item = QListWidgetItem(t)
            item.setFlags(item.flags()|Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.secondary_tiers.addItem(item)

    def _on_textgrid_dir_btn(self):
        dir_str = QFileDialog.getExistingDirectory(
            self,
            'Select a folder with TextGrid files',
            Path().home().as_posix(),
        )
        if not dir_str == '':
            self.textgrid_dir_ed.setText(dir_str)

    def accept(self):
        # Check inserted values
        src_dir = Path(self.textgrid_dir_ed.text())
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
            'src_dir': self.textgrid_dir_ed.text(),
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
