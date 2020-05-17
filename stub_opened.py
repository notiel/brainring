from stub import Ui_Form
from PyQt5 import QtWidgets, QtGui
import questiondata


class StubForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, category: questiondata.Category):
        super().__init__()
        self.setupUi(self)
        if category.media_path:
            pic = QtGui.QPixmap(category.media_path)
            self.LblPicture.setPixmap(pic)
        if category.questions:
            self.LblCat.setText(category.name)
            self.LblPoints.setText(str(category.questions[0].points))
            self.LblNumber.setText(str(len(category.questions)))
        else:
            self.LblCat.hide()
            self.LblCatLabel.hide()
            self.LblNumberlabel.hide()
            self.LblPointsLabel.hide()
            self.LblPoints.hide()
            self.LblNumber.hide()
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        self.setGeometry(screen_res.x() + screen_res.width()/3, screen_res.y() + screen_res.height()/4,
                         screen_res.width()/3, screen_res.height()/3)
