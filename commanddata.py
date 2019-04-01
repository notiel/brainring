from dataclasses import *
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant

available_commands = 4
max_commands = 16
headers = {0: 'Имя команды', 1: 'Число вопросов', 2: 'Общий счет'}


class Commands:
    def __init__(self):
        self.commands = [Command(button_id=i, name='Команда %i' % (i+1)) for i in range(max_commands)]
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
        """
        reimplements row Count function of Abstract Table Model.
        :param parent: necessary field
        :param args: necessary field
        :param kwargs: necessary field
        :return: number of commands available
        """
        return sum(1 for command in self.data.commands if command.available)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        reimplements column Count function of Abstract Table Model.
        :param parent: necessary field
        :param args: necessary field
        :param kwargs: necessary field
        :return: we have three data columns
        """
        return 3

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
            if y == 0:
                return self.data.commands[x].name
            if y == 1:
                return self.data.commands[x].questions
            if y == 2:
                return self.data.commands[x].points
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
