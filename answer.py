import answer_design
from PyQt5 import QtWidgets
import common_functions
import os


class AnswerDialog(QtWidgets.QWidget, answer_design.Ui_Form):

    def __init__(self, answer: str, filepath: str):
        super().__init__()
        self.setupUi(self)
        self.LblAnswer.setText(answer)
        self.image = None
        self.media = False
        self.mediapath = ""
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        self.setGeometry(screen_res.x() + 20, screen_res.y() + 40, screen_res.width() - 20, screen_res.height() - 40)
        if filepath:
            if os.path.exists(filepath) and (filepath.endswith(".jpg") or filepath.endswith('.png')):
                self.image = common_functions.ImageShow(filepath)
            elif os.path.exists(filepath) and filepath.endswith('.mp3'):
                self.media = True
                self.mediapath = filepath
            else:
                self.media = True
                self.mediapath = ""

    def closeEvent(self, event):

        if self.image:
            self.image.destroy()
        event.accept()
