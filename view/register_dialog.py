from getpass import getuser

from qtpy.QtGui import *
from qtpy.QtWidgets import *

from view import BaseView


class RegisterDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
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
        self._imap_port_edit.setValidator(QIntValidator(1, 65535))
        main_layout.addRow("Порт:", self._imap_port_edit)
        
        self._imap_ssl_checkbox = QCheckBox()
        self._imap_ssl_checkbox.setChecked(True)
        main_layout.addRow("Использовать SSL: ", self._imap_ssl_checkbox)
        
        main_layout.addRow(QLabel("<b>Параметры SMTP</b>"))
        
        self._smtp_host_edit = QLineEdit()
        self._smtp_host_edit.setPlaceholderText("smtp.example.com")
        main_layout.addRow("Сервер:", self._smtp_host_edit)
        
        self._smtp_port_edit = QLineEdit("465")
        self._smtp_port_edit.setValidator(QIntValidator(1, 65535))
        main_layout.addRow("Порт:", self._smtp_port_edit)
        
        self._smtp_ssl_checkbox = QCheckBox()
        self._smtp_ssl_checkbox.setChecked(True)
        main_layout.addRow("Использовать SSL: ", self._smtp_ssl_checkbox)
        
        buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена")
        cancel_button.pressed.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        self._add_button = QPushButton("Добавить")
        self._add_button.pressed.connect(self._controller.add)
        buttons_layout.addWidget(self._add_button)
        main_layout.addRow(buttons_layout)
        
        self._fields = [self._name_edit, self._address_edit,
                        self._password_edit, self._imap_host_edit,
                        self._imap_port_edit, self._smtp_host_edit,
                        self._smtp_port_edit]
        for field in self._fields:
            field.textChanged.connect(self._on_field_changed)
        
        self._on_field_changed()
        
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Создание учётной записи')
        self.show()
        self._center()
        self.setFocus()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def _on_field_changed(self):
        if any(not field.text() for field in self._fields):
            self._add_button.setDisabled(True)
        else:
            self._add_button.setEnabled(True)
    
    @property
    def name(self):
        return self._name_edit.text()
    
    @property
    def address(self):
        return self._address_edit.text()
    
    @property
    def password(self):
        return self._password_edit.text()
    
    @property
    def imap_host(self):
        return self._imap_host_edit.text()
    
    @property
    def imap_port(self):
        return int(self._imap_port_edit.text())
    
    @property
    def imap_ssl(self):
        return self._imap_ssl_checkbox.isChecked()
    
    @property
    def smtp_host(self):
        return self._smtp_host_edit.text()
    
    @property
    def smtp_port(self):
        return int(self._smtp_port_edit.text())
    
    @property
    def smtp_ssl(self):
        return self._smtp_ssl_checkbox.isChecked()
