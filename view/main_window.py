from PyQt4.QtCore import *
from PyQt4.QtGui import *

from database.entity import *
from mail.mailer import Mailer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._mailer = Mailer()
        
        self._init_ui()

        self._sync()
    
    def _init_ui(self):
        self._init_toolbar()
        
        self._splitter = QSplitter()
        self._splitter.setChildrenCollapsible(False)
        self.connect(self._splitter, SIGNAL('splitterMoved(int, int)'),
                     self._splitter_moved)
        self.setCentralWidget(self._splitter)

        self._folders_widget = QTreeWidget()
        self._folders_widget.setMinimumWidth(200)
        self._folders_widget.header().close()
        self.connect(self._folders_widget, SIGNAL('itemSelectionChanged()'),
                     self._folder_changed)
        self._splitter.addWidget(self._folders_widget)

        mails_area = QScrollArea()
        self._mails_layout = QVBoxLayout()
        mails_area.setLayout(self._mails_layout)
        self._splitter.addWidget(mails_area)

        mail_area = QScrollArea()
        self._splitter.addWidget(mail_area)
        
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
    
    def _sync(self):
        # self._mailer.sync()
        # for account in self._mailer.get_accounts():
        for account in Account.select():
            account_node = QTreeWidgetItem(self._folders_widget,
                                           [account.address])
            
            def load_children(parent_folder, parent_node):
                for child in parent_folder.folders:
                    child_node = QTreeWidgetItem([child.name])
                    
                    parent_node.addChild(child_node)
                    
                    load_children(child, child_node)
            
            for folder in account.folders.select().where(
                            Folder.parent == None):
                folder_node = QTreeWidgetItem([folder.name])
                
                account_node.addChild(folder_node)
                
                load_children(folder, folder_node)
        
        self._folders_widget.expandToDepth(-1)
    
    def _folder_changed(self):
        if not self._folders_widget.currentItem().parent():
            return
        
        self._clear_folder()
        
        folder_name = self._folders_widget.currentItem().text(0)
        
        for email in Mail.select().where(Mail.folder == Folder.get(
                        Folder.name == folder_name)).order_by(Mail.id.desc()):
            
            message = MessageWidget(email.sender, email.subject)
            self._mails_layout.addWidget(message)
    
    def _clear_folder(self):
        for i in reversed(range(self._mails_layout.count())):
            widget_to_remove = self._mails_layout.itemAt(i).widget()
            self._mails_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
    
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


class MessageWidget(QWidget):
    def __init__(self, sender, subject):
        super().__init__()
        
        self._sender = sender
        self._subject = subject
        
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        
        sender_label = QLabel(self._sender)
        layout.addWidget(sender_label)
        
        subject_label = QLabel(self._subject)
        layout.addWidget(subject_label)
        
        self.setLayout(layout)
