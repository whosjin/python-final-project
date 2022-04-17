import sys

from PyQt5 import uic, QtWidgets

Ui_MainWindow, QTBaseWindow = uic.loadUiType("league_editor.ui")


class LeagueEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._league = league
        if self._league:
            self.lbl_teams.setText("Teams in " + league.name + ":")
            self.setWindowTitle("League (" + league.name + ") Editor")
            self.update_ui()

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