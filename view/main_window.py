from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *

from database.entity import Mail


# noinspection PyUnusedLocal
class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self._controller = controller
        self._controller.set_view(self)
        
        self._init_ui()

        self._controller.sync()
    
    def update_folders_tree(self, accounts):
        def load_children(folders, parent_node):
            for folder, children in folders.items():
                folder_node = QTreeWidgetItem(parent_node, [folder])
                
                load_children(children, folder_node)

        for account, top_folders in accounts.items():
            account_node = QTreeWidgetItem(self._folders_widget, [account])

            load_children(top_folders, account_node)
        
        self._folders_widget.expandToDepth(-1)
    
    def clear_mails_widget(self):
        self._mails_widget.clear()
    
    def add_mail(self, mail: Mail):
        message = MessageWidget(mail)
        self._mails_widget.addItem(message)
    
    @property
    def current_folder(self):
        return self._folders_widget.currentItem().text(0)
    
    @property
    def current_mail_id(self):
        return self._mails_widget.currentItem().data(Qt.UserRole)

    def set_mail(self, from_, to, subject, body):
        self._from_label.setText(from_)
        self._to_label.setText(to)
        self._subject_label.setText(subject)
        self._mail_area.setHtml(body)

    def select_first_folder(self):
        first_account = self._folders_widget.topLevelItem(0)

        self._folders_widget.setCurrentItem(first_account.child(0))

    def select_first_mail(self):
        self._mails_widget.setCurrentRow(0)
    
    def _init_ui(self):
        self._init_toolbar()
        
        self._splitter = QSplitter()
        self._splitter.setChildrenCollapsible(False)
        self._splitter.splitterMoved.connect(self._splitter_moved)
        self.setCentralWidget(self._splitter)

        self._folders_widget = QTreeWidget()
        self._folders_widget.setMinimumWidth(200)
        self._folders_widget.header().close()
        self._folders_widget.itemSelectionChanged.connect(
            self._controller.folder_changed)
        self._splitter.addWidget(self._folders_widget)

        self._mails_widget = QListWidget()
        self._mails_widget.setMinimumWidth(200)
        self._mails_widget.itemSelectionChanged.connect(
            self._controller.mail_changed)
        self._splitter.addWidget(self._mails_widget)

        self._init_mail_widget()
        
        self.resize(700, 500)
        self.setWindowTitle('PyMail')
        self.showMaximized()
        self.center()
        self._update_search_size()

    @staticmethod
    def _open_link(url):
        QDesktopServices().openUrl(url)

    def _init_mail_widget(self):
        mail_widget = QWidget()
        mail_layout = QVBoxLayout()
        mail_widget.setLayout(mail_layout)

        header_layout = QFormLayout()
        self._from_label = QLabel()
        self._from_label.setWordWrap(True)
        self._from_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        header_layout.addRow("От:", self._from_label)
        self._to_label = QLabel()
        self._to_label.setWordWrap(True)
        self._to_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        header_layout.addRow("Кому:", self._to_label)
        self._subject_label = QLabel()
        self._subject_label.setWordWrap(True)
        self._subject_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        header_layout.addRow("Тема:", self._subject_label)
        mail_layout.addLayout(header_layout)

        self._mail_area = QWebView()
        self._mail_area.page().setLinkDelegationPolicy(
            QWebPage.DelegateAllLinks)
        self._mail_area.linkClicked.connect(self._open_link)

        mail_layout.addWidget(self._mail_area)
        self._splitter.addWidget(mail_widget)
    
    def _init_toolbar(self):
        self._toolbar = QToolBar()
        self._toolbar.setMovable(False)
        
        self._toolbar.addAction("Написать")
        
        self._search_edit = QLineEdit()
        self._toolbar.addWidget(self._search_edit)

        # self._toolbar.addWidget(QPushButton("Раз кнопка"))
        # self._toolbar.addWidget(QPushButton("Два кнопка"))
        
        self.addToolBar(Qt.TopToolBarArea, self._toolbar)
    
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


class MessageWidget(QListWidgetItem):
    def __init__(self, email):
        super().__init__()

        self.setText("\n".join([email.sender, email.subject]))
        self.setData(Qt.UserRole, email.id)
