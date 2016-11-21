from sys import argv, exit

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from database.entity import init_database, Account
from view import MainWindow, RegisterDialog

if __name__ == '__main__':
    app = QApplication(argv)
    init_database("project.db")
    
    accounts = Account.select()

    if not accounts:
        register_dialog = RegisterDialog()
        if register_dialog.exec():
            Account.create(**register_dialog.get_info())
        else:
            app.quit()

    window = MainWindow()
    exit(app.exec_())
