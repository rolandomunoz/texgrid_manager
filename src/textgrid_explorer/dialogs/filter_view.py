from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

class FilterView(QDialog):

    def __init__(self, parent, proxy_model=None):
        super().__init__(parent)
        self.setWindowTitle('Filter')
        self.proxy_model = proxy_model
        self.init_ui()

    def init_ui(self):
        # Headers
        ncols = self.proxy_model.columnCount()
        orientation = Qt.Orientation.Horizontal
        headers = [self.proxy_model.headerData(i, orientation) for i in range(ncols)]

        # Filter form
        self.form = QFormLayout()
        for header_str in headers:
            editor = QLineEdit(self)
            editor.setPlaceholderText('Insert value')
            self.form.addRow(header_str, editor)

        # Buttons
        filter_btn = QPushButton('Filter', self)
        filter_btn.clicked.connect(self.filter_rows)

        reset_btn = QPushButton('Reset', self)

        hbox = QHBoxLayout()
        hbox.addWidget(filter_btn)
        hbox.addWidget(reset_btn)

        # Main Layout
        layout = QVBoxLayout()
        layout.addLayout(self.form)
        layout.addLayout(hbox)
        self.setLayout(layout)

    def filter_rows(self):
        for i in range(self.form.rowCount()):
            editor = self.form.itemAt(i, QFormLayout.FieldRole).widget()
            expression = editor.text()
            if expression:
                self.proxy_model.setFilterRegularExpression(expression)
                self.proxy_model.setFilterKeyColumn(i)
