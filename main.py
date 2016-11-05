from sys import argv, exit

from PyQt4.QtGui import *

from database.entity import init_database, Account
from mail import imap
from view import MainWindow, RegisterDialog

if __name__ == '__main__':
    app = QApplication(argv)
    init_database("project.db")
    
    accounts = Account.select()
    if not accounts:
        register_dialog = RegisterDialog()
        if register_dialog.exec():
            accounts = [Account.create(**register_dialog.get_info())]
        else:
            app.quit()
    
    imap.accounts = accounts
    
    window = MainWindow()
    exit(app.exec_())
