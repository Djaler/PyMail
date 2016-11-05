from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self._init_ui()
    
    def _init_ui(self):
        self._init_toolbar()
        
        self._splitter = QSplitter()
        self._splitter.setChildrenCollapsible(False)
        self.connect(self._splitter, SIGNAL('splitterMoved(int, int)'),
                     self._splitter_moved)
        self.setCentralWidget(self._splitter)
        
        self._splitter.addWidget(self._folders_widget())
        
        mails = QScrollArea()
        self._splitter.addWidget(mails)
        
        mail = QScrollArea()
        self._splitter.addWidget(mail)
        
        self.resize(700, 500)
        self.setWindowTitle('PyMail')
        self.center()
        self.show()
        self._update_search_size()
    
    def _init_toolbar(self):
        self._toolbar = QToolBar()
        self._toolbar.setMovable(False)
        
        self._toolbar.addAction("Написать")
        
        self._search_edit = QLineEdit()
        self._toolbar.addWidget(self._search_edit)
        
        self._toolbar.addWidget(QPushButton("Раз кнопка"))
        self._toolbar.addWidget(QPushButton("Два кнопка"))
        
        self.addToolBar(Qt.TopToolBarArea, self._toolbar)
    
    def _folders_widget(self):
        folders = QTreeWidget()
        folders.setMinimumWidth(200)
        folders.header().close()
        account1 = QTreeWidgetItem(folders, ["djaler1@gmail.com"])
        inbox = QTreeWidgetItem(account1, ["Входящие"])
        drafts = QTreeWidgetItem(account1, ["Черновики"])
        sent = QTreeWidgetItem(account1, ["Отправленные"])
        folders.expandToDepth(0)
        return folders
    
    def _splitter_moved(self, pos, index):
        if index != 2:
            return
        
        self._update_search_size()
    
    def _update_search_size(self):
        self._search_edit.setFixedWidth(
            self._splitter.handle(2).pos().x() - self._search_edit.pos().x())
    
    def resizeEvent(self, event):
        self._update_search_size()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
