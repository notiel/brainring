from dataclasses import *
from typing import List, Optional, Tuple
from openpyxl import load_workbook
question_time = 60
time_low_threshold = 5


@dataclass
class Game:
    categories: List['Category']
    length: int

    def get_category_by_name(self, name: str) -> Optional['Category']:
        """
        gets category by name if it exists
        :param name: cetegory or None
        :return:
        """
        for category in self.categories:
            if category.name == name:
                return category
        return None


@dataclass
class Category:
    name: str
    questions: List['Question']
    was_used: bool

    def get_total_points(self) -> int:
        """
        returns total points for category
        :return: points
        """
        total = 0
        for question in self.questions:
            total += question.points

        return total

    def get_question_number(self) -> int:
        """
        returns total number of questions for category
        :return: number of questions
        """
        return len(self.questions)


@dataclass
class Question:
    category: str
    description: str
    points: int
    number: int
    answer: str
    show_answer: bool = False
    filepath: str = ""
    answer_filepath: str = ""


def create_game(filename: str) -> Tuple[Optional[Game], str]:
    """
    reads game questions from xlsx datafile
    :param filename:
    :return:
    """
    try:
        wb = load_workbook(filename=filename)
        sheet = wb.active
    except FileNotFoundError:
        return None, "file not found"
    game = Game(categories=list(), length=0)
    error = ""
    for i in range(2, sheet.max_row+1):
        try:
            category = sheet['A%i' % i].value
            number = int(sheet['B%i' % i].value)
            points = int(sheet['C%i' % i].value)
            text = sheet['D%i' % i].value if sheet['D%i' % i].value else ""
            filepath = sheet['E%i' % i].value if sheet['E%i' % i].value else ""
            answer = sheet['F%i' % i].value
            show_answer = True if sheet['G%i' % i].value and sheet['G%i' % i].value.strip().lower() == 'да' else False
            answer_filepath = sheet['H%i' % i].value if sheet['H%i' % i].value else ""
            question = Question(category=category, description=text, points=points, number=number, answer=answer,
                                filepath=filepath, show_answer=show_answer, answer_filepath=answer_filepath)
            existing_category = game.get_category_by_name(category)
            if existing_category:
                existing_category.questions.append(question)
            else:
                new_category = Category(name=category, questions=[question], was_used=False)
                game.categories.append(new_category)
                game.length += 1

        except (AttributeError, TypeError, ValueError) as e:
            error += "Wrong %i row\n" % i
    return game, error
