import questiondata
import category_rewritten
import question_opened
import designmain
import sys
import os
from loguru import logger
from PyQt5 import QtWidgets, QtCore
from enum import Enum
from typing import Optional


def setup_exception_logging():
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


class States (Enum):
    NO_CAT = 0
    CAT_SELECTED = 1
    QUEST_SELECTED = 2
    ANSWER_READY = 3
    TIMER_STOPPED = 4
    TIMER_ENDED = 5
    

class GameState(QtWidgets.QWidget):
    state_signal = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.game: Optional[questiondata.Game] = None
        self.time: bool = False
        self.state: States = States.NO_CAT
        self.category: Optional[questiondata.Category] = None
        self.question: int = -1

    def set_game(self, game: questiondata.Game):
        """
        sets game to state
        :param game: gamedata
        :return:
        """
        self.game = game

    def set_category(self, name: str):
        """
        sets category to state
        :param name: category name
        :return:
        """
        self.category = name
        self.set_state(States.CAT_SELECTED)

    def set_state(self, state: States):
        """
        sets state and enits corresponding signal
        :param state: new state
        :return:
        """
        self.state = state
        if state == States.QUEST_SELECTED:
            self.time = True
            self.next_question()
        if state == States.CAT_SELECTED:
            self.time = False
            self.question = -1
        if state == States.TIMER_ENDED:
            self.time = False
        self.state_signal.emit()

    def next_question(self):
        """
        increases question id
        :return:
        """
        self.question += 1


class BrainRing(QtWidgets.QMainWindow, designmain.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Open.setShortcut('Ctrl+O')
        self.game = None
        self.category_form = None
        self.state: GameState = GameState()
        self.state.state_signal.connect(self.StateChanged)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.TimerEvent)
        self.timer.start(1000)

        self.Open.triggered.connect(self.OpenPressed)
        self.BtnNew.clicked.connect(self.NewQuestion)
        self.BtnNext.clicked.connect(self.NewQuestion)
        self.BtnEnd.clicked.connect(self.NewCategory)
        self.BtnTimer.clicked.connect(self.TimerPressed)

    def OpenPressed(self):
        openfilename = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите игру', "")[0]
        if openfilename and openfilename.endswith(".xlsx"):
            self.game, error = questiondata.create_game(openfilename)
            if self.game:
                if error:
                    ErrorMessage(error)
                self.state.set_game(self.game)
                self.category_form = category_rewritten.CategoryForm(self.game)
                self.category_form.category_signal[str].connect(self.CategorySelected)
                self.category_form.show()
        else:
            ErrorMessage('Файл не выбран или формат неверный (выберите .xlxs файл')

    def StateChanged(self):
        """
        applies state to UI
        :return:
        """
        if self.state.state == States.CAT_SELECTED:
            self.SetStateCategory()
        if self.state.state == States.QUEST_SELECTED:
            self.SetStateQuestion()
        if self.state.state == States.TIMER_ENDED:
            self.SetStateTimeEnded()

    def CategorySelected(self,  category):
        """
        changes game state
        :param category: category name
        :return:
        """
        category = self.game.get_category_by_name(category)
        self.state.set_category(category)

    def NewQuestion(self):
        """
        shows next question
        :return:
        """
        self.category_form.stub.setVisible(False)
        self.state.set_state(States.QUEST_SELECTED)

    def CloseQuestion(self):
        """

        :return:
        """
        pass

    def NewCategory(self):
        """

        :return:
        """
        self.category_form.setVisible(True)

    def TimerEvent(self):
        """
        decreases time and disables controls if time is over
        :return:
        """
        if self.state.time:
            current = self.Timer.intValue()
            if current > 0:
                self.Timer.display(current - 1)
                if current == questiondata.time_low_threshold + 1:
                    self.Timer.setStyleSheet("color: red")
            else:
                self.state.set_state(States.TIMER_ENDED)

    def TimerPressed(self):
        """
        starts and stops timer at any moment
        :return:
        """
        if self.state.time:
            self.state.time = False
            self.BtnTimer.setText('Старт')
        else:
            self.state.time = True
            self.BtnTimer.setText('Стоп')

    def SetStateCategory(self):
        """
        sets controls states when Category Selected
        :return:
        """
        self.BtnEnd.setEnabled(False)
        self.BtnNew.setEnabled(False)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnNext.setEnabled(True)
        self.BtnTimer.setEnabled(True)
        self.LblDscr.setText("Категория: " + self.state.category.name)
        self.TxtQstn.clear()
        self.LblAnswer.clear()

    def SetStateQuestion(self):
        """
        sets controls state when Question exists
        :return:
        """
        self.Timer.display(questiondata.question_time)
        self.Timer.setStyleSheet('color: blue')
        self.BtnEnd.setEnabled(True)
        category: questiondata.Category = self.state.category
        if self.state.question == len(self.state.category.questions) - 1:
            self.BtnNew.setEnabled(False)
        else:
            self.BtnNew.setEnabled(True)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnNext.setEnabled(False)
        self.BtnTimer.setEnabled(True)
        self.BtnTimer.setText('Стоп')

        self.LblDscr.setText("%s: Вопрос № %i из %i. Стоимость %i " %
                             (category.name, self.state.question+1, len(category.questions),
                              category.questions[self.state.question].points))
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
                             % category.questions[self.state.question].description)
        self.LblAnswer.setText(category.questions[self.state.question].answer)
        self.category_form.question = question_opened.QuestionDialog(category, self.state.question)
        self.category_form.question.show()

    def SetStateAnswer(self):
        # self.time = False
        self.BtnEnd.setEnabled(True)
        self.BtnNew.setEnabled(True)
        self.BtnTrue.setEnabled(True)
        self.BtnFalse.setEnabled(True)
        self.BtnNext.setEnabled(False)
        self.BtnTimer.setEnabled(True)

    def SetStateTimeEnded(self):
        """
        sets controls state for end of time
        :return:
        """
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnFinish.setEnabled(True)
        self.BtnNew.setEnabled(True)
        self.BtnNext.setEnabled(False)
        self.BtnTimer.setEnabled(False)

    def closeEvent(self, event):
        if self.category_form:
            if self.category_form.question:
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
    setup_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = BrainRing()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
