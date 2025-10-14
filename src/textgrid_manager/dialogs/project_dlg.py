from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from textgrid_manager import utils

class NewProjectDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.setWindowTitle('New Project settings')
        self._tiers = []

    def init_ui(self):
        self.textgrid_dir = QLineEdit(r'C:\Users\GILGAMESH\Documents\projects\texgrid-explorer\tests\data\2018-02-08', self)
        update_btn = QPushButton('&Scan TextGrid files', self)
        update_btn.clicked.connect(self.on_scan_tiers)

        self.primary_tier = QComboBox(self)
        self.primary_tier.currentTextChanged.connect(self.on_primary_tier)
        self.secondary_tiers = QListWidget(self)

        ok_btn = QPushButton('Ok', self)
        ok_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton('Cancel', self)
        cancel_btn.clicked.connect(self.reject)

        btn_box = QHBoxLayout()
        btn_box.addWidget(ok_btn)
        btn_box.addWidget(cancel_btn)

        main_box = QVBoxLayout()
        main_box.addWidget(QLabel('TextGrid directory:'))
        main_box.addWidget(self.textgrid_dir)
        main_box.addWidget(update_btn)

        main_box.addWidget(QLabel('Build Table:'))
        main_box.addWidget(QLabel('Primary tier'))
        main_box.addWidget(self.primary_tier)
        main_box.addWidget(QLabel('Secondary tiers'))
        main_box.addWidget(self.secondary_tiers)
        main_box.addLayout(btn_box)

        self.setLayout(main_box)

    def on_scan_tiers(self):
        self._tiers = utils.get_tier_names(self.textgrid_dir.text())

        self.primary_tier.clear()
        self.primary_tier.addItems(self._tiers)

    def on_primary_tier(self, text):
        self.secondary_tiers.clear()
        self.secondary_tiers.addItems(
            [t for t in self._tiers if t != text]
        )

    def data(self):
        dict_ = {
            'src_dir': self.textgrid_dir.text(),
            'primary_tier': self.primary_tier.currentText,
            'secondary_tiers': []
        }
        return dict_

class OpenProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

class ProjectSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

