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
