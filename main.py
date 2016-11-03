from sys import argv, exit

from PyQt4.QtGui import *

from models.entities import init_database
from views.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(argv)
    init_database("project.db")
    window = MainWindow()
    exit(app.exec_())
