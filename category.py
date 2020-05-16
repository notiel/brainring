from PyQt5 import QtCore, QtGui, QtWidgets
from typing import Tuple, List
from math import sqrt
import questiondata
import stub_opened


class CategoryForm(QtWidgets.QWidget):

    category_signal = QtCore.pyqtSignal(str)

    def __init__(self, game: questiondata.Game):
        super().__init__()
        self.game: questiondata.Game = game
        self.question = None
        self.answer = None
        self.stub = None
        self.buttons: List[QtWidgets.QPushButton] = list()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Category")
        self.setWindowTitle("Категории")
        self.create_layout(self.game.categories)
        for btn in self.buttons:
            label = get_category_name_from_btn(btn.text())
            if self.game.get_category_by_name(label).was_used:
                btn.setEnabled(False)
            else:
                btn.setEnabled(True)
            btn.clicked.connect(self.btn_clicked)

    def create_layout(self, categories: List[questiondata.Category]):
        """
        creates category buttons layout
        :param categories: list of game categories
        :return:
        """
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        maxx, maxy = get_size_data(len(categories))
        x, y = 0, 0
        for category in categories:
            btn: QtWidgets.QPushButton = create_button(category, x, y)
            layout.addWidget(btn, y, x)
            if x < maxx-1:
                x += 1
            else:
                x = 0
                y += 1
            self.buttons.append(btn)
        w: int = 340 * maxx + 10
        h: int = 120 * maxy + 10
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        self.setGeometry(screen_res.x() + (screen_res.width() - w)/2, screen_res.y() + (screen_res.height() - h)/2,
                         w, h)

    def btn_clicked(self):
        """
        disables used category
        opens first question window
        :return:
        """
        btn = self.sender()
        btn.setEnabled(False)
        btn.setStyleSheet("color: gray; background-color: rgb(221, 219, 255)")
        self.category_signal.emit(get_category_name_from_btn(btn.text()))
        self.stub = stub_opened.StubForm(self.game.get_category_by_name(get_category_name_from_btn(btn.text())))
        self.stub.show()
        self.setVisible(False)


def get_size_data(total: int) -> Tuple[int, int]:
    """
    gets size of rectangle for total categories number
    for 36 it would be 6x6, fjr 35 7x5, for 37 7x5 and wone in extra row below
    :param total:
    :return: width and height
    """
    root = round(sqrt(total))
    if root*root == total:
        return root, root
    elif total % (root + 1) == 0:
        return root + 1, int(total/(root + 1))
    else:
        return root, int(total/root + 1)


def create_button(category: questiondata.Category, x: int, y: int) -> QtWidgets.QPushButton:
    """
    creates on selected form button with parameters
    :param category: caption on button
    :param x: x position in grid
    :param y: y position in grid
    :return: button
    """
    button = QtWidgets.QPushButton()
    button.setMinimumSize(QtCore.QSize(320, 120))
    font = QtGui.QFont()
    font.setFamily("Tahoma")
    font.setPointSize(14)
    font.setBold(True)
    font.setWeight(75)
    font.setStrikeOut(False)
    button.setFont(font)
    button.setStyleSheet("color: rgb(55, 81, 255); background-color: rgb(221, 219, 255)")
    button.setDefault(False)
    button.setFlat(False)
    button.setObjectName("CategoryBtn%i_%i" % (x, y))
    if category.questions:
        button.setText("%i\n%s\nвопросов: %i" % (category.questions[0].points, category.name.upper(),
                       len(category.questions)))
    else:
        button.setText(category.name.upper())
    return button


def get_category_name_from_btn(label: str) -> str:
    """
    gets category name from str label
    :param label: btn label
    :return:
    """
    if 'вопросов' in label and label.count('\n') >= 2:
        start = label.find('\n')
        end = label.rfind('\n')
        label = label[start + 1:end]
    return label.lower()


# def show_categories(main_window, game: questiondata.Game):
#     category = CategoryForm(main_window, game)
#     category.exec_()
