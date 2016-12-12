import os.path
from sys import argv, exit

from qtpy.QtWidgets import QApplication

from controller import RegisterController
from controller.main_controller import MainController
from model import init_database, Account
from utils import get_app_folder
from view import RegisterDialog
from view.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(argv)
    init_database(os.path.join(get_app_folder(), "database.sqlite"))
    
    accounts = Account.select()

    if not accounts:
        register_controller = RegisterController()
        register_dialog = RegisterDialog(register_controller)
        register_dialog.exec()
    
    controller = MainController()
    window = MainWindow(controller)
    
    exit(app.exec_())
