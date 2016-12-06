import os.path
from sys import argv, exit

from qtpy.QtWidgets import QApplication

from controller import MainController
from model import init_database, Account
from utils import get_app_folder
from view import MainWindow, RegisterDialog

if __name__ == '__main__':
    app = QApplication(argv)
    init_database(os.path.join(get_app_folder(), "database.sqlite"))
    
    accounts = Account.select()

    if not accounts:
        register_dialog = RegisterDialog()
        if register_dialog.exec():
            Account.create(**register_dialog.get_info())
        else:
            app.quit()

    controller = MainController()
    window = MainWindow(controller)
    
    exit(app.exec_())
