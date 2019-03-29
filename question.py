# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Question.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1215, 778)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.LblPoints = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.LblPoints.setFont(font)
        self.LblPoints.setObjectName("LblPoints")
        self.gridLayout.addWidget(self.LblPoints, 2, 0, 1, 1)
        self.LblCategory = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.LblCategory.setFont(font)
        self.LblCategory.setObjectName("LblCategory")
        self.gridLayout.addWidget(self.LblCategory, 0, 0, 1, 1)
        self.LCDTimer = QtWidgets.QLCDNumber(Form)
        self.LCDTimer.setStyleSheet("color:blue;")
        self.LCDTimer.setDigitCount(3)
        self.LCDTimer.setProperty("value", 100.0)
        self.LCDTimer.setProperty("intValue", 100)
        self.LCDTimer.setObjectName("LCDTimer")
        self.gridLayout.addWidget(self.LCDTimer, 0, 1, 3, 1)
        self.LblQuestion = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.LblQuestion.setFont(font)
        self.LblQuestion.setObjectName("LblQuestion")
        self.gridLayout.addWidget(self.LblQuestion, 1, 0, 1, 1)
        self.TxtQuestion = QtWidgets.QTextBrowser(Form)
        self.TxtQuestion.setObjectName("TxtQuestion")
        self.gridLayout.addWidget(self.TxtQuestion, 3, 0, 1, 2)
        self.BtnAnswer = QtWidgets.QPushButton(Form)
        self.BtnAnswer.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.BtnAnswer.setFont(font)
        self.BtnAnswer.setObjectName("BtnAnswer")
        self.gridLayout.addWidget(self.BtnAnswer, 4, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Вопрос"))
        self.LblPoints.setText(_translate("Form", "Стоимость вопроса: 100"))
        self.LblCategory.setText(_translate("Form", "Категория: пословицы"))
        self.LblQuestion.setText(_translate("Form", "Вопрос № 1"))
        self.TxtQuestion.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Calibri\'; font-size:30pt; font-weight:600; color:#000000;\">В архипелаге Норденшельда есть острова Тугут, Корсар и Грозный, названные так экспедицией Толя. Там же есть остров Матрос, имя которому дал экипаж судна «Норд» в честь своего друга. На Таймыре мы можем увидеть гору Верти и мыс Дика.Кем же были те, в чью честь названы эти объекты?»</span></p></body></html>"))
        self.BtnAnswer.setText(_translate("Form", "Отвечает команда..."))

