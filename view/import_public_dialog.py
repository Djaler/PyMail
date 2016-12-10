from qtpy.QtWidgets import *

from view import BaseView


class ImportPublicDialog(QDialog, BaseView):
    def __init__(self, controller):
        super().__init__(controller=controller)
        
        self._init_ui()
    
    def _init_ui(self):
        main_layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)
        
        self._address_edit = QLineEdit()
        form_layout.addRow("Адрес собеседника:", self._address_edit)
        
        import_button = QPushButton("Импортировать")
        import_button.pressed.connect(self._controller.import_)
        main_layout.addWidget(import_button)
        
        self.setLayout(main_layout)
        self.setMinimumWidth(300)
        self.setWindowTitle('Импорт публичного ключа')
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
