from qtpy.QtWidgets import *

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
        self.setWindowTitle('Создание письма')
        self.setModal(True)
        self.show()
        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @property
    def to(self):
        return self._address_edit.text()

    @property
    def subject(self):
        return self._subject_edit.text()

    @property
    def body(self):
        return self._body_edit.toPlainText()

    def show_error(self, text):
        QMessageBox().warning(self, 'Ошибка', text)
