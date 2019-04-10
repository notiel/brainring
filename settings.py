import settings_ui
import commanddata
import questiondata
import usbhost
from PyQt5 import QtWidgets, QtCore
from typing import List, Optional


retry_number = 20


class Settings(QtWidgets.QWidget, settings_ui.Ui_Settings):

    def __init__(self, commandmodel, port):
        super().__init__()
        self.setupUi(self)
        self.SpinBefore.setValue(questiondata.time_low_threshold)
        self.SpinLength.setValue(questiondata.question_time)
        self.scanning: bool = False
        self.port: str = port
        self.opened_port = None
        self.testing: Optional[QtWidgets.QPushButton] = None
        self.retries: int = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.TimerEvent)
        self.timer.start(500)

        self.commanddata: commanddata.CommandTableModel = commandmodel
        self.checklist: List[QtWidgets.QCheckBox] = [self.CB1, self.CB2, self.CB3, self.CB4, self.CB5, self.CB6,
                                                     self.CB7, self.CB8, self.CB9, self.CB10, self.CB11, self.CB12,
                                                     self.CB13, self.CB14, self.CB15, self.CB16]
        self.btnlist: List[QtWidgets.QPushButton] = [self.Btn1, self.Btn2, self.Btn3, self.Btn4, self.Btn5, self.Btn6,
                                                     self.Btn7, self.Btn8, self.Btn9, self.Btn10, self.Btn11,
                                                     self.Btn12, self.Btn13, self.Btn14, self.Btn15, self.Btn16]
        self.CBlist: List[QtWidgets.QComboBox] = [self.CBButton1, self.CBButton2, self.CBButton3, self.CBButton4,
                                                  self.CBButton5, self.CBButton6, self.CBButton7, self.CBButton8,
                                                  self.CBButton9, self.CBButton10, self.CBButton11, self.CBButton12,
                                                  self.CBButton13, self.CBButton14, self.CBButton15, self.CBButton16]
        self.CBlabels: List[str] = list()
        self.initUi()

    def initUi(self):
        if not self.port:
            for btn in self.btnlist:
                btn.setEnabled(False)
        for CB in self.checklist:
            CB.stateChanged.connect(self.CommandActivated)
        for CB in self.CBlist:
            caption: str = "Кнопка %i" % (self.CBlist.index(CB) + 1)
            CB.setCurrentText(caption)
            self.CBlabels.append(caption)
            CB.currentTextChanged.connect(self.ButtonSelected)
        for btn in self.btnlist:
            btn.clicked.connect(self.SelectButtonPressed)
        self.SpinLength.valueChanged.connect(self.QuestionTimeChanged)

    def CommandActivated(self):
        """
        activates and deactivates corresponging command
        :return:
        """
        CB: QtWidgets.QCheckBox = self.sender()
        i: int = self.checklist.index(CB)
        status: bool = CB.isChecked()
        self.btnlist[i].setEnabled(status)
        self.CBlist[i].setEnabled(status)
        if status:
            self.commanddata.enable_command(i)
        else:
            self.commanddata.disable_command(i)

    def ButtonSelected(self):
        """
        selects button for command (each command must have unique button id)
        :return:
        """
        sender: QtWidgets.QComboBox = self.sender()
        current: str = sender.currentText()
        # self.commanddata.data()
        self.commanddata.update_button_id(self.CBlist.index(sender), int(current.replace("Кнопка ", "")))
        # find absent button and set duplicate to absent
        current_labels: List[str] = [CB.currentText() for CB in self.CBlist]
        set_current = set(current_labels)
        if len(set_current) != len(self.CBlabels):
            absent: str = list(set(self.CBlabels) - set_current)[0]
            for CB in self.CBlist:
                if CB != sender and CB.currentText() == current:
                    CB.setCurrentText(absent)
                    self.commanddata.update_button_id(self.CBlist.index(CB), int(absent.replace("Кнопка ", "")))

    def QuestionTimeChanged(self):
        """
        change question length
        :return:
        """
        self.SpinBefore.setMaximum(self.SpinLength.value())
        questiondata.question_time = self.SpinLength.value()

    def TimeLowThresholdChanged(self):
        """
        change time threshold for giving signal that time is almost ended
        :return:
        """
        questiondata.time_low_threshold = self.SpinBefore.value()

    def SelectButtonPressed(self):
        """
        enables timer if any button pressed, button is remembered in self.testing variable
        :return:
        """
        self.opened_port = usbhost.open_port(self.port)
        if not self.opened_port:
            self.port = usbhost.scan_ports()
            if not self.port:
                ErrorMessage("Нет подключенных кнопок")
                return
            else:
                self.opened_port = usbhost.open_port(self.port)
        error = usbhost.reset_timer(self.opened_port)
        if error:
            ErrorMessage(error)
            return
        self.testing = self.sender()
        self.scanning = True
        self.retries = 0
        self.LblInstruction.setText("Ждем ответа кнопки")
        print("Successfully started timer")

    def TimerEvent(self):
        """
        if timer as active, try to get button pressed
        :return:
        """
        if self.scanning:
            caption = self.LblInstruction.text() + "."
            self.LblInstruction.setText(caption)
            self.retries += 1
            button: int = usbhost.get_first_button(self.opened_port)
            if button:
                self.CBlist[self.btnlist.index(self.testing)].setCurrentText("Кнопка %i" % button)
                usbhost.close_port(self.opened_port)
                self.opened_port = None
            print(self.retries)
            if self.retries > retry_number:
                ErrorMessage("Ни одна кнопка не нажата в течение 10 секунд, попробуйте еще раз")
                self.scanning = False
                usbhost.close_port(self.opened_port)
                self.opened_port = None
                self.LblInstruction.setText("Нажмите на кнопку с именем команды для автоопределения")


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
