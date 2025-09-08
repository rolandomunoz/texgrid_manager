from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QFormLayout,
)

class FilterDialog(QDialog):

    def __init__(self, parent, headers):
        super().__init__(parent)
        self.setWindowTitle('Filter')
        self.headers = headers
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        for header_str in self.headers:
            editor = QLineEdit(self)
            editor.setPlaceholderText('Insert value')
            layout.addRow(header_str, editor)

        self.setLayout(layout)
