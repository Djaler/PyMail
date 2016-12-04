from PyQt5.QtWidgets import *

from view import BaseView


class SendDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        self._address_edit = QLineEdit()
        form_layout.addRow("Кому:", self._address_edit)
        
        self._subject_edit = QLineEdit()
        form_layout.addRow("Тема:", self._subject_edit)
        
        self._body_edit = QTextEdit()
        main_layout.addWidget(self._body_edit)
        
        self._send_btn = QPushButton("Отправить")
        self._send_btn.pressed.connect(self._controller.send)
        main_layout.addWidget(self._send_btn)
        
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Создание учётной записи')
        self.show()
        self.center()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
