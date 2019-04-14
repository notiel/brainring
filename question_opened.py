import question
from PyQt5 import QtWidgets, QtCore, QtGui
import questiondata
import common_functions
import usbhost
import os


class QuestionDialog(QtWidgets.QWidget, question.Ui_Form):

    question_signal = QtCore.pyqtSignal(int)

    def __init__(self, category: questiondata.Category, number, port):
        super().__init__()
        self.setupUi(self)
        self.count: int = 0
        self.port = port
        self.opened_port = None
        self.scanning = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)
        self.LCDTimer.display(questiondata.question_time)

        self.image = None
        self.initUi(category, number)
        self.open_port()

    def initUi(self, category: questiondata.Category, number):
        current_question: questiondata.Question = category.questions[number]
        self.LblPoints.setText("Стоимость вопроса: %i" % current_question.points)
        self.LblCategory.setText("Категория: %s" % category.name)
        self.LblQuestion.setText("Вопрос № %i" % (number + 1))
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
                                 % current_question.description)
        self.image = None
        filepath: str = current_question.filepath.lower()
        if filepath:
            if os.path.exists(filepath) and (filepath.endswith(".jpg") or filepath.endswith('.png')):
                self.image = ImageShow(filepath)
            else:
                common_functions.error_message("Файла с картинкой не существует")

    def open_port(self):
        """
        opens serial port and change state to scanning

        :return:
        """
        self.opened_port = usbhost.open_port(self.port)
        if not self.opened_port:
            self.port = usbhost.scan_ports()
            if not self.port:
                common_functions.error_message("Нет подключенных кнопок")
                return
            else:
                self.opened_port = usbhost.open_port(self.port)
        error = usbhost.reset_timer(self.opened_port)
        if error:
            common_functions.error_message(error)
            return
        self.scanning = True
        usbhost.reset_timer(self.opened_port)

    def timerEvent(self):
        """
        decreases timer every second and scans buttons if scanning mode enables
        :return:
        """
        if self.scanning:
            current = self.LCDTimer.intValue()
            if current > 0:
                self.LCDTimer.display(current - 1)
                if current == questiondata.time_low_threshold + 1:
                    self.LCDTimer.setStyleSheet("color: red")
            button: int = usbhost.get_first_button(self.opened_port)
            print(button)
            if button:
                self.BtnAnswer.setText("Отвечает команда %i" % button)
                self.question_signal.emit(button)
                self.scanning = False
                usbhost.close_port(self.opened_port)

    def closeEvent(self, event):
        if self.image:
            self.image.destroy()
        if self.opened_port:
            usbhost.close_port(self.opened_port)
        event.accept()


class ImageShow(QtWidgets.QWidget):
    def __init__(self, filepath: str):
        super().__init__()
        self.setWindowTitle(" ")
        layout = QtWidgets.QVBoxLayout(self)
        self.imageLabel = QtWidgets.QLabel("No image")
        self.imageLabel.setScaledContents(True)
        layout.addWidget(self.imageLabel)
        pixmap = QtGui.QPixmap()
        pixmap.load(filepath)
        self.imageLabel.setPixmap(pixmap)
