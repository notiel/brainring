import serial
import serial.tools.list_ports
from typing import Optional, List


state_color_dict = {'color_idle': (255, 200, 0),
                    'color_answer': (0, 255, 255),
                    'color_pressed': (0, 255, 0),
                    'color_pressed_second': (0, 0, 255)}
pause_ms = 500


"""
Use this module to communicate with Ostranna USB Host (Usb2radio)
*get_port_list() function returns list of available comports as ['COM3', 'COM5', 'COM20' ...]
*get_device_port function returns first found port with Ostranna device (answer 'Ack 0' to 'Ping\r\n') as 'COM4'
*get_all_device_ports() returns list of comports with Ostranna devices connected 
                        (answer 'Ack 0' to 'Ping\r\n') as ['COM4', ...]
*open_port(port_id: str) takes comport as str parameter (open_port('COM4') and returns open port or None
*send command(ser, command, parameters) send command with parameters to ser port, returns send status
              ("ok", "Bad data", "Unknown command" or "No device port") 
*send query(ser, command, parameters) send query with parameters to ser port and returns answer
*close_port(ser) gets result of open_port(port_id) as parameter and closes it 
"""


class UsbHost:

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
                ser = self.open_port(comport)
                command: bytes = bytes("ping\r\n", encoding='utf-8')
                ser.write(command)
                answer: str = ser.readall().decode('utf-8')
                ser.close()
                if 'Ack 0' in answer:
                    return comport
            except serial.SerialException:
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
            except serial.SerialException:
                continue
        return result

    @staticmethod
    def open_port(port_id: str, timeout: float = 0.2):
        """
        opens selected serial port with selected timeout and 115200 baudrate and returns it
        :param port_id: id of port (COM4 for example)
        :param timeout: timeout for serial port
        :return: port
        """
        if port_id == None:
            return None
        try:
            ser = serial.Serial(port_id, baudrate=115200, timeout=timeout)
            return ser
        except serial.SerialException:
            return None

    @staticmethod
    def close_port(ser):
        """
        closes selected port
        :param ser: serial port
        :return:
        """
        ser.close()

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

    def send_command(self, ser, command: str, *parameters) -> str:
        """
        sends command with parameters to comport
        :param ser: opened port
        :param command: command to send
        :param parameters: list of parameters
        :return: 'Ok' for success, 'Bad data', 'Wrong command' or 'No Device' for errors
        """
        try:
            command: bytes = bytes(self.create_command(command, parameters), encoding='utf-8') if parameters \
                else bytes(self.create_command(command), encoding='utf-8')
            ser.write(command)
            answer: str = ser.readall().decode('utf-8')
            if answer.strip().lower() == 'ack 0':
                return 'Ok'
            elif answer.strip().lower() == 'ack 6':
                return 'Unknown command'
            else:
                return 'Bad data'
        except serial.SerialException:
            return 'No device port'
        except Exception:
            raise

    def send_query(self, ser, command: str, *parameters) -> str:
        """
        send query to comport and returns answer
        :param ser: opened port
        :param command: query to send
        :param parameters: query parameters
        :return: port answer
        """
        try:
            command: bytes = bytes(self.create_command(command, parameters), encoding='utf-8')
            ser.write(command)
            answer: str = ser.readall().decode('utf-8')
            if answer.lower() == 'ack 7':
                return 'Bad data'
            if answer.lower() == 'ack 6':
                return 'Unknown command'
            else:
                return answer.strip()
        except serial.SerialException:
            return 'Port error'
        except Exception:
            raise
