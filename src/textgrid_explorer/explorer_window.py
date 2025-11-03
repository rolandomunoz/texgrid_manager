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
import re
import shutil
import subprocess
from importlib import resources

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QMessageBox,
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
    QPixmap,
    QAction,
    QIcon,
)

from textgrid_explorer.models import TGTableModel
from textgrid_explorer.dialogs import NewProjectDialog
from textgrid_explorer.dialogs import FilterByDialog
from textgrid_explorer.dialogs import FindAndReplaceDialog
from textgrid_explorer.dialogs import MapAnnotationDialog
from textgrid_explorer.dialogs import PreferencesDialog
from textgrid_explorer.resources import rc_icons
from textgrid_explorer import utils

resources_dir = resources.files('textgrid_explorer.resources')
settings = QSettings('Gilgamesh', 'TGExplorer')

class EditorView(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.table_view = QTableView()

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

        praat_path_ = settings.value('praat/path')
        praat_path = shutil.which(praat_path_)
        if praat_path is None:
            QMessageBox.critical(
                self,
                'Open selection in Praat',
                'It seems like the <b>Praat path</b> does not exist. Please, go to <b>Edit > Preferences</br'
            )

        praat_maximize_audibility = settings.value('praat/maximize_audibility')
        script_path = resources_dir / 'open_file.praat'
        subprocess.run(
            [praat_path, '--hide-picture', '--new-send', script_path, textgrid_path, sound_path, str(praat_maximize_audibility), str(interval.xmin), str(interval.xmax)]
        )

    def filter_rows(self, key_column, str_expression):
        proxy_model = self.table_view.model()
        proxy_model.setFilterKeyColumn(key_column)
        proxy_model.setFilterRegularExpression(str_expression)

    def set_table_data(self, headers, data):
        """
        Set the table data.

        Parameters
        ----------
        headers : list of str
            Column names.
        data : list of list
            The inner list have n-dimensions and the first element is a `pathlib.Path`
            and the rest of the elements are `mytextgrid.core.interval_tier.Interval` or None.
        """
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
        # File
        self.new_project_act = QAction(self.tr('&New project...'), self)
        self.new_project_act.setShortcut('Ctrl+N')
        self.new_project_act.triggered.connect(self.new_project_dlg.open)

        self.open_project_act = QAction(self.tr('&Open project...'), self)
        self.open_project_act.setShortcut('Ctrl+O')
        self.open_project_act.triggered.connect(self.on_open_project)

        self.close_project_act = QAction(self.tr('&Close project'), self)
        self.close_project_act.triggered.connect(self.on_close_project)

        self.project_settings_act = QAction(self.tr('&Project settings...'), self)
        self.project_settings_act.setShortcut('Ctrl+R')
        self.project_settings_act.triggered.connect(self.on_project_settings)

        self.quit_act = QAction(self.tr('&Quit'), self)
        self.quit_act.setShortcut('Ctrl+Q')
        self.quit_act.triggered.connect(self.close)

        # Data
        self.sort_az_act = QAction(self.tr('Sort table by column (A to Z)'), self)
        self.sort_az_act.triggered.connect(self.on_sort_az)

        self.sort_za_act = QAction(self.tr('Sort table by column (Z to A)'), self)
        self.sort_za_act.triggered.connect(self.on_sort_za)

        funnel_icon = QIcon(QPixmap(':icons/funnel.png'))
        self.filter_act = QAction(funnel_icon, self.tr('&Filter by...'), self)
        self.filter_act.triggered.connect(self.open_filter_dlg)

        praat_icon = QIcon(QPixmap(':icons/praat_icon.png'))
        self.open_praat_act = QAction(praat_icon, self.tr('&Open selection in Praat'), self)
        self.open_praat_act.triggered.connect(self.editor_view.open_praat)
        self.open_praat_act.setShortcut('Alt+P')

        # Edit
        self.find_and_replace_act = QAction(self.tr('&Find and replace...'), self)
        self.find_and_replace_act.setShortcut('Ctrl+H')
        self.find_and_replace_act.triggered.connect(lambda: self.open_find_and_replace_dlg(1))

        self.find_act = QAction(self.tr('&Find...'), self)
        self.find_act.setShortcut('Ctrl+F')
        self.find_act.triggered.connect(lambda: self.open_find_and_replace_dlg(0))

        self.map_annotation_act = QAction(self.tr('&Map annotation...'), self)
        self.map_annotation_act.triggered.connect(self.open_map_annotation_dlg)

        self.preferences_act = QAction(self.tr('&Preferences...'), self)
        self.preferences_act.triggered.connect(self.open_preferences_dlg)

    def init_menubar(self):
        menu_bar = QMenuBar()

        file_bar = menu_bar.addMenu(self.tr('&File'))
        file_bar.addAction(self.new_project_act)
        file_bar.addAction(self.open_project_act)
        file_bar.addAction(self.close_project_act)
        file_bar.addSeparator()
        file_bar.addAction(self.project_settings_act)
        file_bar.addSeparator()
        file_bar.addAction(self.quit_act)

        edit_bar = menu_bar.addMenu(self.tr('&Edit'))
        edit_bar.addAction(self.find_and_replace_act)
        edit_bar.addAction(self.find_act)
        edit_bar.addAction(self.map_annotation_act)
        edit_bar.addSeparator()
        edit_bar.addAction(self.preferences_act)

        data_bar = menu_bar.addMenu(self.tr('&Data'))
        data_bar.addAction(self.sort_az_act)
        data_bar.addAction(self.sort_za_act)
        data_bar.addSeparator()
        data_bar.addAction(self.filter_act)
        data_bar.addSeparator()
        data_bar.addAction(self.open_praat_act)

        self.setMenuBar(menu_bar)

    def init_toolbar(self):
        data_toolbar = QToolBar(self)
        data_toolbar.addAction(self.open_praat_act)
        data_toolbar.addAction(self.filter_act)

        self.addToolBar(data_toolbar)

    def init_ui(self):
        self.editor_view = EditorView(self)
        selection_model = self.editor_view.table_view.selectionModel()
        selection_model.currentColumnChanged.connect(self.on_sorting_act)
        self.setCentralWidget(self.editor_view)

    def init_dialogs(self):
        self.preferences_dlg = PreferencesDialog(self)
        self.preferences_dlg.accepted.connect(self.on_preferences)

        self.new_project_dlg = NewProjectDialog(self)
        self.new_project_dlg.accepted.connect(self.on_load_data)

        self.simple_filter_dlg = FilterByDialog(self)
        self.simple_filter_dlg.accepted.connect(self.on_filter_rows)

        self.find_and_replace_dlg = FindAndReplaceDialog(self)
        self.find_and_replace_dlg.replace_all_clicked.connect(self.on_replace_all)
        self.find_and_replace_dlg.replace_clicked.connect(self.on_replace)
        self.find_and_replace_dlg.find_all_clicked.connect(self.on_find_all)
        self.find_and_replace_dlg.find_clicked.connect(lambda: self.on_find(1))

        self.map_annotations_dlg = MapAnnotationDialog(self)
        self.map_annotations_dlg.accepted.connect(self.on_map_annotations)

    def open_preferences_dlg(self):
        praat_path = settings.value('praat/path')
        praat_maximize_audibility = settings.value('praat/maximize_audibility')

        self.preferences_dlg.set_data(praat_path, int(praat_maximize_audibility))
        self.preferences_dlg.open()

    def open_filter_dlg(self):
        proxy_model = self.editor_view.table_view.model()
        ncols = proxy_model.columnCount()
        orientation = Qt.Orientation.Horizontal
        fields = [proxy_model.headerData(i, orientation) for i in range(ncols)]

        self.simple_filter_dlg.set_fields(fields)
        self.simple_filter_dlg.show()

    def open_find_and_replace_dlg(self, tab_index=0):
        column_index = -1
        column_names = []
        find_pattern = ''

        # Get column names
        model = self.editor_view.table_view.model()
        for i in range(model.columnCount()):
            column_names.append(
                model.headerData(i, Qt.Orientation.Horizontal)
            )

        # On selection
        indexes = self.editor_view.table_view.selectedIndexes()
        if indexes:
            index = indexes[0] #topleft selection
            column_index = index.column()

            if len(indexes) == 1: # If selected on cell
                find_pattern = index.data()

        ## Fill up find tab
        self.find_and_replace_dlg.set_column_field(column_names, column_index)
        self.find_and_replace_dlg.set_find_field(find_pattern)

        ## Fill up replace tab
        self.find_and_replace_dlg.display_tab(tab_index)
        self.find_and_replace_dlg.show()

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

    def on_find(self, step=1):
        """
        Find the next item in the specified column starting from the
        selected row.
        """
        table_view = self.editor_view.table_view
        proxy_model = table_view.model()
        source_model = proxy_model.sourceModel()

        # 1. From the QDialog, get the column index and the search pattern
        dlg_dict = self.find_and_replace_dlg.data()
        col_ind = dlg_dict['column_index']
        pattern = dlg_dict['pattern']

        # 2. From the QTableView, get the current selected row
        row_ind = 0
        proxy_indexes = table_view.selectedIndexes()
        if proxy_indexes:
            current_source_index = proxy_model.mapToSource(proxy_indexes[0])
            row_ind = current_source_index.row() + step

        # 3. Find the next item moving on from the current selected row,
        # the specified column and the pattern
        p = re.compile(pattern)
        for i in range(row_ind, source_model.rowCount()):
            source_index = source_model.index(i, col_ind)
            cell_text = source_index.data()
            if not p.search(cell_text):
                continue

            proxy_index = proxy_model.mapFromSource(source_index)
            if not proxy_index.isValid():
                continue

            sel_model = table_view.selectionModel()
            sel_model.select(proxy_index, sel_model.SelectionFlag.ClearAndSelect)
            table_view.setCurrentIndex(proxy_index) # Focus
            table_view.scrollTo(proxy_index)
            return True
        return False

    def on_find_all(self):
        print('Find All')

    def on_replace(self):
        """
        Replace the items, one by one, that match a pattern in the
        QTableView.
        """
        table_view = self.editor_view.table_view

        # 1. Use the find to match a value
        match = self.on_find(0)

        if not match:
            return False

        # 2. From the QDialog, get the column index, the search pattern
        #    and the replace
        dlg_dict = self.find_and_replace_dlg.data()
        col_ind = dlg_dict['column_index']
        pattern = dlg_dict['pattern']
        repl = dlg_dict['replace']

        # 3. Once match is found, replace the item
        proxy_model = table_view.model()
        proxy_indexes = table_view.selectedIndexes()
        if not proxy_indexes:
            return False

        proxy_index = proxy_indexes[0]
        source_index = proxy_model.mapToSource(proxy_index)

        source_model = proxy_model.sourceModel()
        source_model.replace([source_index], pattern, repl)
        return True

    def on_replace_all(self):
        """
        Replace all items in the specified column that match a pattern.
        """
        table_view = self.editor_view.table_view

        # 1. From the QDialog, get the column index, the search pattern
        #    and the replace
        dlg_dict = self.find_and_replace_dlg.data()
        col_ind = dlg_dict['column_index']
        pattern = dlg_dict['pattern']
        repl = dlg_dict['replace']

        # 2. Get the all the indexes from the selected column
        proxy_model = table_view.model()
        source_model = proxy_model.sourceModel()

        source_indexes = []
        for i in range(proxy_model.rowCount()):
            proxy_item = proxy_model.index(i, col_ind)
            source_item = proxy_model.mapToSource(proxy_item)
            if not source_item.isValid():
                continue
            source_indexes.append(source_item)

        # 3. Replace All
        source_model.replace(source_indexes, pattern, repl)
        return True

    def on_map_annotations(self):
        r = self.map_annotations_dlg.data()

        proxy_model = self.editor_view.table_view.model()
        model = proxy_model.sourceModel()
        model.replace_all(
            r.find, r.replace, r.src_column_index, r.dst_column_index,
        )

    def on_enabled_buttons(self, b):
        self.close_project_act.setEnabled(b)
        self.project_settings_act.setEnabled(b)
        self.open_project_act.setEnabled(b)
        self.open_praat_act.setEnabled(b)
        self.filter_act.setEnabled(b)
        self.find_and_replace_act.setEnabled(b)
        self.find_act.setEnabled(b)
        self.map_annotation_act.setEnabled(b)
        self.sort_az_act.setEnabled(b)
        self.sort_za_act.setEnabled(b)

    def on_open_project(self):
        pass

    def on_project_settings(self):
        pass

    def on_close_project(self):
        self.editor_view.load_textgrids_from_dir('')
        self.on_enabled_buttons(False)

    def on_load_data(self):
        # Get variables from a dialog
        dict_ = self.new_project_dlg.data()

        src_dir = dict_['src_dir']

        primary_tier = dict_['primary_tier']
        if primary_tier is None:
            primary_tier = []

        secondary_tiers = dict_['secondary_tiers']
        if secondary_tiers is None:
            secondary_tiers = []

        # Build table headers and data
        headers, data = utils.create_aligned_tier_table(
            src_dir, primary_tier, secondary_tiers
        )

        # Fill up table
        self.editor_view.set_table_data(headers, data)

        # Enable buttons
        self.on_enabled_buttons(True)

    def on_filter_rows(self):
        field, value = self.simple_filter_dlg.data()
        self.editor_view.filter_rows(field, value)

    def on_sort_az(self):
        table_view = self.editor_view.table_view
        indexes = table_view.selectedIndexes()
        if indexes:
            topleft_index = indexes[0]
            column_index = topleft_index.column()
            table_view.sortByColumn(column_index, Qt.SortOrder.AscendingOrder)

    def on_sort_za(self):
        table_view = self.editor_view.table_view
        indexes = table_view.selectedIndexes()
        if indexes:
            topleft_index = indexes[0]
            column_index = topleft_index.column()
            table_view.sortByColumn(column_index, Qt.SortOrder.DescendingOrder)

    def on_sorting_act(self, current_index, previous_index):
        """
        Update the name of the `Sort by column (A to Z)` command with the
        selected column name.
        """
        column_index = current_index.column()
        column_name = current_index.model().headerData(column_index, Qt.Orientation.Horizontal)
        self.sort_az_act.setText(f'Sort by column "{column_name}" (A to Z)')
        self.sort_za_act.setText(f'Sort by column "{column_name}" (Z to A)')

    def on_preferences(self):
        preferences = self.preferences_dlg.data()
        settings.setValue('praat/path', preferences.praat_path)
        settings.setValue('praat/maximize_audibility', preferences.praat_maximize_audibility)
