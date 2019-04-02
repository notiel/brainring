import settings_ui
import commanddata
import questiondata
from PyQt5 import QtWidgets
from typing import List


class Settings(QtWidgets.QWidget, settings_ui.Ui_Settings):

    def __init__(self, commandmodel):
        super().__init__()
        self.setupUi(self)
        self.SpinBefore.setValue(questiondata.time_low_threshold)
        self.SpinLength.setValue(questiondata.question_time)
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
        for CB in self.checklist:
            CB.stateChanged.connect(self.CommandActivated)
        for CB in self.CBlist:
            caption:str = "Кнопка %i" % (self.CBlist.index(CB) + 1)
            CB.setCurrentText(caption)
            self.CBlabels.append(caption)
            CB.currentTextChanged.connect(self.ButtonSelected)
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