import sys

from PyQt5 import uic, QtWidgets

from league_manager.exceptions import DuplicateOid, DuplicateEmail
from league_manager.team_member import TeamMember
from pyqt5.logic.messages import Message

Ui_MainWindow, QTBaseWindow = uic.loadUiType("ui/team_editor.ui")


class TeamEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, team=None, db=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.add_btn_clicked)
        self.btn_delete.clicked.connect(self.delete_btn_clicked)
        self.btn_update.clicked.connect(self.update_btn_clicked)
        self.btn_confirm.setVisible(False)
        self.btn_confirm.clicked.connect(self.confirm_btn_clicked)
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
            try:
                self._team.add_member(TeamMember(oid, new_member_name, new_member_email))
                self.update_ui()
            except DuplicateOid:
                self._message.warn("Issue Adding Member", "Member has Duplicate ID")
            except DuplicateEmail:
                self._message.warn("Issue Adding Member", "Member has Duplicate Email Address")
        else:
            self._message.warn("No Input", "You Must Enter a Valid Member Name and Email")

    def delete_btn_clicked(self):
        selected_row = self.selected_row()
        if selected_row == -1:
            return self._message.warn("No Selection", "No Member Selected for Deletion")

        dialog, btn_yes, btn_no = self._message.confirmation("Delete Member",
                                                             "Are You Sure You Want to Delete Member ("
                                                             + str(self._team.members[selected_row]) + ")?")
        dialog.exec()
        if dialog.clickedButton() == btn_yes:
            del self._team.members[selected_row]
        self.update_ui()

    def update_btn_clicked(self):
        selected_row = self.selected_row()
        if selected_row == -1:
            return self._message.warn("No Selection", "No Member Selected to Update")

        selected_member = self._team.members[selected_row]

        self.lbl_new_member.setText("Update " + selected_member.name)
        self.line_edit_member_name.setText(selected_member.name)
        self.line_edit_member_email.setText(selected_member.email)
        self.btn_add.setVisible(False)
        self.btn_confirm.setVisible(True)

    def confirm_btn_clicked(self):
        selected_row = self.list_widget_members.currentRow()
        selected_member = self._team.members[selected_row]
        selected_member.name = self.line_edit_member_name.text()
        selected_member.email = self.line_edit_member_email.text()
        self.update_ui()

    def update_ui(self):
        self.line_edit_member_name.clear()
        self.line_edit_member_email.clear()
        self.list_widget_members.clear()
        self.lbl_new_member.setText("New Member:")
        self.btn_add.setVisible(True)
        self.btn_confirm.setVisible(False)

        for member in self._team.members:
            self.list_widget_members.addItem(str(member))

        selected_row = self.selected_row()
        if selected_row != -1 and len(self._team.members) > selected_row:
            self.list_widget_members.setCurrentItem(self.list_widget_members.item(selected_row))

    def selected_row(self):
        selection = self.list_widget_members.selectedItems()

        if not selection:
            return -1
        assert len(selection) == 1
        selected_row = selection[0]
        try:
            return [str(member) for member in self._team.members].index(selected_row.text())
        except ValueError:
            pass
        return -1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditor()
    window.show()
    sys.exit(app.exec_())
