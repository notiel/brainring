from PyQt5 import QtWidgets, QtGui
from typing import Optional, List
import re
state_color_dict = {'color_idle': (255, 200, 0),
                    'color_answer': (0, 255, 255),
                    'color_pressed': (0, 255, 0),
                    'color_pressed_second': (0, 0, 255)}
pause_ms = 500
wrong_answers = ['Bad data', "Unknown command", "No device port", 'Port error']
answer_translate = {'Bad data': "Неверные данные", "Unknown command": 'Неизвестная команда',
                    "No device port": "Устройство не подключено", "Port error": "Ошибка порта"}
font_sizes = {10: 50, 50: 50, 100: 48, 200: 36, 250: 30, 500: 24}


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
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        used_height = screen_res.height() - 80
        pixmap_resized = pixmap.scaledToHeight(2*used_height/3 - 20)
        self.imageLabel.setPixmap(pixmap_resized)
        self.setGeometry(screen_res.x() + 5, screen_res.y() + used_height / 3 + 20, screen_res.width() - 10,
                         2 * used_height / 3 - 20)
        print(screen_res.width() - 10)
        print(2 * used_height / 3 - 20)


def resize_to_third(window):
    """"""
    current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
    screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
    window.setGeometry(screen_res.x() + 5, screen_res.y() + 40, screen_res.width() - 10, screen_res.height() / 3 - 40)


def error_message(text):
    """
    shows error window with text
    :param text: error text
    :return:
    """
    error = QtWidgets.QMessageBox()
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Ошибка!')
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


def get_first_button(usbhost, state: str, used_buttons: List[int]) -> Optional[int]:
    """
    asks comport about buttons pressed
    :param used_buttons: list of already used buttons. we may not return them
    :param usbhost: usbhost class example for send commands to usb
    :param state: state to get color back ("idle" for idle color, "question" for question color"
    :return: number of first pressed button
    """
    answer = usbhost.send_query("Getbtns")
    if answer in wrong_answers:
        return -1
    buttons: str = answer.replace("Btns: ", "")
    btn = get_first_button_from_answer(buttons, used_buttons)
    if btn:
        clr1 = state_color_dict['color_pressed']
        clr2 = state_color_dict['color_answer'] if state == 'answer' else state_color_dict['color_idle']
        usbhost.send_query("Flash", btn, clr1[0], clr1[1], clr1[2], pause_ms, clr2[0], clr2[1], clr2[2])
    return btn


def get_first_button_from_answer(answer: str, used_buttons: List[int]) -> Optional[int]:
    """

    :param answer: string with answer from radio
    :param used_buttons: list of already used buttons. we may not return them
    :return:
    """
    answer_list: List[str] = answer.split()
    button_keys: List[int] = [int(button) for button in answer_list[::2]]
    buttons_values: List[int] = [int(value) for value in answer_list[1::2]]
    buttons_list = list(zip(button_keys, buttons_values))
    buttons_list = [btn for btn in buttons_list if btn[1] not in [0, -1] and btn[0] not in used_buttons]
    buttons_list.sort(key=lambda i: i[1])
    if buttons_list:
        return buttons_list[0][0]
    return None


def update_button_list(usbhost, buttons: List[int]) -> str:
    """
    updates button list for host
    :param usbhost: serial port with host
    :param buttons: list of available buttons
    :return: error or empty string
    """
    answer = usbhost.send_query("SetBtnList", *buttons)
    if answer in wrong_answers:
        return answer_translate[answer]
    return ""


def get_questions_text_size(question: str) -> int:
    """
    gets size for text
    :param question: question text wit no format
    :return: font size
    """
    for key in sorted(font_sizes.keys()):
        if len(question) < key:
            return font_sizes[key]
    # if all length are incorrect take last
    if font_sizes.keys():
        return font_sizes[sorted(font_sizes.keys())[-1]]
    # 30 by default
    return 30


def get_question_text(question: str) -> str:
    """
    gets formatted question text
    :param question:
    :return:
    """
    font_size = get_questions_text_size(question)
    html = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
    html += "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    html += "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
    html += "p, li { white-space: pre-wrap; }\n"
    html += "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; "
    html += "font-weight:400; font-style:normal;\">\n"
    html += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
    html += " -qt-block-indent:0; text-indent:0px;\">"
    html += "<span style=\" font-family:\'Calibri\'; font-size:%ipt; " % font_size
    html += "color:#000000;\">%s</span></p></body></html>" % question
    html = get_formatted_question_text(html, font_size)
    return html


def get_formatted_question_text(question: str, fontsize: int) -> str:
    """
    gets text with bold, italic and underline
    :param question: text of question
    :param fontsize: font size
    :return:
    """
    text = re.sub(r'<b>(.+?)</b?>',
                  r'<span style=" font-family:\'Calibri\'; font-size:%ipt; font-weight:600; color:#000000;">\1</span>'
                  r'<span style=" font-family:\'Calibri\'; font-size:%ipt; color:#000000;">'
                  % (fontsize, fontsize), question)
    text = re.sub(r'<i>(.+?)</i?>',
                  r'<span style=" font-family:\'Calibri\'; font-size:%ipt;  font-style:italic; color:#000000;">\1'
                  r'</span><span style=" font-family:\'Calibri\'; font-size:%ipt; color:#000000;">'
                  % (fontsize, fontsize), text)
    text = re.sub(r'<u>(.+?)</u?>',
                  r'<span style=" font-family:\'Calibri\'; font-size:%ipt;   '
                  r'text-decoration: underline; color:#000000;">\1'
                  r'</span><span style=" font-family:\'Calibri\'; font-size:%ipt; color:#000000;">'
                  % (fontsize, fontsize), text)
    return text
