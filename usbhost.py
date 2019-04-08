import serial
import serial.tools.list_ports
from typing import Optional


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
