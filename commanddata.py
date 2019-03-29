from dataclasses import *


@dataclass
class Command:
    name: str = "Команда"
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
