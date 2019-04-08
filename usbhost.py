import serial
import serial.tools.list_ports
from typing import Optional, List


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

def get_first_button(ser) -> Optional[int]:
    """
    asks comport about buttons pressed
    :param ser: serial port with radio 
    :return: number of first pressed button
    """
    command: bytes = bytes("Getbtns\r\n", encoding='utf-8')
    ser.write(command)
    answer: str = ser.readall().decode('utf-8')
    buttons: str = answer.replace("Btns: ", "")
    return get_first_button_from_answer(buttons)


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



