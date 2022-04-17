import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog

from league_manager.team import Team
from pyqt5.messages import Message
from pyqt5.team_editor import TeamEditor

Ui_MainWindow, QTBaseWindow = uic.loadUiType("league_editor.ui")


class LeagueEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, league=None, db=None, parent=None):
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
        selected_row = self.list_widget_teams.currentRow()
        dialog, btn_yes, btn_no = self._message.confirmation("Delete Team",
                                                             "Are You Sure You Want to Delete Team ("
                                                             + str(self._league.teams[selected_row]) + ")?")

        if selected_row == -1:
            self._message.warn("No Selection", "No Team Selected for Deletion")
            return

        dialog.exec()

        if dialog.clickedButton() == btn_yes:
            del self._league.teams[selected_row]

        self.update_ui()

    def edit_btn_clicked(self):
        selected_row = self.list_widget_teams.currentRow()

        if selected_row == -1:
            self._message.warn("No Selection", "No Team Selected to Edit")
            return

        team = self._league.teams[selected_row]
        team_editor = TeamEditor(team, self._db)

        if team_editor.exec() == QDialog.DialogCode.Accepted:
            print("save")
        else:
            print("cancel")

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