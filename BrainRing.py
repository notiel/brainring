import questiondata
import category
import question_opened
import commanddata
import designmain
import settings

import common_functions
import show_table
import sys
import os
from loguru import logger
from PyQt5 import QtWidgets, QtCore
from enum import Enum
from typing import Optional, List

MOCKED = False
if not MOCKED:
    import usbhost
else:
    import mock as usbhost


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


class States(Enum):
    NO_CAT = 0
    CAT_SELECTED = 1
    QUEST_SELECTED = 2
    ANSWER_READY = 3
    CONTINUE = 4
    ANSWERED = 5
    LAST_QUESTION = 6
    TIMER_STOPPED = 7
    TIMER_ENDED = 8


class GameState(QtWidgets.QWidget):
    state_signal = QtCore.pyqtSignal()
    answer_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.game: Optional[questiondata.Game] = None
        self.time: bool = False
        self.state: States = States.NO_CAT
        self.category: Optional[questiondata.Category] = None
        self.question: int = -1
        self.command: int = -1

    def set_game(self, game: questiondata.Game):
        """
        sets game to state
        :param game: gamedata
        :return:
        """
        self.game = game

    def set_category(self, new_category: Optional[questiondata.Category]):
        """
        sets category to state
        :param new_category: category name
        :return:
        """
        self.category = new_category
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
        if state == States.ANSWER_READY:
            self.time = False
        if state == States.LAST_QUESTION:
            self.time = False
        if state == States.CONTINUE:
            self.time = True
        self.state_signal.emit()

    def next_question(self):
        """
        increases question id
        :return:
        """
        self.question += 1

    def stop_time(self):
        """
        stops timer
        :return:
        """
        self.time = False

    def start_time(self):
        """
        starts timer
        :return:
        """
        self.time = True

    def set_command(self, command: int):
        """
        sets answering command id
        :param command: id of answering command
        :return:
        """

        self.command = command

    def delete_command(self):
        """
        resets answering command number
        :return:
        """
        self.command = -1


class BrainRing(QtWidgets.QMainWindow, designmain.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.game = None
        self.category_form = None
        self.settings_form = None
        self.scoretable = None
        self.usbhost = usbhost.UsbHost()
        if MOCKED:
            import mock
            mock.amock_init()
            self.mock = mock.amock
            self.mock.show()
        self.port = self.scan_ports()
        self.set_color("color_idle")
        self.state: GameState = GameState()
        self.state.state_signal.connect(self.state_changed)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)

        self.Open.setShortcut('Ctrl+O')
        self.Open.triggered.connect(self.menu_open_pressed)
        self.Settings_2.setShortcut('Ctrl+S')
        self.Settings_2.triggered.connect(self.menu_settings_pressed)
        self.BtnNew.clicked.connect(self.new_question)
        self.BtnNext.clicked.connect(self.new_question)
        self.BtnEnd.clicked.connect(self.new_category)
        self.BtnTimer.clicked.connect(self.btn_timer_pressed)
        self.BtnTest.clicked.connect(self.btn_test_pressed)
        self.BtnTrue.clicked.connect(self.btn_true_pressed)
        self.BtnFalse.clicked.connect(self.btn_false_pressed)

        self.model: commanddata.CommandTableModel = commanddata.CommandTableModel()
        self.TblCmnd.setModel(self.model)

        self.Timer.display(questiondata.question_time)

    def menu_open_pressed(self):
        openfilename = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите игру', "")[0]
        if openfilename and openfilename.endswith(".xlsx"):
            self.game, error = questiondata.create_game(openfilename)
            if self.game:
                if error:
                    common_functions.error_message(error)
                self.state.set_game(self.game)
                self.category_form = category.CategoryForm(self.game)
                self.category_form.category_signal[str].connect(self.category_selected)
                self.category_form.show()
        else:
            common_functions.error_message('Файл не выбран или формат неверный (выберите .xlxs файл')

    def state_changed(self):
        """
        applies state to UI
        :return:
        """
        if self.state.state == States.CAT_SELECTED:
            self.set_state_category()
        if self.state.state == States.QUEST_SELECTED:
            self.set_state_new_question()
        if self.state.state == States.TIMER_ENDED:
            self.set_state_time_ended()
        if self.state.state == States.ANSWER_READY:
            self.set_state_answer()
        if self.state.state == States.ANSWERED:
            self.set_state_answered()
        if self.state.state == States.LAST_QUESTION:
            self.set_state_last_question()
        if self.state.state == States.CONTINUE:
            self.set_state_continue()

    def category_selected(self, category_passed):
        """
        changes game state
        :param category_passed: category name
        :return:
        """
        actual_category: questiondata.Category = self.game.get_category_by_name(category_passed)
        self.state.set_category(actual_category)

    def new_question(self):
        """
        shows next question
        :return:
        """
        if self.state.state == States.LAST_QUESTION:
            self.scoretable = show_table.CommandCount(self.model)
            self.scoretable.show()
        else:
            self.category_form.stub.setVisible(False)
            self.state.set_state(States.QUEST_SELECTED)

    def close_question(self):
        """

        :return:
        """
        pass

    def new_category(self):
        """

        :return:
        """
        self.category_form.setVisible(True)

    def timerEvent(self):
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

    def btn_timer_pressed(self):
        """
        starts and stops timer at any moment
        :return:
        """
        if self.state.time:
            self.state.stop_time()
            self.BtnTimer.setText('Старт')
        else:
            self.state.start_time()
            self.BtnTimer.setText('Стоп')

    def set_state_category(self):
        """
        sets controls states when Category Selected
        :return:
        """
        self.set_color('color_idle')
        self.BtnEnd.setEnabled(False)
        self.BtnNew.setEnabled(True)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnNext.setEnabled(True)
        self.BtnTimer.setEnabled(True)
        self.LblDscr.setText("Категория: " + self.state.category.name)
        self.TxtQstn.clear()
        self.LblAnswer.clear()

    def set_state_new_question(self):
        """
        sets controls state when Question exists
        :return:
        """
        self.Timer.display(questiondata.question_time)
        self.Timer.setStyleSheet('color: blue')
        self.set_question_state()
        self.set_question_ui()

    def set_question_ui(self):
        """
        sets ui of question (text and other question data)
        :return:
        """

        actual_category: questiondata.Category = self.state.category
        self.LblDscr.setText("%s:\nВопрос № %i из %i. Стоимость %i " %
                             (actual_category.name, self.state.question + 1, len(actual_category.questions),
                              actual_category.questions[self.state.question].points))
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
                             % actual_category.questions[self.state.question].description)
        self.LblAnswer.setText(actual_category.questions[self.state.question].answer)
        self.category_form.question = question_opened.QuestionDialog(actual_category, self.state.question, self.port,
                                                                     self.model, self.usbhost)
        self.category_form.question.question_signal[int].connect(self.cmd_button_pressed)
        self.state.answer_signal[bool].connect(self.category_form.question.answer_processed)
        self.category_form.question.show()
        if self.category_form.question.image:
            self.category_form.question.image.show()

    def cmd_button_pressed(self, button):
        """
        gets signal from buttons and allows to score a question (change state to answer)
        :return:
        """
        self.state.set_state(States.ANSWER_READY)
        self.state.set_command(self.model.commanddata.get_command_by_button(button))
        self.LblCommand.setText("Отвечает команда «%s»" % self.model.commanddata.commands[self.state.command].name)
        self.LblCommand.setStyleSheet("color: red")

    def btn_true_pressed(self):
        """
        scores a question, sends back scoring signal, sets state to category selected state
        :return:
        """
        self.model.score_question(self.state.command, self.state.category.questions[self.state.question].points)
        if self.state.question != len(self.state.category.questions) - 1:
            self.state.set_state(States.ANSWERED)
        else:
            self.state.set_state(States.LAST_QUESTION)
        self.state.answer_signal.emit(True)

    def btn_false_pressed(self):
        """
        enables answering
        :return:
        """
        self.state.set_state(States.CONTINUE)
        self.state.answer_signal.emit(False)

    def set_state_answer(self):
        """
        sets ui state fir answer
        :return:
        """
        self.set_color('color_idle')
        # self.state.stop_time()
        self.BtnTimer.setText("Старт")
        self.BtnEnd.setEnabled(True)
        self.BtnNew.setEnabled(False)
        self.BtnTrue.setEnabled(True)
        self.BtnFalse.setEnabled(True)
        self.BtnNext.setEnabled(False)
        self.BtnTimer.setEnabled(True)

    def set_state_answered(self):
        """
        sets ui for answered
        :return:
        """
        self.set_color('color_idle')
        self.BtnEnd.setEnabled(False)
        self.BtnNew.setEnabled(True)
        self.BtnNext.setEnabled(True)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnTimer.setEnabled(True)

    def set_state_continue(self):
        """
        sets controls state when Question is continued after wrong answer
        :return:
        """
        self.LblCommand.setText("Отвечает команда:")
        self.set_question_state()

    def set_question_state(self):
        """
        sets ui state for question
        :return:
        """
        self.set_color('color_answer')
        self.BtnEnd.setEnabled(True)
        self.BtnNew.setEnabled(False)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnNext.setEnabled(False)
        self.BtnTimer.setEnabled(True)
        self.BtnTimer.setText('Стоп')

    def set_state_time_ended(self):
        """
        sets controls state for end of time
        :return:
        """
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnFinish.setEnabled(True)
        self.BtnNew.setEnabled(False)
        self.BtnNext.setEnabled(False)
        self.BtnTimer.setEnabled(False)

    def set_state_last_question(self):
        """
        sets ui for last question (next question not available)
        :return:
        """
        self.set_color('color_idle')
        self.BtnEnd.setEnabled(True)
        self.BtnNew.setEnabled(False)
        self.BtnNext.setEnabled(True)
        self.BtnTrue.setEnabled(False)
        self.BtnFalse.setEnabled(False)
        self.BtnTimer.setEnabled(True)

    def btn_test_pressed(self):
        """
        rescan ports and shows pressed buttons for all command
        :return:
        """
        self.port = self.scan_ports()
        if self.port:
            # will be done later
            pass
        else:
            common_functions.error_message("Нет связи с кнопками")

    def menu_settings_pressed(self):
        self.port = self.scan_ports()
        self.settings_form = settings.Settings(self.model, self.port, self.usbhost)
        self.settings_form.show()

    def scan_ports(self) -> Optional[str]:
        """
        returns comport with our radiodevice and updates statusbar
        :return: comport as "COMX" or None
        """
        radioport = self.usbhost.get_device_port()
        if radioport:
            self.statusbar.showMessage("Usb2Radio at port %s is available" % radioport)
            return radioport
        else:
            self.statusbar.showMessage("USB2Radio not found")
            return None

    def set_color(self, color_key: str):
        """
        opens port, tries to set color, closes port
        :param color_key: color key to choose color
        :return:
        """
        opened_port = self.usbhost.open_port(self.port)
        if not opened_port:
            common_functions.error_message("Нет связи с кнопками")
        else:
            clr: List[int] = common_functions.state_color_dict[color_key]
            answer: str = self.usbhost.send_command(opened_port, "SetClrAll", clr[0], clr[1], clr[2])
            if answer in common_functions.wrong_answers:
                self.statusbar.showMessage(common_functions.answer_translate[answer])
            self.usbhost.close_port(opened_port)

    def closeEvent(self, event):
        if self.category_form:
            if self.category_form.question:
                self.category_form.question.close()
            self.category_form.close()
        event.accept()


@logger.catch
def main():
    setup_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = BrainRing()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
