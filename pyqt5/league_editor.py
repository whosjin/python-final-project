import sys

from PyQt5 import uic, QtWidgets

from league_manager.team import Team
from pyqt5.messages import Message

Ui_MainWindow, QTBaseWindow = uic.loadUiType("league_editor.ui")


class LeagueEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, league, db, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.add_btn_clicked)
        self.btn_delete.clicked.connect(self.delete_btn_clicked)
        self.btn_edit.clicked.connect(self.edit_btn_clicked)
        self._message = Message()
        self._league = league
        self._db = db
        if self._league:
            self.lbl_teams.setText("Teams in " + league.name + ":")
            self.setWindowTitle("League (" + league.name + ") Editor")
            self.update_ui()

    def add_btn_clicked(self):
        new_team_name = self.line_edit_team_name.text()
        oid = self._db.next_oid()

        if new_team_name:
            self._league.add_team(Team(oid, new_team_name))
        else:
            self._message.warn("No Input", "You must enter a valid Team Name")

        self.update_ui()

    def delete_btn_clicked(self):
        pass

    def edit_btn_clicked(self):
        pass

    def update_ui(self):
        self.line_edit_team_name.clear()
        self.list_widget_teams.clear()

        for team in self._league.teams:
            self.list_widget_teams.addItem(str(team))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec_())