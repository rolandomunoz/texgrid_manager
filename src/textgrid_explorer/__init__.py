from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from textgrid_explorer.explorer_window import TGExplorer

def init_preferences():
    settings = QSettings('Gilgamesh', 'TGExplorer')

    if not settings.contains('data_dir'):
        settings.setValue('data_dir', '')

    if not settings.contains('dict_path'):
        settings.setValue('dict_path', '')

    if not settings.contains('mode'):
        settings.setValue('mode', 'simple')

    if not settings.contains('praat_path'):
        settings.setValue('praat_path', '')

def main():
    init_preferences()

    app = QApplication([])
    app.setStyle('Fusion')
    main_window = TGExplorer()
    main_window.show()
    app.exec()
