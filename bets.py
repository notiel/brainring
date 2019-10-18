import design_bets
import bets_data
from PyQt5 import QtWidgets


class BetsDialog(QtWidgets.QWidget, design_bets.Ui_Form):

    def __init__(self, model, bets: bets_data.CurrentBets):
        super().__init__()
        self.setupUi(self)
        self.model = model
        self.bets = bets
        self.init_ui()
        self.CBCmd1.currentTextChanged.connect(self.src_command_changed)
        self.BtnAdd.clicked.connect(self.add_pressed)
        self.BtnAdBet.clicked.connect(self.score_bet)
        self.BtnDeleteBet.clicked.connect(self.delete_bet)
        self.LstBets.currentItemChanged.connect(self.item_changed)

    def init_ui(self):
        self.LstBets.addItems(list(map(str, self.bets.bets)))
        self.CBCmd1.addItems(self.model.commanddata.get_available_names_list())
        self.CBCmd2.addItems(self.model.commanddata.get_available_names_list())
        self.src_command_changed()
        self.BtnAdBet.setEnabled(False)
        self.BtnDeleteBet.setEnabled(False)

    def src_command_changed(self):
        """
        scores for command changed
        :return:
        """
        new_command = self.CBCmd1.currentText()
        score = self.model.commanddata.get_command_by_name(new_command).points
        self.SpinScore.setMaximum(score)

    def add_pressed(self):
        """
        btn add pressed
        :return:
        """
        self.model.score_bet(self.CBCmd1.currentText(), self.SpinScore.value(), "")
        bet = self.bets.add_bet(self.CBCmd1.currentText(), self.CBCmd2.currentText(),
                                self.SpinScore.value(), self.LineBet.text())
        self.LstBets.addItem(str(bet))

    def item_changed(self):
        """
        selected bet
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
        bet deleted
        :return:
        """
        bet_id = self.LstBets.currentRow()
        self.bets.delete_bet(bet_id)
        self.LstBets.clear()
        self.LstBets.addItems((list(map(str, self.bets.bets))))
        self.BtnDeleteBet.setEnabled(False)
        self.BtnAdBet.setEnabled(False)

    def score_bet(self):
        """
        bet scored
        :return:
        """
        bet_id = self.LstBets.currentRow()
        self.model.score_bet(self.bets.bets[bet_id].command_source, self.bets.bets[bet_id].points, "add")
        bet_id = self.LstBets.currentRow()
        self.bets.delete_bet(bet_id)
        self.LstBets.clear()
        self.LstBets.addItems((list(map(str, self.bets.bets))))
        self.BtnDeleteBet.setEnabled(False)
        self.BtnAdBet.setEnabled(False)
