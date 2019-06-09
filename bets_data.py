from dataclasses import *
from typing import List


@dataclass
class Bets:
    command_source: str
    command_target: str
    points: int
    subj: str

    def __str__(self):
        return "Команда %s на команду %s %i очков (условие: %s)" % \
               (Bets.command_source, Bets.command_target, Bets.points, Bets.subj)


class CurrentBets:
    def __init__(self):
        self.bets: List[Bets] = list()

    def add_bet(self, cmd1: str, cmd2: str, bet: int, subj: str):
        """
        adds new bet
        :param cmd1: source command
        :param cmd2: target command
        :param bet: points for bet
        :param subj: subject of bet
        :return:
        """
        self.bets.append(Bets(command_source=cmd1, command_target=cmd2, points=bet, subj=subj))

    def delete_bet(self, bet_id: int):
        """
        deletes bet by id
        :param bet_id: id of bet
        :return:
        """
        self.bets.remove(self.bets[bet_id])
