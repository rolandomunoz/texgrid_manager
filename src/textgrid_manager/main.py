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

from textgrid_manager.models import TGTableModel
from textgrid_manager.dialogs import InitWizard
from textgrid_manager.dialogs import FilterView
from textgrid_manager import utils

resources_dir = resources.files('textgrid_manager.resources')
icon_dir = resources_dir / 'icons'
settings = QSettings('Gilgamesh', 'TGManager')
  
class EditorView(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            
    def load_textgrids_from_dir(self, src_dir):
        headers, data = utils.create_aligned_tier_table(
            src_dir, 'text', ['gloss', 'id']
        )
        model = self.table_view.model().sourceModel()
        model.set_full_dataset(headers, data)
        self.init_filter_view()

class TGManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('TGManager')
        self.setMinimumSize(800, 500)
        #self.showMaximized()
        self.init_ui()
        self.init_actions()
        self.init_menubar()
        self.init_toolbar()

        # Init session
        self.init_dlg = InitWizard(self)
        self.init_dlg.set_data_dir(settings.value('data_dir'))
        self.init_dlg.set_dict_path(settings.value('dict_path'))
        self.init_dlg.accepted.connect(self.init_session)
        self.init_dlg.open()

    def init_session(self):
        data_dir = self.init_dlg.data_dir()
        settings.setValue('data_dir', data_dir)
        settings.setValue('dict_path', self.init_dlg.dict_path())

        self.editor_view.load_textgrids_from_dir(data_dir)

    def init_actions(self):
        """
        Create actions
        """
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

        files_bar = menu_bar.addMenu('&Files')
        self.setMenuBar(menu_bar)

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

    def filter_table(self):
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
    main_window = TGManager()
    main_window.show()
    app.exec()
