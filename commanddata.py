from dataclasses import *
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant

available_commands = 4
max_commands = 16
headers = ["Команда", "Вопросы", "Очки", "Номер кнопки"]


class Commands:
    def __init__(self):
        self.commands = [Command(button_id=i, name='Команда %i' % i) for i in range(1, max_commands+1)]
        for i in range(available_commands):
            self.commands[i].available = True


@dataclass
class Command:
    button_id: int
    name: str = "Команда"
    available: bool = False
    questions: int = 0
    points: int = 0

    def add_questions(self, points: int):
        """
        question is added: increase question number and add points
        :param points:
        :return:
        """
        self.questions += 1
        self.points += points


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
        return 4

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
                return commands_in_game[x].button_id
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
