import question
from PyQt5 import QtWidgets, QtCore, QtGui
import questiondata
import common_functions
import os


class QuestionDialog(QtWidgets.QWidget, question.Ui_Form):

    question_signal = QtCore.pyqtSignal(int)

    def __init__(self, category: questiondata.Category, number, port, model, my_usbhost, used_buttons):
        super().__init__()
        self.setupUi(self)
        self.count: int = 0
        self.port = port
        self.model = model
        self.opened_port = None
        self.scanning = False
        self.usbhost = my_usbhost
        self.used_buttons = used_buttons

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
        self.TxtQuestion.setHtml(common_functions.get_question_text(current_question.description))
        self.image = None
        filepath: str = current_question.filepath.lower()
        if filepath:
            if os.path.exists(filepath) and (filepath.endswith(".jpg") or filepath.endswith('.png')):
                self.image = ImageShow(filepath)
            elif os.path.exists(filepath) and filepath.endswith('.mp3'):
                os.system(r"start %s" % filepath)
            else:
                common_functions.error_message("Файла с медиаконтентом не существует или формат неверный")

    def open_port(self):
        """
        opens serial port and change state to scanning

        :return:
        """
        self.opened_port = self.usbhost.open_port(self.port)
        if not self.opened_port:
            self.port = self.usbhost.get_device_port()
            if not self.port:
                common_functions.error_message("Нет подключенных кнопок")
                return
            else:
                self.opened_port = self.usbhost.open_port(self.port)
        answer = self.usbhost.send_command(self.opened_port, "RstTmr")
        if answer in common_functions.wrong_answers:
            common_functions.error_message(common_functions.answer_translate[answer])
            return
        self.scanning = True

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
            button: int = common_functions.get_first_button(self.usbhost, self.opened_port, "answer", self.used_buttons)
            if button != None:
                commands = self.model.commanddata
                self.BtnAnswer.setText("Отвечает команда «%s»" %
                                       commands.commands[commands.get_command_by_button(button)].name)
                self.BtnAnswer.setStyleSheet("color: red")
                self.scanning = False
                self.usbhost.close_port(self.opened_port)
                self.question_signal.emit(button)

    def answer_processed(self, result):
        """
        destroys question form if answered
        :param result:
        :return:
        """
        if result:
            self.destroy()
        else:
            self.open_port()
            self.BtnAnswer.setText("Отвечает команда...")

    def closeEvent(self, event):
        if self.image:
            self.image.destroy()
        if self.opened_port:
            self.usbhost.close_port(self.opened_port)
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
