# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignMain.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1450, 921)
        MainWindow.setMinimumSize(QtCore.QSize(1330, 0))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.BtnEnd = QtWidgets.QPushButton(self.centralwidget)
        self.BtnEnd.setEnabled(False)
        self.BtnEnd.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.BtnEnd.setFont(font)
        self.BtnEnd.setObjectName("BtnEnd")
        self.gridLayout.addWidget(self.BtnEnd, 9, 4, 1, 1)
        self.LblPnts = QtWidgets.QLabel(self.centralwidget)
        self.LblPnts.setMinimumSize(QtCore.QSize(0, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LblPnts.setFont(font)
        self.LblPnts.setObjectName("LblPnts")
        self.gridLayout.addWidget(self.LblPnts, 0, 3, 1, 1)
        self.BtnTrue = QtWidgets.QPushButton(self.centralwidget)
        self.BtnTrue.setEnabled(False)
        self.BtnTrue.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.BtnTrue.setFont(font)
        self.BtnTrue.setStyleSheet("background-color:rgb(5, 255, 1)")
        self.BtnTrue.setObjectName("BtnTrue")
        self.gridLayout.addWidget(self.BtnTrue, 8, 0, 1, 1)
        self.BtnNew = QtWidgets.QPushButton(self.centralwidget)
        self.BtnNew.setEnabled(False)
        self.BtnNew.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BtnNew.setFont(font)
        self.BtnNew.setObjectName("BtnNew")
        self.gridLayout.addWidget(self.BtnNew, 9, 0, 1, 1)
        self.BtnFinish = QtWidgets.QPushButton(self.centralwidget)
        self.BtnFinish.setEnabled(False)
        self.BtnFinish.setMinimumSize(QtCore.QSize(250, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BtnFinish.setFont(font)
        self.BtnFinish.setObjectName("BtnFinish")
        self.gridLayout.addWidget(self.BtnFinish, 9, 1, 1, 1)
        self.BtnTest = QtWidgets.QPushButton(self.centralwidget)
        self.BtnTest.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BtnTest.setFont(font)
        self.BtnTest.setObjectName("BtnTest")
        self.gridLayout.addWidget(self.BtnTest, 8, 4, 1, 1)
        self.LblTmr = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LblTmr.setFont(font)
        self.LblTmr.setObjectName("LblTmr")
        self.gridLayout.addWidget(self.LblTmr, 7, 2, 1, 1)
        self.BtnFalse = QtWidgets.QPushButton(self.centralwidget)
        self.BtnFalse.setEnabled(False)
        self.BtnFalse.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BtnFalse.setFont(font)
        self.BtnFalse.setStyleSheet("background-color: red;")
        self.BtnFalse.setObjectName("BtnFalse")
        self.gridLayout.addWidget(self.BtnFalse, 8, 1, 1, 1)
        self.LblCommand = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LblCommand.setFont(font)
        self.LblCommand.setObjectName("LblCommand")
        self.gridLayout.addWidget(self.LblCommand, 7, 0, 1, 2)
        self.Timer = QtWidgets.QLCDNumber(self.centralwidget)
        self.Timer.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.Timer.setStyleSheet("color: rgb(0, 0, 255)")
        self.Timer.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.Timer.setFrameShadow(QtWidgets.QFrame.Plain)
        self.Timer.setLineWidth(0)
        self.Timer.setMidLineWidth(10)
        self.Timer.setSmallDecimalPoint(True)
        self.Timer.setDigitCount(3)
        self.Timer.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.Timer.setProperty("value", 100.0)
        self.Timer.setProperty("intValue", 100)
        self.Timer.setObjectName("Timer")
        self.gridLayout.addWidget(self.Timer, 8, 2, 4, 1)
        self.BtnNext = QtWidgets.QPushButton(self.centralwidget)
        self.BtnNext.setEnabled(False)
        self.BtnNext.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BtnNext.setFont(font)
        self.BtnNext.setObjectName("BtnNext")
        self.gridLayout.addWidget(self.BtnNext, 8, 3, 1, 1)
        self.TxtQstn = QtWidgets.QTextBrowser(self.centralwidget)
        self.TxtQstn.setMinimumSize(QtCore.QSize(0, 0))
        self.TxtQstn.setMaximumSize(QtCore.QSize(2000, 16777215))
        self.TxtQstn.setObjectName("TxtQstn")
        self.gridLayout.addWidget(self.TxtQstn, 3, 0, 1, 3)
        self.TblCmnd = QtWidgets.QTableView(self.centralwidget)
        self.TblCmnd.setMinimumSize(QtCore.QSize(750, 0))
        self.TblCmnd.setMaximumSize(QtCore.QSize(2000, 2000))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.TblCmnd.setFont(font)
        self.TblCmnd.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TblCmnd.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.TblCmnd.setLineWidth(2)
        self.TblCmnd.setMidLineWidth(2)
        self.TblCmnd.setObjectName("TblCmnd")
        self.gridLayout.addWidget(self.TblCmnd, 2, 3, 2, 2)
        self.BtnTimer = QtWidgets.QPushButton(self.centralwidget)
        self.BtnTimer.setEnabled(True)
        self.BtnTimer.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BtnTimer.setFont(font)
        self.BtnTimer.setObjectName("BtnTimer")
        self.gridLayout.addWidget(self.BtnTimer, 9, 3, 1, 1)
        self.LblDscr = QtWidgets.QLabel(self.centralwidget)
        self.LblDscr.setMinimumSize(QtCore.QSize(0, 45))
        self.LblDscr.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LblDscr.setFont(font)
        self.LblDscr.setObjectName("LblDscr")
        self.gridLayout.addWidget(self.LblDscr, 0, 0, 1, 3)
        self.BtnMusic = QtWidgets.QPushButton(self.centralwidget)
        self.BtnMusic.setEnabled(False)
        self.BtnMusic.setObjectName("BtnMusic")
        self.gridLayout.addWidget(self.BtnMusic, 4, 0, 1, 1)
        self.LblAnswer = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.LblAnswer.setFont(font)
        self.LblAnswer.setObjectName("LblAnswer")
        self.gridLayout.addWidget(self.LblAnswer, 5, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1450, 26))
        self.menubar.setObjectName("menubar")
        self.Game = QtWidgets.QMenu(self.menubar)
        self.Game.setObjectName("Game")
        self.Settings = QtWidgets.QMenu(self.menubar)
        self.Settings.setObjectName("Settings")
        self.Bets = QtWidgets.QMenu(self.menubar)
        self.Bets.setObjectName("Bets")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Settings_2 = QtWidgets.QAction(MainWindow)
        self.Settings_2.setObjectName("Settings_2")
        self.Open = QtWidgets.QAction(MainWindow)
        self.Open.setObjectName("Open")
        self.EndGame = QtWidgets.QAction(MainWindow)
        self.EndGame.setObjectName("EndGame")
        self.MenuBet = QtWidgets.QAction(MainWindow)
        self.MenuBet.setObjectName("MenuBet")
        self.Game.addAction(self.Open)
        self.Game.addAction(self.EndGame)
        self.Settings.addAction(self.Settings_2)
        self.Bets.addAction(self.MenuBet)
        self.menubar.addAction(self.Game.menuAction())
        self.menubar.addAction(self.Bets.menuAction())
        self.menubar.addAction(self.Settings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Шевели извилиной"))
        self.BtnEnd.setText(_translate("MainWindow", "Новый раунд"))
        self.LblPnts.setText(_translate("MainWindow", "Счет команд:"))
        self.BtnTrue.setText(_translate("MainWindow", "Верный ответ"))
        self.BtnNew.setText(_translate("MainWindow", "Новый вопрос"))
        self.BtnFinish.setText(_translate("MainWindow", "Завершить вопрос"))
        self.BtnTest.setText(_translate("MainWindow", "Тест кнопок"))
        self.LblTmr.setText(_translate("MainWindow", "Оставшееся время:"))
        self.BtnFalse.setText(_translate("MainWindow", "Неверный ответ"))
        self.LblCommand.setText(_translate("MainWindow", "Отвечает команда: "))
        self.BtnNext.setText(_translate("MainWindow", "Далее"))
        self.TxtQstn.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.BtnTimer.setText(_translate("MainWindow", "Старт"))
        self.LblDscr.setText(_translate("MainWindow", "Тема не выбрана"))
        self.BtnMusic.setText(_translate("MainWindow", "Проиграть звук"))
        self.LblAnswer.setText(_translate("MainWindow", "Ответ: "))
        self.Game.setTitle(_translate("MainWindow", "Игра"))
        self.Settings.setTitle(_translate("MainWindow", "Настройки"))
        self.Bets.setTitle(_translate("MainWindow", "Ставки"))
        self.Settings_2.setText(_translate("MainWindow", "Настройки"))
        self.Open.setText(_translate("MainWindow", "Открыть"))
        self.EndGame.setText(_translate("MainWindow", "Завершить игру"))
        self.MenuBet.setText(_translate("MainWindow", "Ставки"))

