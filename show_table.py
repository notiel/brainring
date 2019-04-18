import commanddata
import commandtable_ui
from PyQt5 import QtWidgets


class CommandCount(QtWidgets.QWidget, commandtable_ui.Ui_Form):
    def __init__(self, model: commanddata.CommandTableModel):
        super().__init__()
        self.setupUi(self)
        self.CmdTable.setModel(model)

