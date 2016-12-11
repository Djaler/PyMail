from qtpy.QtWidgets import *

from view import BaseView


class CreateKeysDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        
        self._address_edit = QLineEdit()
        form_layout.addRow("Адрес собеседника:", self._address_edit)
        
        create_btn = QPushButton("Создать")
        create_btn.pressed.connect(self._controller.create)
        main_layout.addWidget(create_btn)
        
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Создание пары ключей')
        self.setModal(True)
        self.show()
        self._center()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    @property
    def address(self):
        return self._address_edit.text()
