import questiondata
import category_rewritten
import designmain
import tests
import sys
import os
from loguru import logger
from PyQt5 import QtWidgets, QtCore


def initiate_exception_logging():
    # generating our hook
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        logger.exception(f"{exctype}, {value}, {traceback}")
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


class BrainRing(QtWidgets.QMainWindow, designmain.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Open.triggered.connect(self.OpenPressed)
        self.Open.setShortcut('Ctrl+O')
        self.game = None
        self.category_form = None
        self.time = False

        self.BtnNew.clicked.connect(self.NewQuestion)

    def OpenPressed(self):
        openfilename = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите игру', "")[0]
        if openfilename and '.' in openfilename and openfilename.split('.')[1].lower() == 'xlsx':
            self.game, error = questiondata.create_game(openfilename)
            if self.game:
                if error:
                    ErrorMessage(error)
                self.category_form = category_rewritten.CategoryForm(self.game)
                self.category_form.category_signal[str].connect(self.CategorySelected)
                self.category_form.show()
        else:
            ErrorMessage('Файл не выбран или формат неверный (выберите .xlxs файл')

    def CategorySelected(self,  category):
        """
        gets first category question data to UI
        :param category: category name
        :return:
        """
        category = self.game.get_category_by_name(category)
        self.LblDscr.setText("%s: Вопрос № 1. Стоимость %i " % (category.name, category.questions[0].points))
        self.TxtQstn.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                 "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                 "p, li { white-space: pre-wrap; }\n"
                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; "
                                 "font-weight:400; font-style:normal;\">\n"
                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
                                 " -qt-block-indent:0; text-indent:0px;\">"
                                 "<span style=\" font-family:\'Calibri\'; font-size:20pt; "
                                 "font-weight:600; color:#000000;\">%s</span></p></body></html>"
                                 % category.questions[0].description)
        self.LblAnswer.setText(category.questions[0].answer)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.TimerEvent)
        self.timer.start(1000)
        self.SetStateQuestion()

    def NewQuestion(self):
        """
        shows next question
        :return:
        """

    def TimerEvent(self):
        """
        decreases time and disables controls if time is over
        :return:
        """
        if self.time:
            current = self.Timer.intValue()
            if current > 0:
                self.Timer.display(current - 1)
                if current == questiondata.time_low_threshold + 1:
                    self.Timer.setStyleSheet("color: red")
            else:
                self.SetStateTimeEnded()

    def SetStateQuestion(self):
        """
        sets controls state when Question exists
        :return:
        """
        self.time = True
        self.Timer.display(questiondata.question_time)
        self.Timer.setStyleSheet('color: blue')
        self.BtnEnd.setEnabled(True)
        self.BtnNew.setEnabled(True)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)

    def SetStateAnswer(self):
        self.time = False
        self.BtnEnd.setEnabled(True)
        self.BtnNew.setEnabled(True)
        self.BtnTrue.setEnabled(True)
        self.BtnFalse.setEnabled(True)

    def SetStateTimeEnded(self):
        """
        sets controls state for end of time
        :return:
        """
        # self.Timer.setStyleSheet("color:gray")
        self.time = False
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnFinish.setEnabled(True)
        self.BtnNew.setEnabled(False)

    def closeEvent(self, event):
        self.category_form.question.close()
        self.category_form.close()
        event.accept()


def ErrorMessage(text):
    """
    shows error window with text
    :param text: error text
    :return:
    """
    error = QtWidgets.QMessageBox()
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Ошибка!')
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


@logger.catch
def main():
    initiate_exception_logging()
    tests.test_main()
    app = QtWidgets.QApplication(sys.argv)
    window = BrainRing()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
