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
        if filepath:
            if os.path.exists(filepath) and (filepath.endswith(".jpg") or filepath.endswith('.png')):
                self.image = common_functions.ImageShow(filepath)
            elif os.path.exists(filepath) and filepath.endswith('.mp3'):
                os.system(r"start %s" % filepath)
            else:
                common_functions.error_message("Файла с медиаконтентом не существует или формат неверный")

    def closeEvent(self, event):
        if self.image:
            self.image.destroy()
        event.accept()
