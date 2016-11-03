from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self._init_ui()
    
    def _init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self._init_toolbar()
        
        
        
        self.setWindowTitle('PyMail')
        self.center()
        self.show()
    
    def _init_toolbar(self):
        toolbar_new_mail = QToolBar()
        toolbar_new_mail.setMovable(False)
        toolbar_new_mail.addAction("Написать")
        self.addToolBar(Qt.TopToolBarArea, toolbar_new_mail)
        
        toolbar_search = QToolBar()
        toolbar_search.setMovable(False)
        search_edit = QLineEdit()
        toolbar_search.addWidget(search_edit)
        self.addToolBar(Qt.TopToolBarArea, toolbar_search)
        
        toolbar_buttons = QToolBar()
        toolbar_buttons.setMovable(False)
        toolbar_buttons.addWidget(QPushButton("Раз кнопка"))
        toolbar_buttons.addWidget(QPushButton("Два кнопка"))
        self.addToolBar(Qt.TopToolBarArea, toolbar_buttons)
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
