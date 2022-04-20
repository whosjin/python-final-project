from PyQt5.QtWidgets import QMessageBox


class Message:
    def warn(self, title, message):
        error_msg = QMessageBox(QMessageBox.Icon.Critical, title, message, QMessageBox.StandardButton.Ok)
        return error_msg.exec_()

    def confirmation(self, title, message):
        dialog = QMessageBox(QMessageBox.Icon.Question, title, message)
        btn_yes = dialog.addButton("Yes", QMessageBox.ButtonRole.YesRole)
        btn_no = dialog.addButton("No", QMessageBox.ButtonRole.NoRole)
        return dialog, btn_yes, btn_no
