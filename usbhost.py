import serial
import serial.tools.list_ports
from typing import Optional, List


state_color_dict = {'color_idle': (255, 200, 0),
                    'color_answer': (0, 255, 255),
                    'color_pressed': (0, 255, 0),
                    'color_pressed_second': (0, 0, 255)}
pause_ms = 500

# todo change description
"""
Use this class module to communicate with Ostranna USB Host (Usb2radio)
*init module with expected baudrate (115200 used by default)
*get_port_list() function returns list of available comports as ['COM3', 'COM5', 'COM20' ...]
*get_device_port function returns first found port with Ostranna device (answer 'Ack 0' to 'Ping\r\n') as 'COM4'
*get_all_device_ports() returns list of comports with Ostranna devices connected 
                        (answer 'Ack 0' to 'Ping\r\n') as ['COM4', ...]
*open_port_by_id(port_id: str) takes comport as str parameter (open_port('COM4') and returns open port or None
*open_port() opens self.comport port and writes opened port (or None) to self.ser
*send command(command, parameters) send command with parameters to self.ser port, returns send status
              ("ok", "Bad data", "Unknown command" or "No device port") 
*send query(command, parameters) send query with parameters to self.ser port and returns answer
*close_port() closes self.ser 
"""


class UsbHost:

    def __init__(self, baudrate: int = 115200):
        """
        inits usbhost
        :param baudrate: baudrate for serial port
        """
        self.ser = None
        self.comport = self.get_device_port()
        self.baudrate = baudrate

    def rescan(self):
        """
        rescans and opens port
        :return:
        """
        try:
            self.close_port()
        except (serial.SerialException, AttributeError):
            pass
        self.comport = self.get_device_port()

    @staticmethod
    def get_ports_list() -> List[str]:
        """
        scans COM ports and returns their list
        :return: list of available COM ports
        """
        return [comport.device for comport in serial.tools.list_ports.comports()]

    def get_device_port(self) -> Optional[str]:
        """
        scans COM ports and returns first found ostranna device port
        :return: port with ostranna device or None
        """
        devices = [comport.device for comport in serial.tools.list_ports.comports()]
        for comport in devices:
            try:
                # find comport with our device
                ser = self.open_port_by_id(comport)
                command: bytes = bytes("ping\r\n", encoding='utf-8')
                ser.write(command)
                answer: str = ser.readall().decode('utf-8')
                ser.close()
                if 'Ack 0' in answer:
                    return comport
            except (serial.SerialException, Exception):
                continue
        return None

    @staticmethod
    def get_all_device_ports() -> List[str]:
        """
        scans COM ports and returns first found ostranna device port
        :return: port with ostranna device or None
        """
        devices = [comport.device for comport in serial.tools.list_ports.comports()]
        result = list()
        for comport in devices:
            try:
                # find comport with our device
                ser = serial.Serial(comport, timeout=0.2)
                command: bytes = bytes("ping\r\n", encoding='utf-8')
                ser.write(command)
                answer: str = ser.readall().decode('utf-8')
                ser.close()
                if 'Ack 0' in answer:
                    result.append(comport)
            except (serial.SerialException, AttributeError):
                continue
        return result

    def open_port_by_id(self, comport: str, timeout: float = 0.2):
        """
        opens selected serial port with selected timeout and 115200 baudrate and returns it
        :param comport: id of port to open
        :param timeout: timeout for serial port
        :return: port
        """
        if not comport:
            return None
        try:
            return serial.Serial(self.comport, self.baudrate, timeout=timeout)
        except (serial.SerialException, AttributeError):
            return None

    def open_port(self, timeout: float = 0.2):
        """
        opens selected serial port with selected timeout and 115200 baudrate and returns it
        :param timeout: timeout for serial port
        :return: port
        """
        if not self.comport:
            self.ser = None
        try:
            self.ser = serial.Serial(self.comport, self.baudrate, timeout=timeout)
        except (serial.SerialException, AttributeError):
            self.ser = None

    def close_port(self):
        """
        closes selected port
        :return:
        """
        try:
            self.ser.close()
        except AttributeError:
            raise

    @staticmethod
    def create_command(command: str, *parameters) -> str:
        """
        forms command string using command and parameters
        :param command: command
        :param parameters: list wit parameters
        :return: string <command param1 param2 ... \r\n>
        """
        if parameters and isinstance(parameters, tuple) and isinstance(parameters[0], tuple):
            parameters = parameters[0]
        str_param: str = ' '.join([str(param) for param in parameters]) if parameters else ""
        result = command + ' ' + str_param + '\r\n' if str_param else command + '\r\n'
        return result

    def send_command(self, command: str, *parameters) -> str:
        """
        sends command with parameters to comport
        :param command: command to send
        :param parameters: list of parameters
        :return: 'Ok' for success, 'Bad data', 'Wrong command' or 'No Device' for errors
        """
        try:
            self.close_port()
        except (serial.SerialException, AttributeError):
            pass
        self.open_port()
        try:
            command: bytes = bytes(self.create_command(command, parameters), encoding='utf-8') if parameters \
                else bytes(self.create_command(command), encoding='utf-8')
            self.ser.write(command)
            answer: str = self.ser.readall().decode('utf-8')
            if answer.strip().lower() == 'ack 0':
                res = 'Ok'
            elif answer.strip().lower() == 'ack 6':
                res = 'Unknown command'
            else:
                res = 'Bad data'
            self.close_port()
            return res
        except (serial.SerialException, AttributeError):
            return 'No device port'
        except Exception:
            raise

    def send_query(self, command: str, *parameters) -> str:
        """
        send query to comport and returns answer
        :param command: query to send
        :param parameters: query parameters
        :return: port answer
        """
        try:
            self.close_port()
        except (serial.SerialException, AttributeError):
            pass
        self.open_port()
        try:
            command: bytes = bytes(self.create_command(command, parameters), encoding='utf-8')
            self.ser.write(command)
            answer: str = self.ser.readall().decode('utf-8')
            if answer.lower() == 'ack 7':
                res = 'Bad data'
            elif answer.lower() == 'ack 6':
                res = 'Unknown command'
            else:
                self.close_port()
                res = answer.strip()
            self.close_port()
            return res
        except (serial.SerialException, AttributeError) as e:
            return 'Port error' + e
        except Exception:
            raise
