from PyQt4.QtCore import *
from PyQt4.QtGui import *

from mail.imap import ImapService


class MainWindow(QMainWindow):
    def __init__(self, imap_service: ImapService):
        super().__init__()

        self._imap_service = imap_service
        
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
        self.show()
        self.center()
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
        for connection in self._imap_service.get_connections():
            account = QTreeWidgetItem(folders, [connection.username])
            # TODO Рекурсивная загрузка папок, занесение в базу
            for folder in connection.folders():
                account.addChild(QTreeWidgetItem([folder]))
        folders.expandToDepth(0)
        return folders
    
    def _splitter_moved(self, pos, index):
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
