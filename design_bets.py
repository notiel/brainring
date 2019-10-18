# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bets.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(867, 368)
        font = QtGui.QFont()
        font.setPointSize(12)
        Form.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.LstBets = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LstBets.setFont(font)
        self.LstBets.setObjectName("LstBets")
        self.gridLayout.addWidget(self.LstBets, 0, 0, 1, 6)
        self.LblCmd = QtWidgets.QLabel(Form)
        self.LblCmd.setObjectName("LblCmd")
        self.gridLayout.addWidget(self.LblCmd, 2, 0, 1, 1)
        self.SpinScore = QtWidgets.QSpinBox(Form)
        self.SpinScore.setObjectName("SpinScore")
        self.gridLayout.addWidget(self.SpinScore, 2, 4, 1, 1)
        self.CBCmd2 = QtWidgets.QComboBox(Form)
        self.CBCmd2.setObjectName("CBCmd2")
        self.gridLayout.addWidget(self.CBCmd2, 2, 3, 1, 1)
        self.LblCmd2 = QtWidgets.QLabel(Form)
        self.LblCmd2.setObjectName("LblCmd2")
        self.gridLayout.addWidget(self.LblCmd2, 2, 2, 1, 1)
        self.CBCmd1 = QtWidgets.QComboBox(Form)
        self.CBCmd1.setObjectName("CBCmd1")
        self.gridLayout.addWidget(self.CBCmd1, 2, 1, 1, 1)
        self.LblScore = QtWidgets.QLabel(Form)
        self.LblScore.setObjectName("LblScore")
        self.gridLayout.addWidget(self.LblScore, 2, 5, 1, 1)
        self.BtnAdd = QtWidgets.QPushButton(Form)
        self.BtnAdd.setEnabled(True)
        self.BtnAdd.setObjectName("BtnAdd")
        self.gridLayout.addWidget(self.BtnAdd, 3, 5, 1, 1)
        self.LineBet = QtWidgets.QLineEdit(Form)
        self.LineBet.setObjectName("LineBet")
        self.gridLayout.addWidget(self.LineBet, 3, 1, 1, 4)
        self.LblBet = QtWidgets.QLabel(Form)
        self.LblBet.setObjectName("LblBet")
        self.gridLayout.addWidget(self.LblBet, 3, 0, 1, 1)
        self.BtnAdBet = QtWidgets.QPushButton(Form)
        self.BtnAdBet.setEnabled(False)
        self.BtnAdBet.setObjectName("BtnAdBet")
        self.gridLayout.addWidget(self.BtnAdBet, 1, 0, 1, 3)
        self.BtnDeleteBet = QtWidgets.QPushButton(Form)
        self.BtnDeleteBet.setEnabled(False)
        self.BtnDeleteBet.setObjectName("BtnDeleteBet")
        self.gridLayout.addWidget(self.BtnDeleteBet, 1, 3, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Сделать ставки"))
        self.LblCmd.setText(_translate("Form", "Команда"))
        self.LblCmd2.setText(_translate("Form", "ставит на команду"))
        self.LblScore.setText(_translate("Form", "очков"))
        self.BtnAdd.setText(_translate("Form", "Добавить ставку"))
        self.LblBet.setText(_translate("Form", "Суть ставки"))
        self.BtnAdBet.setText(_translate("Form", "Зачесть ставку"))
        self.BtnDeleteBet.setText(_translate("Form", "Удалить ставку"))

