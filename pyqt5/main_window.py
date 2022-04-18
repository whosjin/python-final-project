import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog

from league_manager.league_database import LeagueDatabase
from league_manager.league import League
from pyqt5.league_editor import LeagueEditor
from pyqt5.messages import Message

Ui_MainWindow, QTBaseWindow = uic.loadUiType("main_window.ui")


class MainWindow(Ui_MainWindow, QTBaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.add_btn_clicked)
        self.btn_delete.clicked.connect(self.delete_btn_clicked)
        self.btn_edit.clicked.connect(self.edit_btn_clicked)
        self._db = LeagueDatabase.instance()
        self._message = Message()
        self.update_ui()

    def add_btn_clicked(self):
        new_league_name = self.line_edit_league_name.text()
        oid = self._db.next_oid()

        if new_league_name:
            self._db.add_league(League(oid, new_league_name))
            self.update_ui()
        else:
            self._message.warn("No Input", "You Must Enter a Valid League Name")

    def delete_btn_clicked(self):
        selected_row = self.list_widget_leagues.currentRow()
        if selected_row == -1:
            self._message.warn("No Selection", "No League Selected for Deletion")
            return

        dialog, btn_yes, btn_no = self._message.confirmation("Delete League",
                                                             "Are You Sure You Want to Delete League ("
                                                             + str(self._db.leagues[selected_row]) + ")?")
        dialog.exec()
        if dialog.clickedButton() == btn_yes:
            del self._db.leagues[selected_row]
            self.update_ui()

    def edit_btn_clicked(self):
        selected_row = self.list_widget_leagues.currentRow()

        if selected_row == -1:
            self._message.warn("No Selection", "No League Selected to Edit")
            return

        lg = self._db.leagues[selected_row]
        league_editor = LeagueEditor(lg, self._db)

        if league_editor.exec() == QDialog.DialogCode.Accepted:
            self.update_ui()
        else:
            print("cancel")

    def update_ui(self):
        self.line_edit_league_name.clear()
        self.list_widget_leagues.clear()

        for lg in self._db.leagues:
            self.list_widget_leagues.addItem(str(lg))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
