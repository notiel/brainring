from PyQt5 import QtWidgets
from typing import Optional, List
state_color_dict = {'color_idle': (255, 200, 0),
                    'color_answer': (0, 255, 255),
                    'color_pressed': (0, 255, 0),
                    'color_pressed_second': (0, 0, 255)}
pause_ms = 500
wrong_answers = ['Bad data', "Unknown command", "No device port", 'Port error']
answer_translate = {'Bad data': "Неверные данные", "Unknown command": 'Неизвестная команда',
                    "No device port": "Устройство не подключено", "Port error": "Ошибка порта"}
font_sizes = {10: 72, 50: 60, 100: 48, 200: 36, 250: 30, 500: 24}



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


def get_first_button(usbhost, ser, state: str, used_buttons: List[str]) -> Optional[int]:
    """
    asks comport about buttons pressed
    :param used_buttons: list of already used buttons. we may not return them
    :param usbhost: usbhost class example for send commands to usb
    :param ser: serial port with radio
    :param state: state to get color back ("idle" for idle color, "question" for question color"
    :return: number of first pressed button
    """
    answer = usbhost.send_query(ser, "Getbtns")
    if answer in wrong_answers:
        return -1
    buttons: str = answer.replace("Btns: ", "")
    btn = get_first_button_from_answer(buttons, used_buttons)
    if btn:
        clr1 = state_color_dict['color_pressed']
        clr2 = state_color_dict['color_answer'] if state == 'answer' else state_color_dict['color_idle']
        usbhost.send_query(ser, "Flash", btn, clr1[0], clr1[1], clr1[2], pause_ms, clr2[0], clr2[1], clr2[2])
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


def update_button_list(usbhost, buttons: List[int])->str:
    """
    updates button list for host
    :param usbhost: serial port with host
    :param buttons: list of available buttons
    :return: error or empty string
    """
    port: str = usbhost.get_device_port()
    if not port:
        return "Ошибка связи с устройством"
    opened_port = usbhost.open_port(port)
    answer = usbhost.send_query(opened_port, "SetBtnList", *buttons)
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
    return font_sizes[key]


def get_question_text(question: str) -> str:
    """
    gets formatted question text
    :param question:
    :return:
    """
    font_size = get_questions_text_size(question)
    html = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
    html +="\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    html += "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
    html += "p, li { white-space: pre-wrap; }\n"
    html += "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; "
    html += "font-weight:400; font-style:normal;\">\n"
    html += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
    html += " -qt-block-indent:0; text-indent:0px;\">"
    html += "<span style=\" font-family:\'Calibri\'; font-size:%ipt; " % font_size
    html += "color:#000000;\">%s</span></p></body></html>" % question
    return html
