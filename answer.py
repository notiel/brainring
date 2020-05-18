import answer_design
from PyQt5 import QtWidgets, QtGui, QtCore
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
        self.setGeometry(screen_res.x() + 50, screen_res.y() + 50, screen_res.width()/4*3, screen_res.height() - 100)
        if filepath:
            if os.path.exists(filepath) and (filepath.endswith(".jpg") or filepath.endswith('.png')):
                pixmap = QtGui.QPixmap()
                pixmap.load(filepath)
                self.LblPicture.setScaledContents(True)
                image_height = 2 * (screen_res.height() - 100) / 3
                image_wight = image_height * 4 / 3
                self.LblPicture.setAlignment(QtCore.Qt.AlignCenter)
                self.LblPicture.setPixmap(pixmap)
                self.LblPicture.setFixedWidth(image_wight)
                self.LblPicture.setFixedHeight(image_height)
                self.LblPicture.setAlignment(QtCore.Qt.AlignCenter)
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
