import mytextgrid
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMenuBar,
    QTableView,
    QVBoxLayout,
)
from PySide6.QtCore import (
    QSortFilterProxyModel,
)

from PySide6.QtGui import (
    QAction,
)

from textgrid_manager.models import TGTableModel

class EditorView(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.tableview = QTableView()

        model = TGTableModel([])
        proxy_model = QSortFilterProxyModel(model)
        proxy_model.setSourceModel(model)
        self.tableview.setModel(proxy_model)

        proxy_model.setFilterRegularExpression("text")
        proxy_model.setFilterKeyColumn(1)

        box_layout = QVBoxLayout()
        box_layout.addWidget(self.tableview)
        self.setLayout(box_layout)

class TGManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('TGManager')
        self.setMinimumSize(800, 500)
        #self.showMaximized()
        self.init_ui()
        self.init_actions()
        self.init_menubar()

    def init_actions(self):
        """
        Create actions
        """
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

    def init_ui(self):
        self.editor_view = EditorView()
        self.setCentralWidget(self.editor_view)

    def filter_table(self):
        pass

def run_app():
    app = QApplication([])
    app.setStyle('Fusion')
    main_window = TGManager()
    main_window.show()
    app.exec()
