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
    QWidget,
    QPushButton,
    QLineEdit,
    QCheckBox,
    QTabWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
)
from PySide6.QtCore import Qt

class PraatTab(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.path_ed = QLineEdit()
        self.maximize_audibility_checkbox = QCheckBox(
            'Maximize audibility'
        )

        form = QFormLayout()
        form.addRow('Path', self.path_ed)
        form.addRow(self.maximize_audibility_checkbox)
        self.setLayout(form)

    def data(self):
        PraatPreferences = namedtuple('PraatPreferences', ['path', 'maximize_audibility'])

        results = PraatPreferences(
            self.path_ed.text(),
            int(self.maximize_audibility_checkbox.isChecked()),
        )
        return results

    def set_data(self, praat_path=None, maximize_audibility=None):
        if not praat_path is None:
            self.path_ed.setText(praat_path)

        if not maximize_audibility is None:
            self.maximize_audibility_checkbox.setChecked(maximize_audibility)

class PreferencesDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        self.init_ui()

    def init_ui(self):
        self.praat_tab = PraatTab(self)

        tabs = QTabWidget(self)
        tabs.setTabPosition(QTabWidget.West)
        tabs.addTab(self.praat_tab, 'Praat')
        tabs.addTab(QWidget(), 'Others')

        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        hbox = QHBoxLayout()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        layout.addLayout(hbox)

        self.setLayout(layout)

    def data(self):
        praat = self.praat_tab.data()

        Preferences = namedtuple('Preferences', ['praat_path', 'praat_maximize_audibility'])
        prefs = Preferences(
            praat.path,
            praat.maximize_audibility,
        )
        return prefs

    def set_data(self, praat_path=None, praat_maximize_audibility=None):
        self.praat_tab.set_data(praat_path, praat_maximize_audibility)
