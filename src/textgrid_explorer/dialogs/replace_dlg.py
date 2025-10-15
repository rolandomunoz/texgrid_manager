from collections import namedtuple

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

Result = namedtuple('Results', ['field_index', 'field', 'search', 'replace'])

class SearchAndReplaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Search and replace')
        self._fields = []
        self.init_ui()

    def init_ui(self):
        self.fields_box = QComboBox(self)
        self.fields_box.addItems(self._fields)

        self.search_ed = QLineEdit(self)
        self.replace_ed = QLineEdit(self)

        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        btn_box = QHBoxLayout()
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)

        main_box = QVBoxLayout()
        main_box.addWidget(QLabel('Column name:'))
        main_box.addWidget(self.fields_box)

        main_box.addWidget(QLabel('Find what:'))
        main_box.addWidget(self.search_ed)

        main_box.addWidget(QLabel('Replace with:'))
        main_box.addWidget(self.replace_ed)
        main_box.addLayout(btn_box)

        self.setLayout(main_box)

    def set_fields(self, fields):
        if not self._fields == fields:
            self._fields = fields
            self.fields_box.clear()
            self.fields_box.addItems(fields)

    def data(self):
        r = Result(
            self.fields_box.currentIndex(),
            self.fields_box.currentText(),
            self.search_ed.text(),
            self.replace_ed.text()
        )
        return r
