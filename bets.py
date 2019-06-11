import design_bets
import bets_data
from PyQt5 import QtWidgets


class BetsDialog(QtWidgets.QWidget, design_bets.Ui_Form):

    def __init__(self, model, bets: bets_data.CurrentBets):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.bets = bets
        self.initUi()
        self.CBCmd1.currentTextChanged.connect(self.src_command_changed)
        self.BtnAdd.clicked.connect(self.add_pressed)
        self.BtnAdBet.clicked.connect(self.score_bet)
        self.BtnDeleteBet.clicked.connect(self.delete_bet)
        self.LstBets.currentItemChanged.connect(self.item_changed)

    def initUi(self):
        self.LstBets.addItems(list(map(str, self.bets.bets)))
        self.CBCmd1.addItems(self.model.commanddata.get_available_names_list())
        self.CBCmd2.addItems(self.model.commanddata.get_available_names_list())
        self.src_command_changed()

    def src_command_changed(self):
        """

        :return:
        """
        new_command = self.CBCmd1.currentText()
        score = self.model.commanddata.get_command_by_name(new_command).points
        self.SpinScore.setMaximum(score)

    def add_pressed(self):
        """

        :return:
        """
        bet = self.bets.add_bet(self.CBCmd1.currentText(), self.CBCmd2.currentText(),
                                self.SpinScore.value(), self.LineBet.text())
        self.LstBets.addItem(str(bet))

    def item_changed(self):
        """

        :return:
        """
        current = self.LstBets.currentItem()
        if current:
            self.BtnDeleteBet.setEnabled(True)
            self.BtnAdBet.setEnabled(True)
        else:
            self.BtnDeleteBet.setEnabled(False)
            self.BtnAdBet.setEnabled(False)

    def delete_bet(self):
        """

        :return:
        """
        id = self.LstBets.currentRow()
        self.bets.delete_bet(id)
        self.LstBets.clear()
        self.LstBets.addItems((list(map(str, self.bets.bets))))
        self.BtnDeleteBet.setEnabled(False)
        self.BtnAdBet.setEnabled(False)

    def score_bet(self):
        """

        :return:
        """
        current = self.LstBets.currentItem().text()

        # self.model.score_bet()