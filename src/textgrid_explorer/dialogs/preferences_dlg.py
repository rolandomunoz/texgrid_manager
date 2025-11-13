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
        self.sound_extensions_ed = QLineEdit()
        self.maximize_audibility_checkbox = QCheckBox(
            'Maximize audibility'
        )
        self.plugins_checkbox = QCheckBox(
            'Activate plug-ins'
        )
        form = QFormLayout()
        form.addRow('Praat path:', self.path_ed)
        form.addRow('Sound extensions:', self.sound_extensions_ed)
        form.addRow(self.maximize_audibility_checkbox)
        form.addRow(self.plugins_checkbox)
        self.setLayout(form)

    def to_dict(self):
        dict_ = {
            'praat_path': self.path_ed.text(),
            'praat_sound_extensions': self.sound_extensions_ed.text(),
            'praat_maximize_audibility': self.maximize_audibility_checkbox.isChecked(),
            'praat_activate_plugins': self.plugins_checkbox.isChecked(),
        }
        return dict_

    def set_values(self, praat_path: str, praat_sound_extensions: str, maximize_audibility: bool, activate_plugins: bool) -> None:
        """
        Set widget values.
        """
        self.path_ed.setText(praat_path)
        self.sound_extensions_ed.setText(praat_sound_extensions)
        self.maximize_audibility_checkbox.setChecked(maximize_audibility)
        self.plugins_checkbox.setChecked(activate_plugins)

class PreferencesDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Preferences')
        self.setMinimumWidth(500)
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
        hbox.addStretch()
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        layout.addLayout(hbox)

        self.setLayout(layout)

    def to_dict(self):
        """
        Returns
        -------
        dict of {'path': str, 'maximize_audibility':bool, 'activate_plugins':bool}
        """
        praat_dict = self.praat_tab.to_dict()

        return praat_dict

    def set_values(self, praat_path: str, praat_sound_extensions: str, praat_maximize_audibility: bool, praat_activate_plugins: bool) -> None:
        self.praat_tab.set_values(
            praat_path,
            praat_sound_extensions,
            praat_maximize_audibility,
            praat_activate_plugins
        )
