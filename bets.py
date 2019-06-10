import design_bets
import bets_data
from PyQt5 import QtWidgets


class BetsDialog(QtWidgets.QWidget, design_bets.Ui_Form):

    def __init__(self, model, bets: bets_data.CurrentBets):
        super().__init__()
        self.setupUi(self)
        self.initUi(bets)

    def initUi(self, bets):
        self.LstBets.addItems(bets.bets)
