import subprocess
from importlib import resources

from PySide6.QtWidgets import (
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
from textgrid_explorer.dialogs import FilterByDialog
from textgrid_explorer.dialogs import SearchAndReplaceDialog
from textgrid_explorer.dialogs import MapAnnotationDialog
from textgrid_explorer.dialogs import PreferencesDialog
from textgrid_explorer import utils

resources_dir = resources.files('textgrid_explorer.resources')
icon_dir = resources_dir / 'icons'
settings = QSettings('Gilgamesh', 'TGExplorer')
  
class EditorView(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

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

        praat_path = settings.value('praat/path')
        praat_maximize_audibility = settings.value('praat/maximize_audibility')
        script_path = resources_dir / 'open_file.praat'
        subprocess.run(
            [praat_path, '--hide-picture', '--new-send', script_path, textgrid_path, sound_path, str(praat_maximize_audibility), str(interval.xmin), str(interval.xmax)]
        )

    def filter_rows(self, key_column, str_expression):
        proxy_model = self.table_view.model()
        proxy_model.setFilterKeyColumn(key_column)
        proxy_model.setFilterRegularExpression(str_expression)

    def load_textgrids_from_dir(self, src_dir, primary_tier=None, secondary_tiers=None):
        if primary_tier is None:
            primary_tier = []

        if secondary_tiers is None:
            secondary_tiers = []

        headers, data = utils.create_aligned_tier_table(
            src_dir, primary_tier, secondary_tiers
        )
        model = self.table_view.model().sourceModel()
        model.set_full_dataset(headers, data)

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
        self.on_enabled_buttons(False)

    def init_actions(self):
        """
        Create actions
        """
        self.preferences_act = QAction('&Preferences...', self)
        self.preferences_act.triggered.connect(self.open_preferences_dlg)
        #self.preferences_act.setIcon(QIcon(str(icon_dir/'preferences-desktop.png')))

        self.new_project_act = QAction('&New project...', self)
        self.new_project_act.setShortcut('Ctrl+N')
        self.new_project_act.triggered.connect(self.new_project_dlg.open)

        self.open_project_act = QAction('&Open project...', self)
        self.open_project_act.setShortcut('Ctrl+O')
        self.open_project_act.triggered.connect(self.on_open_project)

        self.close_project_act = QAction('&Close project', self)
        self.close_project_act.triggered.connect(self.on_close_project)

        self.project_settings_act = QAction('&Project settings...', self)
        self.project_settings_act.setShortcut('Ctrl+R')
        self.project_settings_act.triggered.connect(self.on_project_settings)

        self.open_praat_act = QAction('&Open selection in Praat', self)
        self.open_praat_act.setIcon(QIcon(str(icon_dir/'praat_icon.png')))
        self.open_praat_act.triggered.connect(self.editor_view.open_praat)
        self.open_praat_act.setShortcut('Alt+P')

        #self.quit_act = QAction('&Salir', self)
        #self.quit_act.triggered.connect(self.close)

        self.filter_act = QAction('&Filter by...', self)
        self.filter_act.setIcon(QIcon(str(icon_dir/'funnel.png')))
        self.filter_act.triggered.connect(self.open_filter_dlg)
        self.filter_act.setShortcut('Ctrl+F')

        self.search_and_replace_act = QAction('&Search and replace...', self)
        self.search_and_replace_act.triggered.connect(self.open_search_and_replace_dlg)

        self.map_annotation_act = QAction('&Map annotation...', self)
        self.map_annotation_act.triggered.connect(self.open_map_annotation_dlg)

    def init_menubar(self):
        menu_bar = QMenuBar()

        file_bar = menu_bar.addMenu('&File')
        file_bar.addAction(self.new_project_act)
        file_bar.addAction(self.open_project_act)
        file_bar.addAction(self.close_project_act)
        file_bar.addSeparator()
        file_bar.addAction(self.project_settings_act)

        edit_bar = menu_bar.addMenu('&Edit')
        edit_bar.addAction(self.search_and_replace_act)
        edit_bar.addAction(self.map_annotation_act)
        edit_bar.addSeparator()
        edit_bar.addAction(self.preferences_act)

        data_bar = menu_bar.addMenu('&Data')
        data_bar.addAction(self.filter_act)
        data_bar.addAction(self.open_praat_act)

        self.setMenuBar(menu_bar)

    def init_toolbar(self):
        data_toolbar = QToolBar(self)
        data_toolbar.addAction(self.open_praat_act)
        data_toolbar.addAction(self.filter_act)

        self.addToolBar(data_toolbar)

    def init_ui(self):
        self.editor_view = EditorView(self)
        self.setCentralWidget(self.editor_view)

    def init_dialogs(self):
        self.preferences_dlg = PreferencesDialog(self)
        self.preferences_dlg.accepted.connect(self.on_preferences)

        self.new_project_dlg = NewProjectDialog(self)
        self.new_project_dlg.accepted.connect(self.on_load_project)

        self.simple_filter_dlg = FilterByDialog(self)
        self.simple_filter_dlg.accepted.connect(self.on_filter_rows)

        self.search_and_replace_dlg = SearchAndReplaceDialog()
        self.search_and_replace_dlg.accepted.connect(self.on_search_and_replace)

        self.map_annotations_dlg = MapAnnotationDialog()
        self.map_annotations_dlg.accepted.connect(self.on_map_annotations)

    def open_preferences_dlg(self):
        praat_path = settings.value('praat/path')
        praat_maximize_audibility = settings.value('praat/maximize_audibility')

        self.preferences_dlg.set_data(praat_path, int(praat_maximize_audibility))
        self.preferences_dlg.show()

    def open_filter_dlg(self):
        proxy_model = self.editor_view.table_view.model()
        ncols = proxy_model.columnCount()
        orientation = Qt.Orientation.Horizontal
        fields = [proxy_model.headerData(i, orientation) for i in range(ncols)]

        self.simple_filter_dlg.set_fields(fields)
        self.simple_filter_dlg.show()

    def open_search_and_replace_dlg(self):
        proxy_model = self.editor_view.table_view.model()
        ncols = proxy_model.columnCount()
        orientation = Qt.Orientation.Horizontal
        fields = [proxy_model.headerData(i, orientation) for i in range(ncols)]

        self.search_and_replace_dlg.set_fields(fields)
        self.search_and_replace_dlg.show()

    def open_map_annotation_dlg(self):
        """
        Prepare and show non-modal dialog.
        """
        proxy_model = self.editor_view.table_view.model()
        ncols = proxy_model.columnCount()
        orientation = Qt.Orientation.Horizontal
        fields = [proxy_model.headerData(i, orientation) for i in range(ncols)]

        self.map_annotations_dlg.set_fields(fields)
        self.map_annotations_dlg.show()

    def on_search_and_replace(self):
        r = self.search_and_replace_dlg.data()

        proxy_model = self.editor_view.table_view.model()
        model = proxy_model.sourceModel()
        model.search_and_replace(
            r.search, r.replace, r.field_index, r.field_index, 
        )

    def on_map_annotations(self):
        r = self.map_annotations_dlg.data()

        proxy_model = self.editor_view.table_view.model()
        model = proxy_model.sourceModel()
        model.search_and_replace(
            r.search, r.replace, r.src_column_index, r.dst_column_index, 
        )

    def on_enabled_buttons(self, b):
        self.close_project_act.setEnabled(b)
        self.project_settings_act.setEnabled(b)
        self.open_project_act.setEnabled(b)
        self.open_praat_act.setEnabled(b)
        self.filter_act.setEnabled(b)
        self.search_and_replace_act.setEnabled(b)
        self.map_annotation_act.setEnabled(b)

    def on_open_project(self):
        pass

    def on_project_settings(self):
        pass

    def on_close_project(self):
        self.editor_view.load_textgrids_from_dir('')
        self.on_enabled_buttons(False)

    def on_load_project(self):
        dict_ = self.new_project_dlg.data()
        self.editor_view.load_textgrids_from_dir(
            dict_['src_dir'],
            dict_['primary_tier'],
            dict_['secondary_tiers'],
        )
        self.on_enabled_buttons(True)

    def on_filter_rows(self):
        field, value = self.simple_filter_dlg.data()
        self.editor_view.filter_rows(field, value)

    def on_preferences(self):
        preferences = self.preferences_dlg.data()
        settings.setValue('praat/path', preferences.praat_path)
        settings.setValue('praat/maximize_audibility', preferences.praat_maximize_audibility)
