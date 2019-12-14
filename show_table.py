import commanddata
import commandtable_ui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex


class CommandCount(QtWidgets.QWidget, commandtable_ui.Ui_Form):
    def __init__(self, model: commanddata.CommandTableModel):
        super().__init__()
        self.setupUi(self)
        self.CmdTable.setModel(model)
        self.model = model

        self.LblList = [self.LblCmd1, self.LblCmd2, self.LblCmd3, self.LblCmd4, self.LblCmd5, self.LblCmd6,
                        self.LblCmd7, self.LblCmd8, self.LblCmd9, self.LblCmd10, self.LblCmd11, self.LblCmd12,
                        self.LblCmd13, self.LblCmd14, self.LblCmd15, self.LblCmd16]

        self.SpinList = [self.SpinCmd1, self.SpinCmd2, self.SpinCmd3, self.SpinCmd4, self.SpinCmd5, self.SpinCmd6,
                         self.SpinCmd7, self.SpinCmd8, self.SpinCmd9, self.SpinCmd10, self.SpinCmd11, self.SpinCMd12,
                         self.SpinCmd13, self.SpinCmd14, self.SpinCmd15, self.SpinCmd16]

        for cmd in model.commanddata.commands:
            self.LblList[model.commanddata.commands.index(cmd)].setEnabled(True if cmd.available else False)
            self.LblList[model.commanddata.commands.index(cmd)].setText(cmd.name)
            self.SpinList[model.commanddata.commands.index(cmd)].setEnabled(True if cmd.available else False)
            self.SpinList[model.commanddata.commands.index(cmd)].setMaximum(cmd.points)
        self.BtnDecrease.clicked.connect(self.decrease_clicked)
        current_screen = 1 if QtWidgets.QDesktopWidget().screenCount() > 1 else 0
        screen_res = QtWidgets.QDesktopWidget().availableGeometry(current_screen)
        self.setGeometry(screen_res.x() + 5 + screen_res.width()/2 - 500, screen_res.y() + 40, 1000, screen_res.height() - 40)

    def decrease_clicked(self):
        """
        decrease command point for selected valur
        :return:
        """
        for spin in self.SpinList:
            if spin.isEnabled():
                value = spin.value()
                self.model.commanddata.commands[self.SpinList.index(spin)].points -= value
        self.model.dataChanged.emit(QModelIndex(), QModelIndex())
