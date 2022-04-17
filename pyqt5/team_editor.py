import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog

from league_manager.team_member import TeamMember
from pyqt5.messages import Message

Ui_MainWindow, QTBaseWindow = uic.loadUiType("team_editor.ui")


class TeamEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, team=None, db=None, parent=None):
        # def __init__(self, team, db, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.btn_add.clicked.connect(self.add_btn_clicked)
        # self.btn_delete.clicked.connect(self.delete_btn_clicked)
        # self.btn_edit.clicked.connect(self.edit_btn_clicked)
        # self._message = Message()
        # self._team = team
        # self._db = db
        # if self._league:
        #     self.lbl_teams.setText("Member in " + team.name + ":")
        #     self.setWindowTitle("Team (" + team.name + ") Editor")
            # self.update_ui()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec_())
