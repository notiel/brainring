import settings_ui
import commanddata
from PyQt5 import QtWidgets
from typing import List


class Settings(QtWidgets.QWidget, settings_ui.Ui_Settings):

    def __init__(self, commands):
        super().__init__()
        self.setupUi(self)
        self.commanddata: commanddata.Commands = commands
        self.checklist = [self.CB1, self.CB2, self.CB3, self.CB4, self.CB5, self.CB6, self.CB7, self.CB8, self.CB9,
                          self.CB10, self.CB11, self.CB11, self.CB12, self.CB13, self.CB14, self.CB15, self.CB16]
        self.btnlist = [self.Btn1, self.Btn2, self.Btn3, self.Btn4, self.Btn5, self.Btn6, self.Btn7, self.Btn8,
                        self.Btn9, self.Btn10, self.Btn11, self.Btn12, self.Btn13, self.Btn14, self.Btn15, self.Btn16]
        self.CBlist = [self.CBButton1, self.CBButton2, self.CBButton3, self.CBButton4, self.CBButton5,
                       self.CBButton6, self.CBButton7, self.CBButton8, self.CBButton9, self.CBButton10, self.CBButton11,
                       self.CBButton12, self.CBButton13, self.CBButton14, self.CBButton15, self.CBButton16]
        self.CBlabels = list()
        self.initUi()

    def initUi(self):

        for CB in self.checklist:
            CB.stateChanged.connect(self.CommandActivated)
        for CB in self.CBlist:
            caption = "Кнопка %i" % (self.CBlist.index(CB) + 1)
            CB.setCurrentText(caption)
            self.CBlabels.append(caption)
            CB.currentTextChanged.connect(self.ButtonSelected)

    def CommandActivated(self):
        """
        activates
        :return:
        """
        CB = self.sender()
        i = self.checklist.index(CB)
        if CB.isChecked():
            self.btnlist[i].setEnabled(True)
            self.CBlist[i].setEnabled(True)
            self.commanddata.commands[i].available = True
        else:
            self.btnlist[i].setEnabled(False)
            self.CBlist[i].setEnabled(False)
            self.commanddata.commands[i].available = False

    def ButtonSelected(self):
        sender: QtWidgets.QComboBox = self.sender()
        current: str = sender.currentText()
        self.commanddata.commands[self.CBlist.index(sender)].button_id = int(current.replace("Кнопка ", ""))
        current_labels: List[str] = [CB.currentText() for CB in self.CBlist]
        set_current = set(current_labels)
        if len(set_current) != len(self.CBlabels):
            absent = list(set(self.CBlabels) - set_current)[0]
            for CB in self.CBlist:
                if CB != sender and CB.currentText() == current:
                    CB.setCurrentText(absent)
                    self.commanddata.commands[self.CBlist.index(CB)].button_id = int(absent.replace("Кнопка ", ""))
