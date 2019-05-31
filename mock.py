#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from typing import Optional, List, Tuple
from time import sleep


class Mock(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Mock'
        self.left = 10
        self.top = 10
        self.width = 300
        self.height = 100
        self.initUI()
        self.move(200, 200)
        self.state = None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.b1 = QPushButton('team1', self)
        self.b1.move(10, 10)
        self.b2 = QPushButton('team2', self)
        self.b2.move(100, 10)
        self.b3 = QPushButton('team3', self)
        self.b3.move(10, 30)
        self.b4 = QPushButton('team4', self)
        self.b4.move(100, 30)

        self.b1.clicked.connect(self.b1press)
        self.b2.clicked.connect(self.b2press)
        self.b3.clicked.connect(self.b3press)
        self.b4.clicked.connect(self.b4press)
        self.reset()

    @pyqtSlot()
    def b1press(self):
        pass
        self.state = 1

    @pyqtSlot()
    def b2press(self):
        self.state = 2

    @pyqtSlot()
    def b3press(self):
        self.state = 3

    @pyqtSlot()
    def b4press(self):
        self.state = 4

    def reset(self):
        self.state = None


amock = None
mockbutton = dict()


def amock_init():
    global amock
    amock = Mock()
    global mockbutton
    mockbutton = {'b1': amock.b1,
                  'b2': amock.b2,
                  'b3': amock.b3,
                  'b4': amock.b4,
                  }
    pass


state_color_dict = {'color_idle': (255, 200, 0),
                    'color_answer': (0, 255, 255),
                    'color_pressed': (0, 255, 0),
                    'color_pressed_second': (0, 0, 255)}
pause_ms = 500


def scan_ports() -> Optional[str]:
    """
    scans COM ports and returns their list
    :return: list of available COM ports
    """
    return "MockPortName"


def open_port(port_id: str):
    """
    opens selected serial port and returns it
    :param port_id:
    :return:
    """
    print(f"{port_id} opened")
    return "MockSerial"


def close_port(ser):
    """
    closes selected port
    :param ser: serial port
    :return:
    """
    print(f"{ser} closed")
    pass


def reset_timer(ser) -> str:
    """
    resets timer at radio host at ser serial port
    :param ser: serial port number with host
    :return command result:
    """
    amock.reset()
    return ""


def get_first_button(ser, state: str) -> Optional[int]:
    """
    asks comport about buttons pressed
    :param ser: serial port with radio
    :param state: state to get color back ("idle" for idle color, "question" for question color"
    :return: number of first pressed button
    """

    btn = amock.state
    if btn:
        if state == 'idle':
            flash_color(ser, btn, state_color_dict['color_pressed'], pause_ms, state_color_dict['color_idle'])
        if state == 'answer':
            flash_color(ser, btn, state_color_dict['color_pressed'], pause_ms, state_color_dict['color_idle'])
    return btn


def change_color(ser, button: int, color: Tuple[int, int, int]):
    """
    change color of selected button
    :param ser: opened serial port
    :param button: button id
    :param color: new color
    :return:
    """
    button: int = 4 if button > 4 else button
    qbutton: QPushButton = list(mockbutton.values())[button - 1]
    qbutton.setStyleSheet(qpushcolor(color))
    amock.style().unpolish(amock)
    amock.style().polish(amock)
    pass


def flash_color(ser, button: int, color1: Tuple[int, int, int], length: int, color2: Tuple[int, int, int]):
    """
    change color of selected button
    :param ser: opened serial port
    :param button: button id
    :param color1: new color
    :param length: length of pause (ms)
    :param color2: color to return to
    :return:
    """
    change_color(ser, button, color1)
    sleep(float(length) / 1000)
    change_color(ser, button, color2)
    pass


def change_color_all(ser, color: Tuple[int, int, int]):
    """
    change color of selected button
    :param ser: opened serial port
    :param color: new color
    :return:
    """
    qbutton: QPushButton
    for qbutton in mockbutton.values():
        qbutton.setStyleSheet(qpushcolor(color))
        amock.style().unpolish(amock)
        amock.style().polish(amock)
    pass


def qpushcolor(rgb: Tuple[int, int, int]) -> str:
    return f"color: rgb({str(rgb)})"


def get_first_button_from_answer(answer: str) -> Optional[int]:
    """

    :param answer: string with answer from radio
    :return:
    """
    answer_list: List[str] = answer.split()
    button_keys: List[int] = [int(button) for button in answer_list[::2]]
    buttons_values: List[int] = [int(value) for value in answer_list[1::2]]
    buttons_list = list(zip(button_keys, buttons_values))
    buttons_list = [btn for btn in buttons_list if btn[1] not in (0, -1)]
    buttons_list.sort(key=lambda i: i[1])
    if buttons_list:
        return buttons_list[0][0]
    return None
