from dataclasses import *
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from typing import Optional

available_commands = 4
max_commands = 16
koeff = 2
headers = ["Команда", "Вопросы", "Очки", "За вопросы", "Номер\nкнопки", "Ставки"]


class Commands:
    def __init__(self):
        self.commands = [Command(button_id=i, name='Команда %i' % i) for i in range(1, max_commands+1)]
        for i in range(available_commands):
            self.commands[i].available = True

    def get_command_by_button(self, button: int) -> int:
        """
        gets command id by id of button
        :param button: button is
        :return: id of command
        """
        for cmd in self.commands:
            if cmd.button_id == button:
                return self.commands.index(cmd)
        return -1

    def get_command_by_name(self, name: str) -> Optional['Command']:
        """
        gets command  by name
        :param name: name of command
        :return: command
        """
        for cmd in self.commands:
            if cmd.name == name:
                return cmd
        return None

    def get_available_commands_list(self):
        """
        returns ids of buttons that are available
        :return:
        """
        return [cmd.button_id for cmd in self.commands if cmd.available]

    def get_available_names_list(self):
        """
        returns names of commands that are available
        :return:
        """
        return [cmd.name for cmd in self.commands if cmd.available]


@dataclass
class Command:
    button_id: int
    name: str = "Команда"
    available: bool = False
    questions: int = 0
    points: int = 0
    question_points: int = 0
    bets: int = 0

    def add_questions(self, points: int):
        """
        question is added: increase question number and add points
        :param points:
        :return:
        """
        self.questions += 1
        self.points += points
        self.question_points += points


class CommandTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(CommandTableModel, self).__init__(parent)
        self.commanddata = Commands()

    def rowCount(self, parent=None, *args, **kwargs):
        """
        reimplements row Count function of Abstract Table Model.
        :param parent: necessary field
        :param args: necessary field
        :param kwargs: necessary field
        :return: number of commands available
        """
        return sum(1 for command in self.commanddata.commands if command.available)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        reimplements column Count function of Abstract Table Model.
        :param parent: necessary field
        :param args: necessary field
        :param kwargs: necessary field
        :return: we have four data columns
        """
        return len(headers)

    def data(self, idx=QModelIndex(), role=None):
        """
        reimplements data function of  Abstract Table model
        :param idx: index of data (x, y positions)
        :param role: role of query
        :return: appropriate data of selected command (x is command number, y is 0 for name, 1 for question number,
        2 for points
        """
        if role == Qt.DisplayRole:
            x: int = idx.row()
            y: int = idx.column()
            commands_in_game = [command for command in self.commanddata.commands if command.available]
            if y == 0:
                return commands_in_game[x].name
            if y == 1:
                return commands_in_game[x].questions
            if y == 2:
                return commands_in_game[x].points
            if y == 3:
                return commands_in_game[x].question_points
            if y == 4:
                return commands_in_game[x].button_id
            if y == 5:
                return commands_in_game[x].bets
        return QVariant()

    def headerData(self, section, qt_orientation, role=None):
        """
        reimplements headerData function of Abstract Table Model
        :param section: header index
        :param qt_orientation: table orientation (horizontal)
        :param role: role of query (display)
        :return: appropriate header
        """
        if role == Qt.DisplayRole and qt_orientation == Qt.Horizontal:
            return headers[section]

    def enable_command(self, command_id: int):
        """
        :param command_id: number of available comand
        makes one more command available, model reloaded
        :return:
        """
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.commanddata.commands[command_id].available = True
        self.endInsertRows()

    def disable_command(self, command_id: int):
        """
        :param command_id: number of available command
        makes one more command available, model reloaded
        :return:
        """
        self.beginRemoveRows(QModelIndex(), 0, 0)
        self.commanddata.commands[command_id].available = False
        self.endRemoveRows()

    def update_button_id(self, command_number: int, new_button: int):
        """
        sets new button for selected command
        :param new_button: new button number
        :param command_number: number of command to update
        :return:
        """
        self.commanddata.commands[command_number].button_id = new_button
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def score_question(self, command: int, points: int):
        """
        score question (update points and question number)
        :param command: command to score
        :param points: points to add
        :return:
        """
        self.commanddata.commands[command].points += points
        self.commanddata.commands[command].question_points += points
        self.commanddata.commands[command].questions += 1
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def score_bet(self, command_name: str, bet: int, bet_type: str):
        """
        score bet if type "add" and delete bet at any other case
        :param command_name: command to score
        :param bet: bet to score
        :param bet_type: type of scoring
        :return:
        """
        command = self.commanddata.get_command_by_name(command_name)
        if bet_type == 'add':
            command.points += koeff * bet
            command.bets += koeff * bet
        else:
            command.points -= bet
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def setData(self, idx, value, role=None):
        """
        replaces set data standart function
        :param idx: index of changed data
        :param value: new value
        :param role: role (editing)
        :return:
        """
        if role == Qt.EditRole:
            command_id = idx.row()
            command = [command for command in self.commanddata.commands if command.available][command_id]
            if idx.column() == 0:
                command.name = value
                # self.commanddata.commands[command_id].name = value
            if idx.column() == 1:
                try:
                    command.questions = int(value)
                except ValueError:
                    pass
            if idx.column() == 2:
                try:
                    command.points = int(value)
                except ValueError:
                    pass
            if idx.column() == 3:
                try:
                    command.question_points = int(value)
                except ValueError:
                    pass
            if idx.column() == 5:
                try:
                    command.bets = int(value)
                except ValueError:
                    pass
            return True
        return False

    def flags(self, idx):
        """
        special function to support editing
        :param idx:
        :return: flags for editing
        """
        return Qt.ItemIsEditable | QAbstractTableModel.flags(self, idx)
