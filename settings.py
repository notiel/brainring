import settings_ui
import commanddata
import questiondata
import common_functions
from PyQt5 import QtWidgets, QtCore
from typing import List, Optional


retry_number = 20


class Settings(QtWidgets.QWidget, settings_ui.Ui_Settings):

    timer_signal = QtCore.pyqtSignal(int)
    end_signal = QtCore.pyqtSignal(int)

    def __init__(self, commandmodel, my_usbhost):
        super().__init__()
        self.setupUi(self)
        self.usbhost = my_usbhost
        self.scanning: bool = False
        self.testing: Optional[QtWidgets.QPushButton] = None
        self.retries: int = 0
        self.commanddata: commanddata.CommandTableModel = commandmodel

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(500)

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

        self.SpinBefore.setValue(questiondata.time_low_threshold)
        self.SpinLength.setValue(questiondata.question_time)

        self.init_ui()

    def init_ui(self):
        for CB in self.checklist:
            CB.stateChanged.connect(self.command_activated)
        for CB in self.CBlist:
            caption: str = "Кнопка %i" % (self.CBlist.index(CB) + 1)
            CB.setCurrentText(caption)
            self.CBlabels.append(caption)
            CB.currentTextChanged.connect(self.button_selected)
        for btn in self.btnlist:
            btn.clicked.connect(self.btn_select_pressed)
        for i in range(len(self.commanddata.commanddata.commands)):
            value = self.commanddata.commanddata.commands[i].available
            self.checklist[i].setChecked(value)
            self.btnlist[i].setEnabled(value)
            self.CBlist[i].setEnabled(value)
        if not self.port:
            for btn in self.btnlist:
                btn.setEnabled(False)
        self.SpinLength.valueChanged.connect(self.question_time_changed)

    def command_activated(self):
        """
        activates and deactivates corresponging command
        :return:
        """
        cb: QtWidgets.QCheckBox = self.sender()
        i: int = self.checklist.index(cb)
        status: bool = cb.isChecked()
        if self.port:
            self.btnlist[i].setEnabled(status)
        self.CBlist[i].setEnabled(status)
        if status:
            self.commanddata.enable_command(i)
        else:
            self.commanddata.disable_command(i)
        common_functions.update_button_list(self.usbhost, self.commanddata.commanddata.get_available_commands_list())

    def button_selected(self):
        """
        selects button for command (each command must have unique button id)
        :return:
        """
        sender: QtWidgets.QComboBox = self.sender()
        current: str = sender.currentText()
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

    def question_time_changed(self):
        """
        change question length
        :return:
        """
        self.SpinBefore.setMaximum(self.SpinLength.value())
        questiondata.question_time = self.SpinLength.value()
        self.timer_signal.emit(self.SpinLength.value())

    def time_low_threshold_changed(self):
        """
        change time threshold for giving signal that time is almost ended
        :return:
        """
        questiondata.time_low_threshold = self.SpinBefore.value()
        self.end_signal.emit(self.SpinBefore.value())

    def btn_select_pressed(self):
        """
        enables timer if any button pressed, button is remembered in self.testing variable
        :return:
        """
        error = self.usbhost.send_command("rsttmr")
        if error in common_functions.wrong_answers:
            common_functions.error_message(common_functions.answer_translate[error])
            return
        self.testing = self.sender()
        self.scanning = True
        self.retries = 0
        self.LblInstruction.setText("Ждем ответа кнопки")
        print("Successfully started timer")

    def timerEvent(self):
        """
        if timer as active, try to get button pressed
        :return:
        """
        if self.scanning:
            print('scan')
            caption = self.LblInstruction.text() + "."
            self.LblInstruction.setText(caption)
            self.retries += 1
            button: int = common_functions.get_first_button(self.usbhost, "idle", list())
            if button:
                self.CBlist[self.btnlist.index(self.testing)].setCurrentText("Кнопка %i" % button)
                self.state_not_scanning()
            if self.retries > retry_number:
                common_functions.error_message("Ни одна кнопка не нажата в течение 10 секунд, попробуйте еще раз")
                self.state_not_scanning()

    def state_not_scanning(self):
        """
        closes port, sets not scanning state
        :return:
        """
        self.scanning = False
        self.LblInstruction.setText("Нажмите на кнопку с именем команды для автоопределения")
