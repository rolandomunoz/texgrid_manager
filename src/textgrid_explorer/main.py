import mytextgrid
import subprocess
from importlib import resources

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTableView,
    QMenuBar,
    QToolBar,
    QVBoxLayout,
)
from PySide6.QtCore import (
    QSettings,
    QSortFilterProxyModel,
    Qt,
)

from PySide6.QtGui import (
    QAction,
    QIcon,
)

from textgrid_explorer.models import TGTableModel
from textgrid_explorer.dialogs import NewProjectDialog
from textgrid_explorer.dialogs import FilterView
from textgrid_explorer import utils

resources_dir = resources.files('textgrid_explorer.resources')
icon_dir = resources_dir / 'icons'
settings = QSettings('Gilgamesh', 'TGExplorer')
  
class EditorView(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        self.init_filter_view()

    def init_ui(self):
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)

        model = TGTableModel([])
        proxy_model = QSortFilterProxyModel(model)
        proxy_model.setSourceModel(model)
        self.table_view.setModel(proxy_model)

        box_layout = QVBoxLayout()
        box_layout.addWidget(self.table_view)
        self.setLayout(box_layout)

    def open_praat(self):
        indexes = self.table_view.selectedIndexes()
        if not indexes:
            return
        index = indexes[0]
        textgrid_path = index.data(Qt.ItemDataRole.UserRole)[0]
        sound_path = textgrid_path.with_suffix('.wav')
        interval = index.data(Qt.ItemDataRole.UserRole)[1]

        praat_path = r'Praat.exe'
        script_path = resources_dir / 'open_file.praat'
        subprocess.run(
            [praat_path, '--new-send', script_path, textgrid_path, sound_path, str(interval.xmin), str(interval.xmax)]
        )

    def init_filter_view(self):
        proxy_model = self.table_view.model()
        self.filter_dlg = FilterView(self, proxy_model)

    def view_filter(self, clicked):
        if clicked:
            self.filter_dlg.show()
        else:
            self.filter_dlg.hide()
            
    def load_textgrids_from_dir(self, src_dir, primary_tier, secondary_tiers):
        headers, data = utils.create_aligned_tier_table(
            src_dir, primary_tier, secondary_tiers
        )
        print(data)
        #model = self.table_view.model().sourceModel()
        #model.set_full_dataset(headers, data)
        #self.init_filter_view()

class TGExplorer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('TGExplorer')
        self.setMinimumSize(800, 500)
        #self.showMaximized()
        self.init_ui()
        self.init_dialogs()
        self.init_actions()
        self.init_menubar()
        self.init_toolbar()

    def init_session(self):
        data_dir = self.init_dlg.data_dir()
        settings.setValue('data_dir', data_dir)
        settings.setValue('dict_path', self.init_dlg.dict_path())

        self.editor_view.load_textgrids_from_dir(data_dir)

    def init_actions(self):
        """
        Create actions
        """
        self.new_project_act = QAction('&New project...', self)
        self.new_project_act.setShortcut('Ctrl+N')
        self.new_project_act.triggered.connect(self.on_new_project)

        self.open_project_act = QAction('&Open project...', self)
        self.open_project_act.setShortcut('Ctrl+O')
        self.new_project_act.triggered.connect(self.on_open_project)

        self.close_project_act = QAction('&Close project', self)
        self.new_project_act.triggered.connect(self.on_close_project)

        self.project_settings_act = QAction('&Project settings...', self)
        self.project_settings_act.setShortcut('Ctrl+R')
        self.new_project_act.triggered.connect(self.on_project_settings)

        self.open_praat_act = QAction('&Open selected in Praat', self)
        self.open_praat_act.setIcon(QIcon(str(icon_dir/'praat_icon.png')))
        self.open_praat_act.triggered.connect(self.editor_view.open_praat)
        self.open_praat_act.setShortcut('Alt+P')

        #self.quit_act = QAction('&Salir', self)
        #self.quit_act.triggered.connect(self.close)

        self.filter_act = QAction('&Filter', self)
        self.filter_act.setIcon(QIcon(str(icon_dir/'funnel.png')))
        self.filter_act.triggered.connect(self.editor_view.view_filter)
        self.filter_act.setShortcut('Ctrl+F')
        self.filter_act.setCheckable(True)

    def init_menubar(self):
        menu_bar = QMenuBar()

        file_bar = menu_bar.addMenu('&File')
        self.setMenuBar(menu_bar)
        file_bar.addAction(self.new_project_act)
        file_bar.addAction(self.open_project_act)
        file_bar.addAction(self.close_project_act)
        file_bar.addSeparator()
        file_bar.addAction(self.project_settings_act)

        edit_bar = menu_bar.addMenu('&Edit')
        self.setMenuBar(menu_bar)

        data_bar = menu_bar.addMenu('&Data')
        self.setMenuBar(menu_bar)
        data_bar.addAction(self.filter_act)
        data_bar.addAction(self.open_praat_act)

    def init_toolbar(self):
        data_toolbar = QToolBar(self)
        data_toolbar.addAction(self.open_praat_act)
        data_toolbar.addAction(self.filter_act)

        self.addToolBar(data_toolbar)

    def init_ui(self):
        self.editor_view = EditorView(self)
        self.setCentralWidget(self.editor_view)

    def init_dialogs(self):
        self.new_project_dlg = NewProjectDialog(self)
        self.new_project_dlg.finished.connect(self.load_project)

    def load_project(self, result):
        if result == 1:
            dict_ = self.new_project_dlg.data()
            self.editor_view.load_textgrids_from_dir(
                dict_['src_dir'],
                dict_['primary_tier'],
                dict_['secondary_tiers'],
            )

    def filter_table(self):
        pass

    def on_close_project(self):
        pass

    def on_new_project(self):
        self.new_project_dlg.open()

    def on_open_project(self):
        pass

    def on_project_settings(self):
        pass

def init_preferences():
    if not settings.contains('data_dir'):
        settings.setValue('data_dir', '')

    if not settings.contains('dict_path'):
        settings.setValue('dict_path', '')

    if not settings.contains('mode'):
        settings.setValue('mode', 'simple')

    if not settings.contains('praat_path'):
        settings.setValue('praat_path', '')

def run_app():
    init_preferences()

    app = QApplication([])
    app.setStyle('Fusion')
    main_window = TGExplorer()
    main_window.show()
    app.exec()
