import question
from PyQt5 import QtWidgets, QtCore, QtGui
import questiondata
import common_functions
import os


class QuestionDialog(QtWidgets.QWidget, question.Ui_Form):

    question_signal = QtCore.pyqtSignal(int)

    def __init__(self, category: questiondata.Category, number, model, my_usbhost, used_buttons, timer):
        super().__init__()
        self.setupUi(self)
        self.count: int = 0
        self.model = model
        self.opened_port = None
        self.scanning = False
        self.usbhost = my_usbhost
        self.used_buttons = used_buttons
        self.image = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(250)

        self.init_ui(category, number)
        self.parentTimer = timer
        self.LCDTimer.display(self.parentTimer.intValue())

        self.open_port()

    def init_ui(self, category: questiondata.Category, number):
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
        answer = self.usbhost.send_command("RstTmr")
        if answer in common_functions.wrong_answers:
            common_functions.error_message(common_functions.answer_translate[answer])
            return
        self.scanning = True

    def timerEvent(self):
        """
        decreases timer every second and scans buttons if scanning mode enables
        :return:
        """
        current = self.parentTimer.intValue()
        if current > 0:
            self.LCDTimer.display(current)
            if current == questiondata.time_low_threshold:
                self.LCDTimer.setStyleSheet("color: red")
        if self.scanning:
            button: int = common_functions.get_first_button(self.usbhost, "answer", self.used_buttons)
            if button:
                commands = self.model.commanddata
                self.BtnAnswer.setText("Отвечает команда «%s»" %
                                       commands.commands[commands.get_command_by_button(button)].name)
                self.BtnAnswer.setStyleSheet("color: red")
                self.scanning = False
                self.usbhost.close_port()
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
            self.BtnAnswer.setText("Отвечает команда...")

    def closeEvent(self, event):
        if self.image:
            self.image.destroy()
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
