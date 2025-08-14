import mytextgrid
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QMenuBar,
    QTableView,
    QVBoxLayout,
)

from textgrid_manager.models import TGTableModel
from textgrid_manager.models import scan_library

class EditorView(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.tableview = QTableView()

        model=TGTableModel([])
        self.tableview.setModel(model)
        #self.tableview.setModel(proxymodel)

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
        self.init_menubar()

    def init_menubar(self):
        menu_bar = QMenuBar()
        main = menu_bar.addMenu('&Files')
        self.setMenuBar(menu_bar)

    def init_ui(self):
        self.editor_view = EditorView()
        self.setCentralWidget(self.editor_view)

def run_app():
    app = QApplication([])
    app.setStyle('Fusion')
    main_window = TGManager()
    main_window.show()
    app.exec()
