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
        self.media = False
        self.mediapath = ""

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(250)

        self.init_ui(category, number)
        self.parentTimer = timer
        self.LCDTimer.display(self.parentTimer.intValue())

    def init_ui(self, category: questiondata.Category, number):
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        self.setGeometry(screen_res.x()+50, screen_res.y() + 50, screen_res.width()/4*3, screen_res.height() - 100)
        current_question: questiondata.Question = category.questions[number]
        self.LblPoints.setText("Стоимость вопроса: %i" % current_question.points)
        self.LblCategory.setText("Категория: %s" % category.name)
        self.LblQuestion.setText("Вопрос № %i" % (number + 1))
        self.TxtQuestion.setHtml(common_functions.get_question_text(current_question.description))
        filepath: str = current_question.filepath.lower()
        if filepath:
            if os.path.exists(filepath) and (filepath.endswith(".jpg") or filepath.endswith('.png')):
                pixmap = QtGui.QPixmap()
                pixmap.load(filepath)
                self.LblPicture.setScaledContents(True)
                image_height = 2*(screen_res.height() - 100)/3
                image_wight = image_height*4/3
                self.LblPicture.setAlignment(QtCore.Qt.AlignCenter)
                self.LblPicture.setPixmap(pixmap)
                self.LblPicture.setFixedWidth(image_wight)
                self.LblPicture.setFixedHeight(image_height)
                self.LblPicture.setAlignment(QtCore.Qt.AlignCenter)
            elif os.path.exists(filepath) and filepath.endswith('.mp3'):
                self.media = True
                self.mediapath = filepath
            else:
                self.media = True
                self.mediapath = ""
        self.open_port()

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
        if hasattr(self, 'parentTimer'):
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
            if self.image:
                self.image.destroy()
            self.destroy()
        else:
            self.BtnAnswer.setText("Отвечает команда...")

    def closeEvent(self, event):
        if self.image:
            self.image.destroy()
        event.accept()
