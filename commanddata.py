from dataclasses import *
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant

available_commands = 4
max_commands = 16
headers = {0: 'Имя команды', 1: 'Число вопросов', 2: 'Общий счет'}


class Commands:

    def __init__(self):
        self.commands = list()
        for i in range(max_commands):
            command = Command(button_id=i, name='Команда %i' % i)
            self.commands.append(command)
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
    def __init__(self, commanddata: Commands, parent=None):
        super(CommandTableModel, self).__init__(parent)
        self.data = commanddata

    def rowCount(self, parent=None, *args, **kwargs):
        return len([command for command in self.data.commands if command.available]) + 1

    def columnCount(self, parent=None, *args, **kwargs):
        return 3

    def data(self, idx=QModelIndex(), role=None):
        if role == Qt.DisplayRole:
            x: int = idx.row()
            y: int = idx.column()
            if x == 0:
                return headers[y]
            else:
                if y == 0:
                    return self.data.commands[x].name
                if y == 1:
                    return self.data.commands[x].questions
                if y == 2:
                    return self.data.commands[x].points
        return QVariant()
