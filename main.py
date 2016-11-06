from sys import argv, exit

from PyQt4.QtGui import *

from database.entity import init_database, Account
from mail.imap import ImapService
from view import MainWindow, RegisterDialog

if __name__ == '__main__':
    app = QApplication(argv)
    init_database("project.db")
    
    accounts = Account.select()

    imap_service = ImapService()
    if not accounts:
        register_dialog = RegisterDialog()
        if register_dialog.exec():
            imap_service.add_account(
                Account.create(**register_dialog.get_info()))
        else:
            app.quit()
    else:
        imap_service.set_accounts(accounts)

    imap_service.connect_all()
    connections = list(imap_service.get_connections())

    window = MainWindow(imap_service)
    exit(app.exec_())
