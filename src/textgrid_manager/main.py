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
from textgrid_manager import dialogs
from textgrid_manager import utils

resources_dir = resources.files('textgrid_manager.resources')
icon_dir = resources_dir / 'icons'
settings = QSettings('Gilgamesh', 'TGManager')

class EditorView(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.tableview = QTableView()
        self.tableview.setSortingEnabled(True)

        model = TGTableModel([])
        proxy_model = QSortFilterProxyModel(model)
        proxy_model.setSourceModel(model)
        self.tableview.setModel(proxy_model)

        #proxy_model.setFilterRegularExpression("text")
        #proxy_model.setFilterKeyColumn(1)

        box_layout = QVBoxLayout()
        box_layout.addWidget(self.tableview)
        self.setLayout(box_layout)

    def open_praat(self):
        indexes = self.tableview.selectedIndexes()
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

    def load_textgrids_from_dir(self, src_dir):
        headers, data = utils.create_aligned_tier_table(
            src_dir, 'text', ['gloss', 'id']
        )
        model = self.tableview.model().sourceModel()
        model.set_full_dataset(headers, data)

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
        self.init_dlg = dialogs.InitWizard(self)
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
        #self.filter_act.setIcon(QIcon(gear_icon_path.as_posix()))
        #self.filter_act.triggered.connect(self.show_config)
        self.filter_act.setShortcut('F')

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

        self.addToolBar(data_toolbar)

    def init_ui(self):
        self.editor_view = EditorView()
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
