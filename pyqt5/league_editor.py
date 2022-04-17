import sys

from PyQt5 import uic, QtWidgets

Ui_MainWindow, QTBaseWindow = uic.loadUiType("league_editor.ui")


class LeagueEditor(Ui_MainWindow, QTBaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditor()
    window.show()
    sys.exit(app.exec_())