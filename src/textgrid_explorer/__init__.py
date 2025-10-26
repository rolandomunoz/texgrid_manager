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
import platform

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from textgrid_explorer.explorer_window import TGExplorer

def init_preferences():
    settings = QSettings('Gilgamesh', 'TGExplorer')

    if not settings.contains('data_dir'):
        settings.setValue('data_dir', '')

    if not settings.contains('dict_path'):
        settings.setValue('dict_path', '')

    if not settings.contains('praat/path'):
        praat_path = ''
        if platform.system() == 'Windows':
            praat_path = 'Praat.exe'
        elif platform.system() == 'Linux':
            praat_path = 'praat'
        elif platform.system() == 'Darwin':
            praat_path = 'praat'
        settings.setValue('praat/path', praat_path)

    if not settings.contains('praat/maximize_audibility'):
        settings.setValue('praat/maximize_audibility', 0)

def main():
    init_preferences()   
    app = QApplication([])
    app.setStyle('Fusion')
    main_window = TGExplorer()
    main_window.show()
    app.exec()
