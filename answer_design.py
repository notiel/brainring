# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Answer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1215, 225)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.LblHeader = QtWidgets.QLabel(Form)
        self.LblHeader.setMaximumSize(QtCore.QSize(16777215, 150))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.LblHeader.setFont(font)
        self.LblHeader.setStyleSheet("color: red")
        self.LblHeader.setObjectName("LblHeader")
        self.gridLayout.addWidget(self.LblHeader, 0, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.LblAnswer = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.LblAnswer.setFont(font)
        self.LblAnswer.setObjectName("LblAnswer")
        self.gridLayout.addWidget(self.LblAnswer, 1, 0, 1, 2, QtCore.Qt.AlignHCenter)
        self.LblPicture = QtWidgets.QLabel(Form)
        self.LblPicture.setText("")
        self.LblPicture.setObjectName("LblPicture")
        self.gridLayout.addWidget(self.LblPicture, 2, 0, 1, 2, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Ответ"))
        self.LblHeader.setText(_translate("Form", "  Ответ"))
        self.LblAnswer.setText(_translate("Form", "Текст ответа"))

