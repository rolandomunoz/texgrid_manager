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
