from dataclasses import *
available_commands = 4
max_commands = 16


class Commands:

    def __init__(self):
        self.commands = list()

        for i in range(max_commands):
            command = Command(name='Команда %i' % i)
            self.commands.append(command)
            command.button_id = 1
        for i in range(available_commands):
            self.commands[i].available = True

@dataclass
class Command:
    button_id: int
    name: str = "Команда"
    available: bool = False
    questions: int = 0
    points: int = 0

    def __init__(self, name: str):
        self.name = name

    def add_questions(self, points: int):
        """
        question is added: increase question number and add points
        :param points:
        :return:
        """
        self.questions += 1
        self.points += points
