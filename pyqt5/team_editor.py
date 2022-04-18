import sys

from PyQt5 import uic, QtWidgets

from league_manager.team_member import TeamMember
from pyqt5.messages import Message

Ui_MainWindow, QTBaseWindow = uic.loadUiType("team_editor.ui")


class TeamEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, team=None, db=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.add_btn_clicked)
        self.btn_delete.clicked.connect(self.delete_btn_clicked)
        # self.btn_edit.clicked.connect(self.edit_btn_clicked)
        self._message = Message()
        self._team = team
        self._db = db
        if self._team:
            self.lbl_members.setText("Members in " + team.name + ":")
            self.setWindowTitle("Team (" + team.name + ") Editor")
            self.update_ui()

    def add_btn_clicked(self):
        new_member_name = self.line_edit_member_name.text()
        new_member_email = self.line_edit_member_email.text()
        oid = self._db.next_oid()

        if new_member_name and new_member_email:
            self._team.add_member(TeamMember(oid, new_member_name, new_member_email))
            self.update_ui()
        else:
            self._message.warn("No Input", "You Must Enter a Valid Member Name and Email")

    def delete_btn_clicked(self):
        selected_row = self.list_widget_members.currentRow()
        if selected_row == -1:
            self._message.warn("No Selection", "No Member Selected for Deletion")
            return

        dialog, btn_yes, btn_no = self._message.confirmation("Delete Member",
                                                             "Are You Sure You Want to Delete Member ("
                                                             + str(self._team.members[selected_row]) + ")?")
        dialog.exec()
        if dialog.clickedButton() == btn_yes:
            del self._team.members[selected_row]
            self.update_ui()

    def update_ui(self):
        self.line_edit_member_name.clear()
        self.line_edit_member_email.clear()
        self.list_widget_members.clear()

        for member in self._team.members:
            self.list_widget_members.addItem(str(member))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec_())
