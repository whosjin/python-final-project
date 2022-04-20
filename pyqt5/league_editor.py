import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog

# from league_manager.exceptions import NoDataInFile, DuplicateOid
# from league_manager.team import Team
# from messages import Message
# from team_editor import TeamEditor
from league_manager.exceptions import DuplicateOid, NoDataInFile
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
        self.btn_import.clicked.connect(self.import_btn_clicked)
        self.btn_export.clicked.connect(self.export_btn_clicked)
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
            try:
                self._league.add_team(Team(oid, new_team_name))
                self.update_ui()
            except DuplicateOid:
                self._message.warn("Issue Adding Team", "Team has Duplicate ID")
        else:
            self._message.warn("No Input", "You Must Enter a Valid Team Name")

    def delete_btn_clicked(self):
        selected_row = self.selected_row()
        if selected_row == -1:
            return self._message.warn("No Selection", "No Team Selected for Deletion")

        dialog, btn_yes, btn_no = self._message.confirmation("Delete Team",
                                                             "Are You Sure You Want to Delete Team ("
                                                             + str(self._league.teams[selected_row]) + ")?")
        dialog.exec()
        if dialog.clickedButton() == btn_yes:
            del self._league.teams[selected_row]
        self.update_ui()

    def edit_btn_clicked(self):
        selected_row = self.selected_row()
        if selected_row == -1:
            return self._message.warn("No Selection", "No Team Selected to Edit")

        team = self._league.teams[selected_row]
        team_editor = TeamEditor(team, self._db)

        if team_editor.exec() == QDialog.DialogCode.Accepted:
            self.update_ui()

    def import_btn_clicked(self):
        try:
            file = QFileDialog.getOpenFileName(self, "Open File", "", "CSV files (*.csv)")
            self._db.import_league_teams(self._league, file[0])
            self.update_ui()
        except FileNotFoundError:
            self._message.warn("Error", "File Not Found")
        except NoDataInFile:
            self._message.warn("Error", "No Data in File")
        except:
            self._message.warn("Error", "Issue Loading File")

    def export_btn_clicked(self):
        try:
            file = QFileDialog.getSaveFileName(self, "Save File", "", "CSV files (*.csv)")
            self._db.export_league_teams(self._league, file[0])
        except:
            self._message.warn("Error", "Issue Exporting File")

    def update_ui(self):
        self.line_edit_team_name.clear()
        self.list_widget_teams.clear()

        for team in self._league.teams:
            self.list_widget_teams.addItem(str(team))

        selected_row = self.selected_row()
        if selected_row != -1 and len(self._league.teams) > selected_row:
            self.list_widget_teams.setCurrentItem(self.list_widget_teams.item(selected_row))

    def selected_row(self):
        selection = self.list_widget_teams.selectedItems()

        if not selection:
            return -1
        assert len(selection) == 1
        selected_row = selection[0]
        try:
            return [str(team) for team in self._league.teams].index(selected_row.text())
        except ValueError:
            pass
        return -1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec_())
