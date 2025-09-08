from PySide6.QtWidgets import (
    QMessageBox,
    QWizard,
    QWizardPage,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QFormLayout,
)

class InitWizard(QWizard):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Example Wizard')

        self.addPage(IntroPage())

    def set_dict_path(self, dict_path=''):
        self.setField('dict_path', dict_path)

    def set_data_dir(self, data_dir=''):
        self.setField('data_dir', data_dir)

    def data_dir(self):
        return self.field('data_dir')

    def dict_path(self):
        return self.field('dict_path')

class IntroPage(QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('Start')
        self.init_ui()

    def init_ui(self):
        textgrid_ed = QLineEdit()

        dict_ed = QLineEdit()

        mode_list = ['Simple']
        combo_box = QComboBox(self)
        combo_box.insertItems(0, mode_list)

        form_layout = QFormLayout()
        form_layout.addRow('TextGrid directory', textgrid_ed)
        form_layout.addRow('Dictionary path', dict_ed)
        form_layout.addRow('Mode', combo_box)

        self.setLayout(form_layout)

        self.registerField('data_dir', textgrid_ed)
        self.registerField('dict_path', dict_ed)
        self.registerField('mode', combo_box)

class SelectTierPage(QWizardPage):
    pass
