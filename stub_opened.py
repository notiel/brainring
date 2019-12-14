from stub import Ui_Form
from PyQt5 import QtWidgets
import questiondata


class StubForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, category: questiondata.Category):
        super().__init__()
        self.setupUi(self)
        self.LblCat.setText(category.name)
        self.LblPoints.setText(str(category.questions[0].points))
        self.LblNumber.setText(str(len(category.questions)))
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        self.setGeometry(screen_res.x() + screen_res.width()/3, screen_res.y() + screen_res.height()/4,
                         screen_res.width()/3, screen_res.height()/3)
