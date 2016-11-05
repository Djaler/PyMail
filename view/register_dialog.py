from getpass import getuser

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QFormLayout()
        
        self._name_edit = QLineEdit(getuser())
        main_layout.addRow("Имя:", self._name_edit)
        
        self._address_edit = QLineEdit()
        self._address_edit.setPlaceholderText("address@example.com")
        main_layout.addRow("Адрес почты:", self._address_edit)
        
        self._password_edit = QLineEdit()
        self._password_edit.setEchoMode(QLineEdit.Password)
        self._password_edit.setPlaceholderText("***********")
        main_layout.addRow("Пароль:", self._password_edit)
        
        main_layout.addRow(QLabel("<b>Параметры IMAP</b>"))
        
        self._imap_host_edit = QLineEdit()
        self._imap_host_edit.setPlaceholderText("imap.example.com")
        main_layout.addRow("Сервер:", self._imap_host_edit)
        
        self._imap_port_edit = QLineEdit("993")
        self._imap_port_edit.setValidator(QIntValidator())
        main_layout.addRow("Порт:", self._imap_port_edit)
        
        self._imap_ssl_checkbox = QCheckBox()
        self._imap_ssl_checkbox.setChecked(True)
        main_layout.addRow("Использовать SSL: ", self._imap_ssl_checkbox)
        
        main_layout.addRow(QLabel("<b>Параметры SMTP</b>"))
        
        self._smtp_host_edit = QLineEdit()
        self._smtp_host_edit.setPlaceholderText("smtp.example.com")
        main_layout.addRow("Сервер:", self._smtp_host_edit)
        
        self._smtp_port_edit = QLineEdit("465")
        self._smtp_port_edit.setValidator(QIntValidator())
        main_layout.addRow("Порт:", self._smtp_port_edit)
        
        self._smtp_ssl_checkbox = QCheckBox()
        self._smtp_ssl_checkbox.setChecked(True)
        main_layout.addRow("Использовать SSL: ", self._smtp_ssl_checkbox)
        
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена")
        self.connect(cancel_button, SIGNAL('pressed()'), self.reject)
        buttons_layout.addWidget(cancel_button)
        self._add_button = QPushButton("Добавить")
        self.connect(self._add_button, SIGNAL('pressed()'), self.accept)
        buttons_layout.addWidget(self._add_button)
        main_layout.addRow(buttons_layout)
        
        self._fields = [self._name_edit, self._address_edit,
                        self._password_edit, self._imap_host_edit,
                        self._imap_port_edit, self._smtp_host_edit,
                        self._smtp_port_edit]
        for field in self._fields:
            self.connect(field, SIGNAL('textChanged(QString)'),
                         self._on_field_changed)
        
        self._on_field_changed()
        
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Создание учётной записи')
        self.show()
        self.center()
        self.setFocus()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def _on_field_changed(self):
        if any(not field.text() for field in self._fields):
            self._add_button.setDisabled(True)
        else:
            self._add_button.setEnabled(True)
    
    def name(self):
        return self._name_edit.text()
    
    def address(self):
        return self._address_edit.text()
    
    def password(self):
        return self._password_edit.text()
    
    def imap_host(self):
        return self._imap_host_edit.text()
    
    def imap_port(self):
        return int(self._imap_port_edit.text())
    
    def imap_ssl(self):
        return self._imap_ssl_checkbox.isChecked()
    
    def smtp_host(self):
        return self._smtp_host_edit.text()
    
    def smtp_port(self):
        return int(self._smtp_port_edit.text())
    
    def smtp_ssl(self):
        return self._smtp_ssl_checkbox.isChecked()
    
    def get_info(self):
        return {"name": self.name(), "address": self.address(),
                "password": self.password(), "imap_host": self.imap_host(),
                "imap_port": self.imap_port(), "imap_ssl": self.imap_ssl(),
                "smtp_host": self.smtp_host(), "smtp_port": self.smtp_port(),
                "smtp_ssl": self.smtp_ssl()}
