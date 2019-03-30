import settings_ui
from PyQt5 import  QtWidgets


class Settings(QtWidgets.QWidget, settings_ui.Ui_Settings):

    def __init__(self):
        super().__init__()
        self.setupUi(self)