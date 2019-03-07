import question
from PyQt5 import QtWidgets, QtCore
import questiondata


class QuestionDialog(QtWidgets.QWidget, question.Ui_Form):
    def __init__(self, category: questiondata.Category):
        super().__init__()
        self.setupUi(self)

        self.count = 0
        self.LblPoints.setText("Стоимость вопроса: %i" % category.questions[0].points)
        self.LblCategory.setText("Категория: %s" % category.name)
        self.LblQuestion.setText("Вопрос № 1")
        self.TxtQuestion.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                 "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                 "p, li { white-space: pre-wrap; }\n"
                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; "
                                 "font-weight:400; font-style:normal;\">\n"
                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
                                 " -qt-block-indent:0; text-indent:0px;\">"
                                 "<span style=\" font-family:\'Calibri\'; font-size:30pt; "
                                 "font-weight:600; color:#000000;\">%s</span></p></body></html>"
                                 % category.questions[0].description)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.LCDTimer.display(questiondata.question_time)

    def timerEvent(self):
        """
        decreases timer every second
        :return:
        """
        current = self.LCDTimer.intValue()
        if current > 0:
            self.LCDTimer.display(current - 1)
            if current == questiondata.time_low_threshold + 1:
                self.LCDTimer.setStyleSheet("color: red")

# def open_question(category: questiondata.Category):
#     """
#     shows current question window
#     :return:
#     """
#     question_window = QuestionDialog(category)
#     question_window.show()
