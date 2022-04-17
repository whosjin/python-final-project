import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from league_manager.league_database import LeagueDatabase
from league_manager.league import League

Ui_MainWindow, QTBaseWindow = uic.loadUiType("main_window.ui")


class MainWindow(Ui_MainWindow, QTBaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_add.clicked.connect(self.add_btn_clicked)
        self.btn_delete.clicked.connect(self.delete_btn_clicked)
        self.btn_edit.clicked.connect(self.edit_btn_clicked)
        self._db = LeagueDatabase.instance()

    def add_btn_clicked(self):
        new_league_name = self.line_edit_league_name.text()

        if new_league_name:
            self._db.add_league(League(self._db.next_oid(), new_league_name))
        else:
            self.warn("No Input", "You must enter a valid League Name")

        self.update_ui()

    def delete_btn_clicked(self):
        pass

    def edit_btn_clicked(self):
        pass

    def warn(self, title, message):
        error_msg = QMessageBox(QMessageBox.Icon.Critical, title, message, QMessageBox.StandardButton.Ok)
        return error_msg.exec_()

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
