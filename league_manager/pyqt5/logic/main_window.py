import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog

from .league_editor import LeagueEditor
from .messages import Message
from ...league.league import League
from ...league.league_database import LeagueDatabase

Ui_MainWindow, QTBaseWindow = uic.loadUiType("league_manager/pyqt5/ui/main_window.ui")


class MainWindow(Ui_MainWindow, QTBaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.add_btn_clicked)
        self.btn_delete.clicked.connect(self.delete_btn_clicked)
        self.btn_edit.clicked.connect(self.edit_btn_clicked)
        self.action_load.triggered.connect(self.action_load_clicked)
        self.action_save.triggered.connect(self.action_save_clicked)
        self.action_quit.triggered.connect(self.action_quit_clicked)
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
        selected_row = self.selected_row()
        if selected_row == -1:
            return self._message.warn("No Selection", "No League Selected for Deletion")

        dialog, btn_yes, btn_no = self._message.confirmation("Delete League",
                                                             "Are You Sure You Want to Delete League ("
                                                             + str(self._db.leagues[selected_row]) + ")?")
        dialog.exec()
        if dialog.clickedButton() == btn_yes:
            del self._db.leagues[selected_row]
        self.update_ui()

    def edit_btn_clicked(self):
        selected_row = self.selected_row()
        if selected_row == -1:
            return self._message.warn("No Selection", "No League Selected to Edit")

        lg = self._db.leagues[selected_row]
        league_editor = LeagueEditor(lg, self._db)

        if league_editor.exec() == QDialog.DialogCode.Accepted:
            self.update_ui()

    def update_ui(self):
        self.line_edit_league_name.clear()
        self.list_widget_leagues.clear()

        for lg in self._db.leagues:
            self.list_widget_leagues.addItem(str(lg))

        selected_row = self.selected_row()
        if selected_row != -1 and len(self._db.leagues) > selected_row:
            self.list_widget_leagues.setCurrentItem(self.list_widget_leagues.item(selected_row))

    def selected_row(self):
        selection = self.list_widget_leagues.selectedItems()

        if not selection:
            return -1
        assert len(selection) == 1
        selected_row = selection[0]
        try:
            return [str(league) for league in self._db.leagues].index(selected_row.text())
        except ValueError:
            pass
        return -1

    def action_load_clicked(self):
        try:
            file = QFileDialog.getOpenFileName(self, "Open League File", "", "Any files (*)")
            self._db.load(file[0])
            self._db = LeagueDatabase.instance()
            self.update_ui()
        except FileNotFoundError:
            self._message.warn("Error", "File Not Found")
        except:
            self._message.warn("Error", "Issue Loading League Instance")

    def action_save_clicked(self):
        try:
            file = QFileDialog.getSaveFileName(self, "Save File")
            self._db.save(file[0])
        except:
            self._message.warn("Error", "Issue Exporting League Instance")

    def action_quit_clicked(self):
        QtWidgets.QApplication.quit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
