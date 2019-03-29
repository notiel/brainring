# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Stub.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(813, 649)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LblCatLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.LblCatLabel.setFont(font)
        self.LblCatLabel.setObjectName("LblCatLabel")
        self.verticalLayout.addWidget(self.LblCatLabel, 0, QtCore.Qt.AlignHCenter)
        self.LblCat = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(48)
        self.LblCat.setFont(font)
        self.LblCat.setStyleSheet("color:blue;")
        self.LblCat.setObjectName("LblCat")
        self.verticalLayout.addWidget(self.LblCat, 0, QtCore.Qt.AlignHCenter)
        self.LblNumberlabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.LblNumberlabel.setFont(font)
        self.LblNumberlabel.setObjectName("LblNumberlabel")
        self.verticalLayout.addWidget(self.LblNumberlabel, 0, QtCore.Qt.AlignHCenter)
        self.LblNumber = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(48)
        self.LblNumber.setFont(font)
        self.LblNumber.setStyleSheet("color: blue;")
        self.LblNumber.setObjectName("LblNumber")
        self.verticalLayout.addWidget(self.LblNumber, 0, QtCore.Qt.AlignHCenter)
        self.LblPointsLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.LblPointsLabel.setFont(font)
        self.LblPointsLabel.setObjectName("LblPointsLabel")
        self.verticalLayout.addWidget(self.LblPointsLabel, 0, QtCore.Qt.AlignHCenter)
        self.LblPoints = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(48)
        self.LblPoints.setFont(font)
        self.LblPoints.setStyleSheet("color: blue;")
        self.LblPoints.setObjectName("LblPoints")
        self.verticalLayout.addWidget(self.LblPoints, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Категория"))
        self.LblCatLabel.setText(_translate("Form", "Категория:"))
        self.LblCat.setText(_translate("Form", "Имя"))
        self.LblNumberlabel.setText(_translate("Form", "Количество вопросов: "))
        self.LblNumber.setText(_translate("Form", "1"))
        self.LblPointsLabel.setText(_translate("Form", "Стоимость вопроса: "))
        self.LblPoints.setText(_translate("Form", "100"))

