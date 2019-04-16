import serial
import serial.tools.list_ports
from typing import Optional, List, Tuple
import common_functions

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
    devices = [comport.device for comport in serial.tools.list_ports.comports()]
    for comport in devices:
        try:
            # find comport with our device
            ser = serial.Serial(comport, timeout=0.2)
            command: bytes = bytes("ping\r\n", encoding='utf-8')
            ser.write(command)
            answer: str = ser.readall().decode('utf-8')
            ser.close()
            if 'Ack 0' in answer:
                return comport
        except serial.SerialException:
            continue
    return None


def open_port(port_id: str):
    """
    opens selected serial port and returns it
    :param port_id:
    :return:
    """
    try:
        ser = serial.Serial(port_id)
        return ser
    except serial.SerialException:
        return None


def close_port(ser):
    """
    closes selected port
    :param ser: serial port
    :return:
    """
    ser.close()


def reset_timer(ser) -> str:
    """
    resets timer at radio host at ser serial port
    :param ser: serial port number with host
    :return command result:
    """
    try:
        command: bytes = bytes("rsttmr\r\n", encoding='utf-8')
        ser.write(command)
        answer: str = ser.readline().decode('utf-8')
        if 'Ack 0' in answer:
            return ""
        else:
            return "Ошибка сброса времени"
    except serial.SerialException:
        return "Не удалось связаться с хостом"


def get_first_button(ser, state: str) -> Optional[int]:
    """
    asks comport about buttons pressed
    :param ser: serial port with radio
    :param state: state to get color back ("idle" for idle color, "question" for question color"
    :return: number of first pressed button
    """
    command: bytes = bytes("Getbtns\r\n", encoding='utf-8')
    ser.write(command)
    answer: str = ser.readline().decode('utf-8')
    print(answer)
    buttons: str = answer.replace("Btns: ", "")
    btn = get_first_button_from_answer(buttons)
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
    try:
        command: bytes = bytes("SetClr % i, %i %i %i\r\n" % (button, int(color[0]), int(color[1]), int(color[2])),
                               encoding='utf-8')
        ser.write(command)
        answer: ser = ser.readline().decode('utf-8')
        if "Ack 0" not in answer:
            common_functions.error_message("Ошибка смены цвета")
    except (serial.SerialException, IndexError, AttributeError):
        common_functions.error_message("Ошибка смены цвета")


def flash_color(ser, button: int, color1: Tuple[int, int, int], length: int, color2: Tuple[int, int, int]):
    """
    change color of selected button
    :param ser: opened serial port
    :param button: button id
    :param color1: new color
    :param length: length of pause
    :param color2: color to return to
    :return:
    """
    try:
        command_str: str = "Flash %i %i %i %i %i %i %i %i\r\n" % (button, int(color1[0]), int(color1[1]),
                                                                  int(color1[2]), length, int(color2[0]),
                                                                  int(color2[1]), int(color2[2]))
        command: bytes = bytes(command_str, encoding='utf-8')
        ser.write(command)
        answer: ser = ser.readline().decode('utf-8')
        if "Ack 0" not in answer:
            common_functions.error_message("Ошибка смены цвета")
    except (serial.SerialException, IndexError, AttributeError):
        common_functions.error_message("Ошибка смены цвета")


def change_color_all(ser, color: Tuple[int, int, int]):
    """
    change color of selected button
    :param ser: opened serial port
    :param color: new color
    :return:
    """
    try:
        command: bytes = bytes("SetClrAll %i %i %i\r\n"
                               % (int(color[0]), int(color[1]), int(color[2])), encoding='utf-8')
        ser.write(command)
        answer: ser = ser.readline().decode('utf-8')
        if "Ack 0" not in answer:
            common_functions.error_message("Ошибка смены цвета")
    except (serial.SerialException, IndexError, AttributeError):
        common_functions.error_message("Ошибка смены цвета")


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
