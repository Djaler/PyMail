from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *
from auto_resizing_text_edit import AutoResizingTextEdit

from controller.send_controller import SendController
from database.entity import Mail
from view import BaseView
from view import SendDialog


# noinspection PyUnusedLocal
class MainWindow(QMainWindow, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
        self._controller.set_accounts()
    
    def _init_ui(self):
        self._init_toolbar()
        
        self._splitter = QSplitter()
        self._splitter.setChildrenCollapsible(False)
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

    def _init_mail_widget(self):
        mail_widget = QWidget()
        mail_layout = QVBoxLayout()
        mail_widget.setLayout(mail_layout)

        header_layout = QFormLayout()
        self._from_label = AutoResizingTextEdit()
        self._from_label.setMinimumLines(1)
        self._from_label.setReadOnly(True)
        header_layout.addRow("От:", self._from_label)
        self._to_label = AutoResizingTextEdit()
        self._to_label.setMinimumLines(1)
        self._to_label.setReadOnly(True)
        header_layout.addRow("Кому:", self._to_label)
        self._subject_label = AutoResizingTextEdit()
        self._subject_label.setMinimumLines(1)
        self._subject_label.setReadOnly(True)
        header_layout.addRow("Тема:", self._subject_label)
        mail_layout.addLayout(header_layout)

        self._mail_area = QWebView()
        self._mail_area.page().setLinkDelegationPolicy(
            QWebPage.DelegateAllLinks)
        self._mail_area.linkClicked.connect(
            lambda url: QDesktopServices().openUrl(url))
        
        mail_layout.addWidget(self._mail_area)
        self._splitter.addWidget(mail_widget)
    
    def _init_toolbar(self):
        self._toolbar = QToolBar()
        self._toolbar.setMovable(False)

        self._accounts_combobox = QComboBox()
        self._accounts_combobox.currentIndexChanged.connect(
            self._controller.account_changed)
        self._toolbar.addWidget(self._accounts_combobox)

        self._toolbar.addAction("Синхронизировать", self._controller.sync)
        
        self._toolbar.addAction("Написать", self._open_send_dialog)
        
        # self._toolbar.addWidget(QPushButton("Раз кнопка"))
        # self._toolbar.addWidget(QPushButton("Два кнопка"))
        
        self.addToolBar(Qt.TopToolBarArea, self._toolbar)

    @property
    def current_folder(self):
        return self._folders_widget.currentItem().text(0)

    @property
    def current_mail_id(self):
        return self._mails_widget.currentItem().data(Qt.UserRole)

    def set_accounts(self, accounts):
        self._accounts_combobox.addItems(accounts)

    def update_folders_tree(self, folders):
        self._folders_widget.clear()
        
        self._load_children(folders, self._folders_widget)

        self._folders_widget.expandToDepth(-1)

    def _load_children(self, folders, parent_node):
        for folder, children in folders.items():
            folder_node = QTreeWidgetItem(parent_node, [folder])

            self._load_children(children, folder_node)

    def clear_mails_widget(self):
        self._mails_widget.clear()

    def add_mail(self, mail: Mail):
        message = MessageWidget(mail)
        self._mails_widget.addItem(message)

    def set_mail(self, from_, to, subject, body):
        self._from_label.setText(from_)
        self._to_label.setText(to)
        self._subject_label.setText(subject)
        self._mail_area.setHtml(body)

    def select_first_folder(self):
        first_folder = self._folders_widget.topLevelItem(0)

        self._folders_widget.setCurrentItem(first_folder)

    def select_first_mail(self):
        self._mails_widget.setCurrentRow(0)
    
    @staticmethod
    def _open_send_dialog():
        send_controller = SendController()
        send_dialog = SendDialog(send_controller)
        send_dialog.exec()


class MessageWidget(QListWidgetItem):
    def __init__(self, email):
        super().__init__()

        self.setText("\n".join([email.sender, email.subject]))
        self.setData(Qt.UserRole, email.id)
